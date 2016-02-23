#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
from Analysis.DiBosonTP.PassFailSimulFitter import PassFailSimulFitter

pdfDefData = [
        'RooBreitWigner::signalPhy(mass, 91, 2.5)',
        'Gaussian::signalResPass(mass,meanSmearing[1.0,-1.0,2.0],sigmaSmearing[0.5,0.07,3.0])',
        'Gaussian::signalResFail(mass,meanSmearing              ,sigmaSmearing              )',
        'RooBernstein::backgroundPass(mass, {a0[10,0,50],a1[1,0,50],a2[1,0,50],a3[1,0,50]})',
        'RooBernstein::backgroundFail(mass, {b0[10,0,50],b1[1,0,50],b2[1,0,50],b3[1,0,50]})',
        'FCONV::signalPass(mass, signalPhy, signalResPass)',
        'FCONV::signalFail(mass, signalPhy, signalResFail)',
        'efficiency[0.9,0,1]',
        "expr::numSignalPass('efficiency*numSignalAll', efficiency, numSignalAll[10.,10000000000])",
        "expr::numSignalFail('(1-efficiency)*numSignalAll', efficiency, numSignalAll)",
        "SUM::pdfPass(numSignalPass*signalPass, numBackgroundPass[0.,1000000000]*backgroundPass)",
        "SUM::pdfFail(numSignalFail*signalFail, numBackgroundFail[0.,1000000000]*backgroundFail)",
        "SIMUL::simPdf(decision, Passed=pdfPass, Failed=pdfFail)",
        ]


def main() :
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
            ]
    fitVariable = ROOT.RooRealVar('mass', 'TP Pair Mass', 60, 120, 'GeV')

    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
    ROOT.gStyle.SetOptTitle(True)

    f = ROOT.TFile.Open('TnPTree_mc.root')
    t = f.Get('GsfElectronToRECO/fitter_tree')

    def fit(name, allProbeCondition, passingProbeCondition) :
        hpass = ROOT.TH1F(name+'_passed_probes', '', 60,60,120)
        hfail = hpass.Clone(name+'_failed_probes')
        if type(allProbeCondition) is list :
            allProbeCondition = '&&'.join(allProbeCondition)
        t.Draw('mass >> %s_passed_probes' % name, 'totWeight*(%s)*(%s)' % (allProbeCondition, passingProbeCondition), 'goff')
        t.Draw('mass >> %s_failed_probes' % name, 'totWeight*(%s)*!(%s)' % (allProbeCondition, passingProbeCondition), 'goff')
        if hfail.Integral() < 1 :
            print 'No failed probes for cut:', '(%s)*!(%s)' % (allProbeCondition, passingProbeCondition)
            return
        fitter = PassFailSimulFitter(name, fitVariable)
        fitter.setPdf(pdfDef)
        fitter.setData(hpass, hfail)
        res = fitter.fit('simPdf', 'data')
        c = fitter.drawFitCanvas()
        c.Print('plots/fit_%s.png' % name)
        fout = ROOT.TFile('plots/fit_%s.root' % name, 'recreate')
        d = fout.mkdir('fit_output')
        d.cd()
        c.Write()
        res.Write()
        fitter.workspace.Write()
        fout.Close()

    mcCond = ['mcTrue']

    fit('ZZTight_pt7to15',  mcCond+['probe_Ele_pt>7 && probe_Ele_pt<15'], 'passingZZTight')
    fit('ZZTight_pt15to30', mcCond+['probe_Ele_pt>15 && probe_Ele_pt<30'], 'passingZZTight')
    fit('ZZTight_pt30to50', mcCond+['probe_Ele_pt>30 && probe_Ele_pt<50'], 'passingZZTight')

    fit('ZZLoose_pt7to15',  mcCond+['probe_Ele_pt>7 && probe_Ele_pt<15'], 'passingZZLoose')
    fit('ZZLoose_pt15to30', mcCond+['probe_Ele_pt>15 && probe_Ele_pt<30'], 'passingZZLoose')
    fit('ZZLoose_pt30to50', mcCond+['probe_Ele_pt>30 && probe_Ele_pt<50'], 'passingZZLoose')

    fit('ZZIso_pt7to15',  mcCond+['probe_Ele_pt>7 && probe_Ele_pt<15'],  'passingZZIso')
    fit('ZZIso_pt15to30', mcCond+['probe_Ele_pt>15 && probe_Ele_pt<30'], 'passingZZIso')
    fit('ZZIso_pt30to50', mcCond+['probe_Ele_pt>30 && probe_Ele_pt<50'], 'passingZZIso')

if __name__ == '__main__' :
    main()
