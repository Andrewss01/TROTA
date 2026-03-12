import os
import sys
import time
from tqdm import tqdm
import optparse
# from PhysicsTools.NanoAODTools.postprocessing.modules.common.checkjobs import find_folder
import subprocess
from PhysicsTools.NanoAODTools.postprocessing.samples.samples_with_PF import *


def find_folder(redirector, username, remote_dir, dataset_label, cert_path, ca_path):
    results = subprocess.run([
        'davix-ls', '-E', cert_path, '--capath', ca_path, redirector+"/store/user/"+username+"/"+remote_dir+"/"+dataset_label+"/"
    ], capture_output=True, text=True, check=True)
    subfold = results.stdout.splitlines()
    subfold.sort()
    subfold = subfold[-1]
    #-1 per i Tprime 0 per gli altri perchè sono quelli senza sistematiche

    return remote_dir+"/"+dataset_label+"/"+subfold

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])


usage = 'python3 creating_pkls_submitter.py -d inFile'
parser = optparse.OptionParser(usage)
parser.add_option('-d'   , '--dataset'   , dest='dataset'  , type=str   , default=None ,   help ='dataset to run '         )
# parser.add_option( '--nfiles'    , dest='nfiles'   , type=int   , default=1    ,   help= 'n file to run'           )
parser.add_option('-n'  , '--nevents'   , dest='nevents'  , type=int   , default=-1   ,   help='number of events to run, -1 means all events'  )
parser.add_option('--tier', dest='tier', type=str, default = 'bari', help='Please enter location where to write the output file (tier pisa or bari)')
parser.add_option( '--path_pkl' , dest='path_pkl' , type=str   , default="/eos/user/a/apuglia/Tprime/pkls" ,   help='path to save pkl file'    )
parser.add_option( '--num_pfcs'  , dest='numpfcs'  , type=int   , default=20   ,   help='number of particles used for training, default 20')
parser.add_option( '--pt_cut'    , dest='pt_cut'   , type=float , default= 0   ,   help='pt cut for particles used for training')
parser.add_option('-v'   , '--verbose'   , dest='verbose'  , action='store_true'       , default=False  ,  help='if True do verbose')
parser.add_option('-t', '--tier_folder', dest='tier_folder', type=str, default='Run3Analysis_Tprime', help='folder on the tier with the samples')

(opt, args) = parser.parse_args()

dataset   = opt.dataset

n_events  = opt.nevents
n_PFCs    = opt.numpfcs
pt_cut    = opt.pt_cut
verbose   = opt.verbose
tier      = opt.tier
path_pkl  = opt.path_pkl
tier_folder = opt.tier_folder
username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())

if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")



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

if tier =='pisa':
    redirector = "davs://stwebdav.pi.infn.it:8443/cms"
elif tier =='bari':
    redirector = "davs://webdav.recas.ba.infn.it:8443/cms"
else:
    print("Please select a valid tier (pisa or bari) OTHERWISE add the correct redirector in the code")
    exit()




def sub_writer(folder = './', label = None):
    f = open(folder + label+"/condor.sub","w")
    f.write('Proxy_filename          = x509up\n')
    f.write('Proxy_path              = /afs/cern.ch/user/' + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write('universe                = vanilla\n')
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write('use_x509userproxy       = true\n')
    f.write('should_transfer_files   = YES\n')
    f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    f.write('request_memory          = 30000\n')
    f.write("+JobFlavour             = \"nextweek\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    # f.write("initialdir              = " + folder + "\n")
    f.write("executable              = " + folder+label+"/runner.sh\n")
    f.write("arguments               = \n")
    f.write("output                  = "+ folder+"condor/output/"+label+".out\n")
    f.write("error                   = "+ folder+"condor/error/"+label+".err\n")
    f.write("log                     = "+ folder+"condor/log/"   +label+".log\n")
    f.write("queue\n")
    
def runner_writer(folder, label, path_file, component, path_to_pkl, year, n_events=-1, pt_cut = 0, num_pfc = 20, verbose =False ):
    f = open(folder+label+"/runner.sh", "w")
    f.write("#! /usr/bin/bash\n")
    f.write('cd /afs/cern.ch/user/a/apuglia/CMSSW_14_1_7/src/PhysicsTools/NanoAODTools/python/postprocessing/TROTA_2024/ML\n')
    f.write('cmsenv\n')
    f.write(f"python3 trainingSet_PF_to_pkl.py -c "+component+" -i "+path_file+" --path_pkls "+path_to_pkl+".pkl  -n "+str(n_events)+" --pt_cut "+str(pt_cut)+" -y "+str(year)+" --num_pfcs "+str(num_pfc)+" -v "+str(verbose)+" \n")


for sample in samples: 
    sample_label = sample.label
    sample_year  = sample.year 


  
    condor_folder = os.environ.get('PWD') +"/tmp/creating_pkls/" + sample_label +"/"
    if tier_folder == "Run3Analysis_Tprime":
        folder_tier = find_folder(redirector, username, "Run3Analysis_Tprime", sample_label, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
        print('tier folder is: ', folder_tier)
    if not os.path.exists(condor_folder):
        os.makedirs(condor_folder)
    if not os.path.exists(condor_folder + "condor/output"):
        os.makedirs(condor_folder+"condor/output")
    if not os.path.exists(condor_folder + "condor/error"):
        os.makedirs(condor_folder+"condor/error")
    if not os.path.exists(condor_folder + "condor/log"):
        os.makedirs(condor_folder+"condor/log")

    # path_pkl =  +"/" + sample_label + "/"
    path_pkl_dir = path_pkl+ "/" +sample_label+"/"
    if not os.path.exists(path_pkl_dir):
        os.makedirs(path_pkl_dir)
    n_files = 1
    for idx in range(0,n_files): 
        if tier_folder == "Run3Analysis_Tprime":
            path_file = redirector + "/store/user/" + username +"/"+folder_tier+"/tree_hadd_"+str(idx)+".root"
        else:
            path_file = redirector + "/store/user/" + username +"/"+tier_folder+"/"+sample.label+"/tree_hadd_"+str(idx)+".root"
        print('processing file: ', path_file)
        
        component = sample_label[:-4] + str(idx)
        print('component is: ', component)

        if not os.path.exists(condor_folder + "/file_"+str(idx)): 
            os.makedirs(condor_folder+"/file_"+str(idx))
        path_pkl_file = path_pkl_dir+ component
        sub_writer(folder=condor_folder, label = 'file_'+str(idx))
        runner_writer(folder=condor_folder,label = 'file_'+str(idx), path_file=path_file, component=component, path_to_pkl = path_pkl_file, year =sample_year, num_pfc = n_PFCs, n_events = n_events, verbose = verbose, pt_cut = pt_cut)
        
        print('path to pkl is: ', path_pkl_file)
        os.chdir(condor_folder + "file_" +str(idx))

        os.popen('condor_submit condor.sub')
        time.sleep(5)
print('done')





