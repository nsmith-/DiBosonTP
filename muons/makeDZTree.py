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
config['DEBUG']               = cms.bool(False)
config['json']                = 'Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt'

# file dataset=/DoubleMuon/Run2015D-05Oct2015-v1/MINIAOD
# https://cmsweb.cern.ch/das/request?view=plain&limit=50&instance=prod%2Fglobal&input=file+dataset%3D%2FDoubleMuon%2FRun2015D-05Oct2015-v1%2FMINIAOD
inputFilesData = [
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/529E5F9F-5F6F-E511-83C6-0026189438F4.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/52A8BE9F-5F6F-E511-86A9-0025905AA9CC.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/56CC0262-5E6F-E511-B9BD-0025905A613C.root',
]

# file dataset=/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM
# https://cmsweb.cern.ch/das/request?view=plain&limit=50&instance=prod%2Fglobal&input=file+dataset%3D%2FDYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8%2FRunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3%2FMINIAODSIM
inputFilesMC = [
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/009D49A5-7314-E511-84EF-0025905A605E.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/00C0BECF-6F14-E511-96F8-0025904B739A.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/0260F225-7614-E511-A79F-00A0D1EE8EB4.root',
]

if len(options.inputFiles) is 0 :
    if options.isMC :
        options.inputFiles = inputFilesMC
    else :
        options.inputFiles = inputFilesData

if len(options.outputFile) is 0 :
    if options.isMC :
        options.outputFile = 'TnPTreeDZ_mc.root'
    else :
        options.outputFile = 'TnPTreeDZ_data.root'

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    )

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.hltFilter = hltHighLevel.clone()
process.hltFilter.throw = cms.bool(True)
process.hltFilter.HLTPaths = cms.vstring('HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v*', 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v*')

process.goodMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag(config['MUON_COLL']),
    cut = cms.string(config['MUON_CUTS']),
    filter = cms.bool(True)
)

process.triggerMatchingSequence = cms.Sequence()

process.muonTriggerUpperLeg = cms.EDProducer("PatMuonTriggerCandProducer",
    filterNames = cms.vstring("hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4", "hltL3fL1sDoubleMu103p5L1f0L2f10OneMuL3Filtered17"),
    inputs      = cms.InputTag("goodMuons"),
    bits        = cms.InputTag('TriggerResults::HLT'),
    objects     = cms.InputTag('selectedPatTrigger'),
    dR          = cms.double(0.5),
    isAND       = cms.bool(True)
    )
process.triggerMatchingSequence += process.muonTriggerUpperLeg

process.muonTriggerMu8Leg = process.muonTriggerUpperLeg.clone()
process.muonTriggerMu8Leg.filterNames = cms.vstring("hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4", "hltL3pfL1sDoubleMu103p5L1f0L2pf0L3PreFiltered8")
process.triggerMatchingSequence += process.muonTriggerMu8Leg

process.muonTriggerTkMu8Leg = process.muonTriggerUpperLeg.clone()
process.muonTriggerTkMu8Leg.filterNames = cms.vstring("hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4", "hltDiMuonGlbFiltered17TrkFiltered8")
process.triggerMatchingSequence += process.muonTriggerTkMu8Leg

process.muonDZTriggerMu8Leg = process.muonTriggerUpperLeg.clone()
process.muonDZTriggerMu8Leg.filterNames = cms.vstring("hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4", "hltL3pfL1sDoubleMu103p5L1f0L2pf0L3PreFiltered8", "hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4DzFiltered0p2")
process.triggerMatchingSequence += process.muonDZTriggerMu8Leg

process.muonDZTriggerTkMu8Leg = process.muonTriggerUpperLeg.clone()
process.muonDZTriggerTkMu8Leg.filterNames = cms.vstring("hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4", "hltDiMuonGlbFiltered17TrkFiltered8", "hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4DzFiltered0p2")
process.triggerMatchingSequence += process.muonDZTriggerTkMu8Leg

process.tpPairsMu17Mu8 = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("muonTriggerUpperLeg@+ muonTriggerMu8Leg@-"), # charge coniugate states are implied
    cut   = cms.string("40 < mass < 200")
)

process.tpPairsMu17TkMu8 = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("muonTriggerUpperLeg@+ muonTriggerTkMu8Leg@-"), # charge coniugate states are implied
    cut   = cms.string("40 < mass < 200")
)

process.muMcMatch = cms.EDProducer("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(13),
    src = cms.InputTag(config['MUON_COLL']),
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

process.globalMuonDZTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
    CommonStuffForMuonProbe, mcTruthCommonStuff,
    tagProbePairs = cms.InputTag("tpPairsMu17Mu8"),
    arbitration   = cms.string("BestMass"),
    massForArbitration = cms.double(91.),
    flags         = cms.PSet(
        passingDZ = cms.InputTag("muonDZTriggerMu8Leg"),
    ),
    allProbes     = cms.InputTag("muonTriggerMu8Leg"),
    )

process.trackerMuonDZTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
    CommonStuffForMuonProbe, mcTruthCommonStuff,
    tagProbePairs = cms.InputTag("tpPairsMu17TkMu8"),
    arbitration   = cms.string("BestMass"),
    massForArbitration = cms.double(91.),
    flags         = cms.PSet(
        passingDZ = cms.InputTag("muonDZTriggerTkMu8Leg"),
    ),
    allProbes     = cms.InputTag("muonTriggerTkMu8Leg"),
    )

process.tpPairSeq = cms.Sequence(
    process.tpPairsMu17Mu8 + process.tpPairsMu17TkMu8
)

if options.isMC :
    process.tpPairSeq += process.muMcMatch 
    process.tpPairSeq += process.pileupReweightingProducer
    process.globalMuonDZTree.isMC = cms.bool(True)
    process.globalMuonDZTree.eventWeight   = cms.InputTag("generator")
    process.globalMuonDZTree.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")
    process.trackerMuonDZTree.isMC = cms.bool(True)
    process.trackerMuonDZTree.eventWeight   = cms.InputTag("generator")
    process.trackerMuonDZTree.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")

if not options.isMC :
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/'+config['json']).getVLuminosityBlockRange()

process.p = cms.Path(
    process.goodMuons *
    process.triggerMatchingSequence *
    process.tpPairSeq *
    (process.globalMuonDZTree + process.trackerMuonDZTree)
    )

process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string('debug.root'),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
                               )
if config['DEBUG'] :
    process.outpath = cms.EndPath(process.out)

process.TFileService = cms.Service("TFileService", fileName = cms.string(options.outputFile))

