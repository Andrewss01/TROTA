#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.utils.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.MET_HLT_Filter import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jetId import *
from PhysicsTools.NanoAODTools.postprocessing.modules.preselection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.fatjetId import *
from PhysicsTools.NanoAODTools.postprocessing.modules.NanoTopCandidate import *
from PhysicsTools.NanoAODTools.postprocessing.modules.nanoTopEvaluate_MultiScore import *
p=PostProcessor('.', inputFiles=inputFiles(), modules=[MET_HLT_Filter_2024(), jetid_2024(), fatjetid_2024(),preselection(), nanoTopcand_PFC_SV(year = 2024, isMC =0), nanoTopevaluate_MultiClass(year = 2024,isMC = 0, modelMix_path = 'model_TopMixed_2024_TROTA2D_ptcut.h5', modelRes_path = 'model_TopResolved_2024_TROTA2D_ptcut.h5') ], provenance=True, fwkJobReport=True,histDirName='plots', histFileName='hist.root', haddFileName='tree.root', jsonInput=runsAndLumis(), outputbranchsel='keep_and_drop.txt')
p.run()
print('DONE')
