import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys

process = cms.Process("tnp")

options = dict()
varOptions = VarParsing('analysis')
varOptions.register(
    "isMC",
    True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Compute MC efficiencies"
    )

varOptions.parseArguments()

options['HLTProcessName']          = "HLT"
options['ELECTRON_COLL']           = "slimmedElectrons"
options['ELECTRON_CUTS']           = "abs(eta)<2.5 && pt > 10"
options['ELECTRON_TAG_CUTS']       = "(abs(superCluster.eta)<=2.5) && !(1.4442<=abs(superCluster.eta)<=1.566) && pt >= 25.0"
options['SUPERCLUSTER_COLL']       = "reducedEgamma:reducedSuperClusters"
options['SUPERCLUSTER_CUTS']       = "abs(eta)<2.5 && !(1.4442< abs(eta) <1.566) && et>10.0"
options['MAXEVENTS']               = cms.untracked.int32(-1) 
options['useAOD']                  = cms.bool(False)
options['DOTRIGGER']               = cms.bool(True)
options['DORECO']                  = cms.bool(True)
options['DOID']                    = cms.bool(True)
options['OUTPUTEDMFILENAME']       = 'edmFile.root'
options['DEBUG']                   = cms.bool(False)

if (varOptions.isMC):
    options['INPUT_FILE_NAME']     = "/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/009D49A5-7314-E511-84EF-0025905A605E.root"
    options['OUTPUT_FILE_NAME']    = "TnPTree_mc.root"
    options['TnPPATHS']            = cms.vstring("HLT_Ele22_eta2p1_WP75_Gsf_v*")
    options['TnPHLTTagFilters']    = cms.vstring("hltSingleEle22WP75GsfTrackIsoFilter")
    options['TnPHLTProbeFilters']  = cms.vstring()
    options['GLOBALTAG']           = 'MCRUN2_74_V9A'
    options['EVENTSToPROCESS']     = cms.untracked.VEventRange()
else:
    options['INPUT_FILE_NAME']     = "/store/data/Run2015D/SingleElectron/MINIAOD/05Oct2015-v1/10000/0423304A-3F6F-E511-9875-0025905A609E.root"
    options['OUTPUT_FILE_NAME']    = "TnPTree_data.root"
    options['TnPPATHS']            = cms.vstring("HLT_Ele22_eta2p1_WPTight_Gsf_v*")
    options['TnPHLTTagFilters']    = cms.vstring("hltSingleEle22WPTightGsfTrackIsoFilter")
    options['TnPHLTProbeFilters']  = cms.vstring()
    options['GLOBALTAG']           = 'GR_P_V56'
    options['EVENTSToPROCESS']     = cms.untracked.VEventRange()

###################################################################

process.sampleInfo = cms.EDAnalyzer("tnp::SampleInfoTree",
                                    vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                    genInfo = cms.InputTag("generator")
                                    )

process.eleVarHelper = cms.EDProducer("ElectronVariableHelper",
                                      probes = cms.InputTag(options['ELECTRON_COLL']),
                                      vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices")
                                      )

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.hltFilter = hltHighLevel.clone()
process.hltFilter.throw = cms.bool(True)
process.hltFilter.HLTPaths = options['TnPPATHS']

process.pileupReweightingProducer = cms.EDProducer("PileupWeightProducer",
                                                   hardcodedWeights = cms.untracked.bool(True)
                                                   )

process.GsfDRToNearestTauProbe = cms.EDProducer("DeltaRNearestGenPComputer",
                                                probes = cms.InputTag(options['ELECTRON_COLL']),
                                                objects = cms.InputTag('prunedGenParticles'),
                                                objectSelection = cms.string("abs(pdgId)==15"),
                                                )

process.GsfDRToNearestTauSC = cms.EDProducer("DeltaRNearestGenPComputer",
                                             probes = cms.InputTag("superClusterCands"),
                                             objects = cms.InputTag('prunedGenParticles'),
                                             objectSelection = cms.string("abs(pdgId)==15"),
                                             )

process.GsfDRToNearestTauTag = cms.EDProducer("DeltaRNearestGenPComputer",
                                              probes = cms.InputTag(options['ELECTRON_COLL']),
                                              objects = cms.InputTag('prunedGenParticles'),
                                              objectSelection = cms.string("abs(pdgId)==15"),
                                              )

###################################################################                                                                               
## ELECTRON MODULES                                                                                                                                    
###################################################################                                    
    
process.goodElectrons = cms.EDFilter("PATElectronRefSelector",
                                     src = cms.InputTag(options['ELECTRON_COLL']),
                                     cut = cms.string(options['ELECTRON_CUTS']),
                                     filter = cms.bool(True)
                                     )

###################################################################                                                                     
## SUPERCLUSTER MODULES                                                     
###################################################################         
    
process.superClusterCands = cms.EDProducer("ConcreteEcalCandidateProducer",
                                           src = cms.InputTag(options['SUPERCLUSTER_COLL']),
                                           particleType = cms.int32(11),
                                           )

process.goodSuperClusters = cms.EDFilter("RecoEcalCandidateRefSelector",
                                         src = cms.InputTag("superClusterCands"),
                                         cut = cms.string(options['SUPERCLUSTER_CUTS']),
                                         filter = cms.bool(True)
                                         )

process.GsfMatchedSuperClusterCands = cms.EDProducer("ElectronMatchedCandidateProducer",
                                                     src     = cms.InputTag("superClusterCands"),
                                                     ReferenceElectronCollection = cms.untracked.InputTag("goodElectrons"),
                                                     cut = cms.string(options['SUPERCLUSTER_CUTS'])
                                                     )

###################################################################
## TRIGGER MATCHING
###################################################################

process.goodElectronsTagHLT = cms.EDProducer("PatElectronTriggerCandProducer",
                                             filterNames = cms.vstring(options['TnPHLTTagFilters']),
                                             inputs      = cms.InputTag("goodElectronsTAGCutBasedTight"),
                                             bits        = cms.InputTag('TriggerResults::HLT'),
                                             objects     = cms.InputTag('selectedPatTrigger'),
                                             dR          = cms.double(0.3),
                                             isAND       = cms.bool(True)
                                             )

process.goodElectronsProbeHLT = cms.EDProducer("PatElectronTriggerCandProducer",
                                               filterNames = cms.vstring(options['TnPHLTProbeFilters']),
                                               inputs      = cms.InputTag("goodElectrons"),
                                               bits        = cms.InputTag('TriggerResults::HLT'),
                                               objects     = cms.InputTag('selectedPatTrigger'),
                                               dR          = cms.double(0.3),
                                               isAND       = cms.bool(True)
                                               )

process.goodElectronsProbeMeasureHLT = cms.EDProducer("PatElectronTriggerCandProducer",
                                                      filterNames = cms.vstring(options['TnPHLTProbeFilters']),
                                                      inputs      = cms.InputTag("goodElectrons"),
                                                      bits        = cms.InputTag('TriggerResults::HLT'),
                                                      objects     = cms.InputTag('selectedPatTrigger'),
                                                      dR          = cms.double(0.3),
                                                      isAND       = cms.bool(True)
                                                      )
process.goodElectronsMeasureHLT = cms.Sequence()

process.goodElectronsMeasureHLTEle23 = cms.EDProducer("PatElectronTriggerCandProducer",
                                                filterNames = cms.vstring("hltEle23CaloIdLTrackIdLIsoVLTrackIsoFilter"),
                                                inputs      = cms.InputTag("goodElectronsProbeMeasureHLT"),
                                                bits        = cms.InputTag('TriggerResults::HLT'),
                                                objects     = cms.InputTag('selectedPatTrigger'),
                                                dR          = cms.double(0.3),
                                                isAND       = cms.bool(False)
                                                )
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle23
process.goodElectronsMeasureHLTEle17 = cms.EDProducer("PatElectronTriggerCandProducer",
                                                filterNames = cms.vstring("hltEle17CaloIdLTrackIdLIsoVLTrackIsoFilter"),
                                                inputs      = cms.InputTag("goodElectronsProbeMeasureHLT"),
                                                bits        = cms.InputTag('TriggerResults::HLT'),
                                                objects     = cms.InputTag('selectedPatTrigger'),
                                                dR          = cms.double(0.3),
                                                isAND       = cms.bool(False)
                                                )
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle17
process.goodElectronsMeasureHLTEle12 = cms.EDProducer("PatElectronTriggerCandProducer",
                                                filterNames = cms.vstring("hltEle12CaloIdLTrackIdLIsoVLTrackIsoFilter"),
                                                inputs      = cms.InputTag("goodElectronsProbeMeasureHLT"),
                                                bits        = cms.InputTag('TriggerResults::HLT'),
                                                objects     = cms.InputTag('selectedPatTrigger'),
                                                dR          = cms.double(0.3),
                                                isAND       = cms.bool(False)
                                                )
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle12

process.goodSuperClustersHLT = cms.EDProducer("RecoEcalCandidateTriggerCandProducer",
                                              filterNames  = cms.vstring(options['TnPHLTProbeFilters']),
                                              inputs       = cms.InputTag("goodSuperClusters"),
                                              bits         = cms.InputTag('TriggerResults::HLT'),
                                              objects      = cms.InputTag('selectedPatTrigger'),
                                              dR           = cms.double(0.3),
                                              isAND        = cms.bool(True)
                                              )

###################################################################
## MC MATCHES
###################################################################
    
process.McMatchHLT = cms.EDProducer("MCTruthDeltaRMatcherNew",
                                    matchPDGId = cms.vint32(11),
                                    src = cms.InputTag("goodElectrons"),
                                    distMin = cms.double(0.3),
                                    matched = cms.InputTag("prunedGenParticles"),
                                    checkCharge = cms.bool(True)
                                    )

process.McMatchSC = cms.EDProducer("MCTruthDeltaRMatcherNew",
                                   matchPDGId = cms.vint32(11),
                                   src = cms.InputTag("goodSuperClusters"),
                                   distMin = cms.double(0.3),
                                   matched = cms.InputTag("prunedGenParticles"),
                                   checkCharge = cms.bool(False)
                                   )

process.McMatchTag = cms.EDProducer("MCTruthDeltaRMatcherNew",
                                    matchPDGId = cms.vint32(11),
                                    src = cms.InputTag("goodElectronsTAGCutBasedTight"),
                                    distMin = cms.double(0.2),
                                    matched = cms.InputTag("prunedGenParticles"),
                                    checkCharge = cms.bool(True)
                                    )

process.McMatchRECO = cms.EDProducer("MCTruthDeltaRMatcherNew",
                                     matchPDGId = cms.vint32(11),
                                     src = cms.InputTag("goodElectrons"),
                                     distMin = cms.double(0.2),
                                     matched = cms.InputTag("prunedGenParticles"),
                                     checkCharge = cms.bool(True)
                                     )
    
###################################################################
## TnP PAIRS
###################################################################
    
process.tagTightHLT = cms.EDProducer("CandViewShallowCloneCombiner",
                                     decay = cms.string("goodElectronsTagHLT@+ goodElectronsProbeMeasureHLT@-"), 
                                     checkCharge = cms.bool(True),
                                     cut = cms.string("40<mass<1000"),
                                     )

process.tagTightSC = cms.EDProducer("CandViewShallowCloneCombiner",
                                    decay = cms.string("goodElectronsTagHLT goodSuperClustersHLT"), 
                                    checkCharge = cms.bool(False),
                                    cut = cms.string("40<mass<1000"),
                                    )

process.tagTightRECO = cms.EDProducer("CandViewShallowCloneCombiner",
                                      decay = cms.string("goodElectronsTagHLT@+ goodElectronsProbeHLT@-"), 
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

SCProbeVariablesToStore = cms.PSet(
    probe_sc_eta    = cms.string("eta"),
    probe_sc_abseta = cms.string("abs(eta)"),
    probe_sc_pt     = cms.string("pt"),
    probe_sc_et     = cms.string("et"),
    probe_sc_e      = cms.string("energy"),
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
    probe_Ele_mva           = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
    
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

CommonStuffForSuperClusterProbe = CommonStuffForGsfElectronProbe.clone()
CommonStuffForSuperClusterProbe.variables = cms.PSet(SCProbeVariablesToStore)

mcTruthCommonStuff = cms.PSet(
    isMC = cms.bool(True),
    tagMatches = cms.InputTag("McMatchTag"),
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

process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = options['GLOBALTAG']

process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(options['INPUT_FILE_NAME']),
                            eventsToProcess = options['EVENTSToPROCESS']
                            )

process.maxEvents = cms.untracked.PSet( input = options['MAXEVENTS'])

###################################################################
## ID
###################################################################

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
dataFormat = DataFormat.MiniAOD
if (options['useAOD']):
    dataFormat = DataFormat.AOD
    
switchOnVIDElectronIdProducer(process, dataFormat)
    
# define which IDs we want to produce
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',
                 'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',
                 'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff']
             
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process, idmod, setupVIDElectronSelection)

process.electronZZIDIsoValueMaps = cms.EDProducer("zzElectronIdIsoProducer",
        electrons = cms.InputTag(options['ELECTRON_COLL']),
        mvaIdValueMap = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values")
        )

process.goodElectronsPROBECutBasedVeto = cms.EDProducer("PatElectronSelectorByValueMap",
                                                        input     = cms.InputTag("goodElectrons"),
                                                        cut       = cms.string(options['ELECTRON_CUTS']),
                                                        selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto"),
                                                        id_cut    = cms.bool(True)
                                                        )

process.goodElectronsPROBECutBasedLoose = process.goodElectronsPROBECutBasedVeto.clone()
process.goodElectronsPROBECutBasedLoose.selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose")
process.goodElectronsPROBECutBasedMedium = process.goodElectronsPROBECutBasedVeto.clone()
process.goodElectronsPROBECutBasedMedium.selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium")
process.goodElectronsPROBECutBasedTight = process.goodElectronsPROBECutBasedVeto.clone()
process.goodElectronsPROBECutBasedTight.selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-tight")
process.goodElectronsPROBEZZLoose = process.goodElectronsPROBECutBasedVeto.clone()
process.goodElectronsPROBEZZLoose.selection = cms.InputTag("electronZZIDIsoValueMaps:electronZZIDLoose")
process.goodElectronsPROBEZZTight = process.goodElectronsPROBECutBasedVeto.clone()
process.goodElectronsPROBEZZTight.selection = cms.InputTag("electronZZIDIsoValueMaps:electronZZIDTight")
process.goodElectronsPROBEZZIso = process.goodElectronsPROBECutBasedVeto.clone()
process.goodElectronsPROBEZZIso.selection = cms.InputTag("electronZZIDIsoValueMaps:electronZZIso")

process.goodElectronsTAGCutBasedVeto = cms.EDProducer("PatElectronSelectorByValueMap",
                                                      input     = cms.InputTag("goodElectrons"),
                                                      cut       = cms.string(options['ELECTRON_TAG_CUTS']),
                                                      selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto"),
                                                      id_cut    = cms.bool(True)
                                                      )

process.goodElectronsTAGCutBasedLoose = process.goodElectronsTAGCutBasedVeto.clone()
process.goodElectronsTAGCutBasedLoose.selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose")
process.goodElectronsTAGCutBasedMedium = process.goodElectronsTAGCutBasedVeto.clone()
process.goodElectronsTAGCutBasedMedium.selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium")
process.goodElectronsTAGCutBasedTight = process.goodElectronsTAGCutBasedVeto.clone()
process.goodElectronsTAGCutBasedTight.selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-tight")

###################################################################
## SEQUENCES
###################################################################

process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag(options['ELECTRON_COLL'])
process.ele_sequence = cms.Sequence(
    process.goodElectrons +
    process.egmGsfElectronIDSequence +
    process.goodElectronsPROBECutBasedVeto +
    process.goodElectronsPROBECutBasedLoose +
    process.goodElectronsPROBECutBasedMedium +
    process.goodElectronsPROBECutBasedTight +
    process.goodElectronsTAGCutBasedVeto +
    process.goodElectronsTAGCutBasedLoose +
    process.goodElectronsTAGCutBasedMedium +
    process.goodElectronsTAGCutBasedTight +
    process.goodElectronsTagHLT +
    process.goodElectronsProbeHLT +
    process.goodElectronsProbeMeasureHLT +
    process.goodElectronsMeasureHLT +
    process.electronZZIDIsoValueMaps +
    process.goodElectronsPROBEZZLoose +
    process.goodElectronsPROBEZZTight +
    process.goodElectronsPROBEZZIso
    )

process.sc_sequence = cms.Sequence(process.superClusterCands +
                                   process.goodSuperClusters +
                                   process.goodSuperClustersHLT +
                                   process.GsfMatchedSuperClusterCands
                                   )

###################################################################
## TnP PAIRS
###################################################################

process.allTagsAndProbes = cms.Sequence()

if (options['DOTRIGGER']):
    process.allTagsAndProbes *= process.tagTightHLT

if (options['DORECO']):
    process.allTagsAndProbes *= process.tagTightSC

if (options['DOID']):
    process.allTagsAndProbes *= process.tagTightRECO

process.mc_sequence = cms.Sequence()

if (varOptions.isMC):
    process.mc_sequence *= (process.McMatchHLT + process.McMatchTag + process.McMatchSC + process.McMatchRECO)

##########################################################################
## TREE MAKER OPTIONS
##########################################################################
if (not varOptions.isMC):
    mcTruthCommonStuff = cms.PSet(
        isMC = cms.bool(False)
        )

process.GsfElectronToTrigger = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                              CommonStuffForSuperClusterProbe, mcTruthCommonStuff,
                                              tagProbePairs = cms.InputTag("tagTightHLT"),
                                              arbitration   = cms.string("Random2"),
                                              flags         = cms.PSet(
                                                  passingHLTEle23    = cms.InputTag("goodElectronsMeasureHLTEle23"),
                                                  passingHLTEle17    = cms.InputTag("goodElectronsMeasureHLTEle17"),
                                                  passingHLTEle12    = cms.InputTag("goodElectronsMeasureHLTEle12")
                                              ),
                                              allProbes     = cms.InputTag("goodElectronsProbeMeasureHLT"),
                                              )

if (varOptions.isMC):
    process.GsfElectronToTrigger.probeMatches  = cms.InputTag("McMatchHLT")
    process.GsfElectronToTrigger.eventWeight   = cms.InputTag("generator")
    process.GsfElectronToTrigger.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")
    process.GsfElectronToTrigger.variables.probe_dRTau = cms.InputTag("GsfDRToNearestTauSC")
    process.GsfElectronToTrigger.tagVariables.Ele_dRTau = cms.InputTag("GsfDRToNearestTauTag")

process.GsfElectronToSC = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                         CommonStuffForSuperClusterProbe, mcTruthCommonStuff,
                                         tagProbePairs = cms.InputTag("tagTightSC"),
                                         arbitration   = cms.string("Random2"),
                                         flags         = cms.PSet(passingRECO   = cms.InputTag("GsfMatchedSuperClusterCands", "superclusters"),         
                                                                  ),                                               
                                         allProbes     = cms.InputTag("goodSuperClustersHLT"),
                                         )

if (varOptions.isMC):
    process.GsfElectronToSC.probeMatches  = cms.InputTag("McMatchSC")
    process.GsfElectronToSC.eventWeight   = cms.InputTag("generator")
    process.GsfElectronToSC.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")
    process.GsfElectronToSC.variables.probe_dRTau = cms.InputTag("GsfDRToNearestTauSC")
    process.GsfElectronToSC.tagVariables.Ele_dRTau = cms.InputTag("GsfDRToNearestTauTag")

process.GsfElectronToRECO = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                           mcTruthCommonStuff, CommonStuffForGsfElectronProbe,
                                           tagProbePairs = cms.InputTag("tagTightRECO"),
                                           arbitration   = cms.string("Random2"),
                                           flags         = cms.PSet(passingVeto   = cms.InputTag("goodElectronsPROBECutBasedVeto"),
                                                                    passingLoose  = cms.InputTag("goodElectronsPROBECutBasedLoose"),
                                                                    passingMedium = cms.InputTag("goodElectronsPROBECutBasedMedium"),
                                                                    passingTight  = cms.InputTag("goodElectronsPROBECutBasedTight"),
                                                                    passingZZLoose =cms.InputTag("goodElectronsPROBEZZLoose"),
                                                                    passingZZTight =cms.InputTag("goodElectronsPROBEZZTight"),
                                                                    passingZZIso =  cms.InputTag("goodElectronsPROBEZZIso"),
                                                                    ),                                               
                                           allProbes     = cms.InputTag("goodElectronsProbeHLT"),
                                           )

if (varOptions.isMC):
    process.GsfElectronToRECO.probeMatches  = cms.InputTag("McMatchRECO")
    process.GsfElectronToRECO.eventWeight   = cms.InputTag("generator")
    process.GsfElectronToRECO.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")
    process.GsfElectronToRECO.variables.probe_dRTau = cms.InputTag("GsfDRToNearestTauProbe")
    process.GsfElectronToRECO.tagVariables.Ele_dRTau = cms.InputTag("GsfDRToNearestTauTag")

process.tree_sequence = cms.Sequence()
if (options['DOTRIGGER']):
    process.tree_sequence *= process.GsfElectronToTrigger

if (options['DORECO']):
    process.tree_sequence *= process.GsfElectronToSC

if (options['DOID']):
    process.tree_sequence *= process.GsfElectronToRECO

##########################################################################
## PATHS
##########################################################################

process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string(options['OUTPUTEDMFILENAME']),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
                               )
process.outpath = cms.EndPath(process.out)
if (not options['DEBUG']):
    process.outpath.remove(process.out)

if (varOptions.isMC):
    process.p = cms.Path(
        process.sampleInfo +
        process.hltFilter +
        process.ele_sequence + 
        process.sc_sequence +
        process.allTagsAndProbes +
        process.pileupReweightingProducer +
        process.mc_sequence +
        process.eleVarHelper +
        process.GsfDRToNearestTauProbe + 
        process.GsfDRToNearestTauTag + 
        process.GsfDRToNearestTauSC + 
        process.tree_sequence
        )
else:
    process.p = cms.Path(
        process.sampleInfo +
        process.hltFilter +
        process.ele_sequence + 
        process.sc_sequence +
        process.allTagsAndProbes +
        process.mc_sequence +
        process.eleVarHelper +
        process.tree_sequence
        )

process.TFileService = cms.Service(
    "TFileService", fileName = cms.string(options['OUTPUT_FILE_NAME']),
    closeFileFast = cms.untracked.bool(True)
    )
