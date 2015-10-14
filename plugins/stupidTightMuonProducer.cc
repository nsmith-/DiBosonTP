// Original Author:  Nicholas Charles Smith
//         Created:  Tue, 16 Jun 2015 08:49:00 GMT

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/RefVector.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

class stupidTightMuonProducer : public edm::EDProducer {
   public:
      explicit stupidTightMuonProducer(const edm::ParameterSet&);
      ~stupidTightMuonProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      edm::InputTag srcTag_;
      edm::InputTag vtxTag_;
};

stupidTightMuonProducer::stupidTightMuonProducer(const edm::ParameterSet& iConfig) :
  srcTag_(iConfig.getParameter<edm::InputTag>("src")),
  vtxTag_(iConfig.getParameter<edm::InputTag>("vtx"))
{
   produces<pat::MuonCollection>();

}


stupidTightMuonProducer::~stupidTightMuonProducer()
{
}

void
stupidTightMuonProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   Handle<pat::MuonCollection> muons;
   iEvent.getByLabel(srcTag_, muons);

   Handle<reco::VertexCollection> vtx;
   iEvent.getByLabel(vtxTag_, vtx);
   const auto& pv = vtx->at(0);

   std::unique_ptr<pat::MuonCollection> tightMuons{new pat::MuonCollection};

   for ( size_t i=0; i<muons->size(); ++i ) {
      pat::Muon muon = muons->at(i);
      if ( muon.isTightMuon(pv) ) {
         muon.addUserInt("isTightMuon", 1);
      } else {
         muon.addUserInt("isTightMuon", 0);
      }
      // Some vertex info
      muon.addUserFloat("dxyToPV", muon.muonBestTrack()->dxy(pv.position()));
      muon.addUserFloat("dzToPV", muon.muonBestTrack()->dz(pv.position()));
      tightMuons->push_back(muon);
   }

   iEvent.put(std::move(tightMuons));
}

void 
stupidTightMuonProducer::beginJob()
{
}

void 
stupidTightMuonProducer::endJob() {
}

void
stupidTightMuonProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(stupidTightMuonProducer);
