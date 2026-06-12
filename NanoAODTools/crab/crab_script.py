#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
# from PhysicsTools.NanoAODTools.postprocessing.utils.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.MET_HLT_Filter import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jetId import *
from PhysicsTools.NanoAODTools.postprocessing.modules.preselection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.fatjetId import *
from PhysicsTools.NanoAODTools.postprocessing.modules.NanoTopCandidate import *
from PhysicsTools.NanoAODTools.postprocessing.modules.nanoTopEvaluate_MultiScore import *
p=PostProcessor('.', ["root://cms-xrd-global.cern.ch://store/mc/Run3Summer22NanoAODv12/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/NANOAODSIM/130X_mcRun3_2022_realistic_v5_ext1-v2/2520000/00a70e3c-2fa7-440c-9b75-d516c76b3a97.root"], modules=[MCweight_writer(), GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), MET_HLT_Filter_2022(), jetid_2022(), fatjetid_2022(), preselection(), nanoprepro(),nanoTopcand_PFC_SV(year = 2022), nanoTopevaluate_MultiClass(year = 2022,modelMix_path = '../models/model_TopMixed_2022_TROTA2D_ptcut.h5', modelRes_path = '../models/model_TopResolved_2022_TROTA2D_ptcut.h5')], provenance=True, fwkJobReport=True, histDirName = 'plots', histFileName = 'hist.root', haddFileName = 'tree.root', outputbranchsel='../scripts/keep_and_drop.txt', maxEntries = 10)
p.run()
print('DONE')
