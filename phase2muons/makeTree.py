import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

process = cms.Process("TNP")
options = VarParsing('analysis')
options.register(
    "debug",
    False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "EDM File output"
    )
options.parseArguments()

inputFiles = [
    '/store/relval/CMSSW_8_1_0_pre9/RelValZMM_13/GEN-SIM-RECO/81X_mcRun2_asymptotic_v2_2023GReco-v1/10000/9041DC3E-5954-E611-8DB7-0025905B8566.root',
]

if len(options.inputFiles) is 0:
    options.inputFiles = inputFiles

if len(options.outputFile) is 0:
    options.outputFile = 'TnPTree.root'

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    )

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.tracksSelection = cms.EDFilter("TrackRefSelector",
    src = cms.InputTag("generalTracks"),
    cut = cms.string("pt>10"),
    filter = cms.bool(True),
)

process.makeMuonsFromTracks = cms.EDProducer("OneStopMuonShop",
    tracks = cms.InputTag("tracksSelection"),
    recoMuons = cms.InputTag("muons"),
    patMuons = cms.InputTag("slimmedMuons"),
    vertices = cms.InputTag("offlinePrimaryVertices")
)

isolationDef = "(pfIsolationR04().sumChargedHadronPt+max(pfIsolationR04().sumPhotonEt+pfIsolationR04().sumNeutralHadronEt-0.5*pfIsolationR04().sumPUPt,0.0))/pt"
process.tagMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("makeMuonsFromTracks"),
    cut = cms.string("userInt('isTightMuon')==1 && pt > 25 && abs(eta) < 2.1 && "+isolationDef+" < 0.2"),
    filter = cms.bool(True),
)

process.probeMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("makeMuonsFromTracks"),
    cut = cms.string("pt>10"), 
    filter = cms.bool(True),
)

process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("tagMuons@+ probeMuons@-"), # charge coniugate states are implied
    cut   = cms.string("60 < mass < 120")
)

process.tpPairsMCEmbedded = cms.EDProducer("pairMCInfoEmbedder",
    input = cms.InputTag("tpPairs"),
    leg1Matches = cms.InputTag("tagMatch"),
    leg2Matches = cms.InputTag("probeMatch")
)

process.tagMatch = cms.EDProducer("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(13),
    src = cms.InputTag("tagMuons"),
    distMin = cms.double(0.3),
    matched = cms.InputTag("genParticles"),
    checkCharge = cms.bool(True)
)

process.probeMatch = cms.EDProducer("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(13),
    src = cms.InputTag("probeMuons"),
    distMin = cms.double(0.3),
    matched = cms.InputTag("genParticles"),
    checkCharge = cms.bool(True)
)

#process.pileupReweightingProducer = cms.EDProducer("PileupWeightProducer",
#    hardcodedWeights = cms.untracked.bool(False),
#    PileupMCFile = cms.string('$CMSSW_BASE/src/Analysis/DiBosonTP/data/puWeightMC.root'),
#    PileupDataFile = cms.string('$CMSSW_BASE/src/Analysis/DiBosonTP/data/puWeightData.root'),
#    )

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
    probe_chargedHadronIsoR04 = cms.string("pfIsolationR04().sumChargedHadronPt"),
    probe_neutralHadronIsoR04 = cms.string("pfIsolationR04().sumNeutralHadronEt"),
    probe_photonIsoR04 = cms.string("pfIsolationR04().sumPhotonEt"),
    probe_pileupIsoR04 = cms.string("pfIsolationR04().sumPUPt"),
    )

TagVariablesToStore = cms.PSet(
    tag_eta    = cms.string("eta"),
    tag_abseta = cms.string("abs(eta)"),
    tag_pt     = cms.string("pt"),
    tag_et     = cms.string("et"),
    tag_e      = cms.string("energy"),
    tag_q      = cms.string("charge"),
    tag_chargedHadronIsoR04 = cms.string("pfIsolationR04().sumChargedHadronPt"),
    tag_neutralHadronIsoR04 = cms.string("pfIsolationR04().sumNeutralHadronEt"),
    tag_photonIsoR04 = cms.string("pfIsolationR04().sumPhotonEt"),
    tag_pileupIsoR04 = cms.string("pfIsolationR04().sumPUPt"),
    )

CommonStuffForMuonProbe = cms.PSet(
    variables = cms.PSet(ProbeVariablesToStore),
    ignoreExceptions =  cms.bool (False),
    addRunLumiInfo   =  cms.bool (True),

    addEventVariablesInfo   =  cms.bool(True),
    vertexCollection = cms.InputTag("offlinePrimaryVertices"),
    beamSpot = cms.InputTag("offlineBeamSpot"),

    pairVariables =  cms.PSet(ZVariablesToStore),
    pairFlags     =  cms.PSet(
        mass60to120 = cms.string("60 < mass < 120")
        ),
    tagVariables   =  cms.PSet(TagVariablesToStore),
    tagFlags       =  cms.PSet(),    
    )

mcTruthCommonStuff = cms.PSet(
    isMC = cms.bool(True),
    eventWeight = cms.double(1.),
    tagMatches = cms.InputTag("tagMatch"),
    probeMatches = cms.InputTag("probeMatch"),
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
    tagProbePairs = cms.InputTag("tpPairsMCEmbedded"),
    arbitration   = cms.string("Random2"),
    flags         = cms.PSet(
        passingIDWZLoose  = cms.string("isMediumMuon && trackIso()/pt()<0.25 && abs(userFloat('dxyToPV')) < 0.02 && abs(userFloat('dzToPV')) < 0.1"), 
        passingIDWZLooseNoTrackIso  = cms.string("isMediumMuon && abs(userFloat('dxyToPV')) < 0.02 && abs(userFloat('dzToPV')) < 0.1"), 
        passingTightID  = cms.string("userInt('isTightMuon')==1"), 
        passingIsoWZLoose = cms.string(isolationDef+" < 0.4"),
        passingIsoWZTight = cms.string(isolationDef+" < 0.12"),
    ),
    allProbes     = cms.InputTag("probeMuons"),
    )

# (if isMC)
setattr(process.muonEffs.pairVariables, 'mc_mass', cms.string("userFloat('mc_mass')"))
process.muonEffs.tagProbePairs = cms.InputTag("tpPairsMCEmbedded")

process.p = cms.Path(
    process.tracksSelection *
    (process.makeMuonsFromTracks + process.tagMuons + process.probeMuons) *
    (process.tpPairs + process.tagMatch + process.probeMatch + process.tpPairsMCEmbedded) *
    process.muonEffs
    )

if options.debug:
    process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string('debug.root'),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p")),
                               outputCommands = cms.untracked.vstring("drop *", "keep *_*_*_TNP"),
                               )
    process.outpath = cms.EndPath(process.out)

process.TFileService = cms.Service("TFileService", fileName = cms.string(options.outputFile))

