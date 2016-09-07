// -*- C++ -*-
//
// Package:   Analysis/OneStopMuonShop
// Class:    OneStopMuonShop
// 
/**\class OneStopMuonShop OneStopMuonShop.cc Analysis/OneStopMuonShop/plugins/OneStopMuonShop.cc

 Description: [one line class summary]

 Implementation:
    [Notes on implementation]
*/
//
// Original Author:  Nicholas Charles Smith
//      Created:  Recently?
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "RecoMuon/MuonIdentification/plugins/MuonIdProducer.h"

class OneStopMuonShop : public edm::stream::EDProducer<> {
  public:
    explicit OneStopMuonShop(const edm::ParameterSet&);
    ~OneStopMuonShop();

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:
    virtual void beginStream(edm::StreamID) override;
    virtual void produce(edm::Event&, const edm::EventSetup&) override;
    virtual void endStream() override;

    //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
    //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
    //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
    //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

    edm::EDGetTokenT<reco::TrackRefVector> srcTrackRefToken_;
    edm::EDGetTokenT<reco::MuonCollection> srcRecoToken_;
    edm::EDGetTokenT<pat::MuonCollection> srcPatToken_;

    edm::EDGetTokenT<reco::VertexCollection> vertexToken_;
};

OneStopMuonShop::OneStopMuonShop(const edm::ParameterSet& iConfig) :
  srcTrackRefToken_(consumes<reco::TrackRefVector>(iConfig.getParameter<edm::InputTag>("tracks"))),
  srcRecoToken_(consumes<reco::MuonCollection>(iConfig.getParameter<edm::InputTag>("recoMuons"))),
  srcPatToken_(consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("patMuons"))),
  vertexToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertices")))
{
  produces<pat::MuonCollection>();
}


OneStopMuonShop::~OneStopMuonShop()
{
}

void
OneStopMuonShop::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  std::unique_ptr<pat::MuonCollection> output(new pat::MuonCollection());

  Handle<reco::TrackRefVector> trackRefsH;
  iEvent.getByToken(srcTrackRefToken_, trackRefsH);

  Handle<reco::MuonCollection> muonsH;
  iEvent.getByToken(srcRecoToken_, muonsH);

  Handle<pat::MuonCollection> patMuonsH;
  iEvent.getByToken(srcPatToken_, patMuonsH);

  bool usePat{false};
  if ( patMuonsH.isValid() ) usePat = true;

  Handle<reco::VertexCollection> vtx;
  iEvent.getByToken(vertexToken_, vtx);
  const auto& pv = vtx->at(0);

  for(const reco::TrackRef& track : *trackRefsH) {
    const pat::Muon * matchedMuon{nullptr};
    if ( usePat ) {
      for(const auto& patMuon : *patMuonsH) {
        if ( patMuon.innerTrack() == track ) {
          matchedMuon = &patMuon;
          break;
        }
      }
    } else {
      for(const auto& muon : *muonsH) {
        if ( muon.innerTrack() == track ) {
          matchedMuon = new pat::Muon(muon);
          break;
        }
      }
    }

    if ( matchedMuon != nullptr ) {
      output->push_back(*matchedMuon);
      if ( ! usePat ) delete matchedMuon;
    } else {
      // https://cmssdt.cern.ch/SDT/doxygen/CMSSW_8_0_2/doc/html/df/d17/MuonIdProducer_8cc_source.html#l01166
      const double energy = hypot(track->p(), 0.105658369);
      const math::XYZTLorentzVector p4(track->px(), track->py(), track->pz(), energy);
      pat::Muon newMuon(reco::Muon(track->charge(), p4, track->vertex()));
      newMuon.setMuonTrack(reco::Muon::InnerTrack, track);
      newMuon.setBestTrack(reco::Muon::InnerTrack);
      newMuon.setTunePBestTrack(reco::Muon::InnerTrack);
      output->push_back(newMuon);
    }

    auto& muon = output->back();
    if ( matchedMuon != nullptr && muon.isTightMuon(pv) ) {
      muon.addUserInt("isTightMuon", 1);
    } else {
      muon.addUserInt("isTightMuon", 0);
    }
    muon.addUserFloat("dxyToPV", muon.muonBestTrack()->dxy(pv.position()));
    muon.addUserFloat("dzToPV", muon.muonBestTrack()->dz(pv.position()));
  }

  iEvent.put(std::move(output));
}


void
OneStopMuonShop::beginStream(edm::StreamID)
{
}


void
OneStopMuonShop::endStream() {
}


/*
void
OneStopMuonShop::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 

/*
void
OneStopMuonShop::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 

/*
void
OneStopMuonShop::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 

/*
void
OneStopMuonShop::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 

void
OneStopMuonShop::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


DEFINE_FWK_MODULE(OneStopMuonShop);
