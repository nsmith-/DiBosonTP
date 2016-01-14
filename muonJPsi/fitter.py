import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys

options = VarParsing('analysis')

options.register(
    "isMC",
    True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Compute MC efficiencies"
    )

options.register(
    "inputFileName",
    "TnPTree_mc.root",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Input filename"
    )

options.register(
    "outputFileName",
    "",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Output filename"
    )

options.register(
    "conditions",
    "",
    VarParsing.multiplicity.list,
    VarParsing.varType.string,
    "Additional binned categories (set true)"
    )

options.register(
    "idName",
    "passingTight",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "ID variable name as in the fitter_tree"
    )

options.register(
    "dirName",
    "muonEffs",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Folder name containing the fitter_tree"
    )

options.register(
    "mcTemplateFile",
    "",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "MC Templates for fit"
    )

options.register(
    "doCutAndCount",
    False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Perform cut and count efficiency measurement"
    )

options.register(
    "startEfficiency",
    0.9,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.float,
    "Adjust default efficiency used to seed the start of fit"
    )

options.parseArguments()


process = cms.Process("TagProbe")
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

################################################

InputFileName = options.inputFileName
OutputFile = "efficiency-mc-"+options.idName
if (not options.isMC):
    OutputFile = "efficiency-data-"+options.idName

if (options.outputFileName != ""):
    OutputFile = OutputFile+"-"+options.outputFileName+".root"
else:
    OutputFile = OutputFile+".root"

################################################

EfficiencyBins = cms.PSet(
    probe_pt  = cms.vdouble( 5, 10, 20, 30 ),
    probe_abseta = cms.vdouble( 0.0, 1.5, 2.5), 
    )

EfficiencyBinningSpecification = cms.PSet(
    UnbinnedVariables = cms.vstring("mass", "totWeight"),
    BinnedVariables = cms.PSet(EfficiencyBins),
    BinToPDFmap = cms.vstring("pdfSignalPlusBackground")  
    )

if options.mcTemplateFile :
    for absetabin in range(len(EfficiencyBins.probe_abseta)-1) :
        for ptbin in range(len(EfficiencyBins.probe_pt)-1) :
            EfficiencyBinningSpecification.BinToPDFmap += [
                    "*probe_abseta_bin%d*probe_pt_bin%d*" % (absetabin, ptbin),
                    "pdfSignal_probe_abseta_bin%d__probe_pt_bin%d" % (absetabin, ptbin)
                ]

if len(options.conditions) > 0 :
    for condition in options.conditions :
        setattr(EfficiencyBinningSpecification.BinnedVariables, condition, cms.vstring("true"))

if options.isMC :
    setattr(EfficiencyBinningSpecification.BinnedVariables, 'mcTrue', cms.vstring("true"))

############################################################################################

process.TnPMeasurement = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
                                        InputFileNames = cms.vstring(InputFileName),
                                        InputDirectoryName = cms.string(options.dirName),
                                        InputTreeName = cms.string("fitter_tree"), 
                                        OutputFileName = cms.string(OutputFile),
                                        NumCPU = cms.uint32(1),
                                        SaveWorkspace = cms.bool(False), #VERY TIME CONSUMING FOR MC
                                        doCutAndCount = cms.bool(options.doCutAndCount),
                                        floatShapeParameters = cms.bool(True),
                                        binnedFit = cms.bool(True),
                                        binsForFit = cms.uint32(60),
                                        #fixVars = cms.vstring("meanP", "meanF", "sigmaP", "sigmaF", "sigmaP_2", "sigmaF_2"),
                                        
                                        # defines all the real variables of the probes available in the input tree and intended for use in the efficiencies
                                        Variables = cms.PSet(mass = cms.vstring("Tag-Probe Mass", "2.5", "3.5", "GeV/c^{2}"),
                                                             probe_pt = cms.vstring("Probe p_{T}", "0", "100", "GeV/c"),
                                                             probe_abseta = cms.vstring("Probe |#eta|", "0", "2.5", ""), 
                                                             totWeight = cms.vstring("totWeight", "-100000000", "1000000000", ""),
                                                             ),
                                        
                                        # defines all the discrete variables of the probes available in the input tree and intended for use in the efficiency calculations
                                        Categories = cms.PSet(),
                                        
                                        # defines all the PDFs that will be available for the efficiency calculations; 
                                        # uses RooFit's "factory" syntax;
                                        # each pdf needs to define "signal", "backgroundPass", "backgroundFail" pdfs, "efficiency[0.9,0,1]" 
                                        # and "signalFractionInPassing[0.9]" are used for initial values  
                                        PDFs = cms.PSet(
        pdfSignalPlusBackground = cms.vstring(
            #"ZGeneratorLineShape::signalPhy(mass, \"../data/ZmmGenLevel.root\")", 
            "RooBreitWigner::signalPhy(mass,jpsiMass[3.097],jpsiW[0.0001])", # ~100keV total width
            "Gaussian::signalRes(mass, meanSmear[0,-0.2,0.2], widthSmear[0.05,0.01,0.1])",
            "RooCMSShape::backgroundPass(mass, alphaPass[0.1], betaPass[0.02, 0.,0.1], gammaPass[0.1, 0, 1], peakPass[4.0])",
            "RooCMSShape::backgroundFail(mass, alphaFail[0.1], betaFail[0.02, 0.,0.1], gammaFail[0.1, 0, 1], peakFail[4.0])",
            "FCONV::signalPass(mass, signalPhy, signalRes)",
            "FCONV::signalFail(mass, signalPhy, signalRes)",     
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[1.0]"     
            ),
                                                        ),
                                        )

# Set categories
setattr(process.TnPMeasurement.Categories, options.idName, cms.vstring(options.idName, "dummy[pass=1,fail=0]"))
setattr(process.TnPMeasurement.Categories, "mcTrue", cms.vstring("MC true", "dummy[true=1,false=0]"))
if len(options.conditions) > 0 :
    for condition in options.conditions :
        setattr(process.TnPMeasurement.Categories, condition, cms.vstring(condition, "dummy[true=1,false=0]"))

# Actual efficiency pset
effName = options.idName
if options.isMC :
    effName += '_mcTrue'
if len(options.conditions) > 0 :
    for condition in options.conditions :
        effName += '_'+condition

process.TnPMeasurement.Efficiencies = cms.PSet()
setattr(process.TnPMeasurement.Efficiencies, effName, cms.PSet(
            EfficiencyBinningSpecification,
            EfficiencyCategoryAndState = cms.vstring(options.idName, "pass")
            )
       )

# MC weight
#if options.isMC :
#    setattr(process.TnPMeasurement, 'WeightVariable', cms.string("totWeight"))

# Templates
pdfDef = cms.vstring(
    #"Gaussian::signalResPass(mass,meanPSmearing[0.0,-0.200,0.200],sigmaPSmearing[0.05,0.01,0.100])",
    #"Gaussian::signalResFail(mass,meanFSmearing[0.0,-0.200,0.200],sigmaFSmearing[0.05,0.01,0.100])",
    "Gaussian::signalRes(mass,meanSmearing[0.0,-0.200,0.200],sigmaSmearing[0.05,0.01,0.100])",
    "RooCMSShape::backgroundPass(mass, alphaPass[0.1], betaPass[0.02, 0.,0.1], gammaPass[0.1, 0, 1], peakPass[4.0])",
    "RooCMSShape::backgroundFail(mass, alphaFail[0.1], betaFail[0.02, 0.,0.1], gammaFail[0.1, 0, 1], peakFail[4.0])",
    "FCONV::signalPass(mass, signalPhyPass, signalRes)",
    "FCONV::signalFail(mass, signalPhyFail, signalRes)",     
    "efficiency[%f,0,1]" % options.startEfficiency,
    "signalFractionInPassing[1.0]"     
    )
if options.mcTemplateFile :
    for absetabin in range(len(EfficiencyBins.probe_abseta)-1) :
        for ptbin in range(len(EfficiencyBins.probe_pt)-1) :
            pdfName = "probe_abseta_bin%d__probe_pt_bin%d" % (absetabin, ptbin)
            thisDef = cms.vstring(
                    'ZGeneratorLineShape::signalPhyPass(mass, "%s", "%s")' % (options.mcTemplateFile, 'hMass_%s_Pass' % pdfName),
                    'ZGeneratorLineShape::signalPhyFail(mass, "%s", "%s")' % (options.mcTemplateFile, 'hMass_%s_Fail' % pdfName)
                )
            setattr(process.TnPMeasurement.PDFs, 'pdfSignal_'+pdfName, thisDef+pdfDef)

# switch pdf settings
if (not options.isMC):
    for pdf in process.TnPMeasurement.PDFs.__dict__:
        param =  process.TnPMeasurement.PDFs.getParameter(pdf)
        if (type(param) is not cms.vstring):
            continue
        for i, l in enumerate(getattr(process.TnPMeasurement.PDFs, pdf)):
            if l.find("signalFractionInPassing") != -1:
                getattr(process.TnPMeasurement.PDFs, pdf)[i] = l.replace("[1.0]","[0.5,0.,1.]")
else:
    for pdf in process.TnPMeasurement.PDFs.__dict__:
        param =  process.TnPMeasurement.PDFs.getParameter(pdf)
        if (type(param) is not cms.vstring):
            continue
        for i, l in enumerate(getattr(process.TnPMeasurement.PDFs, pdf)):
            if l.find("backgroundPass") != -1:
                getattr(process.TnPMeasurement.PDFs, pdf)[i] = "RooPolynomial::backgroundPass(mass, a[0.0])"
            if l.find("backgroundFail") != -1:
                getattr(process.TnPMeasurement.PDFs, pdf)[i] = "RooPolynomial::backgroundFail(mass, a[0.0])"

process.fit = cms.Path(
    process.TnPMeasurement  
    )

