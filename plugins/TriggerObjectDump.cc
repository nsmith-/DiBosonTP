// Original Author:  Nicholas Charles Smith
//         Created:  Tue, 16 Jun 2015 08:49:00 GMT

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

class TriggerObjectDump : public edm::EDFilter {
   public:
      explicit TriggerObjectDump(const edm::ParameterSet&);
      ~TriggerObjectDump();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob();
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob();

      edm::EDGetTokenT<edm::View<reco::Candidate>> candidates_;
};

TriggerObjectDump::TriggerObjectDump(const edm::ParameterSet& iConfig) :
   candidates_(consumes<edm::View<reco::Candidate>>(iConfig.getParameter<edm::InputTag>("candidates")))
{

}


TriggerObjectDump::~TriggerObjectDump()
{
}

bool
TriggerObjectDump::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   edm::Handle<edm::View<reco::Candidate>> candidateCollection;

   iEvent.getByToken(candidates_, candidateCollection);

   if ( candidateCollection->size() == 0 ) return false;

   edm::LogVerbatim("triggers") << "New event" << std::endl;
   edm::LogVerbatim("triggers") << "==============================" << std::endl;

   for ( auto& candidate : *candidateCollection ) {
      edm::LogVerbatim("triggers") << "New candidate mass = " << candidate.mass() << std::endl;

      auto tagCand = dynamic_cast<const reco::CompositeCandidate*>(&candidate)->daughter(0);
      auto tagMuon = tagCand->masterClone().castTo<pat::MuonRef>();
      auto tagTriggerObject = tagMuon->triggerObjectMatchByPath("HLT_IsoMu20_eta2p1_v*");

      auto probeCand = dynamic_cast<const reco::CompositeCandidate*>(&candidate)->daughter(1);
      auto probeMuon = probeCand->masterClone().castTo<pat::MuonRef>();

      for ( auto object : probeMuon->triggerObjectMatches() ) {
         edm::LogVerbatim("triggers") << "   Probe muon trigger match dR = " << reco::deltaR(object, *probeMuon) << 
            ", dR to tag trigger object = " << reco::deltaR(object, *tagTriggerObject) << std::endl;
         if ( object.p4() == tagTriggerObject->p4() ) {
            edm::LogError("triggers") << "   \e[31mREUSED TAG TRIGGER OBJECT FOR PROBE!!!\e[0m" << std::endl;
            return false;
         }
         for( auto name : object.pathNames() )
            edm::LogVerbatim("triggers") << "   Path name: " << name << std::endl;
         for( auto name : object.filterLabels() )
            edm::LogVerbatim("triggers") << "   Filter label: " << name << std::endl;
      }
   }

   edm::LogVerbatim("triggers") << std::endl;
   return true;
}

void 
TriggerObjectDump::beginJob()
{
}

void 
TriggerObjectDump::endJob() {
}

void
TriggerObjectDump::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TriggerObjectDump);
