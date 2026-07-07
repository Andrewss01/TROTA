from WMCore.Configuration import Configuration

config = Configuration()
config.section_('General')
config.General.requestName = 'DataMuon1I_v2_2024'
config.General.transferLogs=True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py',  '../scripts/keep_and_drop.txt',  '../models/model_TopMixed_2024_TROTA2D_ptcut.h5', '../models/model_TopResolved_2024_TROTA2D_ptcut.h5']
config.JobType.outputFiles = ['tree.root']
config.section_('Data')
config.Data.inputDataset = '/Muon1/Run2024I-MINIv6NANOv15_v2-v1/NANOAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.lumiMask = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions24/Cert_Collisions2024_378981_386951_Golden.json'
config.Data.unitsPerJob = 500
config.Data.outLFNDirBase = '/store/user/apuglia/TROTA2024/Eval_samples/DataMuon1I_v2_2024'
config.Data.publication = False
config.Data.outputDatasetTag = 'DataMuon1I_v2_2024'
config.section_('Site')
config.Site.storageSite = 'T2_IT_Bari'
