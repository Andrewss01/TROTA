import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
import optparse
import json
import os

usage = 'python3 post_training_studies.py '
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat'   , dest='dat'  , type=str, default = 'TT_dilep_2024', help='Please enter a dataset name')
parser.add_option('-j', '--json'  , dest='json' , type=str, default = '../samples/dict_samples.json', help='Please enter a json input file')
parser.add_option('-v', '--var'   , dest='vars' , type=str, default = "Jet_electronIdx1,Jet_muonIdx1,FatJet_electronIdx3SJ,FatJet_muonIdx3SJ",  help='Please enter variables to read')
parser.add_option('-m', '--max'   , dest='max'  , action = 'store_true')
parser.add_option('-n', '--nfiles', dest='nfiles', type=int, default=1)
parser.add_option('-w', '--wpoint', dest='wpoint', type=str, default="rejected")

(opt, args) = parser.parse_args()
sample = opt.dat
path_json = opt.json
variables = opt.vars.split(",")
num_files = opt.nfiles
max_value = opt.max
wp = opt.wpoint

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())

with open(path_json, 'r') as json_input:
    dict_samples = json.load(json_input)

if sample not in dict_samples.keys():
    print("please enter a valid sample name")
    exit()

var_names = {"Jet"   : {"electronIdx1"  :[0,1], "muonIdx1"  :[0,1], "pt":[0,800]}, 
             "FatJet": {"electronIdx3SJ":[0,1], "muonIdx3SJ":[0,1], "pt":[0,800]}}
            
for var in variables:
    branch = var.split("_")[0]
    var_name = var.split("_")[1]
    if branch not in var_names.keys():
        print("Select a valid branch")
        exit()
    elif var_name not in var_names[branch]:
        print(f"select a valid variable for the {branch} branch") 

wp_points = {"TopResolved":{"QCDScore": {"10%":0.4694105386734009 , "5%":0.7234321236610413 , "1%":0.9433798789978027 , "0.1%":0.9895168542861938} , 
                            "FTScore" : {"10%":0.7186799645423889 , "5%":0.8069701194763184 , "1%":0.9033783078193665 , "0.1%":0.9501141905784607}}, 
             "TopMixed"   : {"QCDScore": {"10%":0.09013006091117859 , "5%":0.33411234617233276 , "1%":0.9027690887451172 , "0.1%":0.9955894947052002} , 
                            "FTScore" : {"10%":0.589518129825592 , "5%":0.7755876183509827 , "1%": 0.9369741678237915, "0.1%":0.9851188659667969}} }


out_file = ROOT.TFile.Open(f"/eos/user/{inituser}/{username}/TROTA/studies_training/studies_post_training_{sample}.root", "UPDATE")


def filling_histo(top, branch_, branch,lep_branch, event, var, histo_all, histo_max = None):
    if branch == 'Jet':
        idx_jet0, idx_jet1, idx_jet2 = top.idxJet0, top.idxJet1, top.idxJet2                  
        jet0 = branch_[idx_jet0]
        jet0_var = getattr(jet0, var)                
        jet1 = branch_[idx_jet1]
        jet1_var = getattr(jet1, var)
        if idx_jet2 != -1:
            jet2 = branch_[idx_jet2]
            jet2_var = getattr(jet2, var)
        if "Idx" in var:               
            leptons = Collection(event,lep_branch )
            frac_values = []

            if jet0_var != -1:
                lep0_pt = leptons[jet0_var].pt
                jet0_pt = jet0.pt
                frac0 = lep0_pt/jet0_pt
                histo_all.Fill(frac0)
                frac_values.append(frac0)
            if jet1_var != -1:
                lep1_pt = leptons[jet1_var].pt
                jet1_pt = jet1.pt
                frac1   = lep1_pt/jet1_pt
                histo_all.Fill(frac1)
                frac_values.append(frac1)

            if idx_jet2 != -1:
                if jet2_var != -1: 
                    lep2_pt = leptons[jet2_var].pt
                    jet2_pt = jet2.pt
                    frac2 = lep2_pt/jet2_pt
                    histo_all.Fill(frac2)
                    frac_values.append(frac2)
            
            if frac_values != []:
                # print(frac_values)
                max_frac =max(frac_values)
                histo_max.Fill(max_frac)
            
            if idx_jet2 != -1:
                histo_all.Fill(jet2_var)
            

    elif branch == "FatJet":
        
        idx_fj = top.idxFatJet
        if idx_fj !=-1:
            fj = branch_[idx_fj]
            fj_var = getattr(fj, var)
            if "Idx" in var:
                
            
                leptons = Collection(event,lep_branch )


                if fj_var != -1:
                    lep0_pt = leptons[fj_var].pt
                    fj_pt = fj.pt
                    frac0 = lep0_pt/fj_pt
                    histo_all.Fill(frac0)

def selection(score, wp, top_type):
    if top_type == 'mixed':
        if wp != "rejected" :
            if score >= wp_points["TopMixed"]["QCDScore"][wp]:
                return True
            else:
                return False
        else:
            if score <= 0.5:
                return True
            else:
                return False
    elif top_type == 'resolved':
        if wp != "rejected" :
            if score >= wp_points["TopResolved"]["QCDScore"][wp]:
                return True
            else:
                return False
        else:
            if score <= 0.5:
                return True
            else:
                return False

    


for idx in range(num_files):
    string = dict_samples[sample][sample]["strings"][idx]
    # print(string)
    rfile = ROOT.TFile.Open(string, "READ")
    tree = InputTree(rfile.Get("Events"))
    
    for var_name in variables:
         
        branch = var_name.split("_")[0]
        var    = var_name.split("_")[1]
        
        
        print(f"Plotting variable: {var} , for branch: {branch}")
         
        start_point, end_point = var_names[branch][var][0], var_names[branch][var][1]
        if "Idx" in var:
            lep_branch =var[:var.index("Idx")].capitalize()
            if branch == 'Jet':
                histo_max_mixed = ROOT.TH1F(f"fraction_{lep_branch}_{branch}_pt_max_{wp}_mixed", f"fraction_{lep_branch}_{branch}_pt_max_{wp}_mixed",50,start_point,end_point)   
                histo_all_mixed = ROOT.TH1F(f"fraction_{lep_branch}_{branch}_pt_all_{wp}_mixed", f"fraction_{lep_branch}_{branch}_pt_all_{wp}_mixed",50,start_point,end_point) 
                histo_max_resolved = ROOT.TH1F(f"fraction_{lep_branch}_{branch}_pt_max_{wp}_resolved", f"fraction_{lep_branch}_{branch}_pt_max_{wp}_resolved",50,start_point,end_point)   
                histo_all_resolved = ROOT.TH1F(f"fraction_{lep_branch}_{branch}_pt_all_{wp}_resolved", f"fraction_{lep_branch}_{branch}_pt_all_{wp}_resolved",50,start_point,end_point) 
            elif branch == 'FatJet':
                # histo_max_mixed = ROOT.TH1F(f"fraction_{lep_branch}_pt_max_{wp}_mixed", f"fraction_{lep_branch}_pt_max_{wp}_mixed",50,start_point,end_point)   
                histo_all_mixed = ROOT.TH1F(f"fraction_{lep_branch}_{branch}_pt_all_{wp}_mixed", f"fraction_{lep_branch}_{branch}_pt_all_{wp}_mixed",50,start_point,end_point) 
                # histo_max_resolved = ROOT.TH1F(f"fraction_{lep_branch}_pt_max_{wp}_resolved", f"fraction_{lep_branch}_pt_max_{wp}_resolved",50,start_point,end_point)   
                histo_all_resolved = ROOT.TH1F(f"fraction_{lep_branch}_{branch}_pt_all_{wp}_resolved", f"fraction_{lep_branch}_{branch}_pt_all_{wp}_resolved",50,start_point,end_point) 
                            



        for i in range(tree.GetEntries()):
            event = Event(tree,i)
            topmixed = Collection(event,"TopMixed")
            topresolved = Collection(event, "TopResolved")
            
            branch_ = Collection(event, branch)

            for top in topmixed:
                score = top.TTScore/(top.QCDScore + top.TTScore)
                if selection(score, wp, "mixed") :
                    filling_histo(top, branch_, branch, lep_branch, event, var, histo_all_mixed, histo_max_mixed)
            if branch != "FatJet":
                for top in topresolved:
                
                    score = top.TTScore/(top.QCDScore + top.TTScore)
                
                    if selection(score, wp, "resolved") :
                
                        filling_histo(top, branch_, branch, lep_branch, event, var, histo_all_resolved, histo_max_resolved)
        try:
            out_file.WriteObject(histo_max_mixed, "")
            out_file.WriteObject(histo_all_mixed, "")
            out_file.WriteObject(histo_max_resolved, "")
            out_file.WriteObject(histo_all_resolved, "")
        except:
            out_file.WriteObject(histo, "")

                    




            
    
    


