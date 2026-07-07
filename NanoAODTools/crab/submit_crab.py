from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from training_models import models
import os
import optparse
import sys

usage = 'python3 submit_crab.py'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('--status', dest = 'status', default = False, action = 'store_true', help = 'Default do not check the status')
parser.add_option('-s', '--sub', dest = 'sub', default = False, action = 'store_true', help = 'Default do not submit')
parser.add_option('-k', '--kill', dest = 'kill', default = False, action = 'store_true', help = 'Default do not kill')
parser.add_option('-r', '--resub', dest = 'resub', default = False, action = 'store_true', help = 'Default do not resubmit')
parser.add_option('-g', '--gout', dest = 'gout', default = False, action = 'store_true', help = 'Default do not do getoutput')
parser.add_option('--sample', dest = 'sample', default = '', help = 'Default do not specify sample')
parser.add_option('--dryrun', dest = 'dryrun', default = False, action = 'store_true')
(opt, args) = parser.parse_args()

def cfg_writer(label, dataset, isData, year, outdir):
    f = open("crab_cfg.py", "w")
    f.write("from WMCore.Configuration import Configuration\n")
    f.write("\nconfig = Configuration()\n")
    f.write("config.section_('General')\n")
    f.write(f"config.General.requestName = '{label}'\n")
    f.write("config.General.transferLogs=True\n")
    f.write("config.section_('JobType')\n")
    f.write("config.JobType.pluginName = 'Analysis'\n")
    f.write("config.JobType.psetName = 'PSet.py'\n")
    f.write("config.JobType.scriptExe = 'crab_script.sh'\n")
    f.write(f"config.JobType.inputFiles = ['crab_script.py',  '../scripts/keep_and_drop.txt',  '../models/model_TopMixed_{year}_TROTA2D_ptcut.h5', '../models/model_TopResolved_{year}_TROTA2D_ptcut.h5']\n") #hadd nano will not be needed once nano tools are in cmssw 
    f.write(f"config.JobType.outputFiles = ['tree.root']\n")
    f.write("config.section_('Data')\n")
    f.write(f"config.Data.inputDataset = '{dataset}'\n")
    #f.write("config.Data.allowNonValidInputDataset = True\n")
    f.write("config.Data.inputDBS = 'global'\n") #'phys03'
    if isData:
        f.write("config.Data.splitting = 'LumiBased'\n")
        if year == '2024':
            f.write("config.Data.lumiMask = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions24/Cert_Collisions2024_378981_386951_Golden.json'\n")
        f.write("config.Data.unitsPerJob = 500\n")
    else:
        f.write("config.Data.splitting = 'FileBased'\n")
        f.write("config.Data.unitsPerJob = 1\n")
    #config.Data.runRange = ''
    #f.write("config.Data.splitting = 'EventAwareLumiBased'")
    #f.write("config.Data.totalUnits = 10\n")
    f.write(f"config.Data.outLFNDirBase = '/store/user/{os.environ.get('USER')}/{outdir}/{label}'\n")
    f.write("config.Data.publication = False\n")
    f.write(f"config.Data.outputDatasetTag = '{label}'\n")
    f.write("config.section_('Site')\n")
    f.write("config.Site.storageSite = 'T2_IT_Bari'\n")
    #f.write("config.Site.storageSite = "T2_CH_CERN"
    #f.write("config.section_("User")
    #f.write("config.User.voGroup = 'dcms'
    f.close()

def crab_script_writer(isData, year, modules):
    f = open("crab_script.py", "w")
    f.write("#!/usr/bin/env python3\n")
    f.write("import os\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.utils.crabhelper import inputFiles,runsAndLumis\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.MET_HLT_Filter import *\n")
    # f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.jetVetoMap import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.jetId import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.preselection import *\n")
    # f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.puWeightProducer import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.nanoprepro_v2 import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.GenPart_MomFirstCp import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.MCweight_writer import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.fatjetId import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.NanoTopCandidate import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.nanoTopEvaluate_MultiScore import *\n")
    #f.write("from tWb_Single_top_CKM.analysis.modules.btagSFProducer import *\n")
    # f.write(f"from module_cfg_{year} import *\n")


    #Deafult PostProcessor(outputDir,inputFiles,cut=None,branchsel=None,modules=[],compression='LZMA:9',friend=False,postfix=None, jsonInput=None,noOut=False,justcount=False,provenance=False,haddFileName=None,fwkJobReport=False,histFileName=None,histDirName=None, outputbranchsel=None,maxEntries=None,firstEntry=0, prefetch=False,longTermCache=False)\n")
    if isData:
        f.write(f"p=PostProcessor('.', inputFiles=inputFiles(), modules=[{modules}], provenance=True, fwkJobReport=True,histDirName='plots', histFileName='hist.root', haddFileName='tree.root', jsonInput=runsAndLumis(), outputbranchsel='keep_and_drop.txt')\n")#
    else: 
        f.write(f"p=PostProcessor('.', inputFiles=inputFiles(), modules=[{modules}], provenance=True, fwkJobReport=True, histDirName = 'plots', histFileName = 'hist.root', haddFileName = 'tree.root', outputbranchsel='keep_and_drop.txt')\n")# haddFileName='"+sample.label+".root'

    f.write("p.run()\n")
    f.write("print('DONE')\n")
    f.close()

    f_sh = open("crab_script.sh", "w")
    f_sh.write("#!/bin/bash\n")
    f_sh.write("echo Check if TTY\n")
    f_sh.write("if [ \"`tty`\" != \"not a tty\" ]; then\n")
    f_sh.write("  echo \"YOU SHOULD NOT RUN THIS IN INTERACTIVE, IT DELETES YOUR LOCAL FILES\"\n")
    f_sh.write("else\n\n")
    f_sh.write("echo \"ENV...................................\"\n")
    f_sh.write("env\n")
    f_sh.write("echo \"VOMS\"\n")
    f_sh.write("voms-proxy-info -all\n")
    f_sh.write("echo \"CMSSW BASE, python path, pwd\"\n")
    f_sh.write("echo $CMSSW_BASE\n")
    f_sh.write("echo $PYTHON_PATH\n")
    f_sh.write("echo $PWD\n")
    f_sh.write("echo Found Proxy in: $X509_USER_PROXY\n")
    f_sh.write("python3 crab_script.py $1\n")
    f_sh.write("fi\n")
    f_sh.close()

#Loading the samples

if not opt.dat in sample_dict.keys():
    print(f"Dataset {opt.dat} not found in sample_dict. Please check the name and try again.")
    sys.exit(1)

dataset = sample_dict[opt.dat]
samples = []

if hasattr(dataset, 'components'):
    samples = [sample for sample in dataset.components]
else:
    samples.append(dataset)
    print("Dataset does not have components, using the dataset directly.")

submit = opt.sub
status = opt.status
kill = opt.kill
resubmit = opt.resub
gout = opt.gout
dryrun = opt.dryrun


for sample in samples:
    label = sample.label
    print(f"Processing sample: {label}")
    if submit:
        year = str(sample.year)
        if "Data" in label:
            isData = True
        else:
            isData = False
        
        modelMix_path = models[f"TopMixed_{year}_TROTA2D_ptcut"]
        modelRes_path = models[f"TopResolved_{year}_TROTA2D_ptcut"]
        met_hlt_mod = f'MET_HLT_Filter_{year}()'  ## These selection could also be passed directly to postprocessor as cut
        jet_ID_mod = f'jetid_{year}()'
        fatjet_ID_mod = f'fatjetid_{year}()'

        print("Producing crab configuration file")
        cfg_writer(label, sample.dataset, isData, year, "TROTA2024/Eval_samples")

        if isData:
            modules = f"{met_hlt_mod}, {jet_ID_mod}, {fatjet_ID_mod},preselection(), nanoTopcand_PFC_SV(year = {year}, isMC =0), nanoTopevaluate_MultiClass(year = {year},isMC = 0, modelMix_path = '{modelMix_path}', modelRes_path = '{modelRes_path}') " # Put here all the modules you want to be run by crab
        else:
            modules = f"MCweight_writer(), GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), {met_hlt_mod}, {jet_ID_mod}, {fatjet_ID_mod}, preselection(), nanoprepro(),nanoTopcand_PFC_SV(year = {year}), nanoTopevaluate_MultiClass(year = {year},modelMix_path = '{modelMix_path}', modelRes_path = '{modelRes_path}')" #, {pu_mod}, {btag_mod}  # Put here all the modules you want to be run by crab

        print("Producing crab script")
        crab_script_writer(isData, year, modules)
        os.system("chmod +x crab_script.sh")
        if not dryrun: 
            #Launching crab
            print("Submitting crab jobs...")
            os.system("crab submit -c crab_cfg.py")
    
    elif kill:
        print("Killing crab jobs...")
        os.system(f"crab kill -d crab_{label}")
        os.system(f"rm -rf crab_{label}")

    elif resubmit:
        print("Resubmitting crab jobs...")
        os.system(f"crab resubmit -d crab_{label}")

    elif status:
        print("Checking crab jobs status...")
        os.system(f"crab status -d crab_{label}")