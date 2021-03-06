import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

process = cms.Process("tnp")
options = VarParsing('analysis')
options.register(
    "isMC",
    False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Compute MC efficiencies"
    )
options.parseArguments()

isolationDef = "(chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/pt"
config = {}
config['MUON_COLL']           = "slimmedMuons"
config['MUON_CUTS']           = "(isTrackerMuon || isGlobalMuon) && abs(eta)<2.5 && pt > 5"
config['MUON_TAG_CUTS']       = "userInt('isTightMuon')==1 && pt > 25 && abs(eta) < 2.1 && "+isolationDef+" < 0.2"
config['MUON_TAG_TRIGGER']    = "hltL3crIsoL1sMu18L1f0L2f10QL3f20QL3trkIsoFiltered0p09"
config['DEBUG']               = cms.bool(False)
config['json']                = 'Cert_271036-274421_13TeV_PromptReco_Collisions16_JSON.txt'

# file dataset=/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD
# https://cmsweb.cern.ch/das/request?view=plain&limit=50&instance=prod%2Fglobal&input=file+dataset%3D%2FSingleMuon%2FRun2015D-05Oct2015-v1%2FMINIAOD
inputFilesData = [
	'/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/273/425/00000/5A500A94-B31B-E611-9477-02163E014682.root'
]

# file dataset=/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM
inputFilesMC = [
    '/store/mc/RunIISpring16MiniAODv2/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/FlatPU8to42RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/50000/12F4768A-F623-E611-966A-003048FFD72C.root',
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

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.tightMuons = cms.EDProducer("stupidTightMuonProducer",
    src = cms.InputTag("slimmedMuons"),
    vtx = cms.InputTag("offlineSlimmedPrimaryVertices")
)
process.muonInitialSequence = cms.Sequence(process.tightMuons)
muonSource = 'tightMuons'

process.tagMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag(muonSource),
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
    src = cms.InputTag(muonSource),
    cut = cms.string(config['MUON_CUTS']), 
)

########### Probe Triggers ###############

process.probeTriggerSeq = cms.Sequence()

process.probeTriggersMu20Leg = cms.EDProducer("PatMuonTriggerCandProducer",
    filterNames = cms.vstring("hltL3crIsoL1sMu18L1f0L2f10QL3f20QL3trkIsoFiltered0p09"),
    inputs      = cms.InputTag("probeMuons"),
    bits        = cms.InputTag('TriggerResults::HLT'),
    objects     = cms.InputTag('selectedPatTrigger'),
    dR          = cms.double(0.5),
    isAND       = cms.bool(True)
    )
process.probeTriggerSeq += process.probeTriggersMu20Leg

process.probeTriggersMu20LegL1Mu18 = cms.EDProducer("L1MuonMatcher",
        inputs = cms.InputTag("probeTriggersMu20Leg"),
        l1extraMuons = cms.InputTag("l1extraParticles"),
        minET = cms.double(18.),
        dRmatch = cms.double(.5)
        )
process.probeTriggerSeq += process.probeTriggersMu20LegL1Mu18

process.probeTriggersMu8Leg = process.probeTriggersMu20Leg.clone()
process.probeTriggersMu8Leg.filterNames = cms.vstring("hltL3crIsoL1sMu18L1f0L2f10QL3f20QL3trkIsoFiltered0p09")
process.probeTriggerSeq += process.probeTriggersMu8Leg

process.probeTriggersTkMu8Leg = process.probeTriggersMu20Leg.clone()
process.probeTriggersTkMu8Leg.filterNames = cms.vstring("hltL3crIsoL1sMu18L1f0L2f10QL3f20QL3trkIsoFiltered0p09")
process.probeTriggerSeq += process.probeTriggersTkMu8Leg

process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("tagMuonsTriggerMatched@+ probeMuons@-"), # charge coniugate states are implied
    cut   = cms.string("40 < mass < 200")
)

process.tpPairsMCEmbedded = cms.EDProducer("pairMCInfoEmbedder",
    input = cms.InputTag("tpPairs"),
    leg1Matches = cms.InputTag("muMcMatch"),
    leg2Matches = cms.InputTag("muMcMatch")
)

process.muMcMatch = cms.EDProducer("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(13),
    src = cms.InputTag(muonSource),
    distMin = cms.double(0.3),
    matched = cms.InputTag("prunedGenParticles"),
    checkCharge = cms.bool(True)
)

process.pileupReweightingProducer = cms.EDProducer("PileupWeightProducer",
    hardcodedWeights = cms.untracked.bool(False),
    PileupMCFile = cms.string('$CMSSW_BASE/src/Analysis/DiBosonTP/data/MC_Spring16.root'),
    PileupDataFile = cms.string('$CMSSW_BASE/src/Analysis/DiBosonTP/data/2016BPileupHistogram.root'),
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
        probe_isPromptFinalState = cms.string("isPromptFinalState")
        ),      
    )

process.muonEffs = cms.EDAnalyzer("TagProbeFitTreeProducer",
    CommonStuffForMuonProbe, mcTruthCommonStuff,
    tagProbePairs = cms.InputTag("tpPairs"),
    arbitration   = cms.string("Random2"),
    flags         = cms.PSet(

        passingIDWZLoose  = cms.string("isMediumMuon && trackIso()/pt()<0.25 && abs(userFloat('dxyToPV')) < 0.02 && abs(userFloat('dzToPV')) < 0.1"), 
        passingIDWZLooseNoTrackIso  = cms.string("isMediumMuon && abs(userFloat('dxyToPV')) < 0.02 && abs(userFloat('dzToPV')) < 0.1"), 
        passingTightID  = cms.string("userInt('isTightMuon')==1"), 
        passingIsoWZLoose = cms.string(isolationDef+" < 0.4"),
        passingIsoWZTight = cms.string(isolationDef+" < 0.12"),

        passingMu17 = cms.InputTag("probeTriggersMu20Leg"),
        passingMu17L1Match = cms.InputTag("probeTriggersMu20LegL1Mu18"),
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
    process.tpPairSeq += process.tpPairsMCEmbedded
    process.muonEffs.isMC = cms.bool(True)
    process.muonEffs.eventWeight   = cms.InputTag("generator")
    process.muonEffs.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")
    setattr(process.muonEffs.pairVariables, 'mc_mass', cms.string("userFloat('mc_mass')"))
    process.muonEffs.tagProbePairs = cms.InputTag("tpPairsMCEmbedded")
    process.tpPairSeq += process.pileupReweightingProducer

if not options.isMC :
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/'+config['json']).getVLuminosityBlockRange()

process.p = cms.Path(
    process.muonInitialSequence *
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

