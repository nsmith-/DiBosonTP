import ROOT
import glob
f0 = ROOT.TFile('pu0.root')
f35 = ROOT.TFile('pu35.root')
f140 = ROOT.TFile('pu140.root')
f200 = ROOT.TFile('pu200.root')

t0 = f0.Get('muonEffs/fitter_tree')
t35 = f35.Get('muonEffs/fitter_tree')
t140 = f140.Get('muonEffs/fitter_tree')
t200 = f200.Get('muonEffs/fitter_tree')

trees = [t0, t35, t140, t200]
map(lambda t: t.SetLineWidth(2), trees)
t0.SetLineColor(ROOT.kRed)
t35.SetLineColor(ROOT.kGreen)
t140.SetLineColor(ROOT.kBlue)
t200.SetLineColor(ROOT.kBlack)

pfRelIso = "(probe_chargedHadronIsoR04 + max(0, probe_neutralHadronIsoR04 + probe_photonIsoR04 - 0.5*probe_pileupIsoR04))/probe_pt >> hRelIsoPu%d(50, 0, 1)"
maxPart = "(probe_neutralHadronIsoR04 + probe_photonIsoR04 - 0.5*probe_pileupIsoR04)/probe_pt >> hRelIsoPu%d(50, -2, 2)"

drawStr = pfRelIso
#title = "(#Sum E_{h^0} + E_{#gamma} - 0.5*E_{PU}) / p_{T,#mu}"
title = "PF Relative Isolation R<0.4 w/#Delta#beta"

t0.Draw(drawStr % 0, "mcTrue&&mc_probe_isPromptFinalState")
t0.GetHistogram().SetTitle("<PU>=0")
t0.GetHistogram().GetXaxis().SetTitle(title)
t35.Draw(drawStr % 35, "mcTrue&&mc_probe_isPromptFinalState", "same")
t35.GetHistogram().SetTitle("<PU>=35")
t140.Draw(drawStr % 140, "mcTrue&&mc_probe_isPromptFinalState", "same")
t140.GetHistogram().SetTitle("<PU>=140")
t200.Draw(drawStr % 200, "mcTrue&&mc_probe_isPromptFinalState", "same")
t200.GetHistogram().SetTitle("<PU>=200")
ROOT.gPad.BuildLegend()
