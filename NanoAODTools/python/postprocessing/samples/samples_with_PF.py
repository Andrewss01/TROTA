

import ROOT
import os


class sample:
    def __init__(self, color, style, fill, leglabel, label):
        self.color = color
        self.style = style
        self.fill = fill
        self.leglabel = leglabel
        self.label = label

######################################### QCD #################################################

QCD_HT70to100_2022              = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT70to100_2022")
QCD_HT70to100_2022.sigma        = 58.6*(10**6) #pb
QCD_HT70to100_2022.year         = 2022
QCD_HT70to100_2022.dataset      = "/QCD-4Jets_HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT70to100_2022_v2-0fa328e40e38f44cd311b92489b92b5b/USER"
QCD_HT70to100_2022.process      = "QCD_2022"
QCD_HT70to100_2022.unix_code    = 31001
QCD_HT70to100_2022.EE           = 0

QCD_HT100to200_2022             = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT100to200_2022")
QCD_HT100to200_2022.sigma       = 25.1*(10**6) #pb
QCD_HT100to200_2022.year        = 2022
QCD_HT100to200_2022.dataset     = "/QCD-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT100to200_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
QCD_HT100to200_2022.process     = "QCD_2022"
QCD_HT100to200_2022.unix_code   = 31002
QCD_HT100to200_2022.EE          = 0

QCD_HT200to400_2022             = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT200to400_2022")
QCD_HT200to400_2022.sigma       = 1.96*(10**6) #pb
QCD_HT200to400_2022.year        = 2022
QCD_HT200to400_2022.dataset     = "/QCD-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT200to400_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
QCD_HT200to400_2022.process     = "QCD_2022"
QCD_HT200to400_2022.unix_code   = 31003
QCD_HT200to400_2022.EE          = 0

QCD_HT400to600_2022             = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT400to600_2022")
QCD_HT400to600_2022.sigma       = 96.0*(10**3) #pb
QCD_HT400to600_2022.year        = 2022
QCD_HT400to600_2022.dataset     = "/QCD-4Jets_HT-400to600_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT400to600_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
QCD_HT400to600_2022.process     = "QCD_2022"
QCD_HT400to600_2022.unix_code   = 31004
QCD_HT400to600_2022.EE          = 0

QCD_HT600to800_2022             = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT600to800_2022")
QCD_HT600to800_2022.sigma       = 13.5*(10**3) #pb
QCD_HT600to800_2022.year        = 2022
QCD_HT600to800_2022.dataset     = "/QCD-4Jets_HT-600to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT600to800_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
QCD_HT600to800_2022.process     = "QCD_2022"
QCD_HT600to800_2022.unix_code   = 31005
QCD_HT600to800_2022.EE          = 0

QCD_HT800to1000_2022            = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT800to1000_2022")
QCD_HT800to1000_2022.sigma      = 3.03*(10**3) #pb
QCD_HT800to1000_2022.year       = 2022
QCD_HT800to1000_2022.dataset    = "/QCD-4Jets_HT-800to1000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT800to1000_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
QCD_HT800to1000_2022.process    = "QCD_2022"
QCD_HT800to1000_2022.unix_code  = 31006
QCD_HT800to1000_2022.EE         = 0

QCD_HT1000to1200_2022           = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT1000to1200_2022")
QCD_HT1000to1200_2022.sigma     = 884 #pb
QCD_HT1000to1200_2022.year      = 2022
QCD_HT1000to1200_2022.dataset   = "/QCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT1000to1200_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
QCD_HT1000to1200_2022.process   = "QCD_2022"
QCD_HT1000to1200_2022.unix_code = 31007
QCD_HT1000to1200_2022.EE        = 0

QCD_HT1200to1500_2022           = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT1200to1500_2022")
QCD_HT1200to1500_2022.sigma     = 384 #pb 
QCD_HT1200to1500_2022.year      = 2022
QCD_HT1200to1500_2022.dataset   = "/QCD-4Jets_HT-1200to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT1200to1500_2022_v2-0fa328e40e38f44cd311b92489b92b5b/USER"
QCD_HT1200to1500_2022.process   = "QCD_2022"
QCD_HT1200to1500_2022.unix_code = 31007
QCD_HT1200to1500_2022.EE        = 0

QCD_HT1500to2000_2022           = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT1500to2000_2022")
QCD_HT1500to2000_2022.sigma     = 125 #pb
QCD_HT1500to2000_2022.year      = 2022
QCD_HT1500to2000_2022.dataset   = "/QCD-4Jets_HT-1500to2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT1500to2000_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
QCD_HT1500to2000_2022.process   = "QCD_2022"
QCD_HT1500to2000_2022.unix_code = 31008
QCD_HT1500to2000_2022.EE        = 0

QCD_HT2000_2022                 = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT2000_2022")
QCD_HT2000_2022.sigma           = 26.5 #pb
QCD_HT2000_2022.year            = 2022
QCD_HT2000_2022.dataset         = "/QCD-4Jets_HT-2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT2000_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
QCD_HT2000_2022.process         = "QCD_2022"
QCD_HT2000_2022.unix_code       = 31009
QCD_HT2000_2022.EE              = 0

QCD_2022                        = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_2022")
QCD_2022.year                   = 2022
QCD_2022.components             = [ 
                                    # QCD_HT40to70_2022, 
                                    QCD_HT70to100_2022, QCD_HT100to200_2022, QCD_HT200to400_2022, QCD_HT400to600_2022, 
                                    QCD_HT600to800_2022, QCD_HT800to1000_2022, 
                                    QCD_HT1000to1200_2022, QCD_HT1200to1500_2022,
                                    QCD_HT1500to2000_2022, QCD_HT2000_2022
                                ]

################################ TTbar ################################

TT_semilep_2022             = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_semilep_2022")
TT_semilep_2022.sigma       = 404.0 #pb
TT_semilep_2022.year        = 2022
TT_semilep_2022.dataset     = "/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/apuglia-TT_semilep_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
TT_semilep_2022.process     = 'TT_2022'
TT_semilep_2022.unix_code   = 31100
TT_semilep_2022.EE          = 0

TT_hadr_2022                = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_hadr_2022")
TT_hadr_2022.sigma          = 422.3
TT_hadr_2022.year           = 2022
TT_hadr_2022.dataset        = "/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/apuglia-TT_hadr_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
TT_hadr_2022.process        = 'TT_2022'
TT_hadr_2022.unix_code      = 31101
TT_hadr_2022.EE             = 0

TT_dilep_2022               = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_dilep_2022")
TT_dilep_2022.sigma         = 96.9
TT_dilep_2022.year          = 2022
TT_dilep_2022.dataset       = "/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/apuglia-TTto2L2Nu_2022_v2-0fa328e40e38f44cd311b92489b92b5b/USER"
TT_dilep_2022.process       = 'TT_2022'
TT_dilep_2022.unix_code     = 31102
TT_dilep_2022.EE            = 0

TT_2022                     = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_2022")
TT_2022.year                = 2022
TT_2022.components          = [TT_semilep_2022, TT_hadr_2022, TT_dilep_2022]

################################ ZJets ################################

ZJetsToNuNu_HT100to200_2022             = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT100to200_2022")
ZJetsToNuNu_HT100to200_2022.sigma       = 273.7 #pb
ZJetsToNuNu_HT100to200_2022.year        = 2022
ZJetsToNuNu_HT100to200_2022.dataset     = "/Zto2Nu-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-ZJetsto2Nu_HT100to200_2022_v2-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_HT100to200_2022.process     = 'ZJetsToNuNu_2022'
ZJetsToNuNu_HT100to200_2022.unix_code   = 31200
ZJetsToNuNu_HT100to200_2022.EE          = 0

ZJetsToNuNu_HT200to400_2022             = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT200to400_2022")
ZJetsToNuNu_HT200to400_2022.sigma       = 75.96 #pb
ZJetsToNuNu_HT200to400_2022.year        = 2022
ZJetsToNuNu_HT200to400_2022.dataset     = "/Zto2Nu-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-ZJetsto2Nu_HT200to400_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_HT200to400_2022.process     = 'ZJetsToNuNu_2022'
ZJetsToNuNu_HT200to400_2022.unix_code   = 31201
ZJetsToNuNu_HT200to400_2022.EE          = 0

ZJetsToNuNu_HT400to800_2022             = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT400to800_2022")
ZJetsToNuNu_HT400to800_2022.sigma       = 13.19 #pb
ZJetsToNuNu_HT400to800_2022.year        = 2022
ZJetsToNuNu_HT400to800_2022.dataset     = "/Zto2Nu-4Jets_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-ZJetsToNuNu_HT400to800_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_HT400to800_2022.process     = 'ZJetsToNuNu_2022'
ZJetsToNuNu_HT400to800_2022.unix_code   = 31202
ZJetsToNuNu_HT400to800_2022.EE          = 0

ZJetsToNuNu_HT800to1500_2022            = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT800to1500_2022")
ZJetsToNuNu_HT800to1500_2022.sigma      = 1.364 #pb
ZJetsToNuNu_HT800to1500_2022.year       = 2022
ZJetsToNuNu_HT800to1500_2022.dataset    = "/Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-ZJetsToNuNu_HT800to1500_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_HT800to1500_2022.process    = 'ZJetsToNuNu_2022'
ZJetsToNuNu_HT800to1500_2022.unix_code  = 31203
ZJetsToNuNu_HT800to1500_2022.EE         = 0

ZJetsToNuNu_HT1500to2500_2022           = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT1500to2500_2022")
ZJetsToNuNu_HT1500to2500_2022.sigma     = 0.09865 #pb
ZJetsToNuNu_HT1500to2500_2022.year      = 2022
ZJetsToNuNu_HT1500to2500_2022.dataset   = "/Zto2Nu-4Jets_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-ZJetsToNuNu_HT1500to2500_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_HT1500to2500_2022.process   = 'ZJetsToNuNu_2022'
ZJetsToNuNu_HT1500to2500_2022.unix_code = 31204
ZJetsToNuNu_HT1500to2500_2022.EE        = 0

ZJetsToNuNu_HT2500_2022                 = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT2500_2022")
ZJetsToNuNu_HT2500_2022.sigma           = 0.006699 #pb
ZJetsToNuNu_HT2500_2022.year            = 2022
ZJetsToNuNu_HT2500_2022.dataset         = "/Zto2Nu-4Jets_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-ZJetsToNuNu_HT2500_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_HT2500_2022.process         = 'ZJetsToNuNu_2022'
ZJetsToNuNu_HT2500_2022.unix_code       = 31205
ZJetsToNuNu_HT2500_2022.EE              = 0

ZJetsToNuNu_2022                        = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2022")
ZJetsToNuNu_2022.year                   = 2022
ZJetsToNuNu_2022.components             = [
                                            ZJetsToNuNu_HT100to200_2022,
                                            ZJetsToNuNu_HT200to400_2022,
                                            ZJetsToNuNu_HT400to800_2022,
                                            ZJetsToNuNu_HT800to1500_2022,
                                            ZJetsToNuNu_HT1500to2500_2022,
                                            ZJetsToNuNu_HT2500_2022 
                                            ]


ZJetsToNuNu_2jets_PT40to100_1J_2022            = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2jets_PT40to100_1J_2022")
ZJetsToNuNu_2jets_PT40to100_1J_2022.sigma      = 929.8	
ZJetsToNuNu_2jets_PT40to100_1J_2022.year       = 2022
ZJetsToNuNu_2jets_PT40to100_1J_2022.dataset    = "/Zto2Nu-2Jets_PTNuNu-40to100_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/apuglia-ZJetsToNuNu_2jets_PT40to100_1J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_2jets_PT40to100_1J_2022.process    = 'ZJetsToNuNu_2jets_2022'
ZJetsToNuNu_2jets_PT40to100_1J_2022.unix_code  = 31206
ZJetsToNuNu_2jets_PT40to100_1J_2022.EE         = 0

ZJetsToNuNu_2jets_PT100to200_1J_2022            = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2jets_PT100to200_1J_2022")
ZJetsToNuNu_2jets_PT100to200_1J_2022.sigma      = 86.38
ZJetsToNuNu_2jets_PT100to200_1J_2022.year       = 2022
ZJetsToNuNu_2jets_PT100to200_1J_2022.dataset    = "/Zto2Nu-2Jets_PTNuNu-100to200_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/apuglia-ZJetsToNuNu_2jets_PT100to200_1J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_2jets_PT100to200_1J_2022.process    = 'ZJetsToNuNu_2jets_2022'
ZJetsToNuNu_2jets_PT100to200_1J_2022.unix_code  = 31207
ZJetsToNuNu_2jets_PT100to200_1J_2022.EE         = 0

ZJetsToNuNu_2jets_PT200to400_1J_2022            = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2jets_PT200to400_1J_2022")
ZJetsToNuNu_2jets_PT200to400_1J_2022.sigma      = 6.354	
ZJetsToNuNu_2jets_PT200to400_1J_2022.year       = 2022
ZJetsToNuNu_2jets_PT200to400_1J_2022.dataset    = "/Zto2Nu-2Jets_PTNuNu-200to400_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/apuglia-ZJetsToNuNu_2jets_PT200to400_1J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_2jets_PT200to400_1J_2022.process    = 'ZJetsToNuNu_2jets_2022'
ZJetsToNuNu_2jets_PT200to400_1J_2022.unix_code  = 31208
ZJetsToNuNu_2jets_PT200to400_1J_2022.EE         = 0

ZJetsToNuNu_2jets_PT400to600_1J_2022            = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2jets_PT400to600_1J_2022")
ZJetsToNuNu_2jets_PT400to600_1J_2022.sigma      = 0.2188
ZJetsToNuNu_2jets_PT400to600_1J_2022.year       = 2022
ZJetsToNuNu_2jets_PT400to600_1J_2022.dataset    = "/Zto2Nu-2Jets_PTNuNu-400to600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/apuglia-ZJetsToNuNu_2jets_PT400to600_1J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_2jets_PT400to600_1J_2022.process    = 'ZJetsToNuNu_2jets_2022'
ZJetsToNuNu_2jets_PT400to600_1J_2022.unix_code  = 31209
ZJetsToNuNu_2jets_PT400to600_1J_2022.EE         = 0

ZJetsToNuNu_2jets_PT600_1J_2022                 = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2jets_PT600_1J_2022")
ZJetsToNuNu_2jets_PT600_1J_2022.sigma           = 0.02583
ZJetsToNuNu_2jets_PT600_1J_2022.year            = 2022
ZJetsToNuNu_2jets_PT600_1J_2022.dataset         = "/Zto2Nu-2Jets_PTNuNu-600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/apuglia-ZJetsToNuNu_2jets_PT600_1J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_2jets_PT600_1J_2022.process         = 'ZJetsToNuNu_2jets_2022'
ZJetsToNuNu_2jets_PT600_1J_2022.unix_code       = 31210
ZJetsToNuNu_2jets_PT600_1J_2022.EE              = 0

ZJetsToNuNu_2jets_PT40to100_2J_2022             = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2jets_PT40to100_2J_2022")
ZJetsToNuNu_2jets_PT40to100_2J_2022.sigma       = 335.5
ZJetsToNuNu_2jets_PT40to100_2J_2022.year        = 2022
ZJetsToNuNu_2jets_PT40to100_2J_2022.dataset     = "/Zto2Nu-2Jets_PTNuNu-40to100_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/apuglia-ZJetsToNuNu_2jets_PT40to100_2J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_2jets_PT40to100_2J_2022.process     = 'ZJetsToNuNu_2jets_2022'
ZJetsToNuNu_2jets_PT40to100_2J_2022.unix_code   = 31211
ZJetsToNuNu_2jets_PT40to100_2J_2022.EE          = 0

ZJetsToNuNu_2jets_PT100to200_2J_2022            = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2jets_PT100to200_2J_2022")
ZJetsToNuNu_2jets_PT100to200_2J_2022.sigma      = 100.4
ZJetsToNuNu_2jets_PT100to200_2J_2022.year       = 2022
ZJetsToNuNu_2jets_PT100to200_2J_2022.dataset    = "/Zto2Nu-2Jets_PTNuNu-100to200_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/apuglia-ZJetsToNuNu_2jets_PT100to200_2J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_2jets_PT100to200_2J_2022.process    = 'ZJetsToNuNu_2jets_2022'
ZJetsToNuNu_2jets_PT100to200_2J_2022.unix_code  = 31212
ZJetsToNuNu_2jets_PT100to200_2J_2022.EE         = 0

ZJetsToNuNu_2jets_PT200to400_2J_2022            = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2jets_PT200to400_2J_2022")
ZJetsToNuNu_2jets_PT200to400_2J_2022.sigma      = 13.86
ZJetsToNuNu_2jets_PT200to400_2J_2022.year       = 2022
ZJetsToNuNu_2jets_PT200to400_2J_2022.dataset    = "/Zto2Nu-2Jets_PTNuNu-200to400_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/apuglia-ZJetsToNuNu_2jets_PT200to400_2J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_2jets_PT200to400_2J_2022.process    = 'ZJetsToNuNu_2jets_2022'
ZJetsToNuNu_2jets_PT200to400_2J_2022.unix_code  = 31213
ZJetsToNuNu_2jets_PT200to400_2J_2022.EE         = 0

ZJetsToNuNu_2jets_PT400to600_2J_2022            = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2jets_PT400to600_2J_2022")
ZJetsToNuNu_2jets_PT400to600_2J_2022.sigma      = 0.7816
ZJetsToNuNu_2jets_PT400to600_2J_2022.year       = 2022
ZJetsToNuNu_2jets_PT400to600_2J_2022.dataset    = "/Zto2Nu-2Jets_PTNuNu-400to600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/apuglia-ZJetsToNuNu_2jets_PT400to600_2J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_2jets_PT400to600_2J_2022.process    = 'ZJetsToNuNu_2jets_2022'
ZJetsToNuNu_2jets_PT400to600_2J_2022.unix_code  = 31214
ZJetsToNuNu_2jets_PT400to600_2J_2022.EE         = 0

ZJetsToNuNu_2jets_PT600_2J_2022                 = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2jets_PT600_2J_2022")
ZJetsToNuNu_2jets_PT600_2J_2022.sigma           = 0.1311
ZJetsToNuNu_2jets_PT600_2J_2022.year            = 2022
ZJetsToNuNu_2jets_PT600_2J_2022.dataset         = "/Zto2Nu-2Jets_PTNuNu-600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/apuglia-ZJetsToNuNu_2jets_PT600_2J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
ZJetsToNuNu_2jets_PT600_2J_2022.process         = 'ZJetsToNuNu_2jets_2022'
ZJetsToNuNu_2jets_PT600_2J_2022.unix_code       = 31215
ZJetsToNuNu_2jets_PT600_2J_2022.EE              = 0

ZJetsToNuNu_2jets_2022 = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2jets_2022")
ZJetsToNuNu_2jets_2022.year = 2022
ZJetsToNuNu_2jets_2022.components = [
                                        ZJetsToNuNu_2jets_PT40to100_1J_2022,
                                        ZJetsToNuNu_2jets_PT100to200_1J_2022,
                                        ZJetsToNuNu_2jets_PT200to400_1J_2022,
                                        ZJetsToNuNu_2jets_PT400to600_1J_2022,
                                        ZJetsToNuNu_2jets_PT600_1J_2022,
                                        ZJetsToNuNu_2jets_PT40to100_2J_2022,
                                        ZJetsToNuNu_2jets_PT100to200_2J_2022,
                                        ZJetsToNuNu_2jets_PT200to400_2J_2022,
                                        ZJetsToNuNu_2jets_PT400to600_2J_2022,
                                        ZJetsToNuNu_2jets_PT600_2J_2022
                                    ]

################################ WJets ################################
WJets_HT120to200_2022               = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_HT120to200_2022") 
WJets_HT120to200_2022.dataset       = "/WtoLNu-4Jets_MLNu-120to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-120to200_v2-0fa328e40e38f44cd311b92489b92b5b/USER"
WJets_HT120to200_2022.sigma         = 167
WJets_HT120to200_2022.year          = 2022
WJets_HT120to200_2022.process       = "WJets_2022"
WJets_HT120to200_2022.unix_code     = 31300
WJets_HT120to200_2022.EE            = 0

WJets_HT200to400_2022               = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_HT200to400_2022") 
WJets_HT200to400_2022.dataset       = "/WtoLNu-4Jets_MLNu-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-200to400_v2-0fa328e40e38f44cd311b92489b92b5b/USER"
WJets_HT200to400_2022.sigma         = 20.3	
WJets_HT200to400_2022.year          = 2022
WJets_HT200to400_2022.process       = "WJets_2022"
WJets_HT200to400_2022.unix_code     = 31301
WJets_HT200to400_2022.EE            = 0

WJets_HT400to800_2022               = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_HT400to800_2022") 
WJets_HT400to800_2022.dataset       = "/WtoLNu-4Jets_MLNu-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-400to800_v2-0fa328e40e38f44cd311b92489b92b5b/USER"
WJets_HT400to800_2022.sigma         = 1.596
WJets_HT400to800_2022.year          = 2022
WJets_HT400to800_2022.process       = "WJets_2022"
WJets_HT400to800_2022.unix_code     = 31302
WJets_HT400to800_2022.EE            = 0

WJets_HT800to1500_2022              = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_HT800to1500_2022") 
WJets_HT800to1500_2022.dataset      = "/WtoLNu-4Jets_MLNu-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-800to1500_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
WJets_HT800to1500_2022.sigma        = 0.1095	
WJets_HT800to1500_2022.year         = 2022
WJets_HT800to1500_2022.process      = "WJets_2022"
WJets_HT800to1500_2022.unix_code    = 31303
WJets_HT800to1500_2022.EE           = 0

WJets_HT1500to2500_2022             = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_HT1500to2500_2022") 
WJets_HT1500to2500_2022.dataset     = "/WtoLNu-4Jets_MLNu-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-1500to2500_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
WJets_HT1500to2500_2022.sigma       = 0.006365
WJets_HT1500to2500_2022.year        = 2022
WJets_HT1500to2500_2022.process     = "WJets_2022"
WJets_HT1500to2500_2022.unix_code   = 31304
WJets_HT1500to2500_2022.EE          = 0

WJets_HT2500to4000_2022             = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_HT2500to4000_2022") 
WJets_HT2500to4000_2022.dataset     = "/WtoLNu-4Jets_MLNu-2500to4000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-2500to4000_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
WJets_HT2500to4000_2022.sigma       = 0.0003463
WJets_HT2500to4000_2022.year        = 2022
WJets_HT2500to4000_2022.process     = "WJets_2022"
WJets_HT2500to4000_2022.unix_code   = 31305
WJets_HT2500to4000_2022.EE          = 0

WJets_HT4000to6000_2022             = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_HT4000to6000_2022") 
WJets_HT4000to6000_2022.dataset     = "/WtoLNu-4Jets_MLNu-4000to6000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-4000to6000_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
WJets_HT4000to6000_2022.sigma       = 0.00001075
WJets_HT4000to6000_2022.year        = 2022
WJets_HT4000to6000_2022.process     = "WJets_2022"
WJets_HT4000to6000_2022.unix_code   = 31306
WJets_HT4000to6000_2022.EE          = 0

WJets_HT6000_2022                   = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_HT6000_2022") 
WJets_HT6000_2022.dataset           = "/WtoLNu-4Jets_MLNu-6000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-6000_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
WJets_HT6000_2022.sigma             = 4.182e-7	
WJets_HT6000_2022.year              = 2022
WJets_HT6000_2022.process           = "WJets_2022"
WJets_HT6000_2022.unix_code         = 31307
WJets_HT6000_2022.EE                = 0

WJets_2022                  = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_2022")
WJets_2022.year             = 2022
WJets_2022.components       = [WJets_HT120to200_2022, WJets_HT200to400_2022, WJets_HT400to800_2022, WJets_HT800to1500_2022, WJets_HT1500to2500_2022, WJets_HT2500to4000_2022, WJets_HT4000to6000_2022, WJets_HT6000_2022]

WJets_2jets0J_2022           = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_2jets0J_2022")
WJets_2jets0J_2022.dataset   = "/WtoLNu-2Jets_0J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/apuglia-WJets_2jets0J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
WJets_2jets0J_2022.sigma     = 55760 
WJets_2jets0J_2022.year      = 2022
WJets_2jets0J_2022.process   = "WJets_2jets_2022"
WJets_2jets0J_2022.unix_code = 31308
WJets_2jets0J_2022.EE        = 0

WJets_2jets1J_2022           = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_2jets1J_2022")
WJets_2jets1J_2022.dataset   = "/WtoLNu-2Jets_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/apuglia-WJets_2jets1J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
WJets_2jets1J_2022.sigma     = 9529 
WJets_2jets1J_2022.year      = 2022
WJets_2jets1J_2022.process   = "WJets_2jets_2022"
WJets_2jets1J_2022.unix_code = 31309
WJets_2jets1J_2022.EE        = 0

WJets_2jets2J_2022           = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_2jets2J_2022")
WJets_2jets2J_2022.dataset   = "/WtoLNu-2Jets_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/apuglia-WJets_2jets2J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
WJets_2jets2J_2022.sigma     = 3532 
WJets_2jets2J_2022.year      = 2022
WJets_2jets2J_2022.process   = "WJets_2jets_2022"
WJets_2jets2J_2022.unix_code = 31310
WJets_2jets2J_2022.EE        = 0

WJets_2jets_2022             = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_2jets_2022")
WJets_2jets_2022.year        = 2022
WJets_2jets_2022.components  = [WJets_2jets0J_2022, WJets_2jets1J_2022, WJets_2jets2J_2022]

#######################################   VLQ T signals   #######################################
TprimeToTZ_700_2022           = sample(ROOT.kGreen, 1, 1001, "T#rightarrow tZ M700GeV", "TprimeToTZ_700_2022")
TprimeToTZ_700_2022.sigma     = 0.07804 #pb  # questa è 2018 non 2022
TprimeToTZ_700_2022.year      = 2022
TprimeToTZ_700_2022.dataset   = "/TprimeBtoTZ_M-700_LH_TuneCP5_13p6TeV_madgraph-pythia8/apuglia-TprimeToTZ_700_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
TprimeToTZ_700_2022.unix_code = 32000
TprimeToTZ_700_2022.process   = "TprimeToTZ_700_2022"
TprimeToTZ_700_2022.EE        = 0

TprimeToTZ_800_2022           = sample(ROOT.kGreen, 1, 1001, "T#rightarrow tZ M800GeV", "TprimeToTZ_800_2022")
TprimeToTZ_800_2022.sigma     = 0.04155 #pb  # questa è 2018 non 2022
TprimeToTZ_800_2022.year      = 2022
TprimeToTZ_800_2022.dataset   = "/TprimeBtoTZ_M-800_LH_TuneCP5_13p6TeV_madgraph-pythia8/apuglia-TprimeToTZ_800_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
TprimeToTZ_800_2022.unix_code = 32001
TprimeToTZ_800_2022.process   = "TprimeToTZ_800_2022"
TprimeToTZ_800_2022.EE        = 0

TprimeToTZ_900_2022           = sample(ROOT.kGreen, 1, 1001, "T#rightarrow tZ M900GeV", "TprimeToTZ_900_2022")
TprimeToTZ_900_2022.sigma     = 0.02335 #pb  # questa è 2018 non 2022
TprimeToTZ_900_2022.year      = 2022
TprimeToTZ_900_2022.dataset   = "/TprimeBtoTZ_M-900_LH_TuneCP5_13p6TeV_madgraph-pythia8/apuglia-TprimeToTZ_900_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
TprimeToTZ_900_2022.unix_code = 32002
TprimeToTZ_900_2022.process   = "TprimeToTZ_900_2022"
TprimeToTZ_900_2022.EE        = 0

TprimeToTZ_1000_2022           = sample(ROOT.kGreen+2, 1, 1001, "T#rightarrow tZ M1000GeV", "TprimeToTZ_1000_2022")
TprimeToTZ_1000_2022.sigma     = 0.01362 #pb  # questa è 2018 non 2022
TprimeToTZ_1000_2022.year      = 2022
TprimeToTZ_1000_2022.dataset   =  "/TprimeBtoTZ_M-1000_LH_TuneCP5_13p6TeV_madgraph-pythia8/apuglia-TprimeToTZ_1000_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
TprimeToTZ_1000_2022.unix_code = 32003
TprimeToTZ_1000_2022.process   = "TprimeToTZ_1000_2022"
TprimeToTZ_1000_2022.EE        = 0

TprimeToTZ_1100_2022           = sample(ROOT.kGreen+2, 1, 1001, "T#rightarrow tZ M1100GeV", "TprimeToTZ_1100_2022")
TprimeToTZ_1100_2022.sigma     = 0.008228 #pb  # questa è 2018 non 2022
TprimeToTZ_1100_2022.year      = 2022
TprimeToTZ_1100_2022.dataset   =  "/TprimeBtoTZ_M-1100_LH_TuneCP5_13p6TeV_madgraph-pythia8/apuglia-TprimeToTZ_1100_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
TprimeToTZ_1100_2022.unix_code = 32003
TprimeToTZ_1100_2022.process   = "TprimeToTZ_1100_2022"
TprimeToTZ_1100_2022.EE        = 0

TprimeToTZ_1200_2022           = sample(ROOT.kGreen+2, 1, 1001, "T#rightarrow tZ M1200GeV", "TprimeToTZ_1200_2022")
TprimeToTZ_1200_2022.sigma     = 0.005113 #pb  # questa è 2018 non 2022
TprimeToTZ_1200_2022.year      = 2022
TprimeToTZ_1200_2022.dataset   =  "/TprimeBtoTZ_M-1200_LH_TuneCP5_13p6TeV_madgraph-pythia8/apuglia-TprimeToTZ_1200_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
TprimeToTZ_1200_2022.unix_code = 32003
TprimeToTZ_1200_2022.process   = "TprimeToTZ_1200_2022"
TprimeToTZ_1200_2022.EE        = 0

TprimeToTZ_1300_2022           = sample(ROOT.kGreen+2, 1, 1001, "T#rightarrow tZ M1300GeV", "TprimeToTZ_1300_2022")
TprimeToTZ_1300_2022.sigma     = 0.003256 #pb  # questa è 2018 non 2022
TprimeToTZ_1300_2022.year      = 2022
TprimeToTZ_1300_2022.dataset   =  "/TprimeBtoTZ_M-1300_LH_TuneCP5_13p6TeV_madgraph-pythia8/apuglia-TprimeToTZ_1300_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
TprimeToTZ_1300_2022.unix_code = 32003
TprimeToTZ_1300_2022.process   = "TprimeToTZ_1300_2022"
TprimeToTZ_1300_2022.EE        = 0

TprimeToTZ_1400_2022           = sample(ROOT.kGreen+2, 1, 1001, "T#rightarrow tZ M1400GeV", "TprimeToTZ_1400_2022")
TprimeToTZ_1400_2022.sigma     = 0.002121 #pb  # questa è 2018 non 2022
TprimeToTZ_1400_2022.year      = 2022
TprimeToTZ_1400_2022.dataset   =  "/TprimeBtoTZ_M-1400_LH_TuneCP5_13p6TeV_madgraph-pythia8/apuglia-TprimeToTZ_1400_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
TprimeToTZ_1400_2022.unix_code = 32003
TprimeToTZ_1400_2022.process   = "TprimeToTZ_1400_2022"
TprimeToTZ_1400_2022.EE        = 0

TprimeToTZ_1500_2022           = sample(ROOT.kGreen+2, 1, 1001, "T#rightarrow tZ M1500GeV", "TprimeToTZ_1500_2022")
TprimeToTZ_1500_2022.sigma     = 0.001407 #pb  # questa è 2018 non 2022
TprimeToTZ_1500_2022.year      = 2022
TprimeToTZ_1500_2022.dataset   =  "/TprimeBtoTZ_M-1500_LH_TuneCP5_13p6TeV_madgraph-pythia8/apuglia-TprimeToTZ_1500_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
TprimeToTZ_1500_2022.unix_code = 32003
TprimeToTZ_1500_2022.process   = "TprimeToTZ_1500_2022"
TprimeToTZ_1500_2022.EE        = 0

TprimeToTZ_1600_2022           = sample(ROOT.kGreen+2, 1, 1001, "T#rightarrow tZ M1600GeV", "TprimeToTZ_1600_2022")
TprimeToTZ_1600_2022.sigma     = 0.0009456 #pb  # questa è 2018 non 2022
TprimeToTZ_1600_2022.year      = 2022
TprimeToTZ_1600_2022.dataset   =  "/TprimeBtoTZ_M-1600_LH_TuneCP5_13p6TeV_madgraph-pythia8/apuglia-TprimeToTZ_1600_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
TprimeToTZ_1600_2022.unix_code = 32003
TprimeToTZ_1600_2022.process   = "TprimeToTZ_1600_2022"
TprimeToTZ_1600_2022.EE        = 0

TprimeToTZ_1700_2022           = sample(ROOT.kGreen+2, 1, 1001, "T#rightarrow tZ M1700GeV", "TprimeToTZ_1700_2022")
TprimeToTZ_1700_2022.sigma     = 0.0006454 #pb  # questa è 2018 non 2022
TprimeToTZ_1700_2022.year      = 2022
TprimeToTZ_1700_2022.dataset   =  "/TprimeBtoTZ_M-1700_LH_TuneCP5_13p6TeV_madgraph-pythia8/apuglia-TprimeToTZ_1700_v1-0fa328e40e38f44cd311b92489b92b5b/USER"
TprimeToTZ_1700_2022.unix_code = 32003
TprimeToTZ_1700_2022.process   = "TprimeToTZ_1700_2022"
TprimeToTZ_1700_2022.EE        = 0

TprimeToTZ_1800_2022           = sample(ROOT.kGreen+4, 1, 1001, "T#rightarrow tZ M1800GeV", "TprimeToTZ_1800_2022")
TprimeToTZ_1800_2022.sigma     = 0.0004463 #pb
TprimeToTZ_1800_2022.year      = 2022
TprimeToTZ_1800_2022.dataset   = ""
TprimeToTZ_1800_2022.unix_code = 22000
TprimeToTZ_1800_2022.process   = "TprimeToTZ_1800_2022"
TprimeToTZ_1800_2022.EE        = 0

################################DATA####################################################



DataMuonC_2022              = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuonC_2022")
DataMuonC_2022.runP         = 'C'
DataMuonC_2022.year         = 2022
DataMuonC_2022.dataset      = '/Muon/apuglia-DataMuon_22Sep2023_v1-9d6cd248ad01d98982be66db74e631c2/USER'
DataMuonC_2022.process     = "DataMuon_2022"
DataMuonC_2022.unix_code    = 30100
DataMuonC_2022.EE           = 0


DataMuon_2022               = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuon_2022")
DataMuon_2022.year          = 2022
DataMuon_2022.components    = [DataMuonC_2022]



####################################################################################################
####################################################################################################
####################################################################################################
################################# 2024 #############################################################
####################################################################################################
####################################################################################################
####################################################################################################


#############################################################
###############ttbar########################################
##############################################################

TT_semilep_2024 = sample(ROOT.kOrange,1,1001,"t#bar{t}","TT_semilep_2024")
TT_semilep_2024.sigma  = 404#pb
TT_semilep_2024.year = 2024
TT_semilep_2024.dataset = "/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/apuglia-TT_semilep_v1-00000000000000000000000000000000/USER"
TT_semilep_2024.process = "TT_2024" 
TT_semilep_2024.unix_code = 31100
TT_semilep_2024.EE = 0

TT_dilep_2024 = sample(ROOT.kOrange,1,1001,"t#bar{t}","TT_dilep_2024")
TT_dilep_2024.sigma = 96.9  #pb
TT_dilep_2024.year = 2024
TT_dilep_2024.dataset = "/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/apuglia-TT_dilep_v1-00000000000000000000000000000000/USER"
TT_dilep_2024.process = "TT_2024"
TT_dilep_2024.unix_code = 31102
TT_dilep_2024.EE = 0


TT_hadr_2024                = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_hadr_2024")
TT_hadr_2024.sigma          = 422.3
TT_hadr_2024.year           = 2024
TT_hadr_2024.dataset        = "/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/apuglia-TT_hadr_v1-00000000000000000000000000000000/USER"
TT_hadr_2024.process        = 'TT_2024'
TT_hadr_2024.unix_code      = 31101
TT_hadr_2024.EE             = 0

TT_2024                     = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_2024")
TT_2024.year                = 2024
TT_2024.components          = [TT_semilep_2024, TT_hadr_2024, TT_dilep_2024]



#############ZJETS#######################

ZJetsToNuNu_HT100to200_2024              = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT100to200_2024")
ZJetsToNuNu_HT100to200_2024.sigma       = 273.7 #pb
ZJetsToNuNu_HT100to200_2024.year        = 2024
ZJetsToNuNu_HT100to200_2024.dataset     = "/Zto2Nu-4Jets_Bin-HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-Zto2Nu_4Jets_HT100to200_v2-00000000000000000000000000000000/USER"
ZJetsToNuNu_HT100to200_2024.process     = 'ZJetsToNuNu_2024'
ZJetsToNuNu_HT100to200_2024.unix_code   = 31200
ZJetsToNuNu_HT100to200_2024.EE          = 0


ZJetsToNuNu_HT200to400_2024             = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT200to400_2024")
ZJetsToNuNu_HT200to400_2024.sigma       = 75.96 #pb
ZJetsToNuNu_HT200to400_2024.year        = 2024
ZJetsToNuNu_HT200to400_2024.dataset     = "/Zto2Nu-4Jets_Bin-HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-Zto2Nu_4Jets_HT200to400_v1-00000000000000000000000000000000/USER"
ZJetsToNuNu_HT200to400_2024.process     = 'ZJetsToNuNu_2024'
ZJetsToNuNu_HT200to400_2024.unix_code   = 31201
ZJetsToNuNu_HT200to400_2024.EE          = 0

ZJetsToNuNu_HT400to800_2024             = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT400to800_2024")
ZJetsToNuNu_HT400to800_2024.sigma       = 13.19 #pb
ZJetsToNuNu_HT400to800_2024.year        = 2024
ZJetsToNuNu_HT400to800_2024.dataset     = "/Zto2Nu-4Jets_Bin-HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-Zto2Nu_4Jets_HT400to800_v1-00000000000000000000000000000000/USER"
ZJetsToNuNu_HT400to800_2024.process     = 'ZJetsToNuNu_2024'
ZJetsToNuNu_HT400to800_2024.unix_code   = 31202
ZJetsToNuNu_HT400to800_2024.EE          = 0

ZJetsToNuNu_HT800to1500_2024            = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT800to1500_2024")
ZJetsToNuNu_HT800to1500_2024.sigma      = 1.364 #pb
ZJetsToNuNu_HT800to1500_2024.year       = 2024
ZJetsToNuNu_HT800to1500_2024.dataset    = "/Zto2Nu-4Jets_Bin-HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-Zto2Nu_4Jets_HT800to1500_v1-00000000000000000000000000000000/USER"
ZJetsToNuNu_HT800to1500_2024.process    = 'ZJetsToNuNu_2024'
ZJetsToNuNu_HT800to1500_2024.unix_code  = 31203
ZJetsToNuNu_HT800to1500_2024.EE         = 0

ZJetsToNuNu_HT1500to2500_2024           = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT1500to2500_2024")
ZJetsToNuNu_HT1500to2500_2024.sigma     = 0.09865 #pb
ZJetsToNuNu_HT1500to2500_2024.year      = 2024
ZJetsToNuNu_HT1500to2500_2024.dataset   = "/Zto2Nu-4Jets_Bin-HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-Zto2Nu_4Jets_HT1500to2500_v1-00000000000000000000000000000000/USER"
ZJetsToNuNu_HT1500to2500_2024.process   = 'ZJetsToNuNu_2024'
ZJetsToNuNu_HT1500to2500_2024.unix_code = 31204
ZJetsToNuNu_HT1500to2500_2024.EE        = 0

ZJetsToNuNu_HT2500_2024                 = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT2500_2024")
ZJetsToNuNu_HT2500_2024.sigma           = 0.006699 #pb
ZJetsToNuNu_HT2500_2024.year            = 2024
ZJetsToNuNu_HT2500_2024.dataset         = "/Zto2Nu-4Jets_Bin-HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-Zto2Nu_4Jets_HT2500_v1-00000000000000000000000000000000/USER"
ZJetsToNuNu_HT2500_2024.process         = 'ZJetsToNuNu_2024'
ZJetsToNuNu_HT2500_2024.unix_code       = 31205
ZJetsToNuNu_HT2500_2024.EE              = 0

ZJetsToNuNu_2024                        = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2024")
ZJetsToNuNu_2024.year                   = 2024
ZJetsToNuNu_2024.components             = [
                                            ZJetsToNuNu_HT100to200_2024,
                                            ZJetsToNuNu_HT200to400_2024,
                                            ZJetsToNuNu_HT400to800_2024,
                                            ZJetsToNuNu_HT800to1500_2024,
                                            ZJetsToNuNu_HT1500to2500_2024,
                                            ZJetsToNuNu_HT2500_2024 
                                            ]


################################ WJets ################################

WtoLNu_4Jets_1J_2024 = sample(ROOT.kRed -7, 1, 1001, 'WtoLNu_4Jets_1J_2024', 'WtoLNu_4Jets_1J_2024')
WtoLNu_4Jets_1J_2024.dataset = "/WtoLNu-4Jets_Bin-1J_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu_4Jets_1J_v1-00000000000000000000000000000000/USER"
WtoLNu_4Jets_1J_2024.sigma = 9141
WtoLNu_4Jets_1J_2024.year = 2024
WtoLNu_4Jets_1J_2024.process = 'WtoLNu_4Jets_2024'
WtoLNu_4Jets_1J_2024.EE = 0

WtoLNu_4Jets_2J_2024 = sample(ROOT.kRed -7, 1, 1001, 'WtoLNu_4Jets_2J_2024', 'WtoLNu_4Jets_2J_2024')
WtoLNu_4Jets_2J_2024.dataset = "/WtoLNu-4Jets_Bin-2J_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu_4Jets_2J_v2-00000000000000000000000000000000/USER"
WtoLNu_4Jets_2J_2024.sigma = 2931
WtoLNu_4Jets_2J_2024.year = 2024
WtoLNu_4Jets_2J_2024.process = 'WtoLNu_4Jets_2024'
WtoLNu_4Jets_2J_2024.EE = 0


WtoLNu_4Jets_3J_2024 = sample(ROOT.kRed -7, 1, 1001, 'WtoLNu_4Jets_3J_2024', 'WtoLNu_4Jets_3J_2024')
WtoLNu_4Jets_3J_2024.dataset = "/WtoLNu-4Jets_Bin-3J_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu_4Jets_3J_v1-00000000000000000000000000000000/USER"
WtoLNu_4Jets_3J_2024.sigma = 864.6
WtoLNu_4Jets_3J_2024.year = 2024
WtoLNu_4Jets_3J_2024.process = 'WtoLNu_4Jets_2024'
WtoLNu_4Jets_3J_2024.EE = 0


WtoLNu_4Jets_4J_2024 = sample(ROOT.kRed -7, 1, 1001, 'WtoLNu_4Jets_4J_2024', 'WtoLNu_4Jets_4J_2024')
WtoLNu_4Jets_4J_2024.dataset = "/WtoLNu-4Jets_Bin-4J_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu_4Jets_4J_v2-00000000000000000000000000000000/USER"
WtoLNu_4Jets_4J_2024.sigma = 417.8
WtoLNu_4Jets_4J_2024.year = 2024
WtoLNu_4Jets_4J_2024.process = 'WtoLNu_4Jets_2024'
WtoLNu_4Jets_4J_2024.EE = 0

WtoLNu_4Jets_2024 = sample(ROOT.kRed -7,1,1001, 'WtoLNu_4Jets_2024', 'WtoLNu_4Jets_2024')
WtoLNu_4Jets_2024.year = 2024
WtoLNu_4Jets_2024.components = [WtoLNu_4Jets_1J_2024, WtoLNu_4Jets_2J_2024, 
                                WtoLNu_4Jets_3J_2024, WtoLNu_4Jets_4J_2024]

################################### QCD ############################


QCD_HT40to70_2024 = sample(ROOT.kAzure-4,1,1001, 'QCD_HT40to70_2024','QCD_HT40to70_2024')
QCD_HT40to70_2024.dataset= "/QCD-4Jets_Bin-HT-40to70_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT40to70_v1-00000000000000000000000000000000/USER"
QCD_HT40to70_2024.sigma = 312* (10**6)	
QCD_HT40to70_2024.year = 2024
QCD_HT40to70_2024.process = 'QCD_2024'
QCD_HT40to70_2024.EE = 0

QCD_HT70to100_2024 = sample(ROOT.kAzure-4,1,1001, 'QCD_HT70to100_2024','QCD_HT70to100_2024')
QCD_HT70to100_2024.dataset= "/QCD-4Jets_Bin-HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT70t0100_v2-00000000000000000000000000000000/USER"
QCD_HT70to100_2024.sigma = 58.5 * (10**6)	
QCD_HT70to100_2024.year = 2024
QCD_HT70to100_2024.process = 'QCD_2024'
QCD_HT70to100_2024.EE = 0


QCD_HT100to200_2024 = sample(ROOT.kAzure-4,1,1001, 'QCD_HT100to200_2024','QCD_HT100to200_2024')
QCD_HT100to200_2024.dataset= "/QCD-4Jets_Bin-HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT100to200_v1-00000000000000000000000000000000/USER"
QCD_HT100to200_2024.sigma = 25.3 * (10**6)
QCD_HT100to200_2024.year = 2024
QCD_HT100to200_2024.process = 'QCD_2024'
QCD_HT100to200_2024.EE = 0

QCD_HT200to400_2024 = sample(ROOT.kAzure-4,1,1001, 'QCD_HT200to400_2024','QCD_HT200to400_2024')
QCD_HT200to400_2024.dataset= "/QCD-4Jets_Bin-HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT200to400_v2-00000000000000000000000000000000/USER"
QCD_HT200to400_2024.sigma = 1.96* (10**6)	
QCD_HT200to400_2024.year = 2024
QCD_HT200to400_2024.process = 'QCD_2024'
QCD_HT200to400_2024.EE = 0

QCD_HT400to600_2024 = sample(ROOT.kAzure-4,1,1001, 'QCD_HT400to600_2024','QCD_HT400to600_2024')
QCD_HT400to600_2024.dataset= "/QCD-4Jets_Bin-HT-400to600_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT400to600_v2-00000000000000000000000000000000/USER"
QCD_HT400to600_2024.sigma =97400	
QCD_HT400to600_2024.year = 2024
QCD_HT400to600_2024.process = 'QCD_2024'
QCD_HT400to600_2024.EE = 0

QCD_HT600to800_2024 = sample(ROOT.kAzure-4,1,1001, 'QCD_HT600to800_2024','QCD_HT600to800_2024')
QCD_HT600to800_2024.dataset= "/QCD-4Jets_Bin-HT-600to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT600to800_v2-00000000000000000000000000000000/USER"
QCD_HT600to800_2024.sigma = 13560	
QCD_HT600to800_2024.year = 2024
QCD_HT600to800_2024.process = 'QCD_2024'
QCD_HT600to800_2024.EE = 0

QCD_HT800to1000_2024 = sample(ROOT.kAzure-4,1,1001, 'QCD_HT800to1000_2024','QCD_HT800to1000_2024')
QCD_HT800to1000_2024.dataset= "/QCD-4Jets_Bin-HT-800to1000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT800to1000_v1-00000000000000000000000000000000/USER"
QCD_HT800to1000_2024.sigma = 3010	
QCD_HT800to1000_2024.year = 2024
QCD_HT800to1000_2024.process = 'QCD_2024'
QCD_HT800to1000_2024.EE = 0

QCD_HT1000to1200_2024 = sample(ROOT.kAzure-4,1,1001, 'QCD_HT1000to1200_2024','QCD_HT1000to1200_2024')
QCD_HT1000to1200_2024.dataset= "/QCD-4Jets_Bin-HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT1000to1200_v2-00000000000000000000000000000000/USER"
QCD_HT1000to1200_2024.sigma = 890.3	
QCD_HT1000to1200_2024.year = 2024
QCD_HT1000to1200_2024.process = 'QCD_2024'
QCD_HT1000to1200_2024.EE = 0

QCD_HT1200to1500_2024 = sample(ROOT.kAzure-4,1,1001, 'QCD_HT1200to1500_2024','QCD_HT1200to1500_2024')
QCD_HT1200to1500_2024.dataset= "/QCD-4Jets_Bin-HT-1200to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT1200to1500_v2-00000000000000000000000000000000/USER"
QCD_HT1200to1500_2024.sigma = 384.8	
QCD_HT1200to1500_2024.year = 2024
QCD_HT1200to1500_2024.process = 'QCD_2024'
QCD_HT1200to1500_2024.EE = 0

QCD_HT1500to2000_2024 = sample(ROOT.kAzure-4,1,1001, 'QCD_HT1500to2000_2024','QCD_HT1500to2000_2024')
QCD_HT1500to2000_2024.dataset= "/QCD-4Jets_Bin-HT-1500to2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT1500to2000_v2-00000000000000000000000000000000/USER"
QCD_HT1500to2000_2024.sigma = 384.8	
QCD_HT1500to2000_2024.year = 2024
QCD_HT1500to2000_2024.process = 'QCD_2024'
QCD_HT1500to2000_2024.EE = 0

QCD_HT2000_2024 = sample(ROOT.kAzure-4,1,1001, 'QCD_HT2000_2024','QCD_HT2000_2024')
QCD_HT2000_2024.dataset= "/QCD-4Jets_Bin-HT-2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT2000_v1-00000000000000000000000000000000/USER"
QCD_HT2000_2024.sigma = 26.26
QCD_HT2000_2024.year = 2024
QCD_HT2000_2024.process = 'QCD_2024'
QCD_HT2000_2024.EE = 0

QCD_2024 = sample(ROOT.kAzure-4,1,1001, 'QCD_2024', 'QCD_2024')
QCD_2024.year = 2024
QCD_2024.components = [QCD_HT40to70_2024, QCD_HT70to100_2024, QCD_HT100to200_2024, QCD_HT200to400_2024, 
                        QCD_HT400to600_2024, QCD_HT600to800_2024, QCD_HT800to1000_2024, QCD_HT1000to1200_2024, 
                        QCD_HT1200to1500_2024, QCD_HT1500to2000_2024, QCD_HT2000_2024]


############## T W ##############

Top_W_minus_4Q_2024 = sample(ROOT.kYellow,1,1001,'TW_2024', 'Top_W_minus_4Q_2024' )
Top_W_minus_4Q_2024.dataset = "/TWminusto4Q_TuneCP5_13p6TeV_powheg-pythia8/apuglia-Top_W_minus_4Q_2024_v1-00000000000000000000000000000000/USER"
Top_W_minus_4Q_2024.sigma = 36
Top_W_minus_4Q_2024.year = 2024
Top_W_minus_4Q_2024.process = 'TW_2024'
Top_W_minus_4Q_2024.EE = 0

Top_W_minus_LNu2Q_2024 = sample(ROOT.kYellow, 1,1001, 'TW_2024', 'Top_W_minus_LNu2Q_2024')
Top_W_minus_LNu2Q_2024.dataset = "/TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/apuglia-Top_W_minus_LNu2Q_v1-00000000000000000000000000000000/USER"
Top_W_minus_LNu2Q_2024.sigma = 36
Top_W_minus_LNu2Q_2024.year = 2024
Top_W_minus_LNu2Q_2024.process = "TW_2024"
Top_W_minus_LNu2Q_2024.EE = 0

Top_W_minus_2L2Nu_2024 = sample(ROOT.kYellow, 1, 1001  , 'TW_2024', 'Top_W_minus_2L2Nu_2024')
Top_W_minus_2L2Nu_2024.dataset = "/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/apuglia-Top_W_minus_2L2Nu_v1-00000000000000000000000000000000/USER"
Top_W_minus_2L2Nu_2024.sigma = 36
Top_W_minus_2L2Nu_2024.year = 2024
Top_W_minus_2L2Nu_2024.process = "TW_2024"
Top_W_minus_2L2Nu_2024.EE = 0

Top_W_plus_2L2Nu_2024 = sample(ROOT.kYellow, 1, 1001, 'TW_2024', 'Top_W_plus_2L2Nu_2024')
Top_W_plus_2L2Nu_2024.dataset = "/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/apuglia-Top_W_plus_2L2Nu_v1-00000000000000000000000000000000/USER"
Top_W_plus_2L2Nu_2024.sigma = 36
Top_W_plus_2L2Nu_2024.year = 2024
Top_W_plus_2L2Nu_2024.process = "TW_2024"
Top_W_plus_2L2Nu_2024.EE = 0

Top_W_plus_LNu2Q_2024 = sample(ROOT.kYellow, 1, 1001, 'TW_2024', 'Top_W_plus_LNu2Q_2024')
Top_W_plus_LNu2Q_2024.dataset = "/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/apuglia-Top_W_plus_LNu2Q_v1-00000000000000000000000000000000/USER"
Top_W_plus_LNu2Q_2024.sigma = 36
Top_W_plus_LNu2Q_2024.year = 2024
Top_W_plus_LNu2Q_2024.process = "TW_2024"
Top_W_plus_LNu2Q_2024.EE = 0

Top_W_plus_4Q_2024 = sample(ROOT.kYellow, 1, 1001, 'TW_2024', 'Top_W_plus_4Q_2024')
Top_W_plus_4Q_2024.dataset= "/TbarWplusto4Q_TuneCP5_13p6TeV_powheg-pythia8/apuglia-Top_W_plus_4Q_v1-00000000000000000000000000000000/USER"
Top_W_plus_4Q_2024.sigma = 36
Top_W_plus_4Q_2024.year = 2024
Top_W_plus_4Q_2024.process = "TW_2024"
Top_W_plus_4Q_2024.EE = 0


TW_2024 = sample(ROOT.kAzure-4,1,1001, 'TW_2024', 'TW_2024')
TW_2024.year = 2024
TW_2024.components = [Top_W_minus_2L2Nu_2024, Top_W_minus_4Q_2024, Top_W_minus_LNu2Q_2024, 
                        Top_W_plus_2L2Nu_2024, Top_W_plus_4Q_2024, Top_W_plus_LNu2Q_2024]





sample_dict = {


    #######################################
    ############# RUN III ################
    #######################################

    #####################2022
    ############ QCD
    'QCD_2022' : QCD_2022,
    # "QCD_HT40to70_2022": QCD_HT40to70_2022, 
    "QCD_HT70to100_2022": QCD_HT70to100_2022, 
    "QCD_HT100to200_2022": QCD_HT100to200_2022, "QCD_HT200to400_2022": QCD_HT200to400_2022, 
    "QCD_HT400to600_2022": QCD_HT400to600_2022, "QCD_HT600to800_2022": QCD_HT600to800_2022, 
    "QCD_HT800to1000_2022": QCD_HT800to1000_2022, "QCD_HT1000to1200_2022": QCD_HT1000to1200_2022, 
    "QCD_HT1200to1500_2022": QCD_HT1200to1500_2022, "QCD_HT1500to2000_2022": QCD_HT1500to2000_2022, "QCD_HT2000_2022": QCD_HT2000_2022,
    ########### TT
    'TT_2022': TT_2022, 'TT_semilep_2022' : TT_semilep_2022, 'TT_hadr_2022' : TT_hadr_2022, 'TT_dilep_2022' : TT_dilep_2022,
    ########## SingleTop

    ########## WJets
    "WJets_2jets_2022": WJets_2jets_2022, 
    "WJets_2jets0J_2022": WJets_2jets0J_2022, "WJets_2jets1J_2022": WJets_2jets1J_2022, "WJets_2jets2J_2022": WJets_2jets2J_2022,

    "WJets_2022":WJets_2022, 
    "WJets_HT120to200_2022":WJets_HT120to200_2022, "WJets_HT200to400_2022":WJets_HT200to400_2022, 
    "WJets_HT400to800_2022":WJets_HT400to800_2022, "WJets_HT800to1500_2022":WJets_HT800to1500_2022, 
    "WJets_HT1500to2500_2022":WJets_HT1500to2500_2022, "WJets_HT2500to4000_2022":WJets_HT2500to4000_2022, 
    "WJets_HT4000to6000_2022":WJets_HT4000to6000_2022, "WJets_HT6000_2022":WJets_HT6000_2022,
    ########## ZJetsToNuNu
    "ZJetsToNuNu_2022":ZJetsToNuNu_2022, "ZJetsToNuNu_HT100to200_2022":ZJetsToNuNu_HT100to200_2022, 
    "ZJetsToNuNu_HT200to400_2022":ZJetsToNuNu_HT200to400_2022, "ZJetsToNuNu_HT400to800_2022":ZJetsToNuNu_HT400to800_2022, 
    "ZJetsToNuNu_HT800to1500_2022":ZJetsToNuNu_HT800to1500_2022, "ZJetsToNuNu_HT1500to2500_2022":ZJetsToNuNu_HT1500to2500_2022, 
    "ZJetsToNuNu_HT2500_2022":ZJetsToNuNu_HT2500_2022,

    "ZJetsToNuNu_2jets_2022":ZJetsToNuNu_2jets_2022,
    "ZJetsToNuNu_2jets_PT40to100_1J_2022":ZJetsToNuNu_2jets_PT40to100_1J_2022, "ZJetsToNuNu_2jets_PT100to200_1J_2022":ZJetsToNuNu_2jets_PT100to200_1J_2022,
    "ZJetsToNuNu_2jets_PT200to400_1J_2022":ZJetsToNuNu_2jets_PT200to400_1J_2022, "ZJetsToNuNu_2jets_PT400to600_1J_2022":ZJetsToNuNu_2jets_PT400to600_1J_2022,
    "ZJetsToNuNu_2jets_PT600_1J_2022":ZJetsToNuNu_2jets_PT600_1J_2022, "ZJetsToNuNu_2jets_PT40to100_2J_2022":ZJetsToNuNu_2jets_PT40to100_2J_2022,
    "ZJetsToNuNu_2jets_PT100to200_2J_2022":ZJetsToNuNu_2jets_PT100to200_2J_2022, "ZJetsToNuNu_2jets_PT200to400_2J_2022":ZJetsToNuNu_2jets_PT200to400_2J_2022,
    "ZJetsToNuNu_2jets_PT400to600_2J_2022":ZJetsToNuNu_2jets_PT400to600_2J_2022, "ZJetsToNuNu_2jets_PT600_2J_2022":ZJetsToNuNu_2jets_PT600_2J_2022,
                                    
    ########## SIGNALS tDM or Tprime
    "TprimeToTZ_700_2022":TprimeToTZ_700_2022,
    "TprimeToTZ_800_2022":TprimeToTZ_800_2022,
    "TprimeToTZ_900_2022":TprimeToTZ_900_2022,
    "TprimeToTZ_1000_2022":TprimeToTZ_1000_2022,
    "TprimeToTZ_1100_2022":TprimeToTZ_1100_2022,
    "TprimeToTZ_1200_2022":TprimeToTZ_1200_2022,
    "TprimeToTZ_1300_2022":TprimeToTZ_1300_2022,
    "TprimeToTZ_1400_2022":TprimeToTZ_1400_2022,
    "TprimeToTZ_1500_2022":TprimeToTZ_1500_2022,
    "TprimeToTZ_1600_2022":TprimeToTZ_1600_2022,
    "TprimeToTZ_1700_2022":TprimeToTZ_1700_2022,
    "TprimeToTZ_1800_2022":TprimeToTZ_1800_2022,

    "DataMuon_2022":DataMuon_2022, "DataMuonC_2022":DataMuonC_2022, 

    ################2024##############
    "TT_2024": TT_2024, 
    "TT_dilep_2024": TT_dilep_2024, "TT_hadr_2024": TT_hadr_2024, "TT_semilep_2024": TT_semilep_2024, 

    "QCD_2024": QCD_2024, 
    "QCD_HT40to70_2024": QCD_HT40to70_2024, "QCD_HT70to100_2024": QCD_HT70to100_2024, "QCD_HT100to200_2024": QCD_HT100to200_2024, 
    "QCD_HT200to400_2024": QCD_HT200to400_2024, "QCD_HT400to600_2024": QCD_HT400to600_2024, "QCD_HT600to800_2024": QCD_HT600to800_2024, 
    "QCD_HT800to1000_2024": QCD_HT800to1000_2024, "QCD_HT1000to1200_2024":QCD_HT1000to1200_2024, "QCD_HT1200to1500_2024": QCD_HT1200to1500_2024, 
    "QCD_HT1500to2000_2024": QCD_HT1500to2000_2024, "QCD_HT2000_2024": QCD_HT2000_2024, 

    "TW_2024": TW_2024, 
    "Top_W_plus_4Q_2024": Top_W_plus_4Q_2024, "Top_W_plus_LNu2Q_2024": Top_W_plus_LNu2Q_2024, "Top_W_plus_2L2Nu_2024": Top_W_plus_2L2Nu_2024, 
    "Top_W_minus_4Q_2024": Top_W_minus_4Q_2024, "Top_W_minus_LNu2Q_2024": Top_W_minus_LNu2Q_2024, "Top_W_minus_2L2Nu_2024": Top_W_minus_2L2Nu_2024, 

    "WtoLNu_4Jets_2024": WtoLNu_4Jets_2024, 
    "WtoLNu_4Jets_1J_2024": WtoLNu_4Jets_1J_2024, "WtoLNu_4Jets_2J_2024": WtoLNu_4Jets_2J_2024, "WtoLNu_4Jets_3J_2024":WtoLNu_4Jets_3J_2024, "WtoLNu_4Jets_4J_2024": WtoLNu_4Jets_4J_2024, 

    "ZJetsToNuNu_2024": ZJetsToNuNu_2024, 
    "ZJetsToNuNu_HT100to200_2024": ZJetsToNuNu_HT100to200_2024, "ZJetsToNuNu_HT200to400_2024":ZJetsToNuNu_HT200to400_2024, "ZJetsToNuNu_HT400to800_2024":ZJetsToNuNu_HT400to800_2024, 
    "ZJetsToNuNu_HT800to1500_2024": ZJetsToNuNu_HT800to1500_2024, "ZJetsToNuNu_HT1500to2500_2024": ZJetsToNuNu_HT1500to2500_2024, "ZJetsToNuNu_HT2500_2024": ZJetsToNuNu_HT2500_2024



    }
