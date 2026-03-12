import ROOT

class sample:
    def __init__(self, color, style, fill, leglabel, label):
        self.color = color
        self.style = style
        self.fill = fill
        self.leglabel = leglabel
        self.label = label



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