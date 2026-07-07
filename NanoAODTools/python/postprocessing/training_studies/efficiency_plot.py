import ROOT 
import os
import optparse
import array

usage                   = 'python3 efficiency_cal.py'
parser                  = optparse.OptionParser(usage)
parser.add_option('-f', '--folder'     , dest='folder'     , type=str, default='TROTA/TROTA2022/studies_training', help='folder with the histos'             )
# parser.add_option('-r', '--region'     , dest='region'     , type=str, default='SRTopMix'                     , help='region to calculate the efficiency' )
# parser.add_option('-v', '--variable'   , dest='variable'   , type=str, default='PuppMET_pt'                , help='variable to use'                    )
# parser.add_option('-d', '--denominator', dest='denominator', type=str, default='SR'                         , help='region to do the efficiency'        )
parser.add_option('-n','--names', dest='names', type=str, default='pt_tops_selected_post_training,pt_tops_rejected_post_training')

(opt, args)             = parser.parse_args()

histos_folder = opt.folder
name_histos   = opt.names.split(",")

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])

colors = {
    #             line color           fill alpha
    "True_Top":   ROOT.kRed,
    "False_Top": ROOT.kBlue,
    "QCD":      ROOT.kGreen,
    "ZJets":    ROOT.kOrange,
    "TT_dilep": ROOT.kCyan
}


def classify_sample(sample_name):

    if "True_Top" in sample_name:
        return "True_Top"
    elif "False_Top" in sample_name:
        return "False_Top"
    elif "TT_dilep" in sample_name:
        return "TT_dilep"
    elif "QCD" in sample_name:
        return "QCD"
    elif "ZJ" in sample_name:
        return "ZJets"
    else:
        return None

num_events = {}
pt_values = []
for i in range(1,101):
    pt_values.append(10*(i-1) + 5)
for name_file in name_histos:
    
    path = f"/eos/user/{inituser}/{username}/{histos_folder}/{name_file}.root"
    rfile = ROOT.TFile.Open(path, "READ")
    if "selected" in name_file:
        name_file = "selected"
    elif "rejected" in name_file:
        name_file = "rejected"
    num_events[name_file] = {}
    for dir_name in rfile.GetListOfKeys():
        dir_name = dir_name.GetName()
        dir = rfile.Get(dir_name)
        for key in dir.GetListOfKeys():
            histo_name = key.GetName()
            sample_type = classify_sample(histo_name)
            if sample_type:
                if sample_type not in num_events[name_file].keys():
                    num_events[name_file][sample_type] = []
                histo = dir.Get(histo_name)
                for idx_bin in range(1,101):
                    num_events[name_file][classify_sample(histo_name)].append(histo.GetBinContent(idx_bin))
    processes = num_events[name_file].keys()


effs = {}
rfile = ROOT.TFile.Open(f"/eos/user/{inituser}/{username}/{histos_folder}/efficiency_vs_pt.root", "RECREATE")
graphs = {}


for proc in processes:

    n_passes = num_events["selected"][proc]
    n_failes = num_events["rejected"][proc]
    effs[proc]=[]

    if len(n_passes) == len(n_failes):
        for epass,efail in zip(n_passes,n_failes):
            # print(epass, efail)
            if epass != efail and epass != 0:
                eff = epass/(epass + efail)
                effs[proc].append(eff)
            else:
                print(proc)
                effs[proc].append(0)
    g = ROOT.TGraph(len(pt_values), array.array('f',pt_values), array.array('f',effs[proc]))
    g.SetMarkerStyle(20)
    g.SetMarkerColor(colors[proc])
    graphs[proc] = g
    
    g.Write(f"{proc}_eff_vs_pt")

c1 = ROOT.TCanvas(f"c_eff_values", f"c_eff_values", 1500,1200)
procs_sorted = sorted(processes, key=lambda p: graphs[p].GetMaximum(), reverse=True)
for i, proc in enumerate(procs_sorted):
    
    graphs[proc].Draw("P" if i == 0 else "PSAME")


legend = ROOT.TLegend(0.75, 0.8, 0.9, 0.9)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
for proc in processes:
    legend.AddEntry(graphs[proc], f"{proc}", "p")
legend.Draw()
c1.Write()


# print(num_events["selected"]["True_Top"])
# print(num_events["rejected"]["True_Top"])
                
             
