#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
from Analysis.DiBosonTP.PassFailSimulFitter import PassFailSimulFitter

def main() :
    fitVariable = ROOT.RooRealVar('mass', 'TP Pair Mass', 60, 120, 'GeV')
    fitVariable.setBins(60)

    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
    ROOT.Math.MinimizerOptions.SetDefaultTolerance(1.e-2) # default is 1.e-2

    fmc = ROOT.TFile.Open('TnPTree_mc.root')
    tmc = fmc.Get('GsfElectronToRECO/fitter_tree')

    fmcAlt = ROOT.TFile.Open('TnPTree_mcLO.root')
    tmcAlt = fmcAlt.Get('GsfElectronToRECO/fitter_tree')

    fdata = ROOT.TFile.Open('TnPTree_data.root')
    tdata = fdata.Get('GsfElectronToRECO/fitter_tree')

    mcTruthCondition = ['mcTrue']

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
        fitter.addDataFromTree(tmc, 'mcData', allProbeCondition+mcTruthCondition, passingProbeCondition, separatePassFail = True)
        fitter.addDataFromTree(tmcAlt, 'mcAltData', allProbeCondition+mcTruthCondition, passingProbeCondition, separatePassFail = True)
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
        fitter.addDataFromTree(tdata, 'data', allProbeCondition, passingProbeCondition)
        res = fitter.fit('simPdf', 'data')
        effValue = res.floatParsFinal().find('efficiency')
        dataEff = effValue.getVal()
        dataEffErrHi = effValue.getErrorHi()
        dataEffErrLo = effValue.getErrorLo()
        scaleFactor = dataEff / mcEff
        maxSf = (dataEff+dataEffErrHi)/mcEffLo
        minSf = (dataEff+dataEffErrLo)/mcEffHi
        res.SetName('fitresults')
        c = fitter.drawFitCanvas(res)
        c.Write()
        h.Write()
        res.Write()

        print '-'*40, 'Fit with alternate MC template'
        resAlt = fitter.fit('simAltPdf', 'data')
        dataAltEff = resAlt.floatParsFinal().find('efficiency').getVal()
        resAlt.SetName('fitresults_systAltTemplate')
        resAlt.Write()

        print '-'*40, 'Fit with tag pt > 30 (vs. 25)'
        fitter.addDataFromTree(tdata, 'dataTagPt30', allProbeCondition+['tag_Ele_pt>30'], passingProbeCondition)
        resTagPt30 = fitter.fit('simPdf', 'dataTagPt30')
        dataTagPt30Eff = resTagPt30.floatParsFinal().find('efficiency').getVal()
        resTagPt30.Write()

        print '-'*40, 'Fit with CMSShape background (vs. Bernstein)'
        resCMSBkg = fitter.fit('simCMSBkgPdf', 'data')
        dataCMSBkgEff = resCMSBkg.floatParsFinal().find('efficiency').getVal()
        resCMSBkg.Write()

        fitter.workspace.Write()
        print name, ': Data=%.2f, MC=%.2f, Ratio=%.2f' % (dataEff, mcEff, dataEff/mcEff)
        condition = ' && '.join(allProbeCondition+[passingProbeCondition])
        variations = {
                'CENTRAL'  : (scaleFactor, res),
                'STAT_UP'  : (maxSf, res),
                'STAT_DOWN': (minSf, res),
                'SYST_ALT_TEMPL' : (dataAltEff / mcEff, resAlt),
                'SYST_TAG_PT30' : (dataTagPt30Eff / mcEff, resTagPt30),
                'SYST_CMSSHAPE' : (dataCMSBkgEff / mcEff, resCMSBkg),
                'EFF_DATA' : (dataEff, res),
                'EFF_DATA_ERRSYM' : ((dataEffErrHi-dataEffErrLo)/2, res),
                'EFF_MC' : (mcEff, res),
                'EFF_MC_ERRSYM' : ((mcEffHi-mcEffLo)/2, res),
                }
        cutString = ''
        for varName, value in variations.items() :
            (value, fitResult) = value
            cutString += '    if ( variation == Variation::%s && (%s) ) return %f;\n' % (varName, condition, value)
            print '  Variation {:>15s} : {:.4f}, edm={:f}, status={:s}'.format(varName, value, fitResult.edm(), statusInfo(fitResult))
            if 'STAT' not in varName and 'EFF' not in varName and fitResult.statusCodeHistory(0) < 0 :
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
            'pt07to10' : ['probe_Ele_pt>7 && probe_Ele_pt<10'],
            'pt10to20' : ['probe_Ele_pt>10 && probe_Ele_pt<20'],
            'pt20to30' : ['probe_Ele_pt>20 && probe_Ele_pt<30'],
            'pt30to40' : ['probe_Ele_pt>30 && probe_Ele_pt<40'],
            'pt40to50' : ['probe_Ele_pt>40 && probe_Ele_pt<50'],
            'pt50toInf' : ['probe_Ele_pt>50'],
            }

    etaBinning = {
            'abseta0p0to0p8' : ['probe_Ele_abseta < 0.8'],
            'abseta0p8to1p479' : ['probe_Ele_abseta > 0.8 && probe_Ele_abseta < 1.479'],
            'abseta1p479to2p0' : ['probe_Ele_abseta > 1.479 && probe_Ele_abseta < 2.0'],
            'abseta2p0to2p5' : ['probe_Ele_abseta > 2.0 && probe_Ele_abseta < 2.5'],
            }
    
    binning = {}
    for name1, cut1 in ptBinning.items() :
        if name1 is 'pt07to10' :
            binning[name1] = cut1
            continue
        for name2, cut2 in etaBinning.items() :
            binning[name1+'_'+name2] = cut1+cut2

    commonVars = ['float probe_Ele_pt', 'float probe_Ele_abseta']

    fout = ROOT.TFile('fits.root', 'recreate')
    fout.mkdir('electronFits').cd()

    fit('ZZLoose', [], 'passingZZLoose', binning, commonVars+['bool passingZZLoose'])
    fit('ZZTight', [], 'passingZZTight', binning, commonVars+['bool passingZZTight'])
    fit('ZZIso_wrtLoose', ['passingZZLoose'], 'passingZZIso', binning, commonVars+['bool passingZZLoose','bool passingZZIso'])
    fit('ZZIso_wrtTight', ['passingZZTight'], 'passingZZIso', binning, commonVars+['bool passingZZTight','bool passingZZIso'])

if __name__ == '__main__' :
    main()
