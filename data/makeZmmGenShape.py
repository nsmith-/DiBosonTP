#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)

ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Handle, Events

genParticles = Handle("std::vector<reco::GenParticle>")
genWeights = Handle("GenEventInfoProduct")

events = Events(sys.argv[1])

outFile = ROOT.TFile(sys.argv[2], 'recreate')
hGen = ROOT.TH1F('Mass', 'Z#rightarrow #mu#mu Gen-level Mass', 2000, 0, 200.)

for iev,event in enumerate(events):
    if iev%1000 == 0 :
        print "Done with %d events" % iev
    event.getByLabel('prunedGenParticles', genParticles)
    event.getByLabel('generator', genWeights)
    zmms = []
    for p in genParticles.product() :
        if not p.mother() :
            continue
        if abs(p.pdgId()) == 13 and p.isPromptFinalState() :
            zmms.append(p)

    w = -1.
    if genWeights.product().weight() > 0 :
        w = 1.

    if len(zmms) == 2 :
        hGen.Fill((zmms[0].p4()+zmms[1].p4()).mass(), w)

outFile.cd()
hGen.Write()
outFile.Close()
