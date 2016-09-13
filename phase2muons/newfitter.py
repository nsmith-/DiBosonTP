#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
from Analysis.DiBosonTP.PassFailSimulFitter import PassFailSimulFitter
import sys

def main() :
    fitVariable = ROOT.RooRealVar('mass', 'TP Pair Mass', 60, 120, 'GeV')
    fitVariable.setBins(60)

    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
    ROOT.Math.MinimizerOptions.SetDefaultTolerance(1.e-2) # default is 1.e-2

    fmc = ROOT.TFile.Open(sys.argv[-1])
    tmc = fmc.Get('muonEffs/fitter_tree')

    mcTruthCondition = ['mcTrue', 'mc_probe_isPromptFinalState']

    pdfDefinition = []
    with open('pdfDefinition.txt') as defFile :
        for line in defFile :
            line = line.strip()
            if len(line) == 0 or line[0] is '#' :
                continue
            pdfDefinition.append(line)


    def statusInfo(fitResults) :
        fitStatus=':'.join(['% d' % fitResults.statusCodeHistory(i) for i in range(fitResults.numStatusHistory())]),
        return fitStatus

    def fitBin(name, allProbeCondition, passingProbeCondition) :
        ROOT.gDirectory.mkdir(name).cd()
        fitter = PassFailSimulFitter(name, fitVariable)
        fitter.addDataFromTree(tmc, 'mcData', allProbeCondition+mcTruthCondition, passingProbeCondition, separatePassFail = True, weightVariable='weight')
        nMCPass = fitter.workspace.data('mcDataPass').sumEntries()
        nMCFail = fitter.workspace.data('mcDataFail').sumEntries()
        mcEff = nMCPass/(nMCPass+nMCFail)
        mcEffLo = ROOT.TEfficiency.ClopperPearson(int(nMCPass+nMCFail), int(nMCPass), 0.68, False)
        mcEffHi = ROOT.TEfficiency.ClopperPearson(int(nMCPass+nMCFail), int(nMCPass), 0.68, True)
        h=ROOT.TH1F('mc_cutCount', 'Cut & Count', 2, 0, 2)
        h.SetBinContent(1, nMCPass)
        h.SetBinContent(2, nMCPass+nMCFail)

        # All MC templates must be set up by now
        fitter.setPdf(pdfDefinition)

        print '-'*40, 'Central value fit'
        fitter.addDataFromTree(tmc, 'data', allProbeCondition, passingProbeCondition, weightVariable='weight')
        res = fitter.fit('simPdf', 'data')
        effValue = res.floatParsFinal().find('efficiency')
        dataEff = effValue.getVal()
        dataEffErrHi = effValue.getErrorHi()
        dataEffErrLo = effValue.getErrorLo()
        res.SetName('fitresults')
        c = fitter.drawFitCanvas(res)
        c.Write()
        h.Write()
        res.Write()

        fitter.workspace.Write()
        print name, ': Data=%.2f, MC=%.2f, Ratio=%.2f' % (dataEff, mcEff, dataEff/mcEff)
        condition = ' && '.join(allProbeCondition)
        variations = {
                'EFF_CUTCOUNT' : (mcEff, res),
                'EFF_CUTCOUNT_UP' : (mcEffHi, res),
                'EFF_CUTCOUNT_DOWN' : (mcEffLo, res),
                'EFF_FIT' : (mcEff, res),
                'EFF_FIT_UP' : (mcEffHi, res),
                'EFF_FIT_DOWN' : (mcEffLo, res),
                }
        cutString = ''
        for varName, value in variations.items() :
            (value, fitResult) = value
            cutString += '    if ( variation == Variation::%s && (%s) ) return %f;\n' % (varName, condition, value)
            print '  Variation {:>15s} : {:.4f}, edm={:f}, status={:s}'.format(varName, value, fitResult.edm(), statusInfo(fitResult))
            if 'EFF_FIT' == varName and fitResult.statusCodeHistory(0) < 0 :
                cBad = fitter.drawFitCanvas(fitResult)
                cBad.Print('badFit_%s_%s.png' %(name, varName))

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
            'pt10to30' : ['probe_pt>10 && probe_pt<30'],
            'pt30to50' : ['probe_pt>30 && probe_pt<50'],
            'pt50toInf' : ['probe_pt>50'],
            }

    etaBinning = {
            'abseta0p0to1p2' : ['probe_abseta < 1.2'],
            'abseta1p2to2p4' : ['probe_abseta >= 1.2 && probe_abseta < 2.4'],
            }
    
    binning = {}
    for name1, cut1 in ptBinning.items() :
        for name2, cut2 in etaBinning.items() :
            binning[name1+'_'+name2] = cut1+cut2

    commonVars = ['float probe_pt', 'float probe_abseta']

    fout = ROOT.TFile('fits.root', 'recreate')
    fout.mkdir('muonFits').cd()

    fit('WZLoose', [], 'passingIDWZLoose', binning, commonVars)
    fit('Tight', [], 'passingTightID', binning, commonVars)
    fit('RelIso0p4', ['passingTightID'], 'passingIsoWZLoose', binning, commonVars+['bool passingTightID'])
    fit('RelIso0p12', ['passingTightID'], 'passingIsoWZTight', binning, commonVars+['bool passingTightID'])

if __name__ == '__main__' :
    main()
