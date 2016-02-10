import FWCore.ParameterSet.Config as cms

# Make FSR photon collection, give them isolation and cut on it
# might be able to just use packedPFCands selected for pdgID and use
# standard isolation; I haven't checked
from FinalStateAnalysis.PatTools.miniAOD_fsrPhotons_cff import *

dretPhotonSelection = cms.EDFilter(
    "CandPtrSelector",
    src = cms.InputTag('boostedFsrPhotons'),
    cut = cms.string('pt > 2 && abs(eta) < 2.4 && '
                     '((userFloat("fsrPhotonPFIsoChHadPUNoPU03pt02") + '
                     'userFloat("fsrPhotonPFIsoNHadPhoton03")) / pt < 1.8)'),
    )
makeFSRPhotons = cms.Sequence(fsrPhotonSequence *
                              dretPhotonSelection)

# ZZ Loose ID decision will be embedded as userFloat("HZZIDPass"),
# tight ID as userFloat("HZZIDPassTight")
zzIDLabel = 'HZZIDPass'

# Embed HZZ ID decisions because we need to know them for FSR recovery
electronZZIDEmbedding = cms.EDProducer(
    "MiniAODElectronHZZIDDecider",
    src = cms.InputTag("slimmedElectrons"),
    idLabel = cms.string(zzIDLabel), # boolean stored as userFloat with this name
    vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    bdtLabel = cms.string("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
    idCutLowPtLowEta = cms.double(-.265),
    idCutLowPtMedEta = cms.double(-.556),
    idCutLowPtHighEta = cms.double(-.551),
    idCutHighPtLowEta = cms.double(-.072),
    idCutHighPtMedEta = cms.double(-.286),
    idCutHighPtHighEta = cms.double(-.267),
    missingHitsCut = cms.int32(999),
    ptCut = cms.double(7.), 
    )
muonZZIDEmbedding = cms.EDProducer(
    "MiniAODMuonHZZIDDecider",
    src = cms.InputTag("slimmedMuons"),
    idLabel = cms.string(zzIDLabel), # boolean will be stored as userFloat with this name
    vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    # Defaults are correct as of 6 January 2016, overwrite later if needed
    ptCut = cms.double(5.), 
    )

zzIDDecisions = cms.Sequence(
    electronZZIDEmbedding +
    muonZZIDEmbedding
    )

# FSR will be embedded as userCand("fsrCand") if any is found
fsrLabel = "fsrCand"

# Embed fsr as userCands
leptonDRETFSREmbedding = cms.EDProducer(
    "MiniAODLeptonDRETFSREmbedder",
    muSrc = cms.InputTag("muonZZIDEmbedding"),
    eSrc = cms.InputTag("electronZZIDEmbedding"),
    phoSrc = cms.InputTag("dretPhotonSelection"),
    phoSelection = cms.string(""),
    eSelection = cms.string('userFloat("%s") > 0.5'%zzIDLabel),
    muSelection = cms.string('userFloat("%s") > 0.5'%zzIDLabel),
    fsrLabel = cms.string(fsrLabel),
    etPower = cms.double(2.),
    maxDR = cms.double(0.5),
    )

eaFile = 'RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_25ns.txt'
effectiveAreaEmbedding = cms.EDProducer(
    "MiniAODElectronEffectiveAreaEmbedder",
    src = cms.InputTag("leptonDRETFSREmbedding"),
    label = cms.string("EffectiveArea"), # embeds a user float with this name
    configFile = cms.FileInPath(eaFile), # the effective areas file
    )

# isolation decisions embedded as userFloat("HZZIsoPass")
zzIsoLabel = "HZZIsoPass"
# actual rel iso value embedded as userFloat("HZZIsoVal")
zzIsoValueLabel = zzIsoLabel.replace("Pass", "Val")

# embed isolation decisions
leptonZZIsoEmbedding = cms.EDProducer(
    "MiniAODLeptonHZZIsoDecider",
    srcE = cms.InputTag("effectiveAreaEmbedding"),
    srcMu = cms.InputTag("leptonDRETFSREmbedding"),
    isoDecisionLabel = cms.string(zzIsoLabel),
    isoValueLabel = cms.string(zzIsoValueLabel),
    fsrLabel = cms.string(fsrLabel),
    fsrElecSelection = cms.string('userFloat("%s") > 0.5'%zzIDLabel),
    fsrMuonSelection = cms.string('userFloat("%s") > 0.5'%zzIDLabel),
    eaLabel = cms.string('EffectiveArea'),
    isoConeDRMaxE = cms.double(0.3),
    isoConeDRMaxMu = cms.double(0.3),
    isoCutE = cms.double(0.35),
    isoCutMu = cms.double(0.35),
    )

zzIsoDecisions = cms.Sequence(
    effectiveAreaEmbedding
    + leptonZZIsoEmbedding
    )

# electrons and muons in event as 'leptonZZIsoEmbedding:electrons' 
# and 'leptonZZIsoEmbedding:muons'

zzEmbedding = cms.Sequence(makeFSRPhotons
                           + zzIDDecisions
                           + leptonDRETFSREmbedding
                           + zzIsoDecisions
                           )
