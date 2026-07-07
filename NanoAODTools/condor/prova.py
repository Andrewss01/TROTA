# import ROOT
# file="davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA2024/Eval_samples/QCD_HT100to200_2024/20260417_125643/tree_hadd_126.root"
# ntot = []
# out_strings=[]
# rootfile = ROOT.TFile.Open(file)
# out_strings.append(file)
# dir_ = rootfile.Get("plots")
# h_genweight = dir_.Get("h_genweight")
# n = h_genweight.GetBinContent(1)
# ntot.append(n)
# print(ntot)

import pickle as pkl
path_pkl  ="/eos/user/a/apuglia/TROTA/TROTA2024/pkls/training_dataset_1_pt_cut_600_reduced.pkl"
with open(path_pkl, 'rb') as file:
    data = pkl.load(file)
print(data.keys())


#'QCD_HT1000to1200_0,QCD_HT100to200_0,QCD_HT1200to1500_0,QCD_HT1500to2000_0,QCD_HT2000_0,QCD_HT200to400_0,QCD_HT400to600_0,QCD_HT600to800_0,QCD_HT70to100_0,QCD_HT800to1000_0,TT_dilep_0,TT_dilep_1,TT_hadr_0,TT_hadr_1,TT_semilep_0,TT_semilep_1,TprimeToTZ_1000_0,TprimeToTZ_1100_0,TprimeToTZ_1100_1,TprimeToTZ_1200_0,TprimeToTZ_1200_1,TprimeToTZ_1300_0,TprimeToTZ_1400_0,TprimeToTZ_1500_0,TprimeToTZ_1600_0,TprimeToTZ_1600_1,TprimeToTZ_1700_0,TprimeToTZ_1800_0,TprimeToTZ_1800_1,TprimeToTZ_700_0,TprimeToTZ_700_1,TprimeToTZ_800_0,TprimeToTZ_800_1,TprimeToTZ_900_0,TprimeToTZ_900_1,ZJetsToNuNu_HT100to200_0,ZJetsToNuNu_HT1500to2500_0,ZJetsToNuNu_HT200to400_0,ZJetsToNuNu_HT2500_0,ZJetsToNuNu_HT400to800_0,ZJetsToNuNu_HT800to1500_0'])
