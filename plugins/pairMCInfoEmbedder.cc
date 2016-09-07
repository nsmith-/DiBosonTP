// Original Author:  Nicholas Charles Smith

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"

#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

class pairMCInfoEmbedder : public edm::EDProducer {
   public:
      explicit pairMCInfoEmbedder(const edm::ParameterSet&);
      ~pairMCInfoEmbedder();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      edm::EDGetTokenT<reco::CandidateView> srcToken_;
      edm::EDGetTokenT<edm::Association<reco::GenParticleCollection>> leg1MatchesToken_, leg2MatchesToken_;
};

pairMCInfoEmbedder::pairMCInfoEmbedder(const edm::ParameterSet& iConfig) :
  srcToken_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("input"))),
  leg1MatchesToken_(consumes<edm::Association<reco::GenParticleCollection>>(iConfig.getParameter<edm::InputTag>("leg1Matches"))),
  leg2MatchesToken_(consumes<edm::Association<reco::GenParticleCollection>>(iConfig.getParameter<edm::InputTag>("leg2Matches")))
{
   produces<pat::CompositeCandidateCollection>();
}


pairMCInfoEmbedder::~pairMCInfoEmbedder()
{
}

void
pairMCInfoEmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   Handle<reco::CandidateView> src;
   iEvent.getByToken(srcToken_, src);
   
   Handle<edm::Association<reco::GenParticleCollection>> leg1Matches;
   iEvent.getByToken(leg1MatchesToken_, leg1Matches);
   
   Handle<edm::Association<reco::GenParticleCollection>> leg2Matches;
   iEvent.getByToken(leg2MatchesToken_, leg2Matches);
   
   std::unique_ptr<pat::CompositeCandidateCollection> pairsEmbedded{new pat::CompositeCandidateCollection};

   for ( const auto& mother : *src ) {
     if (mother.numberOfDaughters() != 2) throw cms::Exception("CorruptData") << "Pair with " << mother.numberOfDaughters() << " daughters\n";
     pat::CompositeCandidate motherEmbedded((reco::CompositeCandidate) mother);
     reco::GenParticleRef leg1 = (*leg1Matches)[mother.daughter(0)->masterClone()];
     reco::GenParticleRef leg2 = (*leg2Matches)[mother.daughter(1)->masterClone()];
     if ( !leg1.isNull() && !leg2.isNull() ) {
       auto mcVector = leg1->p4() + leg2->p4();
       motherEmbedded.addUserFloat("mc_mass", mcVector.mass());
       motherEmbedded.addUserFloat("mc_pt", mcVector.pt());
     } else {
       motherEmbedded.addUserFloat("mc_mass", 0.);
       motherEmbedded.addUserFloat("mc_pt", 0.);
     }
     pairsEmbedded->push_back(motherEmbedded);
   }

   iEvent.put(std::move(pairsEmbedded));
}

void 
pairMCInfoEmbedder::beginJob()
{
}

void 
pairMCInfoEmbedder::endJob() {
}

void
pairMCInfoEmbedder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(pairMCInfoEmbedder);
