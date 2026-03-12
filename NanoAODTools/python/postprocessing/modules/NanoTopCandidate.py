import ROOT
import math
import numpy as np
from array import array
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import keras.models 
from itertools import combinations, chain
from scipy.special import comb

def ncombs(n, k):  # return (n k) --> numero di k-ple dati n jets
    if (n-k)<0:
        return 0
    else:
        return factorial(n)/(factorial(n-k)*factorial(k))

def factorial(n):
    if n==0:
        return 1
    elif n<0:
        return 0
    else:
        return n*factorial(n-1)

def lowpt_top(j0, j1, j2):
    return j0.p4() + j1.p4() + j2.p4()

def highpt_top(j0, j1, j2, fj):
    if fj == None:
        top = j0.p4()+j1.p4()+j2.p4()
    elif j2==None:
        top = top2j1fj(fj, j0, j1)
    else:
        top = top3j1fj(fj, j0, j1, j2)
    return top



class nanoTopcand_PFC_SV(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC 
        #serve per controllare se vogliamo distinguere i top falsi senza quark matchati
        #da quelli con almeno un quark matchato
        pass
    def beginJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        "branches Top candidate high pt"
        self.out.branch("nTopMixed", "I")
        self.out.branch("TopMixed_idxFatJet", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet0", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet1", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet2", "I", lenVar="nTopMixed")
        # self.out.branch("IndexesPFC_idxPFC", "I", lenVar = "nIndexesPFC")
        # self.out.branch("nIndexesPFC", "I")
        # self.out.branch("nIndexesSV", "I")
        # self.out.branch("IndexesSV_idxSV", "I", lenVar = "nIndexesSV")
        #self.out.branch("TopMixed_sumjetPt", "F", lenVar="nTopMixed")
        #self.out.branch("TopMixed_sumjetEta", "F", lenVar="nTopMixed")
        #self.out.branch("TopMixed_sumjetPhi", "F", lenVar="nTopMixed")
        #self.out.branch("TopMixed_sumjetMass", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_pt", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_eta", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_phi", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_mass", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_truth", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_category", "I", lenVar = "nTopMixed")
        # self.out.branch("TopMixed_nquark", "I", lenVar = "nTopMixed")
        # "branches Top candidate low pt"
        self.out.branch("nTopResolved", "I")
        self.out.branch("TopResolved_idxJet0", "I", lenVar="nTopResolved")
        self.out.branch("TopResolved_idxJet1", "I", lenVar="nTopResolved")
        self.out.branch("TopResolved_idxJet2", "I", lenVar="nTopResolved")
        self.out.branch("TopResolved_pt", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_eta", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_phi", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_mass", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_truth", "F", lenVar="nTopResolved")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        jets                  =  Collection(event,"Jet")
        njets                 =  len(jets)
        fatjets               =  Collection(event,"FatJet")
        nfatjets              =  len(fatjets)
        goodjets, goodfatjets =  presel(jets, fatjets)
        ngoodjets             =  len(goodjets)
        ngoodfatjets          =  len(goodfatjets)
    
        # PFCands = Collection(event, "PFCand")
        # SVs     = Collection(event, "SV")
        # nPFC    = len(PFCands)
        # nSV     = len(SVs)
        # print('n jets is', njets, 'n good jets is', ngoodjets)
        # print('n fatjets is', nfatjets, 'n good fatjets is', ngoodfatjets)

        # for obj_jet in goodjets:
        #     for index in range(len(jets)):
        #         if jets[index] == obj_jet:
        #             if index != obj_jet.jetIdx: 
        #                 print('AAAAAAAAAAAAAAAAAA')
                    # print('index jets', index)
                    # print('index good jets', obj_jet.jetIdx)
            # index  = jets.index(obj_jet)
            # index_good = obj_jet.jetIdx
            # print(index, index_good)
        pt_cut_low = 10000
        pt_cut_high = 0
        
        '''init variables to branch'''
        ntoplowpt = 0
        # toplow_idxfatjet = []
        toplow_idxjet0 = []
        toplow_idxjet1 = []
        toplow_idxjet2 = []
        toplow_pt_ = []
        toplow_eta_ = []
        toplow_phi_ = []
        toplow_mass_ = []
        # toplow_sumjetdeltarfatjet = []
        # toplow_sumjetmaxdeltarjet = []
        toplow_truth = []
        ntophighpt = 0
        tophigh_idxfatjet = []
        tophigh_idxjet0 = []
        tophigh_idxjet1 = []
        tophigh_idxjet2 = []
        tophigh_idxPFC = []
        tophigh_idxSV = []
        tophigh_category = []
        tophigh_pt_ = []
        tophigh_eta_ = []
        tophigh_phi_ = []
        tophigh_mass_ = []
        tophigh_truth = []
        
        # n_idxPFC = 0
        # n_idxSV = 0 

        # tophigh_idxPFC.append(-1)
        # tophigh_idxSV.append(-1)
        # n_idxPFC += 1 
        # n_idxSV += 1
        #low pt top loop
        for idx_j0 in range(ngoodjets):
            for idx_j1 in range(idx_j0):
                for idx_j2 in range(idx_j1):
                    j0, j1, j2 = goodjets[idx_j0], goodjets[idx_j1], goodjets[idx_j2] #per costruire i top utilizza dei good jets
                    top_p4 = lowpt_top(j0, j1, j2)
                    if top_p4.Pt()<pt_cut_low:
                        ntoplowpt+=1
                        toplow_idxjet0.append(j0.jetIdx) #Riempie però le branch con gli indici dei good jets che puntano al jet (nella collection jet) corrispondente
                        toplow_idxjet1.append(j1.jetIdx)
                        toplow_idxjet2.append(j2.jetIdx)
                        toplow_pt_.append(top_p4.Pt())
                        toplow_eta_.append(top_p4.Eta())
                        toplow_phi_.append(top_p4.Phi())
                        toplow_mass_.append(top_p4.M())
                        if self.isMC:
                            toplow_truth.append(truth(j0=j0, j1=j1, j2=j2))
                        else:
                            toplow_truth.append(0)
        #hCATEGORIA 2JETS 1 FAT JET
        for idx_j0 in range(ngoodjets):
                for idx_j1 in range(idx_j0):
                    for idx_fj in range(ngoodfatjets):
                        j0, j1 = goodjets[idx_j0],goodjets[idx_j1]
                        fj = goodfatjets[idx_fj]
                        top_p4 = highpt_top(j0=j0, j1=j1, j2=None, fj=fj)
                        # print('p4 top', top_p4.Pt())
                        if top_p4.Pt()>pt_cut_high:
                            ntophighpt += 1
                            tophigh_idxfatjet.append(fj.fatjetIdx)
                            tophigh_idxjet0.append(j0.jetIdx)
                            tophigh_idxjet1.append(j1.jetIdx)
                            tophigh_idxjet2.append(-1)
                            tophigh_pt_.append(top_p4.Pt())
                            tophigh_eta_.append(top_p4.Eta())
                            tophigh_phi_.append(top_p4.Phi())
                            tophigh_mass_.append(top_p4.M())
                            tophigh_category.append(2)
                          
                            # for pfcand in PFCands:
                            #     if j0.jetIdx == pfcand.JetIdx:
                            #         tophigh_idxPFC.append(pfcand.Idx)
                            #         n_idxPFC += 1
                            #     elif j1.jetIdx == pfcand.JetIdx:
                            #         tophigh_idxPFC.append(pfcand.Idx)
                            #         n_idxPFC+=1
                            #     elif fj.fatjetIdx == pfcand.FatJetIdx:
                            #         tophigh_idxPFC.append(pfcand.Idx)
                            #         n_idxPFC += 1
                                    
                            # for sv in SVs:
                            #     if j0.jetIdx == sv.JetIdx:
                            #         n_idxSV += 1
                            #         tophigh_idxSV.append(sv.Idx)
                            #     elif j1.jetIdx == sv.JetIdx:
                            #         n_idxSV += 1
                            #         tophigh_idxSV.append(sv.Idx)
                            #     elif fj.fatjetIdx == sv.FatJetIdx:
                            #         tophigh_idxSV.append(sv.Idx)
                            #         n_idxSV +=1 

                            if self.isMC:
                                tophigh_truth.append(truth(j0=j0, j1=j1, fj=fj))
                            else:
                                tophigh_truth.append(0) #0
                            
                            # tophigh_idxPFC.append(-1*(ntophighpt+1))
                            # n_idxPFC += 1

                            # tophigh_idxSV.append(-1*(ntophighpt+1))
                            # n_idxSV += 1

                    # CATEGORIA 3 JETS 
                    for idx_j2 in range(idx_j1):
                        j0, j1, j2 = goodjets[idx_j0],goodjets[idx_j1],goodjets[idx_j2]
                        top_p4 = highpt_top(j0=j0, j1=j1, j2=j2, fj=None)
                        if top_p4.Pt()>pt_cut_high:
                            ntophighpt += 1
                            tophigh_idxfatjet.append(-1)
                            tophigh_idxjet0.append(j0.jetIdx)
                            tophigh_idxjet1.append(j1.jetIdx)
                            tophigh_idxjet2.append(j2.jetIdx)
                            tophigh_pt_.append(top_p4.Pt())
                            tophigh_eta_.append(top_p4.Eta())
                            tophigh_phi_.append(top_p4.Phi())
                            tophigh_mass_.append(top_p4.M())
                            tophigh_category.append(1)

                            # for pfcand in PFCands:
                            #     if j0.jetIdx == pfcand.JetIdx:
                            #         tophigh_idxPFC.append(pfcand.Idx)
                            #         n_idxPFC += 1
                            #     elif j1.jetIdx == pfcand.JetIdx:
                            #         tophigh_idxPFC.append(pfcand.Idx)
                            #         n_idxPFC+=1
                            #     elif j2.jetIdx == pfcand.JetIdx:
                            #         tophigh_idxPFC.append(pfcand.Idx)
                            #         n_idxPFC += 1

                            # for sv in SVs:
                            #     if j0.jetIdx == sv.JetIdx:
                            #         tophigh_idxSV.append(sv.Idx)
                            #         n_idxSV += 1
                            #     elif j1.jetIdx == sv.JetIdx:
                            #         tophigh_idxSV.append(sv.Idx)
                            #         n_idxSV+=1
                            #     elif j2.jetIdx == sv.JetIdx:
                            #         tophigh_idxSV.append(sv.Idx)
                            #         n_idxSV +=1
                            
                            # tophigh_idxPFC.append(-1*(ntophighpt+1))
                            # n_idxPFC +=1

                            # tophigh_idxSV.append(-1*(ntophighpt+1))
                            # n_idxSV +=1


                            if self.isMC:
                                tophigh_truth.append(truth(j0=j0, j1=j1, j2=j2))
                            else:
                                tophigh_truth.append(0) 
                    #categoria 3 jets 1 fat jets
                        for idx_fj in range(ngoodfatjets):
                            j0, j1, j2 = goodjets[idx_j0],goodjets[idx_j1],goodjets[idx_j2]
                            fj = goodfatjets[idx_fj]
                            top_p4 = highpt_top(j0=j0, j1=j1, j2=j2, fj=fj)
                            if top_p4.Pt()>pt_cut_high:
                                ntophighpt += 1
                                tophigh_idxfatjet.append(fj.fatjetIdx)
                                tophigh_idxjet0.append(j0.jetIdx)
                                tophigh_idxjet1.append(j1.jetIdx)
                                tophigh_idxjet2.append(j2.jetIdx)
                                tophigh_pt_.append(top_p4.Pt())
                                tophigh_eta_.append(top_p4.Eta())
                                tophigh_phi_.append(top_p4.Phi())
                                tophigh_mass_.append(top_p4.M())
                                tophigh_category.append(0)

                                # for pfcand in PFCands:
                                #     if j0.jetIdx == pfcand.JetIdx:
                                #         tophigh_idxPFC.append(pfcand.Idx)
                                #         n_idxPFC += 1
                                #     elif j1.jetIdx == pfcand.JetIdx:
                                #         tophigh_idxPFC.append(pfcand.Idx)
                                #         n_idxPFC += 1
                                #     elif j2.jetIdx == pfcand.JetIdx:
                                #         tophigh_idxPFC.append(pfcand.Idx)
                                #         n_idxPFC += 1
                                #     elif fj.fatjetIdx == pfcand.FatJetIdx:
                                #         tophigh_idxPFC.append(pfcand.Idx)
                                #         n_idxPFC += 1


                                # for sv in SVs:
                                #     if j0.jetIdx == sv.JetIdx:
                                #         tophigh_idxSV.append(sv.Idx)
                                #         n_idxSV +=1
                                #     elif j1.jetIdx == sv.JetIdx:
                                #         n_idxSV += 1
                                #         tophigh_idxSV.append(sv.Idx)
                                #     elif j2.jetIdx == sv.JetIdx:
                                #         n_idxSV +=1
                                #         tophigh_idxSV.append(sv.Idx)
                                #     elif fj.fatjetIdx == sv.FatJetIdx:
                                #         n_idxSV += 1
                                #         tophigh_idxSV.append(sv.Idx)
                                
                                # tophigh_idxPFC.append(-1*(ntophighpt+1))
                                # n_idxPFC +=1

                                # tophigh_idxSV.append(-1*(ntophighpt+1))
                                # n_idxSV +=1

                                if self.isMC:
                                    tophigh_truth.append(truth(j0=j0, j1=j1, j2=j2, fj=fj))
                                else: 
                                    tophigh_truth.append(0)  #-1
        
        self.out.fillBranch("nTopResolved",        ntoplowpt)
        self.out.fillBranch("TopResolved_idxJet0", toplow_idxjet0)
        self.out.fillBranch("TopResolved_idxJet1", toplow_idxjet1)
        self.out.fillBranch("TopResolved_idxJet2", toplow_idxjet2)
        self.out.fillBranch("TopResolved_pt",      toplow_pt_)
        self.out.fillBranch("TopResolved_eta",     toplow_eta_)
        self.out.fillBranch("TopResolved_phi",     toplow_phi_)
        self.out.fillBranch("TopResolved_mass",    toplow_mass_)
        self.out.fillBranch("TopResolved_truth",   toplow_truth)
        self.out.fillBranch("nTopMixed",           ntophighpt)
        self.out.fillBranch("TopMixed_idxFatJet",  tophigh_idxfatjet)
        self.out.fillBranch("TopMixed_idxJet0",    tophigh_idxjet0)
        self.out.fillBranch("TopMixed_idxJet1",    tophigh_idxjet1)
        self.out.fillBranch("TopMixed_idxJet2",    tophigh_idxjet2)
        self.out.fillBranch("TopMixed_pt",         tophigh_pt_)
        self.out.fillBranch("TopMixed_eta",        tophigh_eta_)
        self.out.fillBranch("TopMixed_phi",        tophigh_phi_)
        self.out.fillBranch("TopMixed_mass",       tophigh_mass_)
        self.out.fillBranch("TopMixed_truth",      tophigh_truth)
        # self.out.fillBranch("nIndexesPFC",         n_idxPFC)
        # self.out.fillBranch("IndexesPFC_idxPFC",   tophigh_idxPFC)
        # self.out.fillBranch("TopMixed_category",   tophigh_category)
        # self.out.fillBranch("nIndexesSV",          n_idxSV)
        # self.out.fillBranch("IndexesSV_idxSV",     tophigh_idxSV)

        # t1 = datetime.now()
        # print("TopCandidate module time :", t1-t0)  
        return True

