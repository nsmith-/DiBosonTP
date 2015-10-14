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
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

class zzElectronIdIsoProducer : public edm::EDProducer {
   public:
      explicit zzElectronIdIsoProducer(const edm::ParameterSet&);
      ~zzElectronIdIsoProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      edm::EDGetTokenT<edm::View<reco::GsfElectron>> electronsToken_;
      edm::EDGetTokenT<edm::ValueMap<float>> mvaIdValueMapToken_;
};

zzElectronIdIsoProducer::zzElectronIdIsoProducer(const edm::ParameterSet& iConfig) :
  electronsToken_(consumes<edm::View<reco::GsfElectron>>(iConfig.getParameter<edm::InputTag>("electrons"))),
  mvaIdValueMapToken_(consumes<edm::ValueMap<float>>(iConfig.getParameter<edm::InputTag>("mvaIdValueMap")))
{
   produces<edm::ValueMap<bool>>("electronZZIDLoose");
   produces<edm::ValueMap<bool>>("electronZZIDTight");
   produces<edm::ValueMap<bool>>("electronZZIso");
}


zzElectronIdIsoProducer::~zzElectronIdIsoProducer()
{
}

void
zzElectronIdIsoProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   Handle<View<reco::GsfElectron>> electrons;
   iEvent.getByToken(electronsToken_, electrons);

   Handle<ValueMap<float>> mvaValues;
   iEvent.getByToken(mvaIdValueMapToken_, mvaValues);

   std::vector<bool> idLooseValues(electrons->size());
   std::vector<bool> idTightValues(electrons->size());
   std::vector<bool> isoValues(electrons->size());

   for ( size_t i=0; i<electrons->size(); ++i ) {
      auto l = electrons->ptrAt(i);
      float BDT = (*mvaValues)[l];
      // https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsZZ4l2015#Electrons
      float pt = l->pt();
      float fSCeta = fabs(l->superCluster()->eta());
      bool isBDT = (pt<=10 && ((fSCeta<0.8                  && BDT > -0.265) ||
                              (fSCeta>=0.8 && fSCeta<1.479 && BDT > -0.556) ||
                              (fSCeta>=1.479               && BDT > -0.551))) 
                || (pt>10  && ((fSCeta<0.8                  && BDT > -0.072) ||
                              (fSCeta>=0.8 && fSCeta<1.479 && BDT > -0.286) || 
                              (fSCeta>=1.479               && BDT > -0.267)));
      idLooseValues[i] = true;
      idTightValues[i] = isBDT;
      isoValues[i] = false;
   }

   // All this just to fill some value maps?!

   std::unique_ptr<ValueMap<bool>> idLoose{new ValueMap<bool>};
   std::unique_ptr<ValueMap<bool>> idTight{new ValueMap<bool>};
   std::unique_ptr<ValueMap<bool>> iso{new ValueMap<bool>};

   ValueMap<bool>::Filler idLooseFill(*idLoose);
   ValueMap<bool>::Filler idTightFill(*idTight);
   ValueMap<bool>::Filler isoFill(*iso);

   idLooseFill.insert(electrons, idLooseValues.begin(), idLooseValues.end());
   idTightFill.insert(electrons, idTightValues.begin(), idTightValues.end());
   isoFill.insert(electrons, isoValues.begin(), isoValues.end());

   idLooseFill.fill();
   idTightFill.fill();
   isoFill.fill();

   iEvent.put(std::move(idLoose), "electronZZIDLoose");
   iEvent.put(std::move(idTight), "electronZZIDTight");
   iEvent.put(std::move(iso), "electronZZIso");
}

void 
zzElectronIdIsoProducer::beginJob()
{
}

void 
zzElectronIdIsoProducer::endJob() {
}

void
zzElectronIdIsoProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(zzElectronIdIsoProducer);
