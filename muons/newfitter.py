#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
from Analysis.DiBosonTP.PassFailSimulFitter import PassFailSimulFitter

pdfDefData = [
        "RooHistPdf::mcTemplatePass(mass,mcDataPass)",
        "RooHistPdf::mcTemplateFail(mass,mcDataFail)",
        'Gaussian::signalRes(mass,meanSmearing[1.0,-1.0,2.0],sigmaSmearing[0.5,0.28,3.0])', # sigma > 1/sqrt(12)
        #'Gaussian::signalResFail(mass,meanSmearing              ,sigmaSmearing              )',
        'RooBernstein::backgroundPass(mass, {a0[10,0,50],a1[1,0,50],a2[1,0,50],a3[1,0,50]})',
        'RooBernstein::backgroundFail(mass, {b0[10,0,50],b1[1,0,50],b2[1,0,50],b3[1,0,50]})',
        'FCONV::signalPass(mass, mcTemplatePass, signalRes)',
        'FCONV::signalFail(mass, mcTemplateFail, signalRes)',
        'efficiency[0.9,0,1]',
        "expr::numSignalPass('efficiency*numSignalAll', efficiency, numSignalAll[10.,10000000000])",
        "expr::numSignalFail('(1-efficiency)*numSignalAll', efficiency, numSignalAll)",
        "SUM::pdfPass(numSignalPass*signalPass, numBackgroundPass[0.,1000000000]*backgroundPass)",
        "SUM::pdfFail(numSignalFail*signalFail, numBackgroundFail[0.,1000000000]*backgroundFail)",
        "SIMUL::simPdf(decision, Passed=pdfPass, Failed=pdfFail)",
        ]

# DEMO
pdfDef = [
        'RooBreitWigner::signalPhy(mass, 91, 2.5)',
        #'Gaussian::signalResPass(mass,meanSmearing[1.0,-1.0,2.0],sigmaSmearing[0.5,0.07,3.0])',
        #'Gaussian::signalResFail(mass,meanSmearing              ,sigmaSmearing              )',
        "RooCBExGaussShape::signalResPass(mass,meanP[-0.0,-5.000,5.000],sigmaP[0.956,0.00,15.000],alphaP[0.999, 0.0,50.0],nP[1.405,0.000,50.000],sigmaP_2[1.000,0.500,15.00])",
        "RooCBExGaussShape::signalResFail(mass,meanF[-0.0,-5.000,5.000],sigmaF[3.331,0.00,15.000],alphaF[1.586, 0.0,50.0],nF[0.464,0.000,20.00], sigmaF_2[1.675,0.500,12.000])",
        'FCONV::signalPass(mass, signalPhy, signalResPass)',
        'FCONV::signalFail(mass, signalPhy, signalResFail)',
        'Gaussian::signalSideband(mass, sbMean[75,60,90], sbSigma[5,3,20])',
        'sigSidebandFracPass[0.001,0,1]',
        'sigSidebandFracFail[0.001,0,1]',
        'efficiency[0.9,0,1]',
        "expr::numSignalPass('efficiency*numSignalAll', efficiency, numSignalAll[10.,10000000000])",
        "expr::numSignalPassPeak('(1-sigSidebandFracPass)*numSignalPass', sigSidebandFracPass, numSignalPass)",
        "expr::numSignalPassSB('sigSidebandFracPass*numSignalPass', sigSidebandFracPass, numSignalPass)",
        "expr::numSignalFail('(1-efficiency)*numSignalAll', efficiency, numSignalAll)",
        "expr::numSignalFailPeak('(1-sigSidebandFracFail)*numSignalFail', sigSidebandFracFail, numSignalFail)",
        "expr::numSignalFailSB('sigSidebandFracFail*numSignalFail', sigSidebandFracFail, numSignalFail)",
        'SUM::pdfPass(numSignalPassPeak*signalPass, numSignalPassSB*signalSideband)',
        'SUM::pdfFail(numSignalFailPeak*signalFail, numSignalFailSB*signalSideband)',
        "SIMUL::simPdf(decision, Passed=pdfPass, Failed=pdfFail)",
        'RooBernstein::backgroundPass(mass, {a0[10,0,50],a1[1,0,50],a2[1,0,50],a3[1,0,50]})',
        'RooBernstein::backgroundFail(mass, {b0[10,0,50],b1[1,0,50],b2[1,0,50],b3[1,0,50]})',
        "RooHistPdf::mcTemplatePass(mass,mcDataPass)",
        "RooHistPdf::mcTemplateFail(mass,mcDataFail)",
        ]

def main() :
    fitVariable = ROOT.RooRealVar('mass', 'TP Pair Mass', 60, 120, 'GeV')
    fitVariable.setBins(60)

    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)

    fmc = ROOT.TFile.Open('TnPTree_mc.root')
    tmc = fmc.Get('muonEffs/fitter_tree')

    fdata = ROOT.TFile.Open('TnPTree_data.root')
    tdata = fdata.Get('muonEffs/fitter_tree')

    def fitBin(name, allProbeCondition, passingProbeCondition) :
        ROOT.gDirectory.mkdir(name).cd()
        fitter = PassFailSimulFitter(name, fitVariable)
        fitter.addDataFromTree(tmc, 'mcData', allProbeCondition+['mcTrue'], passingProbeCondition, separatePassFail = True)
        nMCPass = fitter.workspace.data('mcDataPass').sumEntries()
        nMCFail = fitter.workspace.data('mcDataFail').sumEntries()
        mcEff = nMCPass/(nMCPass+nMCFail)
        h=ROOT.TH1F('mc_cutCount', 'Cut & Count', 2, 0, 2)
        h.SetBinContent(1, nMCPass)
        h.SetBinContent(2, nMCPass+nMCFail)
        fitter.addDataFromTree(tdata, 'data', allProbeCondition, passingProbeCondition)
        fitter.setPdf(pdfDefData)
        res = fitter.fit('simPdf', 'data')
        dataEff = res.floatParsFinal().find('efficiency').getVal()
        res.SetName('fitresults')
        c = fitter.drawFitCanvas('simPdf', 'data')
        c.Write()
        h.Write()
        res.Write()
        fitter.workspace.Write()
        print name, ': Data=%.2f, MC=%.2f, Ratio=%.2f' % (dataEff, mcEff, dataEff/mcEff)
        condition = ' && '.join(allProbeCondition+[passingProbeCondition])
        cutString = 'if ( %s ) return %f;' % (condition, dataEff/mcEff)
        print cutString
        ROOT.TNamed('cutString', cutString).Write()
        print
        ROOT.gDirectory.cd('..')

    def fit(name, allProbeCondition, passingProbeCondition, binningMap, macroVariables) :
        ROOT.gDirectory.mkdir(name).cd()
        ROOT.TNamed('variables', ', '.join(macroVariables)).Write()
        for binName, cut in sorted(binningMap.items()) :
            fitBin(name+'_'+binName, allProbeCondition+cut, passingProbeCondition)
        ROOT.gDirectory.cd('..')

    ptBinning = {
            'pt05to10' : ['probe_pt>5 && probe_pt<10'],
            'pt10to20' : ['probe_pt>10 && probe_pt<20'],
            'pt20to30' : ['probe_pt>20 && probe_pt<30'],
            'pt30to40' : ['probe_pt>30 && probe_pt<40'],
            'pt40to50' : ['probe_pt>40 && probe_pt<50'],
            'pt50toInf' : ['probe_pt>50'],
            }

    etaBinning = {
            'abseta0p0to0p9' : ['probe_abseta < 0.9'],
            'abseta0p9to1p2' : ['probe_abseta > 0.9 && probe_abseta < 1.2'],
            'abseta1p2to2p1' : ['probe_abseta > 1.2 && probe_abseta < 2.1'],
            'abseta2p1to2p4' : ['probe_abseta > 2.1 && probe_abseta < 2.4'],
            }
    
    binning = {}
    for name1, cut1 in ptBinning.items() :
        if name1 is 'pt05to10' :
            binning[name1] = cut1
            continue
        for name2, cut2 in etaBinning.items() :
            binning[name1+'_'+name2] = cut1+cut2

    commonVars = ['float probe_pt', 'float probe_abseta']

    fout = ROOT.TFile('fits.root', 'recreate')
    fout.mkdir('muonFits').cd()

    fit('ZZLoose', [], 'passingIDZZLoose', binning, commonVars+['bool passingIDZZLoose'])
    fit('ZZTight', [], 'passingIDZZTight', binning, commonVars+['bool passingIDZZTight'])
    fit('ZZIso_wrtLoose', ['passingIDZZLoose'], 'passingIsoZZ', binning, commonVars+['bool passingIDZZLoose','bool passingIsoZZ'])
    fit('ZZIso_wrtTight', ['passingIDZZTight'], 'passingIsoZZ', binning, commonVars+['bool passingIDZZTight','bool passingIsoZZ'])

if __name__ == '__main__' :
    main()
