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
config['MUON_CUTS']           = "(isTrackerMuon || isGlobalMuon) && abs(eta)<2.5 && pt > 5"
config['MUON_TAG_CUTS']       = "userInt('isTightMuon')==1 && pt > 22 && abs(eta) < 2.1 && "+isolationDef+" < 0.2"
config['MUON_TAG_TRIGGER']    = "hltL3crIsoL1sMu16L1f0L2f10QL3f20QL3trkIsoFiltered0p09"
config['DEBUG']               = cms.bool(False)
config['json']                = 'Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt'

# file dataset=/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD
# https://cmsweb.cern.ch/das/request?view=plain&limit=50&instance=prod%2Fglobal&input=file+dataset%3D%2FSingleMuon%2FRun2015D-05Oct2015-v1%2FMINIAOD
inputFilesData = [
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/DAF6F553-986F-E511-AB07-002618943982.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/DC242338-986F-E511-9196-00261894394B.root',
    '/store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/30000/DC4D3D93-906F-E511-BEAD-0026189438F9.root',
]

# file dataset=/JPsiToMuMu_Pt20to100-pythia8-gun/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM
inputFilesMC = [
        '/store/mc/RunIISpring15MiniAODv2/JPsiToMuMu_Pt20to100-pythia8-gun/MINIAODSIM/74X_mcRun2_asymptotic_v2-v2/30000/085258CF-CA76-E511-AF11-00237DF20360.root',
        '/store/mc/RunIISpring15MiniAODv2/JPsiToMuMu_Pt20to100-pythia8-gun/MINIAODSIM/74X_mcRun2_asymptotic_v2-v2/30000/2C190717-CB76-E511-911C-00237DF25430.root',
        '/store/mc/RunIISpring15MiniAODv2/JPsiToMuMu_Pt20to100-pythia8-gun/MINIAODSIM/74X_mcRun2_asymptotic_v2-v2/30000/48EAA0D6-CA76-E511-82F0-00237DF25430.root',
]

if len(options.inputFiles) is 0 :
    if options.isMC :
        options.inputFiles = inputFilesMC
    else :
        options.inputFiles = inputFilesData

if len(options.outputFile) is 0 :
    if options.isMC :
        options.outputFile = 'TnPTree_mc.root'
    else :
        options.outputFile = 'TnPTree_data.root'

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
    cut   = cms.string("2.5 < mass < 3.5")
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
    PileupMCFile = cms.string('$CMSSW_BASE/src/Analysis/DiBosonTP/data/puWeightMC.root'),
    PileupDataFile = cms.string('$CMSSW_BASE/src/Analysis/DiBosonTP/data/puWeightData.root'),
    )

ZVariablesToStore = cms.PSet(
    eta = cms.string("eta"),
    abseta = cms.string("abs(eta)"),
    pt  = cms.string("pt"),
    mass  = cms.string("mass"),
    deltaR = cms.string("deltaR(daughter(0).eta, daughter(0).phi, daughter(1).eta, daughter(1).phi)"),
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
        mass60to120 = cms.string("60 < mass < 120"),
        pt_lower_100 = cms.string("pt<100"),
        ),
    tagVariables   =  cms.PSet(TagVariablesToStore),
    tagFlags       =  cms.PSet(),    
    )

mcTruthCommonStuff = cms.PSet(
    isMC = cms.bool(False),
    tagMatches = cms.InputTag("muMcMatch"),
    probeMatches = cms.InputTag("muMcMatch"),
    #motherPdgId = cms.vint32(22,23),
    motherPdgId = cms.vint32(443), # JPsi
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

process.TFileService = cms.Service("TFileService", fileName = cms.string(options.outputFile))

