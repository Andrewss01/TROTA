import os
import sys
import time
from tqdm import tqdm
import optparse


from PhysicsTools.NanoAODTools.postprocessing.samples.samples_2024 import *

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])


usage = 'python3 post_processor_evaluate_submitter.py -d inFile'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('--tier', dest='tier', type=str, default = 'bari', help='Please enter location where to write the output file (tier pisa or bari)')
parser.add_option('--dryrun', dest='debug', action='store_true', default=False, help='dryrun')
parser.add_option('-s', '--submit', dest='submit', action='store_true', default=False, help='submit jobs')
parser.add_option('-n', '--nfiles', dest='nfiles', type=int, default=1, help='choose how many files to use')

(opt, args) = parser.parse_args()
debug = opt.debug 
submit = opt.submit
tier = opt.tier  
nfiles = opt.nfiles

tier_folder = 'TROTA_2024/PostProcessed_samples'
tier_folder_out = "TROTA_2024/Evaluated_samples"

# if not os.path.exists(redirectotier_folder_out):
#     os.makedirs(tier_folder_out)



username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())

if tier == 'bari':
    redirector = "davs://webdav.recas.ba.infn.it:8443/cms"
else: 
    redirector = "davs://webdav.recas.ba.infn.it:8443/cms"

if submit:
    os.popen("davix-mkdir {}/store/user/{}/{}/ -E /tmp/x509up_u{} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(redirector, username, tier_folder_out, str(uid)))
    print("          {}/store/user/{}/{} CREATED".format(redirector, username, tier_folder_out))



dataset_to_run = opt.dat


if dataset_to_run == '':
    print("Please enter a dataset name")
    exit()
elif dataset_to_run not in sample_dict.keys():
    print("Dataset not found")
    exit()
elif dataset_to_run in sample_dict.keys():
    if hasattr(sample_dict[dataset_to_run], "components"):
        print("---------- Running dataset: ", dataset_to_run)
        print("Components: ", [s.label for s in sample_dict[dataset_to_run].components])
        samples = sample_dict[dataset_to_run].components
    else:
        print("You are running a single sample")
        print("---------- Running sample: ", dataset_to_run)
        samples = [sample_dict[dataset_to_run]]
        print('dataset is: ' , sample_dict[dataset_to_run].dataset)

running_folder = os.environ.get('PWD')+"/tmp/evaluate/"
if not os.path.exists(running_folder):
    os.makedirs(running_folder)


def sub_writer(folder, label, file_folder):
    f = open(file_folder + "condor.sub","w")
    f.write('Proxy_filename          = x509up\n')
    f.write('Proxy_path              = /afs/cern.ch/user/' + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write('universe                = vanilla\n')
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write('use_x509userproxy       = true\n')
    # f.write('should_transfer_files   = YES\n')
    # f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    f.write("+JobFlavour             = \"tomorrow\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    # f.write("initialdir              = " + folder + "\n")
    f.write("executable              = " + folder + label +"/runner.sh\n")
    f.write("arguments               = $(Proxy_path)\n")
    f.write("output                  = "+ folder + "condor/output/" + label+".out\n")
    f.write("error                   = "+ folder + "condor/error/"  + label+".err\n")
    f.write("log                     = "+ folder + "condor/log/"    + label+".log\n")
    f.write("queue\n")

def write_post_processor_script(folder, file, modules,idx ): 
    f = open(folder + 'post_processor.py', 'w')
    f.write('import ROOT\n')
    f.write('from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor\n')
    f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.common.TROTA_2024.nanoTopEvaluate_MultiScore import *\n')
    # f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *\n')
    # f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *\n')
    # f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import *\n')
    # f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *\n')
    # f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.common.TROTA_2024.idx_PFC_SV import *\n')
    # f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.common.TROTA_2024.deltaR_PF_SV import *\n')
    # f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.common.TROTA_2024.NanoTopCandidate_PF_SV import *\n')
    # f.write('import sys\n')
    # f.write('from PhysicsTools.NATModules.modules.jetId import *\n')
    # f.write('from PhysicsTools.NATModules.modules.fatjetId import *\n') 
    # f.write('json = "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-07-17/jetid.json.gz"\n')
    f.write(f'p = PostProcessor(".", ["{file}"], branchsel = None, modules = [{modules}],  outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_2024.txt" % os.environ["CMSSW_BASE"], maxEntries=1000)\n')
    # f.write('p = PostProcessor(".", +"'+file+'", branchsel = None, modules = modules_,  haddFileName= "histOut.root", histDirName= "plots", haddFileName ="'+label+'"+".root", )
    f.write('p.run()')


def runner_writer(folder, i, remote_folder_name, sample_folder, outfolder):
    f = open(folder+"/runner.sh", "w")
    f.write("#!/bin/bash\n")
    f.write("cd " +folder+"\n")
    f.write("pwd\n")
    f.write('cmsenv\n')
    f.write('export XRD_NETWORKSTACK=IPv4\n')
    f.write('mkdir -p '+outfolder+'\n')
    f.write('cd '+outfolder+'\n')
    f.write("python3 "+folder+"/post_processor.py\n")
    f.write("pwd\n")
    # f.write("hadd -f tree_hadd_"+str(i)+".root tree.root hist.root\n")
    # f.write("pwd\n")
    f.write("mv tree_hadd_"+str(i)+"_Skim.root tree_hadd_"+str(i)+".root\n")
    f.write("davix-put tree_hadd_{}.root {}/store/user/{}/{}/{}/tree_hadd_{}.root -E $1 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/\n".format(str(i), redirector, username, remote_folder_name, sample_folder, str(i)))
    f.close()


if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")


for sample in samples:
    print('sample is: ', sample.label)
    data_label  = sample.label
        
    condor_folder =running_folder + data_label+"/"


    if not os.path.exists(condor_folder): 
        os.makedirs(condor_folder)
    if not os.path.exists(condor_folder+"condor/output"): 
        os.makedirs(condor_folder+"condor/output")
    if not os.path.exists(condor_folder+"condor/error"): 
        os.makedirs(condor_folder+"condor/error")
    if not os.path.exists(condor_folder+"condor/log"): 
        os.makedirs(condor_folder+"condor/log")


    outfolder = "/tmp/"+username+"/"+data_label+"/"


    # modules_ = "MCweight_writer(), GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),Idx_PFC_SV(), deltaR_PF_SV(), collectionMerger(input=['PFCand'], output= 'PFCand', sortkey=lambda x: x.pt, reverse=True, selector=None, maxObjects=None),collectionMerger(input = ['SV'], output = 'SV', sortkey=lambda x: x.ntracks, reverse = True, selector = None, maxObjects = None),nanoprepro(), jetId(json, jetType='AK4PUPPI'), fatjetId(json, jetType='AK8PUPPI'),nanoTopcand_PFC_SV()"
    modules_ = "nanoTopevaluate_MultiClass()"
    print(redirector + "/store/user/"+username+"/"+tier_folder+"/"+data_label)
    
    
    start_point, final_point = 0,nfiles
    # print(files_list)
    for idx in range(start_point, final_point):
        label = 'file_'+str(idx)
        print('label is: ', label)
        file = redirector+"/store/user/"+username+"/"+ tier_folder +"/"+data_label+"/"+"tree_hadd_"+str(idx)+".root"
        print('file is: ', file)
            
            
        folder_file = condor_folder+ label + "/" 
        outfolder_i = outfolder + label + "/"
        if not os.path.exists(folder_file):
            os.makedirs(folder_file)
        

        write_post_processor_script(folder_file, file, modules_, idx)
        runner_writer(folder_file, idx, tier_folder_out, data_label, outfolder_i)
        sub_writer(condor_folder, label, folder_file)
        print('folder is: ', folder_file, ' path_dataset: ', tier_folder, ' label: ', label)   
        print('outfolder is: ', outfolder_i, ' condor folder is: ', condor_folder, ' out folder is: ', tier_folder_out)
        if submit and not debug:
            os.chdir(folder_file)
            os.popen('condor_submit condor.sub')
            time.sleep(5)
            


print('done')









        
