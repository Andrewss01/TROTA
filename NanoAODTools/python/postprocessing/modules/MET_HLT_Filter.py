import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class MET_HLT_Filter(Module):
    def __init__(self, year):
        self.year = year
        pass
    def endJob(self):
        pass
    def beginJob(self):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        HLT = Object(event, "HLT")
        flag = Object(event, 'Flag')
        if(self.year == "2024"):
            # Taken from https://twiki.cern.ch/twiki/bin/view/CMS/MuonHLT2024
            muon_HLT = HLT.IsoMu24 or HLT.Mu50 or HLT.CascadeMu100 or HLT.HighPtTkMu100 
            # Taken from https://twiki.cern.ch/twiki/bin/view/CMS/EgHLTRunIIISummary
            egm_HLT = HLT.Ele30_WPTight_Gsf
            good_HLT = muon_HLT or egm_HLT
            # Taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
            good_MET = flag.goodVertices and flag.globalSuperTightHalo2016Filter and flag.EcalDeadCellTriggerPrimitiveFilter and flag.BadPFMuonFilter and flag.BadPFMuonDzFilter and flag.hfNoisyHitsFilter and flag.eeBadScFilter and flag.ecalBadCalibFilter
        else:
            print("Please specify the year: possible choices are 2022, 2022EE, 2023, 2023BP, 2024")
        return good_MET and good_HLT

MET_HLT_Filter_2022 = lambda : MET_HLT_Filter("2022")
MET_HLT_Filter_2022EE = lambda : MET_HLT_Filter("2022EE")
MET_HLT_Filter_2023 = lambda : MET_HLT_Filter("2023")
MET_HLT_Filter_2023BP = lambda : MET_HLT_Filter("2023BP")
MET_HLT_Filter_2024 = lambda : MET_HLT_Filter("2024")
