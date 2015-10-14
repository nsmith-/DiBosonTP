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

#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"

class triggerObjectUnpacker : public edm::EDProducer {
   public:
      explicit triggerObjectUnpacker(const edm::ParameterSet&);
      ~triggerObjectUnpacker();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
      edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjects_;
};

triggerObjectUnpacker::triggerObjectUnpacker(const edm::ParameterSet& iConfig) :
   triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"))),
   triggerObjects_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("objects")))
{
   produces<pat::TriggerObjectStandAloneCollection>();

}


triggerObjectUnpacker::~triggerObjectUnpacker()
{
}

void
triggerObjectUnpacker::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   edm::Handle<edm::TriggerResults> triggerBits;
   edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;

   iEvent.getByToken(triggerBits_, triggerBits);
   iEvent.getByToken(triggerObjects_, triggerObjects);

   const edm::TriggerNames &names = iEvent.triggerNames(*triggerBits);

   std::unique_ptr<pat::TriggerObjectStandAloneCollection> unpackedObjects{new pat::TriggerObjectStandAloneCollection};

   for ( auto object : *triggerObjects ) {
      object.unpackPathNames(names);
      unpackedObjects->push_back(object);
      // if ( object.type(trigger::TriggerPhoton) ) {
      //    std::cout << "New electron----------------------------------------" << std::endl;
      //    for( auto name : object.pathNames() )
      //       std::cout << "Path name: " << name << std::endl;
      //    for( auto name : object.filterLabels() )
      //       std::cout << "Filter label: " << name << std::endl;
      // }
 
   }

   iEvent.put(std::move(unpackedObjects));
}

void 
triggerObjectUnpacker::beginJob()
{
}

void 
triggerObjectUnpacker::endJob() {
}

void
triggerObjectUnpacker::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(triggerObjectUnpacker);
