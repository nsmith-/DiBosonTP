#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
from Analysis.DiBosonTP.PassFailSimulFitter import PassFailSimulFitter



def main() :
    # DEMO
    pdfDef = [
            'RooBreitWigner::signalPhy(mass, 91, 2.5)',
            'Gaussian::signalResPass(mass,meanSmearing[1.0,-1.0,2.0],sigmaSmearing[0.5,0.07,3.0])',
            'Gaussian::signalResFail(mass,meanSmearing              ,sigmaSmearing              )',
            'RooBernstein::backgroundPass(mass, {a0[10,0,50],a1[1,0,50],a2[1,0,50],a3[1,0,50]})',
            'RooBernstein::backgroundFail(mass, {b0[10,0,50],b1[1,0,50],b2[1,0,50],b3[1,0,50]})',
            'FCONV::signalPass(mass, signalPhy, signalResPass)',
            'FCONV::signalFail(mass, signalPhy, signalResFail)',
            'efficiency[0.9,0,1]',
            ]
    fitVariable = ROOT.RooRealVar('mass', 'TP Pair Mass', 60, 120, 'GeV')

    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
    ROOT.gStyle.SetOptTitle(True)

    f = ROOT.TFile.Open('TnPTree_mc.root')
    t = f.Get('GsfElectronToRECO/fitter_tree')

    def fit(name, allProbeCondition, passingProbeCondition) :
        hpass = ROOT.TH1F('passed_probes', '', 60,60,120)
        hfail = hpass.Clone('failed_probes')
        t.Draw('mass >> passed_probes', '(%s)*(%s)' % (allProbeCondition, passingProbeCondition), 'goff')
        t.Draw('mass >> failed_probes', '(%s)*!(%s)' % (allProbeCondition, passingProbeCondition), 'goff')
        if hfail.Integral() < 1 :
            print 'No failed probes for cut:', '(%s)*!(%s)' % (allProbeCondition, passingProbeCondition)
            return
        fitter = PassFailSimulFitter(name, pdfDef, fitVariable)
        fitter.setData(hpass, hfail)
        res = fitter.fit()
        c = fitter.drawFitCanvas()
        c.Print('plots/fit_%s.png' % name)
        fout = ROOT.TFile('plots/fit_%s.root' % name, 'recreate')
        d = fout.mkdir('fit_output')
        d.cd()
        c.Write()
        res.Write()
        fitter.workspace.Write()
        fout.Close()

    fit('ZZTight_pt7to15', 'probe_Ele_pt>7 && probe_Ele_pt<15', 'passingZZTight')
    fit('ZZTight_pt15to30', 'probe_Ele_pt>15 && probe_Ele_pt<30', 'passingZZTight')
    fit('ZZTight_pt30to50', 'probe_Ele_pt>30 && probe_Ele_pt<50', 'passingZZTight')

    fit('ZZLoose_pt7to15', 'probe_Ele_pt>7 && probe_Ele_pt<15', 'passingZZLoose')
    fit('ZZLoose_pt15to30', 'probe_Ele_pt>15 && probe_Ele_pt<30', 'passingZZLoose')
    fit('ZZLoose_pt30to50', 'probe_Ele_pt>30 && probe_Ele_pt<50', 'passingZZLoose')

#    from IPython import embed
#    embed()

if __name__ == '__main__' :
    main()
