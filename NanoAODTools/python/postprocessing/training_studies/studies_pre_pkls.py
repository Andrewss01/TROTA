import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
import optparse
import json
import os
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import * 



var_names = { "TopMixed":{"pt":[0,1000]}, "TopResolved":{"pt":[0,1000]}}


PROC_LABEL = {
    "True_Top":   "True Top (TT)",
    "False_Top": "False Top (TT)",
    "QCD":      "QCD"
}


PROC_STYLE = {
    #             line color           fill alpha
    "True_Top":   (ROOT.kRed,           0.25),
    "False_Top": (ROOT.kBlue, 0.25),
    "QCD":      (ROOT.kGreen+2,       0.25),
}

def classify_sample(sample_name):
    """
    Ritorna:
      'TT'       → TT_hadr o TT_semilep  (va separato via truth in Signal/FalseTop)
      'TT_dilep' → TT dileptonic
      'QCD'      → QCD
      'ZJets'    → Z+Jets
      None       → campione sconosciuto, ignorato
    """
    if "TT_hadr" in sample_name or "TT_semilep" in sample_name or "Tprime" in sample_name:
        return "TT"
    elif "TT_dilep" in sample_name:
        return "TT"
    elif "QCD" in sample_name:
        return "QCD"
    elif "ZJ" in sample_name:
        return "QCD"
    else:
        return None





def write_root(proc_data, out_path, var_names, PROCESSES, nbins = 100):
    rfile = ROOT.TFile.Open(out_path, "RECREATE")
    all_vars = sorted(set(var for proc in PROCESSES for var in proc_data[proc].keys()))
    for var in all_vars :
        rfile.mkdir(var)
        rfile.cd(var)
        histos={}
        branch = var.split("_")[0]
        
        var_name = var.split("_")[1]

        for proc in PROCESSES:
            if var in proc_data[proc].keys():
                hname = f"{var}_{proc}"
                start_point, end_point = var_names[branch][var_name][0], var_names[branch][var_name][1]
                h = ROOT.TH1F(hname, hname, nbins, start_point, end_point)
                # print(proc_data[proc].keys())
                
                for value in proc_data[proc][var]:
                    h.Fill(value)
                # if h.Integral() > 0:
                #     h.Scale(1.0 / h.Integral())
                color, alpha = PROC_STYLE[proc]
                h.SetLineColor(color)
                h.SetLineWidth(2)
                h.SetFillColorAlpha(color, alpha)
                # if "QCD" in proc:
                    
                histos[proc] = h
        cname  = f"c_{branch}_{var_name}"
        canvas = ROOT.TCanvas(cname, cname, 900, 650)
        canvas.SetLeftMargin(0.12)

        procs_sorted = sorted(PROCESSES, key=lambda p: histos[p].GetMaximum(), reverse=True)
        for i, proc in enumerate(procs_sorted):
            histos[proc].Draw("HIST" if i == 0 else "HIST SAME")

        
        legend = ROOT.TLegend(0.75, 0.8, 0.9, 0.9)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        for proc in PROCESSES:
            # n = len([proc])
            legend.AddEntry(histos[proc], f"{PROC_LABEL[proc]}", "lf")
        legend.Draw()

        for proc in PROCESSES:
            histos[proc].Write()
        canvas.Write()

    rfile.cd()
    rfile.Close()
    print(f"\nFile ROOT scritto in: {out_path}")



def accumulate(samples,vars, PROCESSES, year, dict_samples):
    proc_data = {proc:{} for proc in PROCESSES}
    
    def num_files(s):
        if "TT_hadr" in s or "TT_semilep" in s:
            num_files = 2

        elif "Tprime" in s:
            num_files = 2
        elif "QCD" or "ZJets" in s:
            num_files = 1
        elif "TT_dilep" in s:
            num_files = 1
        if len(dict_samples[s][s]["strings"]) < num_files:
            num_files = len(dict_samples[s][s]["strings"])
        return num_files

    def fill_dict(proc, branch, var, list_data, truth):
        if (proc == 'TT') and truth==1:
            proc_data["True_Top"][branch+"_"+var] += list_data
        elif (proc == 'TT') and truth==0:
            proc_data["False_Top"][branch+"_"+var] += list_data
        else:
            proc_data[proc][branch+"_"+var] += list_data


    def ensure_keys(proc_type,var):
        if proc_type != "TT":
            if var not in proc_data[proc_type].keys():
                proc_data[proc_type][var] = []
        else:
            for proc in ["True_Top", "False_Top"]:
                if var not in proc_data[proc].keys():
                    proc_data[proc][var] = []

    
    for s in samples:
        proc_type = classify_sample(s) 
        print(f"\n")
        print(f"  Elaborazione campione: {s}  →  {proc_type}")
        num_file = num_files(s)
         
        for idx in range(num_file):
            file = dict_samples[s][s]["strings"][idx]
            rfile = ROOT.TFile.Open(file, "READ")
            tree = InputTree(rfile.Get("Events"))
            for var_name in vars:        
                branch = var_name.split("_")[0]
                var    = var_name.split("_")[1]     
                ensure_keys(proc_type, f"{branch}_{var}")


                
                num_events = tree.GetEntries()
                if "QCD" in s:
                    num_events = int(tree.GetEntries()/10)
               
                for i in range(num_events):
                    event = Event(tree,i)
                    
                    if "Top" in branch:
                        branch_ = Collection(event, branch)
                        for top in branch_:
                            if branch=="TopMixed" and top.pt<600:
                                fill_dict(proc_type, branch, var, [getattr(top,var)], top.truth)
                            elif branch=="TopResolved" and top.pt <600:
                                fill_dict(proc_type, branch, var, [getattr(top,var)], top.truth)
                                   
                        # for top in topresolved:
                            
                        #     score = top.TTScore/(top.QCDScore + top.TTScore)
                        #     if selection(score, wp, "resolved") :
                                
                        #         if "Idx" in var:
                        #             frac_values = fraction_energy(top, branch, lep_branch, event)
                        #             fill_dict(proc_type, branch, lep_branch+"FracEAll", frac_values, top.truth)
                        #             if frac_values == []:
                        #                 num_no_lep += 1
                        #             if branch == "Jet" and frac_values != []:
                        #                 max_value = [max(frac_values)]
                                        
                        #                 fill_dict(proc_type, branch, lep_branch+"FracEMax", max_values, top.truth)
    
    return proc_data
    



usage = 'python3 post_training_studies.py '
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat'   , dest='dat'  , type=str, default = 'TT_2022,QCD_2022,ZJetsToNuNu_2022,TprimeToTZ_700_2022,TprimeToTZ_800_2022,TprimeToTZ_900_2022,TprimeToTZ_1000_2022,TprimeToTZ_1100_2022,TprimeToTZ_1200_2022,TprimeToTZ_1300_2022,TprimeToTZ_1400_2022,TprimeToTZ_1500_2022,TprimeToTZ_1600_2022,TprimeToTZ_1700_2022,TprimeToTZ_1800_2022', help='Please enter a dataset name')
parser.add_option('-j', '--json'  , dest='json' , type=str, default = '../samples/dict_samples_2022.json', help='Please enter a json input file')
parser.add_option('-v', '--var'   , dest='vars' , type=str, default = "TopMixed_pt,TopResolved_pt",  help='Please enter variables to read')

(opt, args) = parser.parse_args()
datasets = opt.dat.split(",")
path_json = opt.json
variables = opt.vars.split(",")



year = str(datasets[0][-4:])
print("year is: ", year)

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())

with open(path_json, 'r') as json_input:
    dict_samples = json.load(json_input)

 
samples = []
for dataset in datasets:
    if hasattr(sample_dict[dataset],"components"):
        if dataset in dict_samples.keys():
            samples += [s for s in dict_samples[dataset].keys()]
    else:
        samples += [dataset]
print("samples utilizzati: ", samples )

PROCESSES = []
for sample in samples:
    proc_type = classify_sample(sample)
    if proc_type=="TT":
        if "True_Top" not in PROCESSES:
            PROCESSES.append("True_Top")
        if "False_Top" not in PROCESSES:
            PROCESSES.append("False_Top")
    elif proc_type not in PROCESSES:
        PROCESSES.append(proc_type)


print("variabili scelte: ",variables)
for var in variables:
    branch = var.split("_")[0]
    var_name = var.split("_")[1]
    if branch not in var_names.keys():
        print("Select a valid branch")
        exit()
    elif var_name not in var_names[branch]:
        print(f"select a valid variable for the {branch} branch") 



print("Raccogliendo insieme i processi...")
proc_data = accumulate(samples, variables, PROCESSES, year,dict_samples)
out_path = f"/eos/user/{inituser}/{username}/TROTA/TROTA{year}/studies_training/pt_tops_pre_pkls_{year}.root"
write_root(proc_data, out_path, var_names, PROCESSES, nbins = 100)

