import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.NanoTopCandidate import *
import sys
from PhysicsTools.NanoAODTools.postprocessing.modules.jetId_v2 import *
p = PostProcessor(".", ["root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24NanoAODv15/Zto2Nu-4Jets_Bin-HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/NANOAODSIM/150X_mcRun3_2024_realistic_v2-v3/100000/d4b5d42c-3b22-49c4-8160-f2a08713cb86.root"], branchsel = None, modules = [MCweight_writer(), jetId(year=2024,EE=0), GenPart_MomFirstCp(flavour="-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24"), nanoprepro(), nanoTopcand_PFC_SV(isMC=True, year=2024)], histFileName= "hist.root", histDirName= "plots", haddFileName="tree.root",  outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop.txt" % os.environ["CMSSW_BASE"])
p.run()