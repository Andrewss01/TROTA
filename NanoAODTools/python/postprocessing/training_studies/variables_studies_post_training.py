import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
import optparse
import json
import os
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import * 



var_names = {"Jet"   : {"electronIdx1"  :[0,1], "muonIdx1"  :[0,1], "pt":[0,800], "ElectronFracEAll":[0,1], "ElectronFracEMax":[0,1], "MuonFracEAll":[0,1], "MuonFracEMax":[0,1]}, 
             "FatJet": {"electronIdx3SJ":[0,1], "muonIdx3SJ":[0,1], "pt":[0,800], "ElectronFracEAll":[0,1], "MuonFracEAll":[0,1]}, 
             "TopMixed":{"pt":[0,1000]}, "TopResolved":{"pt":[0,1000]}}

# PROCESSES = ["True_Top","False_Top" "QCD", "ZJets", "TT_dilep"]

PROC_LABEL = {
    "True_Top":   "True Top (TT)",
    "False_Top": "False Top (TT)",
    "QCD":      "QCD",
    "ZJets":    "Z+Jets",
    "TT_dilep": "TT dileptonic"
}


PROC_STYLE = {
    #             line color           fill alpha
    "True_Top":   (ROOT.kRed,           0.25),
    "False_Top": (ROOT.kBlue, 0.25),
    "QCD":      (ROOT.kGreen+2,       0.25),
    "ZJets":    (ROOT.kOrange+1,      0.25),
    "TT_dilep": (ROOT.kCyan+1,      0.25)
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
        return "TT_dilep"
    elif "QCD" in sample_name:
        return "QCD"
    elif "ZJ" in sample_name:
        return "ZJets"
    else:
        return None


def compute_range(all_finite, vname):
    """
    Calcola (lo, hi) con margine del 35% sul range percentile 0.5–99.5.
    Per le variabili pt impone hi >= PT_MIN_HI.
    """
    lo_raw = float(np.percentile(all_finite, 0.5))
    hi_raw = float(np.percentile(all_finite, 99.5))

    if lo_raw == hi_raw:
        lo_raw -= 1.0
        hi_raw += 1.0

    span = hi_raw - lo_raw
    margin = RANGE_MARGIN * span

    lo = lo_raw - margin
    hi = hi_raw + margin

    return lo, hi




wp_points = {"TopResolved": {"2024" : {"QCDScore": {"10%":0.4694105386734009 , "5%":0.7234321236610413 , "1%":0.9433798789978027 , "0.1%":0.9895168542861938} , 
                            "FTScore" : {"10%":0.7186799645423889 , "5%":0.8069701194763184 , "1%":0.9033783078193665 , "0.1%":0.9501141905784607}},
                             "2022" : {"QCDScore": {"10%":0.6369661688804626 , "5%": 0.8127301931381226, "1%": 0.973943293094635, "0.1%":0.9972833395004272 }, 
                                       "FTScore" : {"10%": 0.7259360551834106, "5%":0.8225459456443787 , "1%": 0.9523900151252747, "0.1%":0.990899384021759 }}}, 
             "TopMixed"   : {"2024" : {"QCDScore": {"10%":0.09013006091117859 , "5%":0.33411234617233276 , "1%":0.9027690887451172 , "0.1%":0.9955894947052002} , 
                            "FTScore" : {"10%":0.589518129825592 , "5%":0.7755876183509827 , "1%": 0.9369741678237915, "0.1%":0.9851188659667969}}, 
                            "2022" : {"QCDScore":{"10%": 0.2122011035680771, "5%": 0.5026928186416626, "1%": 0.9420878291130066, "0.1%": 0.998317539691925}, 
                            "FTScore": {"10%": 0.48361846804618835, "5%": 0.7686988115310669, "1%": 0.9577326774597168, "0.1%": 0.9945845007896423}} }}



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






def selection(score, wp, top_type, year):
    if wp == "rejected" :
        if score <= 0.5:
            return True
        else:
            return False
    elif wp != "all": 
        if score>=wp_points[top_type][year]["QCDScore"][wp]:
            return True
        else: 
            return False
    elif wp == "all":
        return True

    


def accumulate(samples, vars, num_files, wp, PROCESSES,syst, year):
    proc_data = {proc:{} for proc in PROCESSES}
    # print(proc_data)

    def fill_dict(proc, branch, var, list_data, truth):
        if (proc == 'TT') and truth==1:
            proc_data["True_Top"][branch+"_"+var] += list_data
        elif (proc == 'TT') and truth==0:
            proc_data["False_Top"][branch+"_"+var] += list_data
        else:
            proc_data[proc][branch+"_"+var] += list_data




    def fraction_energy(top, branch, lep_branch, event):
        frac_values = []
        branch_ = Collection(event, branch)
        if branch == 'Jet':
        
            idx_jet0, idx_jet1, idx_jet2 = top.idxJet0, top.idxJet1, top.idxJet2                  
            jet0 = branch_[idx_jet0]
            jet0_var = getattr(jet0, var)                
            jet1 = branch_[idx_jet1]
            jet1_var = getattr(jet1, var)
            if idx_jet2 != -1 :
                jet2 = branch_[idx_jet2]
                jet2_var = getattr(jet2, var)             
       
            leptons = Collection(event,lep_branch )


            if jet0_var != -1 and jet0.jetId > 2:
                lep0_pt = leptons[jet0_var].pt
                jet0_pt = jet0.pt
                frac0 = lep0_pt/jet0_pt
                # histo_all.Fill(frac0)
                frac_values.append(frac0)
            if jet1_var != -1 and jet1.jetId > 2:
                lep1_pt = leptons[jet1_var].pt
                jet1_pt = jet1.pt
                frac1   = lep1_pt/jet1_pt
                # histo.Fill(frac1)
                frac_values.append(frac1)

            if idx_jet2 != -1 :
                if jet2_var != -1 and jet2.jetId > 2 : 
                    lep2_pt = leptons[jet2_var].pt
                    jet2_pt = jet2.pt
                    frac2 = lep2_pt/jet2_pt
                    # histo.Fill(frac2)
                    frac_values.append(frac2)


            #     histo_max.Fill(max_frac)
        elif branch == "FatJet":
        
            idx_fj = top.idxFatJet
            if idx_fj !=-1:
                fj = branch_[idx_fj]
                fj_var = getattr(fj, var)
                # if "Idx" in var:
                leptons = Collection(event,lep_branch )


                if fj_var != -1 and fj.jetId > 2:
                    lep0_pt = leptons[fj_var].pt
                    fj_pt = fj.pt
                    frac0 = lep0_pt/fj_pt
                    # histo_all.Fill(frac0)
                    frac_values.append(frac0)
        
        return frac_values

        

        

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
        num_no_lep, n_tot  =0,0 
        print(f"\n")
        print(f"  Elaborazione campione: {s}  →  {proc_type}")
        for idx in range(num_files):
            file = dict_samples[s][s]["strings"][idx]
            rfile = ROOT.TFile.Open(file, "READ")
            tree = InputTree(rfile.Get("Events"))
            for var_name in vars:        
                branch = var_name.split("_")[0]
                var    = var_name.split("_")[1] 
                if syst : 
                    var += '_nominal'
                # print(var, branch)
                if "Idx" in var:
                    lep_branch =var[:var.index("Idx")].capitalize()
                    if branch == "Jet":
                        ensure_keys(proc_type,f"{branch}_{lep_branch}FracEMax")
                    ensure_keys(proc_type,f"{branch}_{lep_branch}FracEAll")

                else:
                    ensure_keys(proc_type, f"{branch}_{var}")
                if tree.GetEntries() <10000:
                    num_events = tree.GetEntries()
                else:
                    num_events = 10000
                for i in range(num_events):
                    event = Event(tree,i)
                    
                    if "Top" in branch:
                        branch_ = Collection(event, branch)
                        for top in branch_:
                            if wp != "all":
                                if syst:
                                    score = top.TTScore_nominal/(top.QCDScore_nominal + top.TTScore_nominal)
                                else:
                                    score = top.TTScore/(top.QCDScore + top.TTScore)
                                if selection(score,wp,branch, year):
                                    fill_dict(proc_type, branch, var, [getattr(top,var)], top.truth)
                            else:
                                fill_dict(proc_type, branch, var, [getattr(top,var)], top.truth)
                    if "Top" not in branch:
                        topmixed = Collection(event,"TopMixed")
                        branch_ = Collection(event, branch)
                        
                        for top in topmixed:
                            if wp != "all":
                                if syst:
                                    score = top.TTScore_nominal/(top.QCDScore_nominal + top.TTScore_nominal)
                                else:
                                    score = top.TTScore/(top.QCDScore + top.TTScore)
                                if selection(score, wp, "TopMixed", year) :
                                    if "Idx" in var:
                                        frac_values = fraction_energy(top, branch, lep_branch, event)
                                        n_tot +=1
                                        if frac_values == []:
                                            num_no_lep += 1
                                        fill_dict(proc_type, branch, lep_branch+"FracEAll", frac_values, top.truth)

                                        if branch == "Jet" and frac_values != []:
                                            max_values = [max(frac_values)]                                        
                                            fill_dict(proc_type, branch, lep_branch+"FracEMax", max_values, top.truth)
                            else:
                                if "Idx" in var:
                                    frac_values = fraction_energy(top, branch, lep_branch, event)
                                    n_tot +=1
                                    if frac_values == []:
                                        num_no_lep += 1
                                    fill_dict(proc_type, branch, lep_branch+"FracEAll", frac_values, top.truth)

                                    if branch == "Jet" and frac_values != []:
                                        max_values = [max(frac_values)]                                        
                                        fill_dict(proc_type, branch, lep_branch+"FracEMax", max_values, top.truth)

                                   
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
        if n_tot != 0:
            print(f"Percentuale di casi in cui nessuno nei jet ha un leptone all'interno: {num_no_lep/n_tot*100}")
        print(f"{'─'*60}")
    
    return proc_data
    



usage = 'python3 post_training_studies.py '
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat'   , dest='dat'  , type=str, default = 'TT_2024,QCD_2024,ZJetsToNuNu_2024', help='Please enter a dataset name')
parser.add_option('-j', '--json'  , dest='json' , type=str, default = '../samples/dict_samples_2024.json', help='Please enter a json input file')
parser.add_option('-v', '--var'   , dest='vars' , type=str, default = "TopMixed_pt",  help='Please enter variables to read')
parser.add_option('-n', '--nfiles', dest='nfiles', type=int, default=1)
parser.add_option('-w', '--wpoint', dest='wpoint', type=str, default="rejected")
parser.add_option('-s', '--syst', dest='syst', action = "store_true", default = False)

(opt, args) = parser.parse_args()
datasets = opt.dat.split(",")
path_json = opt.json
variables = opt.vars.split(",")
num_files = opt.nfiles
syst = opt.syst
wp = opt.wpoint
year = str(datasets[0][-4:])
print("year is: ", year)

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())

with open(path_json, 'r') as json_input:
    dict_samples = json.load(json_input)

# if sample not in dict_samples.keys():
#     print("please enter a valid sample name")
#     exit()  
samples = []
for dataset in datasets:
    if hasattr(sample_dict[dataset],"components"):
        # print("processing sample: ", dataset)
        if dataset in dict_samples.keys():
            samples += [s for s in dict_samples[dataset].keys()]
    else:
        # print("processing a single sample: ", dataset)
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
if wp != "rejected":
    out_path = f"/eos/user/{inituser}/{username}/TROTA/TROTA{year}/studies_training/pt_tops_selected_post_training.root"
else:
    out_path = f"/eos/user/{inituser}/{username}/TROTA/TROTA{year}/studies_training/pt_tops_rejected_post_training.root"

print("Raccogliendo insieme i processi...")
proc_data = accumulate(samples, variables, num_files,wp, PROCESSES, syst, year)
# print(proc_data)
write_root(proc_data, out_path, var_names, PROCESSES, nbins = 100)

