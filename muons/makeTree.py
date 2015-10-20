import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

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

isolationDef = "(chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/pt"
config = {}
config['MUON_COLL']           = "slimmedMuons"
config['MUON_CUTS']           = "(isTrackerMuon || isGlobalMuon) && abs(eta)<2.5 && pt > 10"
config['MUON_TAG_CUTS']       = "userInt('isTightMuon')==1 && pt > 25 && abs(eta) < 2.1 && "+isolationDef+" < 0.2"
config['MUON_TAG_TRIGGER']    = "hltL3crIsoL1sMu16L1f0L2f10QL3f20QL3trkIsoFiltered0p09"
config['DEBUG']               = cms.bool(False)
config['json']                = 'Cert_246908-258714_13TeV_PromptReco_Collisions15_25ns_JSON.txt'

# file dataset=/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD
# https://cmsweb.cern.ch/das/request?view=plain&limit=50&instance=prod%2Fglobal&input=file+dataset%3D%2FSingleMuon%2FRun2015D-05Oct2015-v1%2FMINIAOD
inputFilesData = [
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/DAF6F553-986F-E511-AB07-002618943982.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/DC242338-986F-E511-9196-00261894394B.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/DC4D3D93-906F-E511-BEAD-0026189438F9.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/DC90BDAC-906F-E511-ACBF-0025905938A8.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/DCCC9257-986F-E511-BB7A-003048FFCB8C.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/E0121BCE-906F-E511-964C-002354EF3BDD.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/E092C9F3-966F-E511-8314-003048FFCB9E.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/E20DC50B-936F-E511-9FB9-002618943962.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/E2B6D0D7-9E6F-E511-8808-0025905A60D2.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/E63965DC-A16F-E511-8845-003048FFD736.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/E8046B0E-9D6F-E511-B09E-0025905A60D2.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/E81B4EFB-976F-E511-A665-0025905A48EC.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/E83FAC73-9D6F-E511-A7AD-0025905A6080.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/E8CB40ED-996F-E511-A5C3-0025905A48EC.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/EC1E6D88-9E6F-E511-8F9C-0025905A6080.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/EC1FE156-9C6F-E511-AC11-00261894383B.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/EC91E4F2-9E6F-E511-8B3C-003048FFD730.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/EC945EAB-A06F-E511-ABAD-002354EF3BDD.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/EE5FE055-9D6F-E511-9B16-0025905A613C.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/EE8A1182-976F-E511-B1B2-0025905A611E.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/F2C37BE7-8F6F-E511-91FE-002618943973.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/F6A07DB9-9E6F-E511-AECB-0026189438B3.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/F8922872-926F-E511-92F5-0025905A606A.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/F8A8CEE8-966F-E511-8311-00261894390A.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/FAAD4F35-956F-E511-9F79-002618943900.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/FCAE7710-9E6F-E511-B43F-0025905A60D2.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/FCEFB068-A36F-E511-B0A1-003048FFCC2C.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/FEF2AD81-A16F-E511-B910-002354EF3BDB.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/FEFEF356-986F-E511-BA44-0025905B85E8.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/023BE7DE-696F-E511-B0D3-0025905B85D6.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/02A89057-676F-E511-9068-0025905A606A.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/06245BED-686F-E511-B5D5-002354EF3BE3.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/0EF9F1DC-696F-E511-A093-0025905B860C.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/101EEA20-666F-E511-A5E4-0025905A606A.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/14AB3226-696F-E511-A9C7-0025905A608C.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/1A9D93F6-676F-E511-AE0F-00261894390A.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/1C3EA8D3-696F-E511-B566-00248C65A3EC.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/1E142BFD-676F-E511-84B7-0025905A48D0.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/20C4FDFF-676F-E511-8E9F-00248C65A3EC.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/24A2D2D8-696F-E511-9D59-0025905A60C6.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/261E13E4-686F-E511-AD73-00248C65A3EC.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/264094DB-696F-E511-B3DA-003048FFD730.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/365A08D9-696F-E511-BEB9-0025905A605E.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/3E0456D9-696F-E511-8EF5-0025905A60BC.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/3E2A6421-666F-E511-8CF1-0025905A60F4.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/3E76821E-686F-E511-8018-0025905A608C.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/3EEABCC4-686F-E511-80A5-002618943951.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/40000/405EBCDA-696F-E511-81B3-0025905A608C.root',
]

# file dataset=/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM
# https://cmsweb.cern.ch/das/request?view=plain&limit=50&instance=prod%2Fglobal&input=file+dataset%3D%2FDYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8%2FRunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3%2FMINIAODSIM
inputFilesMC = [
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/009D49A5-7314-E511-84EF-0025905A605E.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/00C0BECF-6F14-E511-96F8-0025904B739A.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/0260F225-7614-E511-A79F-00A0D1EE8EB4.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/02B810EA-7214-E511-BDAB-0025905964C2.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/02CEA7DD-7714-E511-A93E-00266CFAEA68.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/0453351C-7014-E511-A296-0025905B85AA.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/0679BC6F-7714-E511-945E-0025905B8562.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/0823BF6F-7814-E511-8E48-00A0D1EE8B08.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/08271551-9714-E511-B209-0025907FD2DA.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/08D8E2DA-7014-E511-8875-002590593872.root',
]

if len(options.inputFiles) is 0 :
    if options.isMC :
        options.inputFiles = inputFilesMC
    else :
        options.inputFiles = inputFilesData

if options.isMC :
    config['outputFile'] = 'TnPTree_mc.root'
else :
    config['outputFile'] = 'TnPTree_data.root'

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    )

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.tightMuons = cms.EDProducer("stupidTightMuonProducer",
    src = cms.InputTag("slimmedMuons"),
    vtx = cms.InputTag("offlineSlimmedPrimaryVertices")
)

process.tagMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("tightMuons"),
    cut = cms.string(config['MUON_TAG_CUTS']),
    filter = cms.bool(True)
)

process.tagMuonsTriggerMatched = cms.EDProducer("PatMuonTriggerCandProducer",
    filterNames = cms.vstring(config['MUON_TAG_TRIGGER']),
    inputs      = cms.InputTag("tagMuons"),
    bits        = cms.InputTag('TriggerResults::HLT'),
    objects     = cms.InputTag('selectedPatTrigger'),
    dR          = cms.double(0.4),
    isAND       = cms.bool(True)
    )

process.probeMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("tightMuons"),
    cut = cms.string(config['MUON_CUTS']), 
)

########### Probe Triggers ###############

process.probeTriggerSeq = cms.Sequence()

process.probeTriggersMu17Leg = cms.EDProducer("PatMuonTriggerCandProducer",
    filterNames = cms.vstring("hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4", "hltL3fL1sDoubleMu103p5L1f0L2f10OneMuL3Filtered17"),
    inputs      = cms.InputTag("probeMuons"),
    bits        = cms.InputTag('TriggerResults::HLT'),
    objects     = cms.InputTag('selectedPatTrigger'),
    dR          = cms.double(0.5),
    isAND       = cms.bool(True)
    )
process.probeTriggerSeq += process.probeTriggersMu17Leg

process.probeTriggersMu17LegL1Mu12 = cms.EDProducer("L1MuonMatcher",
        inputs = cms.InputTag("probeTriggersMu17Leg"),
        l1extraMuons = cms.InputTag("l1extraParticles"),
        minET = cms.double(12.),
        dRmatch = cms.double(.5)
        )
process.probeTriggerSeq += process.probeTriggersMu17LegL1Mu12

process.probeTriggersMu8Leg = process.probeTriggersMu17Leg.clone()
process.probeTriggersMu8Leg.filterNames = cms.vstring("hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4", "hltL3pfL1sDoubleMu103p5L1f0L2pf0L3PreFiltered8")
process.probeTriggerSeq += process.probeTriggersMu8Leg

process.probeTriggersTkMu8Leg = process.probeTriggersMu17Leg.clone()
process.probeTriggersTkMu8Leg.filterNames = cms.vstring("hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4", "hltDiMuonGlbFiltered17TrkFiltered8")
process.probeTriggerSeq += process.probeTriggersTkMu8Leg

process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("tagMuonsTriggerMatched@+ probeMuons@-"), # charge coniugate states are implied
    cut   = cms.string("40 < mass < 200")
)

process.muMcMatch = cms.EDProducer("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(13),
    src = cms.InputTag("tightMuons"),
    distMin = cms.double(0.3),
    matched = cms.InputTag("prunedGenParticles"),
    checkCharge = cms.bool(True)
)

process.pileupReweightingProducer = cms.EDProducer("PileupWeightProducer",
    hardcodedWeights = cms.untracked.bool(False),
    PileupMCFile = cms.string('../data/puWeightMC.root'),
    PileupDataFile = cms.string('../data/puWeightData.root'),
    )

ZVariablesToStore = cms.PSet(
    eta = cms.string("eta"),
    abseta = cms.string("abs(eta)"),
    pt  = cms.string("pt"),
    mass  = cms.string("mass"),
    )   

ProbeVariablesToStore = cms.PSet(
    probe_eta    = cms.string("eta"),
    probe_abseta = cms.string("abs(eta)"),
    probe_pt     = cms.string("pt"),
    probe_et     = cms.string("et"),
    probe_e      = cms.string("energy"),
    probe_q      = cms.string("charge"),
    )

TagVariablesToStore = cms.PSet(
    tag_eta    = cms.string("eta"),
    tag_abseta = cms.string("abs(eta)"),
    tag_pt     = cms.string("pt"),
    tag_et     = cms.string("et"),
    tag_e      = cms.string("energy"),
    tag_q      = cms.string("charge"),
    )

CommonStuffForMuonProbe = cms.PSet(
    variables = cms.PSet(ProbeVariablesToStore),
    ignoreExceptions =  cms.bool (True),
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

mcTruthCommonStuff = cms.PSet(
    isMC = cms.bool(False),
    tagMatches = cms.InputTag("muMcMatch"),
    probeMatches = cms.InputTag("muMcMatch"),
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

process.muonEffs = cms.EDAnalyzer("TagProbeFitTreeProducer",
    CommonStuffForMuonProbe, mcTruthCommonStuff,
    tagProbePairs = cms.InputTag("tpPairs"),
    arbitration   = cms.string("Random2"),
    flags         = cms.PSet(
        passingIDZZLoose  = cms.string(
            "pt > 5. && abs(eta) < 2.4 && (isGlobalMuon || (isTrackerMuon && numberOfMatches > 0)) && muonBestTrackType != 2 "
            "&& abs(userFloat('dxyToPV')) < 0.5 && abs(userFloat('dzToPV')) < 1."
        ),
        passingIDZZTight  = cms.string(
            "pt > 5. && abs(eta) < 2.4 && (isGlobalMuon || (isTrackerMuon && numberOfMatches > 0)) && muonBestTrackType != 2 "
            "&& abs(userFloat('dxyToPV')) < 0.5 && abs(userFloat('dzToPV')) < 1. && isPFMuon"
        ),
        passingIsoZZ = cms.string(isolationDef+" < 0.4"),

        passingIDWZLoose  = cms.string("isLooseMuon"), 
        passingIDWZTight  = cms.string("userInt('isTightMuon')==1"), 
        passingIsoWZLoose = cms.string(isolationDef+" < 0.2"),
        passingIsoWZTight = cms.string(isolationDef+" < 0.12"),

        passingMu17 = cms.InputTag("probeTriggersMu17Leg"),
        passingMu17L1Match = cms.InputTag("probeTriggersMu17LegL1Mu12"),
        passingMu8= cms.InputTag("probeTriggersMu8Leg"),
        passingTkMu8 = cms.InputTag("probeTriggersTkMu8Leg"),
    ),
    allProbes     = cms.InputTag("probeMuons"),
    )

process.tpPairSeq = cms.Sequence(
    process.tpPairs
)

if options.isMC :
    process.tpPairSeq += process.muMcMatch 
    process.muonEffs.isMC = cms.bool(True)
    process.muonEffs.eventWeight   = cms.InputTag("generator")
    process.muonEffs.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")
    process.tpPairSeq += process.pileupReweightingProducer

if not options.isMC :
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/'+config['json']).getVLuminosityBlockRange()

process.p = cms.Path(
    process.tightMuons *
    (process.tagMuons + process.probeMuons) *
    (process.tagMuonsTriggerMatched + process.probeTriggerSeq) *
    process.tpPairSeq *
    process.muonEffs
    )

process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string('debug.root'),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
                               )
if config['DEBUG'] :
    process.outpath = cms.EndPath(process.out)

process.TFileService = cms.Service("TFileService", fileName = cms.string(config['outputFile']))

