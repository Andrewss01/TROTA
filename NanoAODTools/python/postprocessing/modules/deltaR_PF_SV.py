import ROOT
import math
import numpy as np
from array import array
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
#from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *






class deltaR_PF_SV(Module):
    def __init__(self):
        pass
        
        
    def beginJob(self):
        pass
        
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        #self.out.branch("Jet_deltaR",      "F", lenVar="nJet") 
        self.out.branch("PFCand_JetDeltaR"   ,       "F", lenVar="nPFCands")    #nJetPFCands"? 
        self.out.branch("PFCand_FatJetDeltaR",       "F", lenVar="nPFCands") 
        self.out.branch("PFCand_IsInJet"     ,       "F", lenVar="nPFCands")    #nJetPFCands"? 
        self.out.branch("PFCand_IsInFatJet"  ,       "F", lenVar="nPFCands") 

        self.out.branch("SV_JetDeltaR"        ,       "F", lenVar = "nSV"   )
        self.out.branch("SV_FatJetDeltaR"     ,       "F", lenVar = "nSV")
        #self.out.branch("PFCands_JetdzFromPV",     "I", lenVar="nPFCands")
        #self.out.branch("PFCands_FatJetdzFromPV",  "I", lenVar="nPFCands")
        #self.out.branch("PFCands_JetdxyFromPV",    "I", lenVar="nPFCands")
        #self.out.branch("PFCands_FatJetdxyFromPV", "I", lenVar="nPFCands")

        # self.out.branch("SVs_JetDeltaR", "F", lenVar = "nSV")
        




    def endFile(self, inputFile, outputFile, inputTree,wrappedOutputTree):
        pass


    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""        
        jets       = Collection(event,"Jet")
        Njets      = len(jets)
        fatjets      = Collection(event,"FatJet")
        PFCs       = Collection(event,"PFCand")
        NPFCs      = len(PFCs)
        SVs        = Collection(event, "SV")
        NSVs       = len(SVs)  


        '''init variables to branch'''
        PFCs_jets_dr             = np.full(NPFCs,-1.0)
        PFCs_fat_jets_dr         = np.full(NPFCs,-1.0)
        PFCs_is_in_jet           = np.zeros(NPFCs) 
        PFCs_is_in_fat_jet       = np.zeros(NPFCs)      
        SVs_jets_dr              = np.full(NSVs,-1.0)
        SVs_fat_jets_dr          = np.full(NSVs,-1.0)      



        for i,particle in enumerate(PFCs):
            dr_jet=-1
            dr_Fatjet=-1
            is_in_jet=0
            is_in_fat_jet=0
            if particle.JetIdx!=-1:
                jIdx=int(particle.JetIdx)
                dr_jet=deltaR(particle, jets[jIdx])
                #print("\nche succede?",dr_jet,"\n")
                is_in_jet=1
            if particle.FatJetIdx!=-1:
                fjIdx=int(particle.FatJetIdx)
                dr_Fatjet=deltaR(particle, fatjets[fjIdx])
                is_in_fat_jet=1
            #print("\ni",i,"jet_idx",particle.JetIdx,"dr_jet", dr_jet,"\n")
            #print("\nFatjet_idx",particle.FatJetIdx,"dr_Fatjet", dr_Fatjet,"\n")
            PFCs_jets_dr[i]=dr_jet
            PFCs_fat_jets_dr[i]=dr_Fatjet
            PFCs_is_in_jet[i]=is_in_jet
            PFCs_is_in_fat_jet[i]=is_in_fat_jet
       
        for j,sv_particle in enumerate(SVs):
            dr_jet = -1
            dr_fatjet = -1

            if sv_particle.JetIdx != -1:
                jIdx = int(sv_particle.JetIdx)
                dr_jet = deltaR(sv_particle, jets[jIdx])
            
            if sv_particle.FatJetIdx != -1:
                fjIdx = int(sv_particle.FatJetIdx)
                df_fatjet = deltaR(sv_particle, fatjets[fjIdx])

            SVs_jets_dr[j] = dr_jet
            SVs_fat_jets_dr[j] = dr_fatjet



        self.out.fillBranch("PFCand_JetDeltaR", PFCs_jets_dr)
        self.out.fillBranch("PFCand_FatJetDeltaR", PFCs_fat_jets_dr)
        self.out.fillBranch("PFCand_IsInJet", PFCs_is_in_jet)
        self.out.fillBranch("PFCand_IsInFatJet", PFCs_is_in_fat_jet)

        self.out.fillBranch("SV_JetDeltaR"        ,       SVs_jets_dr   )
        self.out.fillBranch("SV_FatJetDeltaR"     ,       SVs_fat_jets_dr)
        #self.out.fillBranch("PFCands_JetdzFromPV", PFCs_jets_dz_PV)
        #self.out.fillBranch("PFCands_FatJetdzFromPV",  PFCs_fat_jets_dz_PV)
        #self.out.fillBranch("PFCands_JetdxyFromPV", PFCs_jets_dxy_PV)
        #self.out.fillBranch("PFCands_FatJetdxyFromPV",  PFCs_fat_jets_dxy_PV)


        #self.out.fillBranch("Top_indFatJet", ind_fatjets) 
        #self.out.fillBranch("Top_indJet", ind_jets) 
        # t1 = datetime.now()
        # print("nanprepro module time :", t1-t0) 
        return True