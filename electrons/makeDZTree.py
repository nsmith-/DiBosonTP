import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys

process = cms.Process("tnp")

options = VarParsing('analysis')
options.register(
    "isMC",
    True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Compute MC efficiencies"
    )

options.parseArguments()

jsonFile = 'Cert_246908-258714_13TeV_PromptReco_Collisions15_25ns_JSON.txt'

# file dataset=/DoubleEG/Run2015D-05Oct2015-v1/MINIAOD
# https://cmsweb.cern.ch/das/request?view=plain&limit=50&instance=prod%2Fglobal&input=file+dataset%3D%2FDoubleEG%2FRun2015D-05Oct2015-v1%2FMINIAOD
inputFilesData = [
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0014E86F-656F-E511-9D3F-002618943831.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/008CB82F-5D6F-E511-8510-0025905A6090.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/00916A9B-586F-E511-A8F3-002618943800.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0205BAFD-676F-E511-BC7E-0025905A6090.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/02F0DA71-656F-E511-A190-0025905A6136.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/04108B2F-5D6F-E511-9EA3-0025905A4964.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/044F07FF-5E6F-E511-9A8F-00261894390A.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/045AB872-616F-E511-9600-002590596498.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/047AD13A-5B6F-E511-9DCA-0025905A60D0.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/04BF2B2E-696F-E511-BAEB-0025905964A2.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/04CBDB6E-676F-E511-8C2A-002618943976.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0624465C-696F-E511-8C25-003048FFD7BE.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0646060F-3E6F-E511-889C-0025905A6056.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0653CEAC-6B6F-E511-AB15-0025905B8562.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/06DE7E7F-626F-E511-8D21-0025905A605E.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0A460A09-5F6F-E511-AC3B-0025905AA9CC.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0A59D172-616F-E511-9AEE-0025905A6094.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0C13DAAD-6B6F-E511-A9BB-003048FFD7BE.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0C334B2C-486F-E511-B934-0025905A612E.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0E070724-4B6F-E511-9DD5-0026189438CB.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0E13332F-5D6F-E511-96FB-0025905A6110.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0E4F000B-506F-E511-B2E7-002354EF3BE0.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0E581F29-4B6F-E511-957B-0025905B860E.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/0EA5C521-4B6F-E511-A85A-002618943910.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/10184534-5D6F-E511-BF57-0025905B857C.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1038FA0F-3E6F-E511-818C-0025905A6092.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1050CF29-4B6F-E511-9A8F-0025905B860C.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/10ABEC0E-3E6F-E511-A21E-0025905A6056.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1209BE0F-3E6F-E511-BE39-0025905A6092.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1226FCE0-526F-E511-A750-002618943838.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/14DCB7AB-556F-E511-85A9-003048FFD752.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/14E46374-656F-E511-830E-003048FFD728.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/16151D31-5D6F-E511-B62A-002618943919.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/162D6A06-5F6F-E511-912F-0025905938D4.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1672749F-586F-E511-9B99-0025905A60A8.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/16D6ACB0-556F-E511-85EE-0025905938A8.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/18138C38-416F-E511-8D3B-002590596498.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/18515E93-626F-E511-9FF4-0025905A60C6.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1A943E58-696F-E511-B719-0025905A608C.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1AA86802-636F-E511-B13C-0025905B8592.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1C001373-616F-E511-A8AB-0025905A60E0.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1C63338F-626F-E511-8BB3-00248C65A3EC.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1C6B160F-3E6F-E511-973C-0025905A6056.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1C83B76F-656F-E511-BF96-002590593902.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1C9276D2-526F-E511-B8EE-0025905A611E.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1CEF51CB-446F-E511-9C95-002590596484.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1CFCEDF9-676F-E511-B3F7-002618943829.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1CFF8EAE-556F-E511-B33B-0025905A60FE.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1E0F3C45-696F-E511-B21D-0025905A609E.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1E97F138-5B6F-E511-91EF-0025905A60D2.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1EC6DBCC-446F-E511-AA6A-003048FF86CA.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/1EF2FB2C-486F-E511-9F35-0025905A609E.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/2002D9A6-526F-E511-8A0F-002618943918.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/202791CD-446F-E511-B96E-0025905A6118.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/20656C26-4B6F-E511-8F0F-0025905A6088.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/2088FA0E-3E6F-E511-98A2-0025905A6056.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/20B43013-506F-E511-ADD7-0025905A606A.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/20CAD9A8-556F-E511-A4C2-002618943910.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/22C0F6CC-626F-E511-8E7C-002618943845.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/2441CC45-696F-E511-AE72-002618943959.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/248C7CCE-446F-E511-B566-0025905A60F2.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/24ABFBC5-4F6F-E511-80F3-0026189437E8.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/24F877A3-586F-E511-AD67-0025905B85D0.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/26036627-486F-E511-A8EB-002618943829.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/2630BC65-636F-E511-9387-0025905964BC.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/2675AB35-416F-E511-93B2-0025905A6082.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/267DD26E-656F-E511-88A8-0026189438D5.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/26ED4FAD-6B6F-E511-A2A4-0025905A60A6.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/28BE9D34-416F-E511-9DF3-0025905B85AE.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/2A218B2F-5D6F-E511-B481-0025905A4964.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/2A8471CC-446F-E511-AF72-002590596498.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/2A979483-6B6F-E511-8677-003048FFD7BE.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/2E04DB72-656F-E511-874F-0025905A60A6.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/2E1223CA-446F-E511-818F-0025905A612E.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/3059362E-486F-E511-B44B-0025905964A2.root',
        '/store/data/Run2015D/DoubleEG/MINIAOD/05Oct2015-v1/50000/30754D83-656F-E511-BCED-003048FFD7BE.root',
]

# file dataset=/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM
# https://cmsweb.cern.ch/das/request?view=plain&limit=50&instance=prod%2Fglobal&input=file+dataset%3D%2FDYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8%2FRunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3%2FMINIAODSIM
inputFilesMC = [
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/009D49A5-7314-E511-84EF-0025905A605E.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/00C0BECF-6F14-E511-96F8-0025904B739A.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/0260F225-7614-E511-A79F-00A0D1EE8EB4.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/02B810EA-7214-E511-BDAB-0025905964C2.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/02CEA7DD-7714-E511-A93E-00266CFAEA68.root',
]

if len(options.inputFiles) is 0 :
    if options.isMC :
        options.inputFiles = inputFilesMC
    else :
        options.inputFiles = inputFilesData


from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.hltFilter = hltHighLevel.clone()
process.hltFilter.throw = cms.bool(True)
process.hltFilter.HLTPaths = cms.vstring('HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_v*')

process.goodElectrons = cms.EDFilter("PATElectronRefSelector",
                                     src = cms.InputTag("slimmedElectrons"),
                                     cut = cms.string("abs(eta)<2.5 && pt > 10"),
                                     filter = cms.bool(True)
                                     )

process.eleVarHelper = cms.EDProducer("ElectronVariableHelper",
                                      probes = cms.InputTag("slimmedElectrons"),
                                      vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices")
                                      )

process.goodElectronsTagEle17 = cms.EDProducer("PatElectronTriggerCandProducer",
                                             filterNames = cms.vstring("hltEle17Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg1Filter"),
                                             inputs      = cms.InputTag("goodElectrons"),
                                             bits        = cms.InputTag('TriggerResults::HLT'),
                                             objects     = cms.InputTag('selectedPatTrigger'),
                                             dR          = cms.double(0.3),
                                             isAND       = cms.bool(True)
                                             )

process.goodElectronsProbeEle12 = cms.EDProducer("PatElectronTriggerCandProducer",
                                                filterNames = cms.vstring("hltEle17Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg2Filter"),
                                               inputs      = cms.InputTag("goodElectrons"),
                                               bits        = cms.InputTag('TriggerResults::HLT'),
                                               objects     = cms.InputTag('selectedPatTrigger'),
                                               dR          = cms.double(0.3),
                                               isAND       = cms.bool(True)
                                               )

process.goodElectronsMeasureDZ = cms.EDProducer("PatElectronTriggerCandProducer",
                                               filterNames = cms.vstring("hltEle17Ele12CaloIdLTrackIdLIsoVLDZFilter"),
                                               inputs      = cms.InputTag("goodElectronsProbeEle12"),
                                               bits        = cms.InputTag('TriggerResults::HLT'),
                                               objects     = cms.InputTag('selectedPatTrigger'),
                                               dR          = cms.double(0.3),
                                               isAND       = cms.bool(True)
                                               )

###################################################################
## TnP PAIRS
###################################################################
    
process.tagTightHLT = cms.EDProducer("CandViewShallowCloneCombiner",
                                     decay = cms.string("goodElectronsTagEle17@+ goodElectronsProbeEle12@-"), 
                                     checkCharge = cms.bool(True),
                                     cut = cms.string("40<mass<1000"),
                                     )

##########################################################################
## TREE CONTENT
#########################################################################
    
ZVariablesToStore = cms.PSet(
    eta = cms.string("eta"),
    abseta = cms.string("abs(eta)"),
    pt  = cms.string("pt"),
    mass  = cms.string("mass"),
    )   

ProbeVariablesToStore = cms.PSet(
    probe_Ele_eta    = cms.string("eta"),
    probe_Ele_abseta = cms.string("abs(eta)"),
    probe_Ele_pt     = cms.string("pt"),
    probe_Ele_et     = cms.string("et"),
    probe_Ele_e      = cms.string("energy"),
    probe_Ele_q      = cms.string("charge"),
    
    ## super cluster quantities
    probe_sc_energy = cms.string("superCluster.energy"),
    probe_sc_et     = cms.string("superCluster.energy*sin(superClusterPosition.theta)"),    
    probe_sc_eta    = cms.string("superCluster.eta"),
    probe_sc_abseta = cms.string("abs(superCluster.eta)"),
    
    #id based
    probe_Ele_dEtaIn        = cms.string("deltaEtaSuperClusterTrackAtVtx"),
    probe_Ele_dPhiIn        = cms.string("deltaPhiSuperClusterTrackAtVtx"),
    probe_Ele_sigmaIEtaIEta = cms.string("sigmaIetaIeta"),
    probe_Ele_hoe           = cms.string("hadronicOverEm"),
    probe_Ele_ooemoop       = cms.string("(1.0/ecalEnergy - eSuperClusterOverP/ecalEnergy)"),
    probe_Ele_mHits         = cms.InputTag("eleVarHelper:missinghits"),
    probe_Ele_dz            = cms.InputTag("eleVarHelper:dz"),
    probe_Ele_dxy           = cms.InputTag("eleVarHelper:dxy"),
    
    #isolation
    probe_Ele_chIso         = cms.string("pfIsolationVariables().sumChargedHadronPt"),
    probe_Ele_phoIso        = cms.string("pfIsolationVariables().sumPhotonEt"),
    probe_Ele_neuIso        = cms.string("pfIsolationVariables().sumNeutralHadronEt"),
    )

TagVariablesToStore = cms.PSet(
    Ele_eta    = cms.string("eta"),
    Ele_abseta = cms.string("abs(eta)"),
    Ele_pt     = cms.string("pt"),
    Ele_et     = cms.string("et"),
    Ele_e      = cms.string("energy"),
    Ele_q      = cms.string("charge"),
    
    ## super cluster quantities
    sc_energy = cms.string("superCluster.energy"),
    sc_et     = cms.string("superCluster.energy*sin(superClusterPosition.theta)"),    
    sc_eta    = cms.string("superCluster.eta"),
    sc_abseta = cms.string("abs(superCluster.eta)"),
    )

CommonStuffForGsfElectronProbe = cms.PSet(
    variables = cms.PSet(ProbeVariablesToStore),
    ignoreExceptions =  cms.bool (False),
    addRunLumiInfo   =  cms.bool (True),
    addEventVariablesInfo   =  cms.bool(True),
    vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    #pfMet = cms.InputTag(""),
    pairVariables =  cms.PSet(ZVariablesToStore),
    pairFlags     =  cms.PSet(
        mass60to120 = cms.string("60 < mass < 120")
        ),
    tagVariables   =  cms.PSet(TagVariablesToStore),
    tagFlags       =  cms.PSet(),    
    )

process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = 'GR_P_V56'

process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(options.inputFiles),
                            )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents))

if not options.isMC :
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/'+jsonFile).getVLuminosityBlockRange()

##########################################################################
## TREE MAKER OPTIONS
##########################################################################

mcTruthCommonStuff = cms.PSet(
    isMC = cms.bool(True),
    tagMatches = cms.InputTag("McMatchHLT"),
    motherPdgId = cms.vint32(22,23),
    #motherPdgId = cms.vint32(443), # JPsi
    #motherPdgId = cms.vint32(553), # Yupsilon
    makeMCUnbiasTree = cms.bool(False),
    checkMotherInUnbiasEff = cms.bool(False),
    mcVariables = cms.PSet(
        probe_eta = cms.string("eta"),
        probe_abseta = cms.string("abs(eta)"),
        probe_et  = cms.string("et"),
        probe_e  = cms.string("energy"),
        ),
    mcFlags     =  cms.PSet(
        probe_flag = cms.string("pt>0")
        ),      
    )

if (not options.isMC):
    mcTruthCommonStuff = cms.PSet(
        isMC = cms.bool(False)
        )

process.GsfElectronToTrigger = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                              CommonStuffForGsfElectronProbe, mcTruthCommonStuff,
                                              tagProbePairs = cms.InputTag("tagTightHLT"),
                                              arbitration   = cms.string("BestMass"),
                                              massForArbitration = cms.double(91.),
                                              flags         = cms.PSet(
                                                  passingHLTDZFilter    = cms.InputTag("goodElectronsMeasureDZ")
                                              ),
                                              allProbes     = cms.InputTag("goodElectronsProbeEle12"),
                                              )

##########################################################################
## MC stuff
##########################################################################

process.McMatchHLT = cms.EDProducer("MCTruthDeltaRMatcherNew",
                                    matchPDGId = cms.vint32(11),
                                    src = cms.InputTag("goodElectrons"),
                                    distMin = cms.double(0.3),
                                    matched = cms.InputTag("prunedGenParticles"),
                                    checkCharge = cms.bool(True)
                                    )

process.pileupReweightingProducer = cms.EDProducer("PileupWeightProducer",
    hardcodedWeights = cms.untracked.bool(False),
    PileupMCFile = cms.string('../data/puWeightMC.root'),
    PileupDataFile = cms.string('../data/puWeightData.root'),
                                                   )

process.mc_sequence = cms.Sequence()
if (options.isMC):
    process.GsfElectronToTrigger.probeMatches  = cms.InputTag("McMatchHLT")
    process.GsfElectronToTrigger.eventWeight   = cms.InputTag("generator")
    process.GsfElectronToTrigger.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")
    process.mc_sequence *= (process.McMatchHLT+process.pileupReweightingProducer)

process.p = cms.Path(
    process.hltFilter +
    process.goodElectrons + 
    process.goodElectronsTagEle17 +
    process.goodElectronsProbeEle12 +
    process.goodElectronsMeasureDZ +
    process.tagTightHLT +
    process.eleVarHelper +
    process.mc_sequence +
    process.GsfElectronToTrigger
    )

process.TFileService = cms.Service(
    "TFileService", 
    fileName = cms.string(options.outputFile),
    closeFileFast = cms.untracked.bool(True)
)

process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string('debug.root'),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
                               )
#process.outpath = cms.EndPath(process.out)
