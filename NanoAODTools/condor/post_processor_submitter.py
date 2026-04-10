import os
import sys
import time
import ROOT
import optparse
from PhysicsTools.NanoAODTools.postprocessing.utils.get_file_fromdas import *
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from checkjobs import *
from training_models import models

usage = 'python3 postproc_submitter.py -d dataset_name'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('--tier', dest='tier', type=str, default = 'bari', help='Please enter location where to write the output file (tier pisa or bari)')
parser.add_option('--dryrun', dest='debug', action='store_true', default=False, help='True if you want to write trial file but not submitting it (rembeber to set also submit to True)')
parser.add_option('-s', '--submit', dest='submit', action='store_true', default=False, help='True if you want to submit jobs')
parser.add_option('-e', '--evaluate', action = 'store_true', default = False, help='True if you want to evaluate with the training models')
parser.add_option('--status', action='store_true', default=False, help='True if you want to check status of jobs')
parser.add_option('--folder', dest='folder', default='TROTA2024/Eval_samples', help = 'choose the folder name on you tier where the files will be saved')
(opt, args) = parser.parse_args()
debug = opt.debug 
submit = opt.submit
tier = opt.tier  
evaluate = opt.evaluate
status = opt.status
tier_folder = opt.folder



modelMix_path_24 = models["TopMixed_2024_TROTA2D_ptcut"]
modelRes_path_24 = models["TopResolved_2024_TROTA2D_ptcut"]

modelMix_path_22 = models["TopMixed_2022_TROTA2D_ptcut"]
modelRes_path_22 = models["TopResolved_2022_TROTA2D_ptcut"]




username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())

if tier == 'bari':
    redirector = "davs://webdav.recas.ba.infn.it:8443/cms"
else: 
    redirector = "davs://webdav.recas.ba.infn.it:8443/cms"

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

#non togliere il tmp
running_folder = os.environ.get('PWD')+"/tmp/post_processing/"
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
    f.write("+JobFlavour             = \"nextweek\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    # f.write("initialdir              = " + folder + "\n")
    f.write("executable              = " + folder + label +"/runner.sh\n")
    f.write("arguments               = $(Proxy_path)\n")
    f.write("output                  = "+folder+"condor/output/"+label+".out\n")
    f.write("error                   = "+folder+"condor/error/" +label+".err\n")
    f.write("log                     = "+folder+"condor/log/"   +label+".log\n")
    f.write("queue\n")

def write_post_processor_script(folder, file, modules ): 
    f = open(folder + 'post_processor.py', 'w')
    f.write('import ROOT\n')
    f.write('from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor\n')
    f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.nanoprepro_v2 import *\n')
    f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.GenPart_MomFirstCp import *\n')
    # f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.collectionMerger import *\n')
    f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.MCweight_writer import *\n')
    # f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.idx_PFC_SV import *\n')
    # f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.deltaR_PF_SV import *\n')
    f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.NanoTopCandidate import *\n')
    f.write('import sys\n')
    f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.jetId import *\n')
    f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.fatjetId import *\n')
    if evaluate:  
        f.write('from PhysicsTools.NanoAODTools.postprocessing.modules.nanoTopEvaluate_MultiScore import *\n')
    # f.write('from PhysicsTools.N') 
    f.write('json = "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-07-17/jetid.json.gz"\n')
    if not debug:
        f.write(f'p = PostProcessor(".", ["root://cms-xrd-global.cern.ch/{file}"], branchsel = None, modules = [{modules}], histFileName= "hist.root", histDirName= "plots", haddFileName="tree.root",  outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop.txt" % os.environ["CMSSW_BASE"])\n')
    else:
        f.write(f'p = PostProcessor(".", ["root://cms-xrd-global.cern.ch/{file}"], branchsel = None, modules = [{modules}], histFileName= "hist.root", histDirName= "plots", haddFileName="tree.root",  outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop.txt" % os.environ["CMSSW_BASE"], maxEntries = 100)\n')
    # f.write('p = PostProcessor(".", +"'+file+'", branchsel = None, modules = modules_,  haddFileName= "histOut.root", histDirName= "plots", haddFileName ="'+label+'"+".root", )
    f.write('p.run()')


def runner_writer(folder, i, remote_folder_name, sample_folder, launchtime, outfolder):
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
    f.write("hadd -f tree_hadd_"+str(i)+".root tree.root hist.root\n")
    f.write("pwd\n")
    f.write("davix-put tree_hadd_{}.root {}/store/user/{}/{}/{}/{}/tree_hadd_{}.root -E $1 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/\n".format(str(i), redirector, username, remote_folder_name, sample_folder,launchtime, str(i)))
    f.close()


if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")



launchtime = time.strftime("%Y%m%d_%H%M%S")

if submit: 
    print('######### Submitting mode #########')

    print("\nRemote folder name (tier): ", tier_folder)
    if not debug:    
        os.popen("davix-mkdir {}/store/user/{}/{}/ -E /tmp/x509up_u{} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(redirector, username, tier_folder, str(uid)))
    print("  {}/store/user/{}/{} CREATED".format(redirector, username, tier_folder))

    for sample in samples:
        print('Sample is: ', sample.label)
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

        if sample.year == 2024:
            if evaluate:
                modules_ = "MCweight_writer(), GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),nanoprepro(), jetId(json, jetType='AK4PUPPI'), fatjetId(json, jetType='AK8PUPPI'),nanoTopcand_PFC_SV(year= "+str(sample.year)+"),nanoTopevaluate_MultiClass(year = " + str(sample.year)+ ", modelMix_path='"+modelMix_path_24+"', modelRes_path='"+modelRes_path_24+"')"
            else:
                modules_ = "MCweight_writer(), GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),nanoprepro(), jetId(json, jetType='AK4PUPPI'), fatjetId(json, jetType='AK8PUPPI'),nanoTopcand_PFC_SV(year= "+str(sample.year)+")"
        elif sample.year == 2022:
            if evaluate:
                modules_ = "MCweight_writer(), GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),nanoprepro(), nanoTopcand_PFC_SV(year = "+str(sample.year)+ "),nanoTopevaluate_MultiClass(year = " + str(sample.year)+ ", modelMix_path='"+modelMix_path_22+"', modelRes_path='"+modelRes_path_22+"')"
            else:
                modules_ = "MCweight_writer(), GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),nanoprepro(), nanoTopcand_PFC_SV(year = " +str(sample.year)+ ")"


        if not debug: 
            os.popen("davix-mkdir {}/store/user/{}/{}/{}/ -E /tmp/x509up_u{} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(redirector, username, tier_folder, data_label, str(uid)))
            print(" FOLDER:         {}/store/user/{}/{}/{}/ CREATED".format(redirector, username, tier_folder, data_label))
            os.popen("davix-mkdir {}/store/user/{}/{}/{}/{}/ -E /tmp/x509up_u{} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(redirector, username, tier_folder, data_label, launchtime, str(uid)))
            print(" FOLDER:         {}/store/user/{}/{}/{}/{}/ CREATED".format(redirector, username, tier_folder, data_label, launchtime))

        if hasattr(sample, 'dataset'):
            files_list = get_files_string(sample, option =  'global')
            
            if debug: files_list = files_list[:1]
            print('numer total files: ', len(files_list))
            for idx, file in enumerate(files_list):
                print("...submitting file ", idx, end = '\r')
                label = 'file_'+str(idx)
                


                folder_file = condor_folder+ label + "/" 
                outfolder_i = outfolder + label + "/"
                if not os.path.exists(folder_file):
                    os.makedirs(folder_file)


                write_post_processor_script(folder_file, file , modules_)
                runner_writer(folder_file, idx, tier_folder, data_label,  launchtime, outfolder_i,)
                sub_writer(condor_folder, label, folder_file)
                # print('folder is: ', folder_file, ' path_dataset: ', tier_folder, ' label: ', label)   
                # print('outfolder is: ', outfolder_i, ' condor folder is: ', condor_folder)
                if submit and not debug:
                
                    os.chdir(folder_file)
                    os.popen('condor_submit condor.sub')
                    # time.sleep(5)
                
   
if status:
    print('###### Status mode ######')
    print("Do NOT resubmit jobs before they're finished")
    
    for sample in samples:
        davixfolder = find_folder(redirector, username, tier_folder, sample.label, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
        file_sizes = get_file_sizes(davixfolder, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
        print("Checking status for empty files in ", sample.label)
        print("Tier folder: ", davixfolder)
        job_failed = 0
        job_success = 0
        job_running= 0
        print(running_folder+"/"+sample.label)
        listoffile = os.listdir(running_folder+"/"+sample.label)
        jobs_total = 0 
        for f in listoffile: 
            if f.startswith("file"):
                n = int(f.split("file_")[-1])
                if n>jobs_total: jobs_total = n
        jobs_total += 1
        for file_name, file_size in file_sizes.items():
            file_num = file_name.split('.')[0].split('_')[-1]
            if file_size <1000:
                # print(f"File: {file_name}, Size: {file_size} bytes")
                job_failed += 1
            else:
                job_success += 1


        print("--------------------------------------------------------------------------------\n")
        print("dataset: ", sample.label)
        print("Total jobs: ", jobs_total)
        print("\033[91mJobs failed: {} ({:.2f}%)\033[0m".format(job_failed, (job_failed/jobs_total)*100))
        print("\033[92mJobs succeeded: {} ({:.2f}%)\033[0m\n".format(job_success, (job_success/jobs_total)*100))
        print("running jobs: {} ({:.2f}%)\n".format(jobs_total-(job_failed+job_success), ((jobs_total-(job_failed+job_success))/jobs_total)*100))
        check_errors_fromcondor(sample.label, username, uid, tier_folder, redirector, resubmit=False, delete_files_fromtier=False)
        print("\n--------------------------------------------------------------------------------")


