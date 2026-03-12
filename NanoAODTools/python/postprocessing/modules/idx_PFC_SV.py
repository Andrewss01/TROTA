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






class Idx_PFC_SV(Module):
    def __init__(self):
        pass
        
        
    def beginJob(self):
        pass
        
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        #self.out.branch("Jet_deltaR",      "F", lenVar="nJet") 
        self.out.branch("PFCand_JetIdx"   ,       "I", lenVar="nPFCand")    #nJetPFCands"? 
        self.out.branch("PFCand_FatJetIdx",       "I", lenVar="nPFCand")
        self.out.branch("PFCand_Idx"      ,       "I", lenVar="nPFCand")

        self.out.branch("SV_JetIdx"   ,       "I", lenVar = "nSV"   ) 
        self.out.branch("SV_FatJetIdx",       "I", lenVar = "nSV"   )
        self.out.branch("SV_Idx"      ,       "I", lenVar = "nSV"   )
        



        #self.out.branch("PFCands_JetdzFromPV",     "I", lenVar="nPFCands")
        #self.out.branch("PFCands_FatJetdzFromPV",  "I", lenVar="nPFCands")
        #self.out.branch("PFCands_JetdxyFromPV",    "I", lenVar="nPFCands")
        #self.out.branch("PFCands_FatJetdxyFromPV", "I", lenVar="nPFCands")
        




    def endFile(self, inputFile, outputFile, inputTree,wrappedOutputTree):
        pass


    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""        
        jets       = Collection(event,"Jet")
        Njets      = len(jets)
        fatjets    = Collection(event,"FatJet")
        PFCs       = Collection(event,"PFCand")
        NPFCs      = len(PFCs)
        jetPFCs    = Collection(event,"JetPFCand")
        fatjetPFCs = Collection(event,"FatJetPFCand")
        SVs = Collection(event, "SV")
        # jetSVs_idx1 = Collection(event, "Jet_svIdx1")
        # jetSVs_idx2 = Collection(event, "Jet_svIdx2")
        # fatjetSVs_idx1 = Collection(event, "FatJet_svIdx1")
        # fatjetSVs_idx2 = Collection(event, "FatJet_svIdx2")
        NSVs = len(SVs)
        

        

        '''init variables to branch'''
        PFCs_jets_idx          = np.full(NPFCs,-1)
        PFCs_fat_jets_idx      = np.full(NPFCs,-1)
        PFCs_idx               = np.full(NPFCs,-1)
        SVs_jets_idx           = np.full(NSVs ,-1)
        SVs_fat_jets_idx       = np.full(NSVs ,-1)
        SVs_idx                = np.full(NSVs ,-1)
        SVs_multiple_jets      = np.full(NSVs ,-1)
        SVs_multiple_fat_jets  = np.full(NSVs ,-1)
      



        for jPFC in jetPFCs:
            
            if PFCs_jets_idx[jPFC.pfCandIdx] == -1:
                PFCs_jets_idx[jPFC.pfCandIdx]=jPFC.jetIdx
            else: 
                print("errore: a questo pf cands corrisponde più di un jet")
        
        for fjPFC in fatjetPFCs:
            if PFCs_fat_jets_idx[fjPFC.pfCandIdx] == -1:
                PFCs_fat_jets_idx[fjPFC.pfCandIdx]=fjPFC.jetIdx
            else:
                print('errore: a questo pf cands corrisponde più di un fat jet ')

        for i in range(NPFCs):
            PFCs_idx[i]=i

        # print('-----------------------------------------------------')
        for idx_jet,jet in enumerate(jets):
            #prende il jet e il suo indice e controlla che l'indice del primo sv matchato non sia -1
            # print('jet sv index 1: ', jet.svIdx1, 'index jet: ', idx_jet, 'numero di sv: ', NSVs)
            # print('list sv is: ', SVs_multiple_jets)
            if jet.svIdx1 != -1:
                
                if jet.svIdx1 < NSVs: 
                    if SVs_multiple_jets[jet.svIdx1] == -1:
                        sv_particle = SVs[jet.svIdx1]
                        
                        dr = deltaR(sv_particle, jet)
                        # print('dr is: ', dr)
                        if dr <= 0.4:
                            SVs_multiple_jets[jet.svIdx1] = idx_jet
                            # print('if:',SVs_multiple_jets, NSVs)

                    else:

                        #Se c'è già un jet allora mette come indice del jet quello che è più vicino come dR dal vertice
                        jet_1_idx = int(SVs_multiple_jets[jet.svIdx1])
                        sv_particle = SVs[jet.svIdx1]
                        jet_1 = jets[jet_1_idx]
                        dr_1 = deltaR(sv_particle, jet_1)
                        jet_2 = jets[idx_jet] 
                        dr_2 = deltaR(sv_particle, jet_2)
                        # print('dr  1 is: ', dr_1, ' dr 2 is: ', dr_2)
                        if dr_2 < dr_1 and dr_2 <= 0.4: 
                            SVs_multiple_jets[jet.svIdx1] = idx_jet
                        # print('else:',SVs_multiple_jets, NSVs)
            
            # print('jet sv index 2: ', jet.svIdx2, ' index jet: ', idx_jet )
            if jet.svIdx2 != -1:
                
                if jet.svIdx2 < NSVs: 
                    if SVs_multiple_jets[jet.svIdx2] == -1:
                        sv_particle = SVs[jet.svIdx2]
                        
                        dr = deltaR(sv_particle, jet)
                        # print('dr is: ', dr)
                        if dr <= 0.4:
                            SVs_multiple_jets[jet.svIdx2] = idx_jet
                            # print('if:',SVs_multiple_jets, NSVs)

                    else:

                        #Se c'è già un jet allora mette come indice del jet quello che è più vicino come dR dal vertice
                        jet_1_idx = int(SVs_multiple_jets[jet.svIdx2])
                        sv_particle = SVs[jet.svIdx2]
                        jet_1 = jets[jet_1_idx]
                        dr_1 = deltaR(sv_particle, jet_1)
                        jet_2 = jets[idx_jet] 
                        dr_2 = deltaR(sv_particle, jet_2)
                        # print('dr  1 is: ', dr_1, ' dr 2 is: ', dr_2)
                        if dr_2 < dr_1 and dr_2 <= 0.4: 
                            SVs_multiple_jets[jet.svIdx2] = idx_jet
                        # print('else:',SVs_multiple_jets, NSVs)
            
        # print('list sv is: ', SVs_multiple_jets)

        for idx_fj,fj in enumerate(fatjets):
            #prende il jet e il suo indice e controlla che l'indice del primo sv matchato non sia -1
            # print('fj sv index 1: ', fj.svIdx1, 'index fatjet: ', idx_fj, 'numero di sv: ', NSVs)
            # print('list sv is: ', SVs_multiple_fat_jets)
            if fj.svIdx1 != -1:
                
                if fj.svIdx1 < NSVs: 
                    if SVs_multiple_fat_jets[fj.svIdx1] == -1:
                        sv_particle = SVs[fj.svIdx1]
                        
                        dr = deltaR(sv_particle, fj)
                        # print('dr is: ', dr)
                        if dr <= 0.4:
                            SVs_multiple_fat_jets[fj.svIdx1] = idx_fj
                            # print('if:',SVs_multiple_fat_jets, NSVs)

                    else:

                        #Se c'è già un jet allora mette come indice del jet quello che è più vicino come dR dal vertice
                        fj_1_idx = int(SVs_multiple_fat_jets[fj.svIdx1])
                        sv_particle = SVs[fj.svIdx1]
                        fj_1 = fatjets[fj_1_idx]
                        dr_1 = deltaR(sv_particle, fj_1)
                        fj_2 = fatjets[idx_fj] 
                        dr_2 = deltaR(sv_particle, fj_2)
                        # print('dr  1 is: ', dr_1, ' dr 2 is: ', dr_2)
                        if dr_2 < dr_1 and dr_2 <= 0.4: 
                            SVs_multiple_fat_jets[fj.svIdx1] = idx_fj
                        # print('else:',SVs_multiple_fat_jets, NSVs)
            
            # print('fatjet sv index 2: ', fj.svIdx2, ' index fatjet: ', idx_fj )
            if fj.svIdx2 != -1:
                
                if fj.svIdx2 < NSVs: 
                    if SVs_multiple_fat_jets[fj.svIdx2] == -1:
                        sv_particle = SVs[fj.svIdx2]
                        
                        dr = deltaR(sv_particle,fj)
                        # print('dr is: ', dr)
                        if dr <= 0.4:
                            SVs_multiple_fat_jets[fj.svIdx2] = idx_fj
                            # print('if:',SVs_multiple_fat_jets, NSVs)

                    else:

                        #Se c'è già un jet allora mette come indice del jet quello che è più vicino come dR dal vertice
                        fj_1_idx = int(SVs_multiple_fat_jets[fj.svIdx2])
                        sv_particle = SVs[fj.svIdx2]
                        fj_1 = fatjets[fj_1_idx]
                        dr_1 = deltaR(sv_particle, fj_1)
                        fj_2 = fatjets[idx_fj] 
                        dr_2 = deltaR(sv_particle, fj_2)
                        # print('dr  1 is: ', dr_1, ' dr 2 is: ', dr_2)
                        if dr_2 < dr_1 and dr_2 <= 0.4: 
                            SVs_multiple_fat_jets[fj.svIdx2] = idx_fj
                        # print('else:',SVs_multiple_fat_jets, NSVs)

        for j in SVs_multiple_fat_jets:
            if j != -1:
                print(SVs_multiple_fat_jets)

        for j in range(NSVs):
            SVs_idx[j] = j  
        
        for num_fat_jet,fat_jet_idx in enumerate(SVs_multiple_fat_jets):
            SVs_fat_jets_idx[num_fat_jet] = fat_jet_idx
        
        for num_jet, jet_idx in enumerate(SVs_multiple_jets):
            SVs_jets_idx[num_jet] = jet_idx




        self.out.fillBranch("PFCand_JetIdx"   ,    PFCs_jets_idx )
        self.out.fillBranch("PFCand_FatJetIdx", PFCs_fat_jets_idx)
        self.out.fillBranch("PFCand_Idx"      ,       PFCs_idx   )


        self.out.fillBranch("SV_JetIdx"        ,    SVs_jets_idx  ) 
        self.out.fillBranch("SV_FatJetIdx"     , SVs_fat_jets_idx )
        self.out.fillBranch("SV_Idx"           ,       SVs_idx    )
  
        return True