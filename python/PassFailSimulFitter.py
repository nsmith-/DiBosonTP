#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

class PassFailSimulFitter :
    def _wsimport(self, *args) :
        # getattr since import is special in python
        # NB RooWorkspace clones object
        if len(args) < 2 :
            # Useless RooCmdArg: https://sft.its.cern.ch/jira/browse/ROOT-6785
            args += (ROOT.RooCmdArg(),)
        return getattr(self.workspace, 'import')(*args)

    def __init__(self, name, fitVariable) :
        self.workspace = ROOT.RooWorkspace(name)
        self._wsimport(fitVariable)
        self._fitVar = self.workspace.var(fitVariable.GetName())
        self.workspace.factory("decision[Passed,Failed]")

    def setPdf(self, pdfDefinition) :
        for line in pdfDefinition :
            self.workspace.factory(line)

    def setData(self, passed, failed) :
        # TODO: check passing failing hists for consistency
        nPass = passed.Integral()
        nFail = failed.Integral()
        if nPass == 0 or nFail == 0 :
            print 'WARNING: No passing or failing data!'
        m = ROOT.std.map('string, TH1*')()
        # const string: https://root.cern.ch/phpBB3/viewtopic.php?f=15&t=16882&start=15#p86985
        m.insert(ROOT.std.pair('const string, TH1*')('Passed', passed))
        m.insert(ROOT.std.pair('const string, TH1*')('Failed', failed))
        data = ROOT.RooDataHist('data', 'dataset', ROOT.RooArgList(self._fitVar), self.workspace.cat('decision'), m)
        self._wsimport(data)

    def fit(self, pdfName, dataName) :
        w = self.workspace
        rf = ROOT.RooFit
        pdf = w.pdf(pdfName)
        data = w.data(dataName)

        # Initialize some parameters
        signalFractionPassing = 0.9
        nPass = data.sumEntries('decision==decision::Passed')
        nFail = data.sumEntries('decision==decision::Failed')
        initialEff = w.var('efficiency').getVal()
        nSignal = nPass*signalFractionPassing/initialEff
        w.var('numSignalAll').setVal(nSignal)
        if w.var('numBackgroundPass') :
            w.var('numBackgroundPass').setVal(nPass-nSignal*initialEff)
            w.var('numBackgroundFail').setVal(nPass-max(nSignal*(1-initialEff), nFail))
        w.saveSnapshot('preFit', w.components())

        minosVars = ROOT.RooArgSet(w.var('efficiency'))
        args = [
            rf.Save(True),
            rf.Minos(minosVars),
            rf.Verbose(False),
            rf.PrintLevel(-1),
            rf.Minimizer("Minuit2","Migrad"),
        ]
        result = pdf.fitTo(data, *args)
        w.saveSnapshot('postFit', w.components())
        return result

    def drawFitCanvas(self, pdfName, dataName) :
        w = self.workspace
        fitVar = self._fitVar
        rf = ROOT.RooFit

        passFrame = fitVar.frame(rf.Name("Passing"), rf.Title('Passing Probes'))
        failFrame = fitVar.frame(rf.Name('Failing'), rf.Title('Failing Probes'))
        allFrame  = fitVar.frame(rf.Name('All'),     rf.Title('All Probes'))

        pdf = w.pdf(pdfName)
        data = w.data(dataName)
        datapass = data.reduce(rf.Cut('decision==decision::Passed'))
        datafail = data.reduce(rf.Cut('decision==decision::Failed'))

        datapass.plotOn(passFrame)
        pdf.plotOn(passFrame, rf.Slice(w.cat('decision'), 'Passed'), rf.ProjWData(datapass), rf.LineColor(ROOT.kGreen))
        if w.pdf('backgroundPass') :
            pdf.plotOn(passFrame, rf.Slice(w.cat('decision'), 'Passed'), rf.ProjWData(datapass), rf.LineColor(ROOT.kGreen), rf.Components('backgroundPass'), rf.LineStyle(ROOT.kDashed))

        datafail.plotOn(failFrame)
        pdf.plotOn(failFrame, rf.Slice(w.cat('decision'), 'Failed'), rf.ProjWData(datafail), rf.LineColor(ROOT.kRed))
        if w.pdf('backgroundFail') :
            pdf.plotOn(failFrame, rf.Slice(w.cat('decision'), 'Failed'), rf.ProjWData(datafail), rf.LineColor(ROOT.kRed), rf.Components('backgroundFail'), rf.LineStyle(ROOT.kDashed))

        data.plotOn(allFrame)
        pdf.plotOn(allFrame, rf.ProjWData(data))
        if w.pdf('backgroundPass') :
            pdf.plotOn(allFrame, rf.ProjWData(data), rf.LineColor(ROOT.kBlue), rf.Components('backgroundPass,backgroundFail'), rf.LineStyle(ROOT.kDashed))

        # infoFrame is a placeholder
        infoFrame = fitVar.frame(rf.Name("Fit Results"), rf.Title("Fit Results"))
        dispParams = pdf.getParameters(data)
        pdf.paramOn(infoFrame, rf.Format('NE'), rf.Layout(0.15, 0.95, 0.95), rf.Parameters(dispParams))
        paramBox = infoFrame.findObject('%s_paramBox'%pdf.GetName())

        c = ROOT.TCanvas('fit_canvas', 'Fit Canvas', 700, 500)
        c.Divide(2,2)
        c.cd(1)
        passFrame.Draw()
        c.cd(2)
        failFrame.Draw()
        c.cd(3)
        allFrame.Draw()
        c.cd(4)
        paramBox.Draw()
        for obj in [passFrame, failFrame, allFrame, infoFrame] :
            ROOT.SetOwnership(obj, False)
        c.GetListOfPrimitives().SetOwner(True)
        return c

