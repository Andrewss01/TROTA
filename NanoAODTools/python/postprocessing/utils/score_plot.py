import ROOT 
from PhysicsTools.NanoAODTools.postprocessing.samples.samples_2024 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
import optparse
import json
import os

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())



usage = 'python3 score_plot.py -d inFile'
parser = optparse.OptionParser(usage)
parser.add_option('-d'   , '--dataset'   , dest='dataset'  , type=str   , default=None ,   help ='dataset to run '         )
parser.add_option( '--nfiles'    , dest='nfiles'   , type=int   , default=1    ,   help= 'n file to run'           )
parser.add_option('-f'  , '--file'   , dest='file'  , type=str   , default="/eos/user/a/apuglia/TROTA/Study_pt_distribution/histos/pt_topmixed.root"   )
parser.add_option('--tier', dest='tier', type=str, default = 'bari', help='Please enter location where to write the output file (tier pisa or bari)')
parser.add_option('-s', dest = 'selection', action='store_true', default=False, help='select true if the sample used is a signal sample')
parser.add_option('-j', dest='json_file', type=str, default='../samples/dict_samples_2024.json')
(opt, args) = parser.parse_args()

dataset = opt.dataset
nfiles  = opt.nfiles
tier    = opt.tier
save_file = opt.file
do_selection = opt.selection
json_file = opt.json_file
print('selection is: ', do_selection)
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

if dataset not in sample_dict.keys():
    print("error dataset")
    exit()
else: 
    if hasattr(sample_dict[dataset], "components"):
        print("---------- Running dataset: ", dataset)
        print("Components: ", [s.label for s in sample_dict[dataset].components])
        samples = sample_dict[dataset].components

    else:
        print("You are running a single sample")
        print("---------- Running sample: ", dataset)
        samples = [sample_dict[dataset]]


main_sample = sample_dict[dataset]


with open(json_file) as json_file_:
    dict_sample = json.load(json_file_)
    json_file_.close()




list_histo_bkg, list_histo_sig = [], []

wp10_topmixed_ft_score, wp10_topmixed_qcd_score =  0.6126335859298706, 0.20259279012680054

for sample_ in samples:
    print("Running sample:", sample_.label)
    histo_sig = ROOT.TH1F('pT_'+sample_.label+'_true_tops', 'pT_'+sample_.label+'_true_tops',200,0,1000)
    histo_bkg = ROOT.TH1F('pT_'+sample_.label+'_false_tops', 'pT_'+sample_.label+'_false_tops',200,0,1000)

    list_files = dict_sample[sample_.label][sample_.label]["strings"]
    if nfiles == -1:
        nfiles = len(list_files)
    for idx_file in range(nfiles):
        file = list_files[idx_file]
        print('file is: ', file)
        rfile = ROOT.TFile.Open(file, 'READ')
        tree = InputTree(rfile.Get('Events'))
        if "QCD" in sample_.label or "ZJets" in sample_.label:
            for i in range(10000):
                event = Event(tree, i)
                topmixed = Collection(event, "TopMixed")

                for top in topmixed:
                    if top.pt <= 600:
                    
                        if top.truth == 1: 
                            histo_sig.Fill(top.pt)
                        else:
                            histo_bkg.Fill(top.pt)
        else:
            for i in range(tree.GetEntries()):
                event = Event(tree, i)
                topmixed = Collection(event, "TopMixed")

                for top in topmixed:


                    if top.truth == 1: 
                        histo_sig.Fill(top.pt)
                    else:
                        histo_bkg.Fill(top.pt)
        rfile.Close()

    if "ZJets" in main_sample.label or "QCD" in main_sample.label:
        histo_bkg.SetLineColor(ROOT.kBlue)
    else:
        # histo_sig.Draw()
        histo_sig.SetLineColor(ROOT.kGreen)
        histo_bkg.SetLineColor(ROOT.kRed)
    
    if histo_sig.GetEntries() !=0:
        list_histo_sig.append(histo_sig)
    list_histo_bkg.append(histo_bkg)

# histo_bkg.Draw()


# c1.Draw()
file = ROOT.TFile.Open(save_file, 'UPDATE')
# file.Write("", TObject::kOverwrite)

for histo_sig in list_histo_sig:
    histo_sig.Write("", ROOT.TObject.kOverwrite)
for histo_bkg in list_histo_bkg:
    histo_bkg.Write("", ROOT.TObject.kOverwrite)



        
        



    

