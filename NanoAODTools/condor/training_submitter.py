import os
import sys
import time
import optparse
username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])

if username == 'apuglia':
    uid = 180940

usage = 'python3 trainings_submitter.py'
parser = optparse.OptionParser(usage)
parser.add_option('-g', '--grid_search', dest='grid_search', action = 'store_true', default = False, help='Enter True if you want to do the grid search')
parser.add_option('-b', '--best_hps', dest='best_hps', type=str, default =None, help='enter the file name of the hps to use if you have any')
parser.add_option('--trota2d', dest='trota2d', action='store_true', default=False, help='Enter True if you wanto training with trota2d')
parser.add_option('-r', '--resolved', dest='resolved', action ='store_true', default =False)
(opt, args) = parser.parse_args()
grid_search = opt.grid_search
trota_2d = opt.trota2d
best_hps = opt.best_hps
resolved = opt.resolved

launchtime = time.strftime("%d_%m_%Y")
if best_hps == None:
    best_hps = launchtime

if grid_search : 
    name = 'grid_search'
else:
    name = 'training'

if trota_2d: 
    algorithm  ='trota_2D'
else:
    algorithm = 'trota'

if resolved:
    top_type = 'resolved'
else:
    top_type = 'mixed'


def sub_writer(folder = './'):
    f = open(folder + "condor.sub","w")
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
    f.write("executable              = " + folder+ "runner.sh\n")
    f.write("arguments               = \n")
    f.write("output                  = "+ folder+"condor.out\n")
    f.write("error                   = "+ folder+"condor.err\n")
    f.write("log                     = "+ folder+"condor.log\n")
    f.write("queue\n")

def runner_writer(folder = "./", name = None, label = None, file = None, path_to_model = None, components = None, project_name = None):
    f = open(folder + "runner.sh", "w")
    f.write("#! /usr/bin/bash\n")
    f.write('cd /afs/cern.ch/user/a/apuglia/CMSSW_14_1_7/src/PhysicsTools/NanoAODTools/python/postprocessing/TROTA_2024/ML\n')
    f.write('cmsenv\n')
    f.write(f"python3 "+name+"_"+algorithm+"_"+top_type+".py -s "+components+" -i "+file+" -o True -g "+path_to_model+" -m "+path_to_model+"/model_"+label+".h5 -j "+path_to_model+"/scores_"+label+".json -v True -l "+project_name)



label =launchtime
folder = '/afs/cern.ch/user/a/apuglia/CMSSW_14_1_7/src/PhysicsTools/NanoAODTools/condor/tmp/trainings/'+name+'_'+algorithm+'_'+top_type+'_'+label+'/'
in_file = '/eos/user/a/apuglia/TROTA/pkls/training_dataset_1_pt_cut_600.pkl' #file su cui girare la grid search  
components = 'QCD_HT1000to1200_0,QCD_HT100to200_0,QCD_HT1200to1500_0,QCD_HT1500to2000_0,QCD_HT2000_0,QCD_HT200to400_0,QCD_HT400to600_0,QCD_HT40to70_0,QCD_HT600to800_0,QCD_HT70to100_0,QCD_HT800to1000_0,TT_dilep_0,TT_hadr_0,TT_semilep_0,ZJetsToNuNu_HT100to200_0,ZJetsToNuNu_HT1500to2500_0,ZJetsToNuNu_HT200to400_0,ZJetsToNuNu_HT2500_0,ZJetsToNuNu_HT400to800_0,ZJetsToNuNu_HT800to1500_0'
# 'QCD_HT1000to1200_0,QCD_HT100to200_0,QCD_HT1200to1500_0,QCD_HT1500to2000_0,QCD_HT2000_0,QCD_HT200to400_0,QCD_HT400to600_0,QCD_HT40to70_0,QCD_HT600to800_0,QCD_HT70to100_0,QCD_HT800to1000_0,TT_dilep_0,TT_hadr_0,TT_hadr_1,TT_semilep_0,ZJetsToNuNu_HT100to200_0,ZJetsToNuNu_HT1500to2500_0,ZJetsToNuNu_HT200to400_0,ZJetsToNuNu_HT2500_0,ZJetsToNuNu_HT400to800_0,ZJetsToNuNu_HT800to1500_0'


 

#'QCD_HT1000to1200_0,QCD_HT100to200_0,QCD_HT1200to1500_0,QCD_HT1500to2000_0,QCD_HT2000_0,QCD_HT200to400_0,QCD_HT400to600_0,QCD_HT600to800_0,QCD_HT70to100_0,QCD_HT800to1000_0,TT_dilep_0,TT_hadr_0,TT_semilep_0,TprimeToTZ_1000_0,TprimeToTZ_1100_0,TprimeToTZ_1200_0,TprimeToTZ_1300_0,TprimeToTZ_1400_0,TprimeToTZ_1500_0,TprimeToTZ_1600_0,TprimeToTZ_1700_0,TprimeToTZ_700_0,TprimeToTZ_800_0,TprimeToTZ_900_0,ZJetsToNuNu_2jets_PT100to200_1J_0,ZJetsToNuNu_2jets_PT100to200_2J_0,ZJetsToNuNu_2jets_PT200to400_1J_0,ZJetsToNuNu_2jets_PT200to400_2J_0,ZJetsToNuNu_2jets_PT400to600_1J_0,ZJetsToNuNu_2jets_PT400to600_2J_0,ZJetsToNuNu_2jets_PT40to100_1J_0,ZJetsToNuNu_2jets_PT40to100_2J_0,ZJetsToNuNu_2jets_PT600_1J_0,ZJetsToNuNu_2jets_PT600_2J_0'
 
path_to_model = "/afs/cern.ch/user/a/apuglia/CMSSW_14_1_7/src/PhysicsTools/NanoAODTools/python/postprocessing/TROTA_2024/trainings/"+name+"_"+algorithm+"_"+top_type+"_"+label+"/"

best_hps_to_use = best_hps


if not os.path.exists(folder):
    os.makedirs(folder)
if not os.path.exists(path_to_model):
    os.makedirs(path_to_model)

if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

runner_writer(folder = folder, name =name, label = label, file = in_file, path_to_model= path_to_model, components = components, project_name= best_hps_to_use)
sub_writer(folder= folder)
os.chdir(folder)
os.popen('condor_submit condor.sub')
time.sleep(5)
print('done')