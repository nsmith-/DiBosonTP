#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import array
import sys
import subprocess
__gitversion__ = subprocess.check_output(["git", "describe", "--always"]).strip()

#idName = 'ZZLoose'
#idNameNice = 'ZZ Loose ID'
idName = sys.argv[1]
idNameNice = sys.argv[2]

ptbins = [10.,30.,50., 80.]
etabins = [0.,1.2,2.4]
colors = [ROOT.kRed, ROOT.kGreen, ROOT.kBlue, ROOT.kBlack]

ROOT.gROOT.ProcessLine('.L plots/{id}/{id}.C+'.format(id=idName))

variations = [
    ROOT.EFF_FIT_UP,
    ROOT.EFF_FIT_DOWN,
    ]

if 'Iso' in idName :
    eff = lambda pt, eta, var : getattr(ROOT, idName)(pt, eta, True, var)
else :
    eff = lambda pt, eta, var : getattr(ROOT, idName)(pt, eta, var)

effCentral = lambda pt, eta : eff(pt, eta, ROOT.EFF_FIT)
effMax = lambda pt, eta : max(map(lambda v : eff(pt,eta,v), variations))-effCentral(pt,eta)
effMin = lambda pt, eta : effCentral(pt,eta)-min(map(lambda v : eff(pt,eta,v), variations))


xbins = array.array('d', [0.5*sum(ptbins[i:i+2]) for i in range(len(ptbins)-1)])
xlo  = lambda bins: array.array('d', map(lambda (a,b): a-b, zip(bins, ptbins)))
xhi  = lambda bins: array.array('d', map(lambda (a,b): a-b, zip(ptbins[1:], bins)))

def y(eta) : return array.array('d', map(lambda pt : effCentral(pt, eta), xbins))
def eyl(eta) : return array.array('d', map(lambda pt : effMin(pt, eta), xbins))
def eyh(eta) : return array.array('d', map(lambda pt : effMax(pt, eta), xbins))

canvas = ROOT.TCanvas()
mg = ROOT.TMultiGraph('alletaBins', ';Probe p_{T};Scale Factor')

minEff = 1.
for i in range(len(etabins)-1) :
    eta = .5*sum(etabins[i:i+2])
    bins2 = array.array('d', [b-1.5+i for b in xbins])
    graph = ROOT.TGraphAsymmErrors(len(xbins), bins2, y(eta), xlo(bins2), xhi(bins2), eyl(eta), eyh(eta))
    minEff = min(minEff, min(y(eta)))
    graph.SetName('eff_etaBin%d'%i)
    graph.SetTitle('%.1f #leq |#eta| #leq %.1f' % tuple(etabins[i:i+2]))
    graph.SetMarkerColor(colors[i])
    graph.SetLineColor(colors[i])
    mg.Add(graph, 'p')

mg.SetMinimum(0.1*int(minEff*10))
mg.SetMaximum(1.05)
mg.Draw('a')
leg = canvas.BuildLegend(.5,.2,.9,.4)
for entry in leg.GetListOfPrimitives() :
    entry.SetOption('lp')
leg.SetHeader(idNameNice)

canvas.Print('plots/%s/scaleFactor_vs_pt.png'%idName)
canvas.Print('plots/%s/scaleFactor_vs_pt.root'%idName)

