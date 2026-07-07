import ROOT
import pickle as pkl 
import json
import numpy as np
import optparse

'''
Prendere il pkl usato per il training dopo averlo ridotto con la percentuale giusta (controllare dai condor.out del training corrispondente)
in modo da poi poter studiare le variabili del dataset utilizzato. 
'''


usage = 'python3 variables_studies_pre_training'
parser                  = optparse.OptionParser(usage)
parser.add_option('-r', '--resolved'   , dest = 'resolved'   ,default = False, action = 'store_true')
arser.add_argument('-y', '--year'      , dest = 'year'        , default = "2024" )


(opt,args)          = parser.parse_args()
resolved = opt.resolved
year = opt.year
if resolved:
    path_pkl =  "/eos/user/a/apuglia/TROTA/pkls/training_dataset_1_pt_cut_600_reduced_resolved.pkl"
else:
    path_pkl = "/eos/user/a/apuglia/TROTA/pkls/training_dataset_1_pt_cut_600_reduced_mixed.pkl"

with open(path_pkl, 'rb') as file:
    data = pkl.load(file)


if resolved:
    categories = ["3j0fj"]
else:
    categories = ["3j1fj", "2j1fj", "3j0fj"]

pt_dict={}
print(data.keys())


process = ["TT","FT","TT_dilep", "QCD", "ZJ"]
for proc in process: 
    pt_dict[proc] = {}
    pt_dict[proc]["pt_top"] = []
    





for sample in data.keys():
    
    pt_values = []
    pt_values_true, pt_values_false = [],[]
    
    

    if "TT_hadr" in sample or "TT_semilep" in sample:
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

if resolved:
    out_json = f"pre_training_pts_resolved_{year}.json"
else:
    out_json = f"pre_training_pts_mixed_{year}.json"

print(pt_dict.keys())
with open(out_json, 'w') as json_output:
    json.dump(pt_dict, json_output, indent = 2)
    



    
