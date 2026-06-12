from WMCore.Configuration import Configuration

config = Configuration()
config.section_('General')
config.General.requestName = 'TT_hadr_2022'
config.General.transferLogs=True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py',  '../scripts/keep_and_drop.txt',  '../models/model_TopMixed_2022_TROTA2D_ptcut.h5', '../models/model_TopResolved_2022_TROTA2D_ptcut.h5']
config.JobType.outputFiles = ['tree.root']
config.section_('Data')
config.Data.inputDataset = '/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/apuglia/TROTA2024/Eval_Samples/TT_hadr_2022'
config.Data.publication = False
config.Data.outputDatasetTag = 'TT_hadr_2022'
config.section_('Site')
config.Site.storageSite = 'T2_IT_Bari'
