import ROOT

# DZ has more stuff
data = ROOT.TFile('../muons/TnPTreeDZ_data.root')
mc = ROOT.TFile('../muons/TnPTreeDZ_mc.root')

datatree = data.Get('trackerMuonDZTree/fitter_tree')
mctree = mc.Get('trackerMuonDZTree/fitter_tree')

datatree.Draw('event_nPV >> hdata(60, 0, 60)')
#mctree.Draw('event_nPV >> hmc(60, 0, 60)', 'totWeight')
mctree.Draw('event_nPV >> hmcunweight(60, 0, 60)', 'weight/abs(weight)')

hdata = ROOT.gDirectory.Get('hdata')
hmcunweight = ROOT.gDirectory.Get('hmcunweight')

hdata.SetNormFactor(1.)
hmcunweight.SetNormFactor(1.)

#hdata.Draw('ex0hist')
#hmcunweight.Draw('ex0histsame')

dataFile = ROOT.TFile('puWeightData.root', 'recreate')
dataFile.cd()
hdata.SetName('pileup')
hdata.Write()
dataFile.Close()

mcFile = ROOT.TFile('puWeightMC.root', 'recreate')
mcFile.cd()
hmcunweight.SetName('pileup')
hmcunweight.Write()
mcFile.Close()
