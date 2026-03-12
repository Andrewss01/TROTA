import ROOT
import math
import numpy as np
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
#from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *

def Conversion_bitwise(num):
    k=15
    a=np.ones(k)
    for j in range(k,0):
        conv=0
        for i in range(0,k): 
            conv = conv + a[i]*pow(2,i)
        if num<conv: a[j]=0
        else:
            a[j+1]=1
            a[j]=0
    return a

class GenPart_MomFirstCp(Module):
    def __init__(self,isMC=1,flavour=None):
        self.isMC = isMC
        self.flavour=flavour
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("GenPart_genPartIdxMother_prompt","I", lenVar="nGenPart")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if self.isMC==0: return False

        genpart = Collection(event, "GenPart")
        allGenPart=list(filter(lambda x : x.pt>-9999, genpart))
        if self.flavour!=None:
            flavourGenPart=list(filter(lambda x : str(abs(x.pdgId)) in self.flavour, genpart))
            
        else:
            flavourGenPart= allGenPart
        
        momIdx2=[]

        for j in allGenPart:
            if j in flavourGenPart:
                if j.genPartIdxMother>0:
                    if genpart[j.genPartIdxMother].pdgId!=j.pdgId: momIdx2.append(j.genPartIdxMother)
                    else:
                        mom=genpart[j.genPartIdxMother]
                        son=j
                        
                        while (mom.pdgId==son.pdgId and son.genPartIdxMother>0 and mom.genPartIdxMother>0):
                            
                            son=mom
                            mom= genpart[son.genPartIdxMother]
                        if(mom.pdgId==son.pdgId ): momIdx2.append(-1)
                        else: momIdx2.append(allGenPart.index(mom))    

                else: momIdx2.append(-1)
            else: momIdx2.append(-1)


        self.out.fillBranch("GenPart_genPartIdxMother_prompt", momIdx2 )
        #t1 = datetime.now()  
        #print("GenPart_momFirstCP module time :", t1-t0)
        return True


