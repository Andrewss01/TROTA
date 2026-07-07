import os, ROOT
from math import hypot, pi
import numpy as np

# ========= UTILITIES =======================
def topcategory(top):  #take as argument a top candidate and return an int : 0 = 3j1fj, 1 = 3j0fj, 2 = 2j1fj 
    top_category = 0
    if top.idxFatJet==-1: #idxFatJet
        top_category = 1
    elif top.idxJet2==-1:
        top_category = 2
    return top_category

def top_select(top, trs, ptmin, ptmax, dR, category):
    debug = False
    if 'mix' in category:
        tops = np.array(list(filter(lambda x : (x.pt<ptmax)*(x.pt>ptmin)*(x.score2>trs) , top)))
        scores = np.array([t.score2 for t in tops])
        if debug: print("mix category:", tops, scores, [t.score2 for t in tops])
    elif 'res' in category:
        tops = np.array(list(filter(lambda x : (x.pt<ptmax)*(x.scoreDNN>trs) , top)))
        scores = np.array([t.scoreDNN for t in tops])
        if debug: print("res category:", tops, scores, [t.scoreDNN for t in tops])
    elif 'mer' in category:
        tops = np.array(list(filter(lambda x : (x.pt>ptmin)*(x.deepTag_TvsQCD>trs) , top)))
        scores = np.array([t.deepTag_TvsQCD for t in tops])
        if debug: print("mer category:", tops, scores, [t.deepTag_TvsQCD for t in tops])
    top_sel = []
    
    if debug: print("scores before loop ", scores)
    if debug: print("tops before loop ", tops)
    while(np.sum(scores!=0)>0):
        drs = np.array([deltaR(tops[np.argmax(scores)], t) for t in tops])
        if debug: print("deltaRs ", drs)
        for i, d in enumerate(drs):
            if i==np.argmax(scores): continue
            if d<dR: scores[i]=0
        if debug: print("scores after grooming :", scores)    
        top_sel.append(tops[np.argmax(scores)])
        if debug: print("before top grooming (scores, tops):", scores, tops)    
        scores[np.argmax(scores)]=0
        tops = tops[scores!=0]
        scores = scores[scores!=0]
        if debug: print("after top grooming (scores, tops):", scores, tops)    
        drs = np.array([deltaR(tops[np.argmax(scores)], t) for t in tops])
        if debug: print('top selezionati', len(top_sel))
        if debug: print('deltaRs', drs)
    return top_sel

def get_category_top_collection(category, top): #return a collection of tops of the same category
    if category == 0:
        return list(filter(lambda x : x.idxFatJet!=-1 and x.idxJet2!=-1 , top))
    elif category == 1:
        return list(filter(lambda x : x.idxFatJet==-1, top))
    elif category == 2:
        return list(filter(lambda x : x.idxJet2==-1 , top))
    else:
        print("idx category error: ", category)
        return None

def get_best_top(top, score= '', list_idx_toskip = None): #take as argument Top collection return the top with the best score
    #NB: list_idx must be a list python! Numpy array fail such as every other kind of iterable object
    top_score = -100
    top_score_p2 = -100
    t_best = None
    t_best_p2 = None
    if isinstance(list_idx_toskip, list): 
        skip_top = True
    else :
        skip_top=False
    for i, t in enumerate(top):
        if skip_top and i in list_idx_toskip: continue
        if t.score>top_score : 
            top_score = t.score
            t_best = t
        if t.score_p2>top_score_p2 : 
            top_score_p2 = t.score
            t_best_p2 = t
    if '2' in score:
        return t_best_p2
    else:
        return t_best

def get_top_over_trs(top, trs, model): #take as argument Top collection and trashold return the top that pass the selection
    if 'DNN' in model:
        return list(filter(lambda x : x.scoreDNN>trs , top))###
    if 'LSTM' in model:
        return list(filter(lambda x : x.scoreLSTM>trs , top))###
    if 'highpt' in model:
        return list(filter(lambda x : x.score>trs , top))###

def to_clusterize(top1 , top2): 
    if (top1.idxFatJet == top2.idxFatJet) and (top1.idxFatJet!=-1): 
        return True
    else:
        list_jet1 = [top1.idxJet0, top1.idxJet1, top1.idxJet2]
        list_jet2 = [top2.idxJet0, top2.idxJet1, top2.idxJet2]
        if -1 in list_jet1: list_jet1.remove(-1)
        if -1 in list_jet2: list_jet2.remove(-1)
        b = False
        for l in list_jet2:
            if l in list_jet1:
                b= True
        return b

def top_cluster(top, trs):
    top_over_trs = get_top_over_trs(top,trs)
    list_score = np.zeros((len(top_over_trs), len(top)))
    n_cluster = np.zeros(len(top_over_trs))
    n_cluster_over_trs = np.zeros(len(top_over_trs))
    n_up, n_down = np.zeros(len(top_over_trs)), np.zeros(len(top_over_trs))
    n_up_over_trs, n_down_over_trs = np.zeros(len(top_over_trs)), np.zeros(len(top_over_trs))
    for i, t in enumerate(top_over_trs):
        for j, t_ in enumerate(top):
            if not to_clusterize(t, t_): continue
            list_score[i, j] = t_.score
            n_cluster[i]+=1
            if t_.score>trs: n_cluster_over_trs[i] +=1
        n_up[i], n_down[i] = np.sum(list_score[i]>t.score), np.sum(list_score[i]<t.score)
        n_up_over_trs[i], n_down_over_trs[i] = np.sum((list_score[i]>t.score)*(list_score[i]>trs)), np.sum((list_score[i]<t.score)*(list_score[i]>trs))
    dictOut = {
        "n_cluster": n_cluster, "n_cluster_over_trs": n_cluster_over_trs,
        "n_up": n_up, "n_down": n_down,
        "n_up_over_trs": n_up_over_trs, "n_down_over_trs": n_down_over_trs
    }
    return dictOut

#############
def top_cluster_excl(top, trs):
    top_over_trs = get_top_over_trs(top,trs) # fixed collection 
    #variabili da portare fuori 
    list_score = np.zeros((len(top_over_trs), len(top)))
    n_cluster = np.zeros(len(top_over_trs))
    best_score = np.zeros(len(top_over_trs))
    n_cluster_over_trs = np.zeros(len(top_over_trs))
    n_up, n_down = np.zeros(len(top_over_trs)), np.zeros(len(top_over_trs))
    n_up_over_trs, n_down_over_trs = np.zeros(len(top_over_trs)), np.zeros(len(top_over_trs))
    #loop sui top over trs --> partendo dal best
    idx_top_toskip = []
    i = 0 
    #print('idx_top_toskip ', idx_top_toskip)
    #print('len top over trs ', len(top_over_trs))
    while(len(idx_top_toskip)<len(top_over_trs)):
        #print('i ', i)
        #print('idx_top_toskip init loop', idx_top_toskip)
        best_top = get_best_top(top_over_trs, list_idx_toskip = idx_top_toskip)
        best_score[i] = best_top.score
        #print('best top score', best_top.score)
        for j, t_ in enumerate(top):
            if not to_clusterize(best_top, t_): continue
            #print(n_cluster[i])
            list_score[i,j] = t_.score
            n_cluster[i] +=1
        for n, t_ in enumerate(top_over_trs):
            if (not to_clusterize(best_top,t_) and n in idx_top_toskip): continue
            n_cluster_over_trs[i] += 1
            idx_top_toskip.append(n)
        #print('idx_top_toskip fin loop', idx_top_toskip)
        n_up[i], n_down[i] = np.sum(list_score[i]>best_top.score), np.sum(list_score[i]<best_top.score)
        n_up_over_trs[i], n_down_over_trs[i] = np.sum((list_score[i]>best_top.score)*(list_score[i]>trs)), np.sum((list_score[i]<best_top.score)*(list_score[i]>trs))
        i+=1
    dictOut = {
        "n_cluster": n_cluster[:i], "n_cluster_over_trs": n_cluster_over_trs[:i], "best_score": best_score[:i], 
        "n_up": n_up[:i], "n_down": n_down[:i],
        "n_up_over_trs": n_up_over_trs[:i], "n_down_over_trs": n_down_over_trs[:i]
    }
    return dictOut
##########################
 

def get_pos_nums(num):
    pos_nums = []
    while num != 0:
        pos_nums.append(num % 10)
        num = num // 10
    return pos_nums

def truth(j0=0, j1=0, j2=0, fj=0):
    top_truth = 0
    if not hasattr(j2, "pt"):
        if ((j0.matched>0 and j1.matched>0 and fj.matched>0) and
            (j0.topMother== j1.topMother and j0.topMother== fj.topMother)):
            flavs_j0, flavs_j1, flavs_fj = j0.pdgId, j1.pdgId, fj.pdgId
            jetflavs_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) 
            fatjetflavs_list = get_pos_nums(flavs_fj)
        else: 
            jetflavs_list = []
            fatjetflavs_list = []
    else:
        if hasattr(fj, "pt"):
            if ((j0.matched>0 and j1.matched>0 and j2.matched>0 and fj.matched>0) and
                (j0.topMother== j1.topMother and j1.topMother== j2.topMother and
                   j2.topMother==fj.topMother)):
                flavs_j0, flavs_j1, flavs_j2, flavs_fj = j0.pdgId, j1.pdgId, j2.pdgId, fj.pdgId
                jetflavs_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) + get_pos_nums(flavs_j2)
                fatjetflavs_list = get_pos_nums(flavs_fj)
            else: 
                jetflavs_list = []
                fatjetflavs_list = []
        else:
            if ((j0.matched>0 and j1.matched>0 and j2.matched>0) and
                ( j0.topMother== j1.topMother and j1.topMother== j2.topMother)): 
                flavs_j0, flavs_j1, flavs_j2 = j0.pdgId, j1.pdgId, j2.pdgId
                jetflavs_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) + get_pos_nums(flavs_j2)
                fatjetflavs_list = []
            else: 
                jetflavs_list = []
                fatjetflavs_list = []
    
    if len(jetflavs_list)==3:
        top_truth = 1
    elif len(fatjetflavs_list)==3:
        top_truth = 1
    elif len(np.unique(jetflavs_list+fatjetflavs_list))==3:
        top_truth = 1
    else:
        top_truth = 0

    # if len(jetflavs_list) != 0 and len(fatjetflavs_list) != 0:
    #     print('jet:', jetflavs_list)
    #     print('fatjet:' ,fatjetflavs_list)
    #     print(top_truth)
    # elif len(jetflavs_list) != 0 and len(fatjetflavs_list) ==0:
    #     print('jet:', jetflavs_list)
    #     print(top_truth)
    # elif len(fatjetflavs_list) != 0 and len(jetflavs_list) == 0:
    #     print('fatjet: ',fatjetflavs_list)
    #     print(top_truth)
    return top_truth

def top_p4(category, top, jets, fatjets):
    if category == 0:
        p4 = top3j1fj(fatjets[top.idxFatJet], jets[top.idxJet0], jets[top.idxJet1], jets[top.idxJet2])
    elif category == 1:
        p4 = jets[top.idxJet0].p4() + jets[top.idxJet1].p4() + jets[top.idxJet2].p4()
    elif category == 2:
        p4 = top2j1fj(fatjets[top.idxFatJet], jets[top.idxJet0], jets[top.idxJet1])
    else:
        print("Error idx Top category not ecpected : ", category)
    return p4

def top2j1fj(fj, j0, j1, dr0=None, dr1=None, s= None):
    p4 = ROOT.TLorentzVector()
    if dr0==None:
        dr0 = deltaR(fj,j0)<0.8 
        dr1 = deltaR(fj,j1)<0.8
    if dr0*dr1:
        if s == "nominal":
            p4.SetPtEtaPhiM(fj.pt_nominal, fj.eta, fj.phi, fj.mass_nominal)
        elif s == "jesTotalup":
            p4.SetPtEtaPhiM(fj.pt_jesTotalup, fj.eta, fj.phi, fj.mass_jesTotalup)
        elif s == "jesTotaldown":
            p4.SetPtEtaPhiM(fj.pt_jesTotaldown, fj.eta, fj.phi, fj.mass_jesTotaldown)
        elif s == "jerup":
            p4.SetPtEtaPhiM(fj.pt_jerup, fj.eta, fj.phi, fj.mass_jerup)
        elif s == "jerdown":
            p4.SetPtEtaPhiM(fj.pt_jerdown, fj.eta, fj.phi, fj.mass_jerdown)
        elif s == None:
            p4.SetPtEtaPhiM(fj.pt, fj.eta, fj.phi, fj.mass)
    elif dr0:
        fj_p4, j1_p4 = ROOT.TLorentzVector(), ROOT.TLorentzVector()
        if s == "nominal":
            fj_p4.SetPtEtaPhiM(fj.pt_nominal, fj.eta, fj.phi, fj.mass_nominal)
            j1_p4.SetPtEtaPhiM(j1.pt_nominal, j1.eta, j1.phi, j1.mass_nominal)
        elif s == "jesTotalup":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotalup, fj.eta, fj.phi, fj.mass_jesTotalup)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotalup, j1.eta, j1.phi, j1.mass_jesTotalup)
        elif s == "jesTotaldown":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotaldown, fj.eta, fj.phi, fj.mass_jesTotaldown)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotaldown, j1.eta, j1.phi, j1.mass_jesTotaldown)
        elif s == "jerup":
            fj_p4.SetPtEtaPhiM(fj.pt_jerup, fj.eta, fj.phi, fj.mass_jerup)
            j1_p4.SetPtEtaPhiM(j1.pt_jerup, j1.eta, j1.phi, j1.mass_jerup)
        elif s == "jerdown":
            fj_p4.SetPtEtaPhiM(fj.pt_jerdown, fj.eta, fj.phi, fj.mass_jerdown)
            j1_p4.SetPtEtaPhiM(j1.pt_jerdown, j1.eta, j1.phi, j1.mass_jerdown)
        elif s == None:
            fj_p4.SetPtEtaPhiM(fj.pt, fj.eta, fj.phi, fj.mass)
            j1_p4.SetPtEtaPhiM(j1.pt, j1.eta, j1.phi, j1.mass)
        p4 = fj_p4 + j1_p4
    elif dr1:
        fj_p4, j0_p4 = ROOT.TLorentzVector(), ROOT.TLorentzVector()
        if s == "nominal":
            fj_p4.SetPtEtaPhiM(fj.pt_nominal, fj.eta, fj.phi, fj.mass_nominal)
            j0_p4.SetPtEtaPhiM(j0.pt_nominal, j0.eta, j0.phi, j0.mass_nominal)
        elif s == "jesTotalup":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotalup, fj.eta, fj.phi, fj.mass_jesTotalup)
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotalup, j0.eta, j0.phi, j0.mass_jesTotalup)
        elif s == "jesTotaldown":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotaldown, fj.eta, fj.phi, fj.mass_jesTotaldown)
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotaldown, j0.eta, j0.phi, j0.mass_jesTotaldown)
        elif s == "jerup":
            fj_p4.SetPtEtaPhiM(fj.pt_jerup, fj.eta, fj.phi, fj.mass_jerup)
            j0_p4.SetPtEtaPhiM(j0.pt_jerup, j0.eta, j0.phi, j0.mass_jerup)
        elif s == "jerdown":
            fj_p4.SetPtEtaPhiM(fj.pt_jerdown, fj.eta, fj.phi, fj.mass_jerdown)
            j0_p4.SetPtEtaPhiM(j0.pt_jerdown, j0.eta, j0.phi, j0.mass_jerdown)
        elif s == None:
            fj_p4.SetPtEtaPhiM(fj.pt, fj.eta, fj.phi, fj.mass)
            j0_p4.SetPtEtaPhiM(j0.pt, j0.eta, j0.phi, j0.mass)
        p4 = fj_p4 + j0_p4
    else:
        fj_p4, j0_p4, j1_p4 = ROOT.TLorentzVector(), ROOT.TLorentzVector(), ROOT.TLorentzVector()
        if s == "nominal":
            fj_p4.SetPtEtaPhiM(fj.pt_nominal, fj.eta, fj.phi, fj.mass_nominal)
            j0_p4.SetPtEtaPhiM(j0.pt_nominal, j0.eta, j0.phi, j0.mass_nominal)
            j1_p4.SetPtEtaPhiM(j1.pt_nominal, j1.eta, j1.phi, j1.mass_nominal)
        elif s == "jesTotalup":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotalup, fj.eta, fj.phi, fj.mass_jesTotalup)
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotalup, j0.eta, j0.phi, j0.mass_jesTotalup)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotalup, j1.eta, j1.phi, j1.mass_jesTotalup)
        elif s == "jesTotaldown":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotaldown, fj.eta, fj.phi, fj.mass_jesTotaldown)
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotaldown, j0.eta, j0.phi, j0.mass_jesTotaldown)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotaldown, j1.eta, j1.phi, j1.mass_jesTotaldown)
        elif s == "jerup":
            fj_p4.SetPtEtaPhiM(fj.pt_jerup, fj.eta, fj.phi, fj.mass_jerup)
            j0_p4.SetPtEtaPhiM(j0.pt_jerup, j0.eta, j0.phi, j0.mass_jerup)
            j1_p4.SetPtEtaPhiM(j1.pt_jerup, j1.eta, j1.phi, j1.mass_jerup)
        elif s == "jerdown":
            fj_p4.SetPtEtaPhiM(fj.pt_jerdown, fj.eta, fj.phi, fj.mass_jerdown)
            j0_p4.SetPtEtaPhiM(j0.pt_jerdown, j0.eta, j0.phi, j0.mass_jerdown)
            j1_p4.SetPtEtaPhiM(j1.pt_jerdown, j1.eta, j1.phi, j1.mass_jerdown)
        elif s == None:
            fj_p4.SetPtEtaPhiM(fj.pt, fj.eta, fj.phi, fj.mass)
            j0_p4.SetPtEtaPhiM(j0.pt, j0.eta, j0.phi, j0.mass)
            j1_p4.SetPtEtaPhiM(j1.pt, j1.eta, j1.phi, j1.mass)
        p4 = fj_p4 + j0_p4 + j1_p4
    #print(p4, p4.M())
    return p4

def top3j1fj(fj, j0, j1, j2, dr0=None, dr1=None, dr2=None, s=None):
    p4 = ROOT.TLorentzVector()
    if dr0==None:
        dr0 = deltaR(fj,j0)<0.8
        dr1 = deltaR(fj,j1)<0.8
        dr2 = deltaR(fj,j2)<0.8
    if dr0*dr1*dr2:
        if s == "nominal":
            p4.SetPtEtaPhiM(fj.pt_nominal, fj.eta, fj.phi, fj.mass_nominal)
        elif s == "jesTotalup":
            p4.SetPtEtaPhiM(fj.pt_jesTotalup, fj.eta, fj.phi, fj.mass_jesTotalup)
        elif s == "jesTotaldown":
            p4.SetPtEtaPhiM(fj.pt_jesTotaldown, fj.eta, fj.phi, fj.mass_jesTotaldown)
        elif s == "jerup":
            p4.SetPtEtaPhiM(fj.pt_jerup, fj.eta, fj.phi, fj.mass_jerup)
        elif s == "jerdown":
            p4.SetPtEtaPhiM(fj.pt_jerdown, fj.eta, fj.phi, fj.mass_jerdown)
        elif s == None:
            p4.SetPtEtaPhiM(fj.pt, fj.eta, fj.phi, fj.mass)
    elif dr0*dr1:
        fj_p4, j2_p4 = ROOT.TLorentzVector(), ROOT.TLorentzVector()
        if s == "nominal":
            fj_p4.SetPtEtaPhiM(fj.pt_nominal, fj.eta, fj.phi, fj.mass_nominal)
            j2_p4.SetPtEtaPhiM(j2.pt_nominal, j2.eta, j2.phi, j2.mass_nominal)
        elif s == "jesTotalup":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotalup, fj.eta, fj.phi, fj.mass_jesTotalup)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotalup, j2.eta, j2.phi, j2.mass_jesTotalup)
        elif s == "jesTotaldown":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotaldown, fj.eta, fj.phi, fj.mass_jesTotaldown)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotaldown, j2.eta, j2.phi, j2.mass_jesTotaldown)
        elif s == "jerUp":
            fj_p4.SetPtEtaPhiM(fj.pt_jerup, fj.eta, fj.phi, fj.mass_jerup)
            j2_p4.SetPtEtaPhiM(j2.pt_jerup, j2.eta, j2.phi, j2.mass_jerup)
        elif s == "jerdown":
            fj_p4.SetPtEtaPhiM(fj.pt_jerdown, fj.eta, fj.phi, fj.mass_jerdown)
            j2_p4.SetPtEtaPhiM(j2.pt_jerdown, j2.eta, j2.phi, j2.mass_jerdown)
        elif s == None:
            fj_p4.SetPtEtaPhiM(fj.pt, fj.eta, fj.phi, fj.mass)
            j2_p4.SetPtEtaPhiM(j2.pt, j2.eta, j2.phi, j2.mass)
        p4 = fj_p4 + j2_p4
    elif dr0*dr2:
        fj_p4, j1_p4 = ROOT.TLorentzVector(), ROOT.TLorentzVector()
        if s == "nominal":
            fj_p4.SetPtEtaPhiM(fj.pt_nominal, fj.eta, fj.phi, fj.mass_nominal)
            j1_p4.SetPtEtaPhiM(j1.pt_nominal, j1.eta, j1.phi, j1.mass_nominal)
        elif s == "jesTotalup":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotalup, fj.eta, fj.phi, fj.mass_jesTotalup)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotalup, j1.eta, j1.phi, j1.mass_jesTotalup)
        elif s == "jesTotaldown":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotaldown, fj.eta, fj.phi, fj.mass_jesTotaldown)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotaldown, j1.eta, j1.phi, j1.mass_jesTotaldown)
        elif s == "jerUp":
            fj_p4.SetPtEtaPhiM(fj.pt_jerup, fj.eta, fj.phi, fj.mass_jerup)
            j1_p4.SetPtEtaPhiM(j1.pt_jerup, j1.eta, j1.phi, j1.mass_jerup)
        elif s == "jerdown":
            fj_p4.SetPtEtaPhiM(fj.pt_jerdown, fj.eta, fj.phi, fj.mass_jerdown)
            j1_p4.SetPtEtaPhiM(j1.pt_jerdown, j1.eta, j1.phi, j1.mass_jerdown)
        elif s == None:
            fj_p4.SetPtEtaPhiM(fj.pt, fj.eta, fj.phi, fj.mass)
            j1_p4.SetPtEtaPhiM(j1.pt, j1.eta, j1.phi, j1.mass)
        p4 = fj_p4 + j1_p4
    elif dr1*dr2:
        fj_p4, j0_p4 = ROOT.TLorentzVector(), ROOT.TLorentzVector()
        if s == "nominal":
            fj_p4.SetPtEtaPhiM(fj.pt_nominal, fj.eta, fj.phi, fj.mass_nominal)
            j0_p4.SetPtEtaPhiM(j0.pt_nominal, j0.eta, j0.phi, j0.mass_nominal)
        elif s == "jesTotalup":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotalup, fj.eta, fj.phi, fj.mass_jesTotalup)
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotalup, j0.eta, j0.phi, j0.mass_jesTotalup)
        elif s == "jesTotaldown":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotaldown, fj.eta, fj.phi, fj.mass_jesTotaldown)
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotaldown, j0.eta, j0.phi, j0.mass_jesTotaldown)
        elif s == "jerUp":
            fj_p4.SetPtEtaPhiM(fj.pt_jerup, fj.eta, fj.phi, fj.mass_jerup)
            j0_p4.SetPtEtaPhiM(j0.pt_jerup, j0.eta, j0.phi, j0.mass_jerup)
        elif s == "jerdown":
            fj_p4.SetPtEtaPhiM(fj.pt_jerdown, fj.eta, fj.phi, fj.mass_jerdown)
            j0_p4.SetPtEtaPhiM(j0.pt_jerdown, j0.eta, j0.phi, j0.mass_jerdown)
        elif s == None:
            fj_p4.SetPtEtaPhiM(fj.pt, fj.eta, fj.phi, fj.mass)
            j0_p4.SetPtEtaPhiM(j0.pt, j0.eta, j0.phi, j0.mass)
        p4 = fj_p4 + j0_p4
    elif dr0:
        fj_p4, j1_p4, j2_p4 = ROOT.TLorentzVector(), ROOT.TLorentzVector(), ROOT.TLorentzVector()
        if s == "nominal":
            fj_p4.SetPtEtaPhiM(fj.pt_nominal, fj.eta, fj.phi, fj.mass_nominal)
            j1_p4.SetPtEtaPhiM(j1.pt_nominal, j1.eta, j1.phi, j1.mass_nominal)
            j2_p4.SetPtEtaPhiM(j2.pt_nominal, j2.eta, j2.phi, j2.mass_nominal)
        elif s == "jesTotalup":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotalup, fj.eta, fj.phi, fj.mass_jesTotalup)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotalup, j1.eta, j1.phi, j1.mass_jesTotalup)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotalup, j2.eta, j2.phi, j2.mass_jesTotalup)
        elif s == "jesTotaldown":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotaldown, fj.eta, fj.phi, fj.mass_jesTotaldown)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotaldown, j1.eta, j1.phi, j1.mass_jesTotaldown)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotaldown, j2.eta, j2.phi, j2.mass_jesTotaldown)
        elif s == "jerUp":
            fj_p4.SetPtEtaPhiM(fj.pt_jerup, fj.eta, fj.phi, fj.mass_jerup)
            j1_p4.SetPtEtaPhiM(j1.pt_jerup, j1.eta, j1.phi, j1.mass_jerup)
            j2_p4.SetPtEtaPhiM(j2.pt_jerup, j2.eta, j2.phi, j2.mass_jerup)
        elif s == "jerdown":
            fj_p4.SetPtEtaPhiM(fj.pt_jerdown, fj.eta, fj.phi, fj.mass_jerdown)
            j1_p4.SetPtEtaPhiM(j1.pt_jerdown, j1.eta, j1.phi, j1.mass_jerdown)
            j2_p4.SetPtEtaPhiM(j2.pt_jerdown, j2.eta, j2.phi, j2.mass_jerdown)
        elif s == None:
            fj_p4.SetPtEtaPhiM(fj.pt, fj.eta, fj.phi, fj.mass)
            j1_p4.SetPtEtaPhiM(j1.pt, j1.eta, j1.phi, j1.mass)
            j2_p4.SetPtEtaPhiM(j2.pt, j2.eta, j2.phi, j2.mass)
        p4 = fj_p4 + j1_p4 + j2_p4
    elif dr1:
        fj_p4, j0_p4, j2_p4 = ROOT.TLorentzVector(), ROOT.TLorentzVector(), ROOT.TLorentzVector()
        if s == "nominal":
            fj_p4.SetPtEtaPhiM(fj.pt_nominal, fj.eta, fj.phi, fj.mass_nominal)
            j0_p4.SetPtEtaPhiM(j0.pt_nominal, j0.eta, j0.phi, j0.mass_nominal)
            j2_p4.SetPtEtaPhiM(j2.pt_nominal, j2.eta, j2.phi, j2.mass_nominal)
        elif s == "jesTotalup":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotalup, fj.eta, fj.phi, fj.mass_jesTotalup)
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotalup, j0.eta, j0.phi, j0.mass_jesTotalup)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotalup, j2.eta, j2.phi, j2.mass_jesTotalup)
        elif s == "jesTotaldown":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotaldown, fj.eta, fj.phi, fj.mass_jesTotaldown)
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotaldown, j0.eta, j0.phi, j0.mass_jesTotaldown)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotaldown, j2.eta, j2.phi, j2.mass_jesTotaldown)
        elif s == "jerUp":
            fj_p4.SetPtEtaPhiM(fj.pt_jerup, fj.eta, fj.phi, fj.mass_jerup)
            j0_p4.SetPtEtaPhiM(j0.pt_jerup, j0.eta, j0.phi, j0.mass_jerup)
            j2_p4.SetPtEtaPhiM(j2.pt_jerup, j2.eta, j2.phi, j2.mass_jerup)
        elif s == "jerdown":
            fj_p4.SetPtEtaPhiM(fj.pt_jerdown, fj.eta, fj.phi, fj.mass_jerdown)
            j0_p4.SetPtEtaPhiM(j0.pt_jerdown, j0.eta, j0.phi, j0.mass_jerdown)
            j2_p4.SetPtEtaPhiM(j2.pt_jerdown, j2.eta, j2.phi, j2.mass_jerdown)
        elif s == None:
            fj_p4.SetPtEtaPhiM(fj.pt, fj.eta, fj.phi, fj.mass)
            j0_p4.SetPtEtaPhiM(j0.pt, j0.eta, j0.phi, j0.mass)
            j2_p4.SetPtEtaPhiM(j2.pt, j2.eta, j2.phi, j2.mass)
        p4 = fj_p4 + j0_p4 + j2_p4
    elif dr2:
        fj_p4, j0_p4, j1_p4 = ROOT.TLorentzVector(), ROOT.TLorentzVector(), ROOT.TLorentzVector()
        if s == "nominal":
            fj_p4.SetPtEtaPhiM(fj.pt_nominal, fj.eta, fj.phi, fj.mass_nominal)
            j0_p4.SetPtEtaPhiM(j0.pt_nominal, j0.eta, j0.phi, j0.mass_nominal)
            j1_p4.SetPtEtaPhiM(j1.pt_nominal, j1.eta, j1.phi, j1.mass_nominal)
        elif s == "jesTotalup":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotalup, fj.eta, fj.phi, fj.mass_jesTotalup)
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotalup, j0.eta, j0.phi, j0.mass_jesTotalup)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotalup, j1.eta, j1.phi, j1.mass_jesTotalup)
        elif s == "jesTotaldown":
            fj_p4.SetPtEtaPhiM(fj.pt_jesTotaldown, fj.eta, fj.phi, fj.mass_jesTotaldown)
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotaldown, j0.eta, j0.phi, j0.mass_jesTotaldown)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotaldown, j1.eta, j1.phi, j1.mass_jesTotaldown)
        elif s == "jerUp":
            fj_p4.SetPtEtaPhiM(fj.pt_jerup, fj.eta, fj.phi, fj.mass_jerup)
            j0_p4.SetPtEtaPhiM(j0.pt_jerup, j0.eta, j0.phi, j0.mass_jerup)
            j1_p4.SetPtEtaPhiM(j1.pt_jerup, j1.eta, j1.phi, j1.mass_jerup)
        elif s == "jerdown":
            fj_p4.SetPtEtaPhiM(fj.pt_jerdown, fj.eta, fj.phi, fj.mass_jerdown)
            j0_p4.SetPtEtaPhiM(j0.pt_jerdown, j0.eta, j0.phi, j0.mass_jerdown)
            j1_p4.SetPtEtaPhiM(j1.pt_jerdown, j1.eta, j1.phi, j1.mass_jerdown)
        elif s == None:
            fj_p4.SetPtEtaPhiM(fj.pt, fj.eta, fj.phi, fj.mass)
            j0_p4.SetPtEtaPhiM(j0.pt, j0.eta, j0.phi, j0.mass)
            j1_p4.SetPtEtaPhiM(j1.pt, j1.eta, j1.phi, j1.mass)
        p4 = fj_p4 + j0_p4 + j1_p4
    else:
        j0_p4, j1_p4, j2_p4 = ROOT.TLorentzVector(), ROOT.TLorentzVector(), ROOT.TLorentzVector()
        if s == "nominal":
            j0_p4.SetPtEtaPhiM(j0.pt_nominal, j0.eta, j0.phi, j0.mass_nominal)
            j1_p4.SetPtEtaPhiM(j1.pt_nominal, j1.eta, j1.phi, j1.mass_nominal)
            j2_p4.SetPtEtaPhiM(j2.pt_nominal, j2.eta, j2.phi, j2.mass_nominal)
        if s == "jesTotalup":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotalup, j0.eta, j0.phi, j0.mass_jesTotalup)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotalup, j1.eta, j1.phi, j1.mass_jesTotalup)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotalup, j2.eta, j2.phi, j2.mass_jesTotalup)
        if s == "jesTotaldown":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotaldown, j0.eta, j0.phi, j0.mass_jesTotaldown)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotaldown, j1.eta, j1.phi, j1.mass_jesTotaldown)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotaldown, j2.eta, j2.phi, j2.mass_jesTotaldown)
        if s == "jerUp":
            j0_p4.SetPtEtaPhiM(j0.pt_jerup, j0.eta, j0.phi, j0.mass_jerup)
            j1_p4.SetPtEtaPhiM(j1.pt_jerup, j1.eta, j1.phi, j1.mass_jerup)
            j2_p4.SetPtEtaPhiM(j2.pt_jerup, j2.eta, j2.phi, j2.mass_jerup)
        if s == "jerdown":
            j0_p4.SetPtEtaPhiM(j0.pt_jerdown, j0.eta, j0.phi, j0.mass_jerdown)
            j1_p4.SetPtEtaPhiM(j1.pt_jerdown, j1.eta, j1.phi, j1.mass_jerdown)
            j2_p4.SetPtEtaPhiM(j2.pt_jerdown, j2.eta, j2.phi, j2.mass_jerdown)
        if s == None:
            j0_p4.SetPtEtaPhiM(j0.pt, j0.eta, j0.phi, j0.mass)
            j1_p4.SetPtEtaPhiM(j1.pt, j1.eta, j1.phi, j1.mass)
            j2_p4.SetPtEtaPhiM(j2.pt, j2.eta, j2.phi, j2.mass)
        p4 = j0_p4 + j1_p4 + j2_p4
    #print(p4, p4.M())
    return p4


def get_jet(jets):
    goodjet = list(filter(lambda x : x.jetId and x.pt>25 and abs(x.eta)<2.7 , jets))
    # idx_good = 0
    # for idx_jet in range(len(jets)):
    #     if jets[idx_jet] in goodjet:
    #         idx_good = goodjet.index(jets[idx_jet])
    #         goodjet[idx_good].jetIdx = idx_jet
    #         # idx_good += 1
    return goodjet
def get_fatjet(fatjets):
    goodfatjets = list(filter(lambda x : x.jetId and abs(x.eta) < 2.7 and (x.globalParT3_QCD + x.globalParT3_Xbb)>0, fatjets))
    # idx_good = 0
    # for idx_fj in range(len(fatjets)):
    #     if fatjets[idx_fj] in goodfatjets:
    #         idx_good = goodfatjets.index(fatjets[idx_fj])
    #         goodfatjets[idx_good].fatjetIdx = idx_fj
    #         # idx_good += 1
    return goodfatjets

def presel(jets, fatjets): #returns 2 collections of jets and fatjets
    goodjets = get_jet(jets)
    goodfatjets = get_fatjet(fatjets)
    
    return goodjets, goodfatjets


def deltaPhi(phi1, phi2):
    # Catch if being called with two objects
    if type(phi1) != float and type(phi1) != int:
        phi1 = phi1.phi
    if type(phi2) != float and type(phi2) != int:
        phi2 = phi2.phi
    # Otherwise
    dphi = (phi1 - phi2)
    while dphi > pi:
        dphi -= 2 * pi
    while dphi < -pi:
        dphi += 2 * pi
    return dphi

def deltaEta(eta1, eta2):
    # Catch if being called with two objects
    if type(eta1) != float and type(eta1) != int:
        eta1 = eta1.eta
    if type(eta2) != float and type(eta2) != int:
        eta2 = eta2.eta
    # Otherwise
    deta = (eta1-eta2)
    return deta
    

def deltaR(eta1, phi1, eta2=None, phi2=None):
    # catch if called with objects
    if eta2 == None:
        return deltaR(eta1.eta, eta1.phi, phi1.eta, phi1.phi)
    # otherwise
    return hypot(eta1 - eta2, deltaPhi(phi1, phi2))


def closest(obj, collection, presel=lambda x, y: True):
    ret = None
    drMin = 999
    for x in collection:
        if not presel(obj, x):
            continue
        dr = deltaR(obj, x)
        if dr < drMin:
            ret = x
            drMin = dr
    return (ret, drMin)

def closest_(obj, collection, presel=lambda x, y: True):
    ret = None
    drMin = 999
    for i, x in enumerate(collection):
        if not presel(obj, x):
            continue
        dr = deltaR(obj, x)
        if dr < drMin:
            ret = i
            drMin = dr
    return (ret, drMin)


def matchObjectCollection(objs,
                          collection,
                          dRmax=0.4,
                          presel=lambda x, y: True):
    pairs = {}
    if len(objs) == 0:
        return pairs
    if len(collection) == 0:
        return dict(list(zip(objs, [None] * len(objs))))
    for obj in objs:
        (bm, dR) = closest(obj,
                           [mobj for mobj in collection if presel(obj, mobj)])
        if dR < dRmax:
            pairs[obj] = bm
        else:
            pairs[obj] = None
    return pairs


def matchObjectCollectionMultiple(
        objs,
        collection,
        dRmax=0.4,
        presel=lambda x, y: True
):
    pairs = {}
    if len(objs) == 0:
        return pairs
    if len(collection) == 0:
        return dict(list(zip(objs, [None] * len(objs))))
    for obj in objs:
        matched = []
        for c in collection:
            if presel(obj, c) and deltaR(obj, c) < dRmax:
                matched.append(c)
        pairs[obj] = matched
    return pairs

def ensureTFile(filename,option='READ',verbose=False):
  """Open TFile, checking if the file in the given path exists."""
  if not os.path.isfile(filename):
    raise IOError("File in path '%s' does not exist!"%(filename))
  if verbose:
    print("Opening '%s'..."%(filename))
  file = ROOT.TFile.Open(filename,option)
  if not file or file.IsZombie():
    raise IOError("Could not open file by name '%s'"%(filename))
  return file

def extractTH1(file,histname,setdir=True):
  """Get histogram by name from a given file."""
  close = False
  if isinstance(file,str):
    file  = ensureTFile(file,'READ')
    close = True
  if not file or file.IsZombie():
    raise IOError("Could not open file for histogram '%s'!"%(histname))
  hist = file.Get(histname)
  if not hist:
    raise IOError("Did not find histogram '%s' in file '%s'!"%(histname,file.GetName()))
  if setdir and isinstance(hist,ROOT.TH1):
    hist.SetDirectory(0)
    if close:
      file.Close()
  return hist

