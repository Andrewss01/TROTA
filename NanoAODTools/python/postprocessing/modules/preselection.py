import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
# from tWb_Single_top_CKM.analysis.tools import *

class preselection(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("goodMuon_idx","I",lenVar = "ngoodMuon")
        self.out.branch("goodElectron_idx","I",lenVar = "ngoodElectron")
        self.out.branch("goodJets_idx","I", lenVar="ngoodJets")


        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        isGoodEvent = False
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        PV = Object(event, "PV")
        
        #Variable for Selection 
        isGoodPV = False 
        
        isGoodPV = (PV.ndof > 4 and abs(PV.z) < 20 and math.hypot(PV.x,PV.y)<2)
        
        #Indx_for_Muon_Electron
        goodMuon_idx = []
        goodElectron_idx = []

        #Indx_for_Jet_and_bJet
        goodJets_idx = []
        
        #Lepton Selection
        goodMu  = list(filter(lambda x: x.tightId and (abs(x.eta) < 2.4 and x.pfRelIso04_all<0.15), muons))
        goodEle = list(filter(lambda x: x.mvaIso_WP80 and (abs(x.eta) < 1.4442 or abs(x.eta) > 1.566), electrons))
        goodJet = list(filter(lambda x: x.pt > 25 and abs(x.eta) < 4.7 and x.jetId > 2, jets))

        
        #Se if it's a good event
        isGoodEvent =  isGoodPV and (len(goodJet) > 1) and ((len(goodMu) >= 1 or len(goodEle) >= 1)) 
        
        for i, mu in enumerate(muons):
            if mu in goodMu:
                goodMuon_idx.append(i)


        for i, ele in enumerate(electrons):
            if ele in goodEle:
                goodElectron_idx.append(i)
                
        for i, jet in enumerate(jets):
            if jet in goodJet:
                goodJets_idx.append(i)
        
        
        self.out.fillBranch("goodMuon_idx", goodMuon_idx)
        self.out.fillBranch("goodElectron_idx", goodElectron_idx)
        self.out.fillBranch("goodJets_idx", goodJets_idx) 
            
        
        return isGoodEvent

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
#MySelectorModuleConstr = lambda : exampleProducer(jetetaSelection= lambda j : abs(j.eta)<2.4) 
