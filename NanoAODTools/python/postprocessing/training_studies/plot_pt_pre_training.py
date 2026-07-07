import numpy as np
import argparse
import json
import ROOT
import os

'''
Prendere il pkl usato per il training dopo averlo ridotto con la percentuale giusta (controllare dai condor.out del training corrispondente)
in modo da poi poter studiare le variabili del dataset utilizzato. 
'''

usage = 'python3 variables_studies_pre_training'
parser                  = optparse.OptionParser(usage)
parser.add_option('-r', '--resolved'   , dest = 'resolved'   ,default = False, action = 'store_true')
parser.add_option('-y', '--year'       , dest = 'year'       , default = "2024" )
# parser.add_option('-v', '--var'        , dest = 'variable'   , default = 'pt')
# parser.add_option('-c', '--component'  , dest = 'component'  , default = 'top') 
(opt,args)          = parser.parse_args()
resolved = opt.resolved
if resolved:
    type_top = 'resolved'
else:
    type_top = 'mixed'
year     = opt.year
# var      = opt.variable
components = ["jet","fatjet","tops","truth"]

paths_pkl = {"2024":{"resolved":"/eos/user/a/apuglia/TROTA/pkls/training_dataset_1_pt_cut_600_reduced_resolved.pkl" , 
                     "mixed":"/eos/user/a/apuglia/TROTA/pkls/training_dataset_1_pt_cut_600_reduced_mixed.pkl"}, 
             "2022":{"resolved":"" , "mixed":"/eos/user/a/apuglia/TPrime/pkls/training_dataset_1_pt_cut_600_reduced_mixed.pkl"}}
# variables = {"2024": {"jet":["area", "btagDeepB", "deltaEta", "mass", "deltaPhi", "pt", "deltaPhiFatJet", "deltaEtaFatJet"], 
#                       "fatjet":["area", "globalParT3_Xbb", "particleNetWithMass_TvsQCD", "particleNetWithMass_WvsQCD","particleNet_QCD","particleNetWithMass_QCD","particleNet_XbbVsQCD", "particleNet_XqqVsQCD","eta","mass","phi","pt", ]}

path_pkl = paths_pkl[year][type_top]

with open(path_pkl, 'rb') as file:
    data = pkl.load(file)

if resolved:
    categories = ["3j0fj"]
else:
    categories = ["3j1fj", "2j1fj", "3j0fj"]

var_dict={}
print("component used for the trainig: ", data.keys())


process = ["TT","FT","TT_dilep", "QCD", "ZJ"]
for proc in process: 
    var_dict[proc] = {}
    for c in components:
        var_dict[proc][c] = []
    

for sample in data.keys():
    
    pt_values = []
    pt_values_true, pt_values_false = [],[]
    
    

    if "TT_hadr" in sample or "TT_semilep" in sample:
        for cat in categories:
            pts   = np.array(data[sample][cat][2][:,2].flatten())
            truth = np.array(data[sample][cat][3].flatten()) 

            pt_values_true  += list(pts[truth==1])
            pt_values_false += list(pts[truth==0])

        # if cat == "3j0fj":
        #     pt_res_values_true  += list(pts[truth == 1])
        #     pt_res_values_false += list(pts[truth == 0])
            
    else:
        for cat in categories:
            pt_values += list(data[sample][cat][2][:,2])
            # if cat == "3j0fj":
            #     pt_res_values  += list(data[sample][cat][2][:,2][:2])

    if "TT_hadr" in sample or "TT_semilep" in sample:
        pt_dict["TT"]["pt_top"]    += pt_values_true
        # pt_dict["TT"]["TopResolved"] += pt_res_values_true

        pt_dict["FT"]["pt_top"]    += pt_values_false
        # pt_dict["FT"]["TopResolved"] += pt_res_values_false

    elif "TT_dilep" in sample:
        pt_dict["TT_dilep"]["pt_top"]    += pt_values
        # pt_dict["TT_dilep"]["TopResolved"] += pt_res_values

    elif "QCD" in sample:
        pt_dict["QCD"]["pt_top"]    += pt_values
        # pt_dict["QCD"]["TopResolved"] += pt_res_values

    elif "ZJ" in sample:
        pt_dict["ZJ"]["pt_top"]    += pt_values
        # pt_dict["ZJ"]["TopResolved"] += pt_res_values

# if resolved:
#     out_json = f"pre_training_pts_resolved_{year}.json"
# else:
#     out_json = f"pre_training_pts_mixed_{year}.json"


with open(out_json, 'w') as json_output:
    json.dump(pt_dict, json_output, indent = 2)
    


path_root = "/eos/user/a/apuglia/TROTA/TROTA2022/studies_training/"

if not os.path.exists(path_root):
    os.makedirs(path_root)

rfile = ROOT.TFile.Open(path_root+"pre_training_pts_mixed.root", "RECREATE")


# if os.path.exists(path_json):
#     with open(path_json, 'r') as json_input:
#         pt_dict = json.load(json_input)

histo_TT = ROOT.TH1F("","",200,0,800)
histo_FT = ROOT.TH1F("","",200,0,800)
histo_QCD = ROOT.TH1F("","",200,0,800)
histo_ZJ = ROOT.TH1F("","",200,0,800)
histo_dilep = ROOT.TH1F("","",200,0,800)
    


for key in pt_dict.keys():
    histo = ROOT.TH1F(f"pt_pre_training_{key}",f"pt_pre_training_{key}",200,0,800)
    for pt in pt_dict[key]["pt_top"]:
        histo.Fill(pt)
    histo.Write()

histo_tt = rfile.Get("pt_pre_training_TT")
for key in ["FT","ZJ","TT_dilep", "QCD"]:
    canvas = ROOT.TCanvas(f"pt_pre_training_TT_vs_{key}",f"pt_pre_training_TT_vs_{key}",1200,1600)
    histo_tt.SetLineColor(ROOT.kGreen)
    histo = rfile.Get(f"pt_pre_training_{key}")
    histo.SetLineColor(ROOT.kRed)
    if key != 'FT':
        histo_tt.Draw()
        histo.Draw("SAME")
    else:
        histo.Draw()
        histo_tt.Draw('SAME')
    canvas.Write()
    

rfile.Close()
    
    
    


