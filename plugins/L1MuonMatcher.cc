#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/L1Trigger/interface/L1MuonParticle.h"
#include "DataFormats/L1Trigger/interface/L1MuonParticleFwd.h"

#include "DataFormats/PatCandidates/interface/Muon.h"

#include <DataFormats/Math/interface/deltaR.h>

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include <string>
#include <vector>

class L1MuonMatcher : public edm::EDProducer {
 public:
  L1MuonMatcher(const edm::ParameterSet&);
  ~L1MuonMatcher();

  bool l1OfflineMatching(const l1extra::L1MuonParticleCollection& triggerObjects, 
			 math::XYZTLorentzVector refP4, float dRmin, int& index);

 private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  
  edm::EDGetTokenT<pat::MuonRefVector> inputs_;
  edm::EDGetTokenT<l1extra::L1MuonParticleCollection> l1muonObjectsToken_;
  float minET_;
  float dRMatch_;
};

L1MuonMatcher::L1MuonMatcher(const edm::ParameterSet& iConfig ) :
  inputs_(consumes<pat::MuonRefVector>(iConfig.getParameter<edm::InputTag>("inputs"))),
  l1muonObjectsToken_(consumes<l1extra::L1MuonParticleCollection>(iConfig.getParameter<edm::InputTag>("l1extraMuons"))),
  minET_(iConfig.getParameter<double>("minET")),
  dRMatch_(iConfig.getParameter<double>("dRmatch")) {

  produces<pat::MuonRefVector>();
}

L1MuonMatcher::~L1MuonMatcher()
{}

void L1MuonMatcher::produce(edm::Event &iEvent, const edm::EventSetup &eventSetup) {

  edm::Handle<l1extra::L1MuonParticleCollection> l1muonsHandle;
  edm::Handle<pat::MuonRefVector> inputs;

  iEvent.getByToken(l1muonObjectsToken_, l1muonsHandle);
  iEvent.getByToken(inputs_, inputs);

  // Create the output collection
  std::auto_ptr<pat::MuonRefVector> outColRef(new pat::MuonRefVector);

  for (size_t i=0; i<inputs->size(); i++) {
    auto ref = (*inputs)[i];
    int index = -1;

    if (l1OfflineMatching(*l1muonsHandle, ref->p4(), dRMatch_, index)) {
      outColRef->push_back(ref);
    }
  }

  iEvent.put(outColRef);
}

bool L1MuonMatcher::l1OfflineMatching(const l1extra::L1MuonParticleCollection& l1Objects, math::XYZTLorentzVector refP4, float dRmin, int& index) {

  index = 0;
  for (l1extra::L1MuonParticleCollection::const_iterator it=l1Objects.begin(); it != l1Objects.end(); it++) {
    if (it->et() < minET_)
      continue;

  float dR = deltaR(refP4, it->p4());
    if (dR < dRmin)
      return true;

    index++;
  }

  return false;
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(L1MuonMatcher);
