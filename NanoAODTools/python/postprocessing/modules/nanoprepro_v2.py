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


def matching(genpart, gen, jet, sgn_top, dR = 0.4):
    b       = sgn_top*5
    w       = sgn_top*24
    sgn_u   = sgn_top
    sgn_d   = -sgn_top
    match   = False
    jet_out = None

    # Matching della b proveniente da un top con un jet/fatjet
    if (gen.pdgId == b and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == sgn_top*6):
        #print('b quark cand ', gen.pdgId)
        j, dr =  closest_(gen, jet)
        if dr < dR:
            #print('found match b quark', j)
            jet_out = j
            match   = True
    # Matching di un u/c proveniente da una W proveniente dal top con un jet/fatjet      
    elif (gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId) == sgn_u and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == w):
        # La W deve provenire da un top 
        if (genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId == sgn_top*6):
            #print('u quark cand', gen.pdgId)
            j, dr = closest_(gen, jet)
            if dr < dR:
                #print('found match up quark', j)
                jet_out = j
                match   = True
    # Matching di un d/s proveniente da una W proveniente dal top con un jet/fatjet            
    elif (gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId) == sgn_d and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == w):
        # La W deve provenire da un to
        if (genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId == sgn_top*6):
            #print('d quark cand')
            j, dr =  closest_(gen, jet)
            if dr < dR:
                #print('found match down quark', j)
                jet_out = j
                match = True
    return match, jet_out




class nanoprepro(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass
        
        
    def beginJob(self):
        pass
        
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        #self.out.branch("Jet_deltaR",      "F", lenVar="nJet") 
        self.out.branch("Jet_matched",      "F", lenVar="nJet")    # 0,1,2,3
        self.out.branch("Jet_pdgId",        "F", lenVar="nJet")    # quark flav 
        self.out.branch("Jet_topMother",    "F", lenVar="nJet")
        self.out.branch("FatJet_matched",   "F", lenVar="nFatJet") # 0,1,2,3
        self.out.branch("FatJet_pdgId",     "F", lenVar="nFatJet") # quark flav
        self.out.branch("FatJet_topMother", "F", lenVar="nFatJet")

    def endFile(self, inputFile, outputFile, inputTree,wrappedOutputTree):
        pass


    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""        
        jets       = Collection(event,"Jet")
        Njets      = len(jets)
        fatjets    = Collection(event,"FatJet")
        Nfatjets   = len(fatjets)
        muons      = Collection(event, "Muon")
        electrons  = Collection(event, "Electron")
        if self.isMC==1:
            #LHE     = Collection(event, "LHEPart")
            genpart = Collection(event, "GenPart")
        '''init variables to branch'''
        #jets_deltar = []
        #ind_fatjets = []
        #ind_jets    = []
        jets_pdgId        = np.zeros(Njets)
        jets_matched      = np.zeros(Njets)
        jets_topMother    = np.zeros(Njets)
        fatjets_pdgId     = np.zeros(Nfatjets)
        fatjets_matched   = np.zeros(Nfatjets)
        fatjets_topMother = np.zeros(Nfatjets)
        fatjets_truth = np.zeros(Nfatjets)
        if self.isMC==1:
            #if (len(looseMu)>0 or len(looseEle)>0):# and met.pt>25:
            if False:#abs(LHE[1].pdgId)>6 and abs(LHE[2].pdgId)>6:
                return False
            else:
                #print flavquarks
                #print("NEW EVENT <----------------------------")
                
                ntop    = 0
                sgn_top = 0
                for gen in genpart:
                    # Trova i top nei tDM e TTbar
                    if (gen.genPartIdxMother_prompt == -1 and abs(gen.pdgId)==6):
                        if (gen.genPartIdxMother == 0):
                            ntop   += 1
                            sgn_top = gen.pdgId/abs(gen.pdgId)
                    # Trova i top nei Tprime
                    elif (gen.genPartIdxMother_prompt != -1 and abs(gen.pdgId)==6):
                        if ((gen.genPartIdxMother == 0 or abs(genpart[gen.genPartIdxMother_prompt].pdgId) == 8000001)):
                            ntop   += 1
                            sgn_top = gen.pdgId/abs(gen.pdgId)
                #print('# top ',ntop)
                #print(' top sgn ', sgn_top)
                if ntop == 1:
                    uquark_matched   = False
                    dquark_matched   = False 
                    bquark_matched   = False 
                    uquarkFJ_matched = False
                    dquarkFJ_matched = False 
                    bquarkFJ_matched = False 
                elif ntop == 2:
                    b_matched        = False
                    u_matched        = False
                    dbar_matched     = False
                    bbar_matched     = False                    
                    d_matched        = False
                    ubar_matched     = False
                    bFJ_matched      = False
                    uFJ_matched      = False
                    dbarFJ_matched   = False
                    bbarFJ_matched   = False                    
                    dFJ_matched      = False
                    ubarFJ_matched   = False
                for gen in genpart:
                    tosave = False
                    if ntop == 1:
                        match, j = matching(genpart, gen, jets, sgn_top)
                        #if match: print("jet matched ", match, gen.pdgId, j, sgn_top)
                    elif ntop ==2:
                        match, j = matching(genpart, gen, jets, +1)
                        #print('top +6 :', match, j)
                        sgn_top = 1
                        if not match:
                            match, j = matching(genpart, gen, jets, -1)
                            sgn_top = -1
                            #print('top -6 :', match, j)
                    else: match = False
                    #print("genpart (b,u,d)", bquark_matched, uquark_matched, dquark_matched)
                    #print(match)
                    if (match and ntop == 1 and not (bquark_matched*uquark_matched*dquark_matched)):
                        #print("genpart matched (b,u,d)", bquark_matched, uquark_matched, dquark_matched)
                        if (not bquark_matched and gen.pdgId==sgn_top*5) :
                            #print('b quark matched')
                            bquark_matched = True
                            tosave = True
                        elif (not uquark_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top): 
                            #print('u quark matched')
                            uquark_matched = True
                            tosave = True
                        elif (not dquark_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top): 
                            #print('d quark matched')
                            dquark_matched = True
                            tosave = True
                        if tosave:
                            #print("saving jet #", j, gen.pdgId)
                            jets_topMother[j] = sgn_top*6
                            jets_matched[j] += 1
                            if jets_matched[j]==1: jets_pdgId[j] = abs(gen.pdgId)
                            elif jets_matched[j]==2: jets_pdgId[j] += abs(gen.pdgId)*10
                            elif jets_matched[j]==3: jets_pdgId[j] += abs(gen.pdgId)*100
                            #ind_jets[j] = j

                    elif (match and ntop == 2):
                        #print  sgn_top
                        if(sgn_top == 1 and not b_matched*u_matched*dbar_matched):
                            #print "t"
                            if (not b_matched and gen.pdgId==sgn_top*5) :
                                #print "   b matched"
                                b_matched = True
                                tosave = True
                            elif (not u_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                #print "   u matched"
                                u_matched = True
                                tosave = True
                            elif (not dbar_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                #print "   dbar matched"
                                dbar_matched = True
                                tosave = True
                            if tosave :
                                #print "...saving jet pgd"
                                jets_topMother[j] = sgn_top*6
                                jets_matched[j] += 1
                                if jets_matched[j]==1: jets_pdgId[j] = abs(gen.pdgId)
                                elif jets_matched[j]==2: jets_pdgId[j] += abs(gen.pdgId)*10
                                elif jets_matched[j]==3: jets_pdgId[j] += abs(gen.pdgId)*100
                                #ind_jets[-1] = j
                        elif(sgn_top == -1 and not bbar_matched*ubar_matched*d_matched):
                            #print "tbar"
                            if (not bbar_matched and gen.pdgId==sgn_top*5) :
                                #print "   bbar matched"
                                bbar_matched = True
                                tosave = True
                            elif (not ubar_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                #print "   ubar matched"
                                ubar_matched = True
                                tosave = True
                            elif (not d_matched and gen.pdgId%2 != 0 and abs(gen.pdgId)!=5 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                #print "   d matched"
                                d_matched = True
                                tosave = True
                            if tosave:
                                #print "...saving jet pgd"
                                jets_topMother[j] = sgn_top*6
                                jets_matched[j]  += 1
                                #print(jets_matched[j])
                                if jets_matched[j]  ==1: jets_pdgId[j] = abs(gen.pdgId)
                                elif jets_matched[j]==2: jets_pdgId[j] += abs(gen.pdgId)*10
                                elif jets_matched[j]==3: jets_pdgId[j] += abs(gen.pdgId)*100
                                #ind_jets[-1] = j
    
                for gen in genpart:
                    tosave = False
                    if ntop == 1:
                        match,j = matching(genpart, gen, fatjets, sgn_top, dR=0.8)
                    elif ntop ==2:
                        match,j = matching(genpart, gen, fatjets, +1, dR=0.8)
                        sgn_top = 1
                        if not match:
                            match,j = matching(genpart, gen, fatjets, -1, dR=0.8)
                            sgn_top = -1
                    else: match = False

                    if (match and ntop ==1 and 
                        not (bquarkFJ_matched*uquarkFJ_matched*dquarkFJ_matched)):
                        
                        if (not bquarkFJ_matched and gen.pdgId==sgn_top*5) : 
                            bquarkFJ_matched = True
                            tosave = True
                        elif (not uquarkFJ_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top): 
                            uquarkFJ_matched = True
                            tosave = True
                        elif (not dquarkFJ_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top): 
                            dquarkFJ_matched = True
                            tosave = True
                        if tosave:
                            fatjets_topMother[j] = sgn_top*6
                            fatjets_matched[j] += 1
                            if fatjets_matched[j]==1: fatjets_pdgId[j] = abs(gen.pdgId)
                            elif fatjets_matched[j]==2: fatjets_pdgId[j] += abs(gen.pdgId)*10
                            elif fatjets_matched[j]==3: fatjets_pdgId[j] += abs(gen.pdgId)*100

                    elif (match and ntop == 2):
                        #print  sgn_top
                        if(sgn_top == 1 and not bFJ_matched*uFJ_matched*dbarFJ_matched):
                            #print "t"
                            if (not bFJ_matched and gen.pdgId==sgn_top*5) :
                                #print "   b matched"
                                bFJ_matched = True
                                tosave = True
                            elif (not uFJ_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                #print "   u matched"
                                uFJ_matched = True
                                tosave = True
                            elif (not dbarFJ_matched and gen.pdgId%2 != 0 and abs(gen.pdgId)!=5 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                #print "   dbar matched"
                                dbarFJ_matched = True
                                tosave = True
                            if tosave :
                                #print "...saving jet pgd"
                                fatjets_topMother[j] = sgn_top*6
                                fatjets_matched[j] += 1
                                if fatjets_matched[j]==1: fatjets_pdgId[j] = abs(gen.pdgId)
                                elif fatjets_matched[j]==2: fatjets_pdgId[j] += abs(gen.pdgId)*10
                                elif fatjets_matched[j]==3: fatjets_pdgId[j] += abs(gen.pdgId)*100
                            
                        elif(sgn_top == -1 and not bbarFJ_matched*ubarFJ_matched*dFJ_matched):
                            #print "tbar"
                            if (not bbarFJ_matched and gen.pdgId==sgn_top*5) :
                                #print "   bbar matched"
                                bbarFJ_matched = True
                                tosave = True
                            elif (not ubarFJ_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                #print "   ubar matched"
                                ubarFJ_matched = True
                                tosave = True
                            elif (not dFJ_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                #print "   d matched"
                                dFJ_matched = True
                                tosave = True
                            if tosave:
                                #print "...saving jet pgd"
                                fatjets_topMother[j] = sgn_top*6
                                fatjets_matched[j] += 1
                                if fatjets_matched[j]==1: fatjets_pdgId[j] = abs(gen.pdgId)
                                elif fatjets_matched[j]==2: fatjets_pdgId[j] += abs(gen.pdgId)*10
                                elif fatjets_matched[j]==3: fatjets_pdgId[j] += abs(gen.pdgId)*100
                                 
                                
                #self.out.fillBranch("Jet_deltaR", jets_deltar)
                #print(jets_topMother)
                self.out.fillBranch("Jet_matched", jets_matched)
                self.out.fillBranch("Jet_pdgId", jets_pdgId)
                self.out.fillBranch("Jet_topMother", jets_topMother)
                
                self.out.fillBranch("FatJet_matched", fatjets_matched)
                self.out.fillBranch("FatJet_pdgId", fatjets_pdgId)
                self.out.fillBranch("FatJet_topMother", fatjets_topMother)

                #self.out.fillBranch("Top_indFatJet", ind_fatjets) 
                #self.out.fillBranch("Top_indJet", ind_jets) 
                # t1 = datetime.now()
                # print("nanprepro module time :", t1-t0) 
                return True
