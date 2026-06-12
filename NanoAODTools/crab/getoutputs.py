# to run from lxplus9
import ROOT, os
from checkjobs import *
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from checkjobs import find_folders, find_folder

import optparse
import json
from tqdm import tqdm
import sys
import uproot

usage = 'python3 getoutputs.py -d dataset_name'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('-o', '--output', dest='output', type=str, default = 'dict_samples_2024.json', help='Please enter a json output file')
parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Enable verbose output')
parser.add_option('--tier', dest='tier', type=str, default = 'bari', help='Please enter location where to write the output file (tier pisa or bari)')
(opt, args) = parser.parse_args()
where_to_read = opt.tier
verbose = opt.verbose

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
running_folder                      = os.environ.get('PWD') #+ "/tmp/"
remote_folder_name                  = "TROTA2024/Eval_Samples"
 
def get_files_on_tier(folder, cert_path, ca_path):
    try:
        command = "davix-ls -E "+cert_path+" --capath "+ca_path+" "+folder
        if verbose: 
            print(  f"Running command: {command}")
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        output, error = process.communicate()
        output = output.decode('utf-8')

        files = []
        for line in output.splitlines():
            # Ignora le righe non relative ai file (come intestazioni o directory)
            if line.endswith('.root') and line:
                file_name = line
                files.append(file_name)
        if verbose:
            print(files)
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

outjson = opt.output

if os.path.exists('../python/postprocessing/samples/'+outjson):
    with open('../python/postprocessing/samples/'+outjson, 'r') as json_input:
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
    print("-----------Running dataset: ", dataset)
    if json_out.get(sample.process) is None:
        json_out[sample.process] = {}
    print("---------- Running sample: ", sample.label)    
    ntot = []
    out_strings = []
    
    folders_list = find_folders(redirector, username, remote_folder_name, sample, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
    
    for folder in folders_list: 
        path_file = folder 
        
        files_strings = get_files_on_tier(folder, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
        
        for f_name in tqdm(files_strings):
        
            f_path = os.path.join(path_file, f_name)
            
            if verbose: 
                print("Processing file:", f_path)
            #
            rootfile = ROOT.TFile.Open(f_path)
            #
            if not rootfile or rootfile.IsZombie():
                continue  
            
            if "Data" not in sample.label: 
                runstree = rootfile.Get("Runs")
                runstree.SetBranchStatus("*", 0)
                runstree.GetEntry(0) # load the minimal data
                
                if sample.year == 2024:
                    runstree.SetBranchStatus("genEventCount", 1)
                    runstree.GetEntry(0)
                    n = round(runstree.genEventCount)
                else:
                    runstree.SetBranchStatus("genEventSumw", 1)
                    runstree.GetEntry(0)
                    geneventSumw = runstree.genEventSumw
                    
                    tree = rootfile.Get("Events")
                    tree.SetBranchStatus("*", 0) # optimize the reading of Events
                    tree.SetBranchStatus("Generator_weight", 1)
                    tree.GetEntry(0)
                    n = round(abs(geneventSumw / tree.Generator_weight))
                
                ntot.append(n)
                out_strings.append(f_path)
            else:
                out_strings.append(f_path)
                ntot.append(None)
                
            rootfile.Close()
    
    sample_data = {'strings': out_strings, "ntot": ntot}
    json_out[sample.process][sample.label] = sample_data
    if json_out.get(sample.label) is None:
        json_out[sample.label] = {}
    json_out[sample.label][sample.label] = sample_data
    print(f"Sample {sample.label} done!")
    print("-----------------------------------------------------")
    print(sample_data)
    with open('../python/postprocessing/samples/'+outjson, 'w') as json_output:
        json.dump(json_out, json_output, indent = 2)
print(f"Output written to ../python/postprocessing/samples/{outjson}")




