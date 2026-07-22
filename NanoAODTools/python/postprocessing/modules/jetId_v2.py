"""
Add jetId variable, following the example in https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/blob/master/examples/jetidExample.py .
"""
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from correctionlib import _core
from array import array

class jetId(Module):
    def __init__(self, year, EE):
        if year == 2022:
            if EE:
                eratag              = ""
                self.CorrVersion    = ""
            else:
                eratag              = ""
                self.CorrVersion    = ""
        elif year == 2023:
            if EE:
                eratag              = ""
                self.CorrVersion    = ""
            else:
                eratag              = ""
                self.CorrVersion    = ""
        elif year == 2024:
            eratag                  = "Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15"
            self.CorrVersion        = "2026-06-05"
        else:
            print("Please specify the correct era for the jetId correction")

        self.jsonfile               = "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/"+eratag+"/"+self.CorrVersion+"/jetid.json.gz"
        self.evaluator              = _core.CorrectionSet.from_file(self.jsonfile)
        
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Jet_jetId",                    "b", lenVar="nJet",     title="Jet ID flag: bit0 is loose, bit1 is tight, bit2 is tightLepVeto (recomputed using JSON)") # Save as UChar_t as it was up to nanoAODv14
        self.out.branch("Jet_passJetIdTight",           "b", lenVar="nJet",     title="Jet ID flag: true if tight, (recomputed using JSON)") # Save as UChar_t as it was up to nanoAODv14
        self.out.branch("Jet_passJetIdTightLepVeto",    "b", lenVar="nJet",     title="Jet ID flag: true if tightLepVeto, (recomputed using JSON)") # Save as UChar_t as it was up to nanoAODv14
        self.out.branch("FatJet_jetId",                 "b", lenVar="nFatJet",  title="FatJet ID flag: bit2 is tight, bit3 is tightLepVeto (recomputed using JSON)") # Save as UChar_t as it was up to nanoAODv14
        self.out.branch("FatJet_passJetIdTight",        "b", lenVar="nFatJet",  title="FatJet ID flag: true if tight, (recomputed using JSON)") # Save as UChar_t as it was up to nanoAODv14
        self.out.branch("FatJet_passJetIdTightLepVeto", "b", lenVar="nFatJet",  title="FatJet ID flag: true if tightLepVeto, (recomputed using JSON)") # Save as UChar_t as it was up to nanoAODv14
        pass

    def analyze(self, event):
        for collection in ["Jet", "FatJet"]:
            TightFlag           = "AK4PUPPI_Tight" if collection=="Jet" else "AK8PUPPI_Tight"
            LepVetoFlag         = "AK4PUPPI_TightLeptonVeto" if collection=="Jet" else "AK8PUPPI_TightLeptonVeto"
            jets                = Collection(event, collection)
            jet_Ids             = array('B', getattr(event, f"n{collection}")*[0]) # Note: UChar_t is uppercase 'B' in python array
            jet_TightIds        = array('B', getattr(event, f"n{collection}")*[0]) # Note: UChar_t is uppercase 'B' in python array
            jet_TightLepVetoIds = array('B', getattr(event, f"n{collection}")*[0]) # Note: UChar_t is uppercase 'B' in python array
        
            for ijet, jet in enumerate(jets):
                multiplicity                = jet.chMultiplicity + jet.neMultiplicity

                passTight                   = self.evaluator[TightFlag].evaluate(
                                                                                    jet.eta,
                                                                                    jet.chHEF,
                                                                                    jet.neHEF,
                                                                                    jet.chEmEF,
                                                                                    jet.neEmEF,
                                                                                    jet.muEF,
                                                                                    jet.chMultiplicity,
                                                                                    jet.neMultiplicity,
                                                                                    multiplicity
                                                                                    )
                passTightLepVeto            = self.evaluator[LepVetoFlag].evaluate(
                                                                                    jet.eta,
                                                                                    jet.chHEF,
                                                                                    jet.neHEF,
                                                                                    jet.chEmEF,
                                                                                    jet.neEmEF,
                                                                                    jet.muEF,
                                                                                    jet.chMultiplicity,
                                                                                    jet.neMultiplicity,
                                                                                    multiplicity
                                                                                    )
                
                jet_Ids[ijet]               = int(passTight)*2 + int(passTightLepVeto)*4
                jet_TightIds[ijet]          = int(passTight)
                jet_TightLepVetoIds[ijet]   = int(passTightLepVeto)


            self.out.fillBranch(f"{collection}_jetId",                  jet_Ids)
            self.out.fillBranch(f"{collection}_passJetIdTight",         jet_TightIds)
            self.out.fillBranch(f"{collection}_passJetIdTightLepVeto",  jet_TightLepVetoIds)

        return True