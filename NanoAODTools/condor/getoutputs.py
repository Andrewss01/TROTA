# to run from lxplus9
import ROOT, os
import subprocess
from PhysicsTools.NanoAODTools.postprocessing.samples.samples_2024 import *
import optparse
import json
from tqdm import tqdm
import sys

usage = 'python3 getoutputs.py -d dataset_name'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('-o', '--output', dest='output', type=str, default = '../python/postprocessing/samples/dict_samples_2024.json', help='Please enter a json output file')
parser.add_option('--tier', dest='tier', type=str, default = 'bari', help='Please enter location where to write the output file (tier pisa or bari)')
(opt, args) = parser.parse_args()
where_to_read = opt.tier

if where_to_read.lower() =='pisa':
    redirector = "davs://stwebdav.pi.infn.it:8443/cms"
elif where_to_read.lower() =='bari':
    redirector = "davs://webdav.recas.ba.infn.it:8443/cms"
else:
    print("Please select a valid tier (pisa or bari) OTHERWISE add the correct redirector in the code")
    exit()

#Insert here your uid... you can see it typing echo $uid
username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())
workdir  = "user" if "user" in os.environ.get('PWD') else "work"

if(uid == 0):
    print("Please insert your uid")
    exit()
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

# insert here the name of output folder
running_folder                      = os.environ.get('PWD') + "/tmp/"
remote_folder_name                  = "TROTA_2024/PostProcessed_samples"

def get_files_on_tier(folder, cert_path, ca_path):
    try:
        command = "davix-ls -E "+cert_path+" --capath "+ca_path+" "+folder
        print(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        output, error = process.communicate()
        output = output.decode('utf-8')

        files = []
        for line in output.splitlines():
            # Ignora le righe non relative ai file (come intestazioni o directory)
            if line.endswith('.root') and line:
                file_name = line
                files.append(file_name)
        
        return files
    
    except subprocess.CalledProcessError as e:
        print(f"Errore nell'esecuzione di davix-ls: {e}")
        return {}

        
dataset = opt.dat 
if dataset == '':
    print("Please enter a dataset name")
    exit()
elif dataset not in sample_dict.keys():
    print(f"Dataset {dataset} not found")
    exit()
elif dataset in sample_dict.keys():
    if hasattr(sample_dict[dataset], "components"):
        print("---------- Running dataset: ", dataset)
        print("Components: ", [s.label for s in sample_dict[dataset].components])
        samples = sample_dict[dataset].components
    else:
        print("You are running a single sample")
        print("---------- Running sample: ", dataset)
        samples = [sample_dict[dataset]]

out_dict = {}
if hasattr(sample_dict[dataset], "process"):
    out_dict[sample_dict[dataset].process] = {}
else:
    out_dict[dataset] = {}
out_dict[dataset] = {}

outjson = opt.output

if os.path.exists(outjson):
    with open(outjson, 'r') as json_input:
        json_out = json.load(json_input)
        if hasattr(sample_dict[dataset], "process"):
            if json_out.get(sample_dict[dataset].process) is None:
                json_out[sample_dict[dataset].process] = {}
        elif json_out.get(dataset) is None and not hasattr(sample_dict[dataset], "process"):
            json_out[dataset] = {}
else:
    json_out = {}
    if hasattr(sample_dict[dataset], "process"):
        json_out[sample_dict[dataset].process] = {}
    else:
        json_out[dataset] = {}

for sample in samples:
    print("---------- Running dataset: ", dataset)
    out_dict[sample.process][sample.label] = {}

    if dataset!=sample.label: 
        out_dict[sample.label] = {}
        out_dict[sample.label][sample.label] = {}
    print("---------- Running sample: ", sample.label)
    folder = "davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA_2024/PostProcessed_samples/" + sample.label
    
    files_strings   = get_files_on_tier(folder, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")

   
    path_file = folder
    ntot = []
    out_strings = []
    for f in tqdm(files_strings): 
       
        f = str(path_file+"/"+f)
        
        if not "Data" in sample.label:
            try:
                rootfile = ROOT.TFile.Open(f)
                out_strings.append(f)
                dir_ = rootfile.Get("plots")
                h_genweight = dir_.Get("h_genweight")
                # runstree = rootfile.Get("Runs")
                n_toh_genweight.GetBinContent(0)
                # runstree.GetEntry(0)
                # geneventSumw = runstree.genEventSumw
                # tree = rootfile.Get("Events")
                # tree.GetEntry(0)
                # eventweight = abs(tree.Generator_weight)
                # n = round(abs(geneventSumw/eventweight))
                # ntot.append(n)
            except:
                print("Could not open file: ", f)
                # n = rootfile.Get('Events').GetEntries()
                n = None
                ntot.append(n)
                continue
            # histo = rootfile.Get("plots/h_genweight")
            # ntot.append(histo.GetBinContent(2))
        else:
            try:
                rootfile = ROOT.TFile.Open(f,'READ')
                if rootfile.IsZombie():
                    print("Could not open file (zombie): ", f)
                    ntot.append(None)
                    continue
                out_strings.append(f)
                ntot.append(None)
            except:
                print("Could not open file: ", f)
                ntot.append(None)
                continue
    out_dict[sample.process][sample.label] = {'strings': out_strings, "ntot": ntot}
    json_out[sample.process][sample.label] = out_dict[sample.process][sample.label]
    if json_out.get(sample.label) is None:
        json_out[sample.label] = {}
    json_out[sample.label][sample.label] = out_dict[sample.process][sample.label]
    print(f"Sample {sample.label} done!")
    print("-----------------------------------------------------")
    print(out_dict[sample.process][sample.label])
    # print(out_dict.keys())
    # print("-----")
    # print(json_out.keys())
    with open(outjson, 'w') as json_output:
        json.dump(json_out, json_output, indent = 2)
print(f"Output written to {outjson}")
