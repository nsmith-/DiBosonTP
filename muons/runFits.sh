# source me
cmsenv

# MC ID/Iso
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingIDZZLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingIDZZTight 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingIsoZZ conditions=passingIDZZLoose outputFileName=fromZZLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingIsoZZ conditions=passingIDZZTight outputFileName=fromZZTight 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingIDWZLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingIDWZTight 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingIsoWZLoose conditions=passingIDWZLoose outputFileName=fromWZLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingIsoWZTight conditions=passingIDWZTight outputFileName=fromWZTight 2>&1 > /dev/null &

# MC Triggers
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingMu17 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingMu17L1Match 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingMu8 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingTkMu8 2>&1 > /dev/null &

# Data ID/Iso
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingIDZZLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingIDZZTight 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingIsoZZ conditions=passingIDZZLoose outputFileName=fromZZLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingIsoZZ conditions=passingIDZZTight outputFileName=fromZZTight 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingIDWZLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingIDWZTight 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingIsoWZLoose conditions=passingIDWZLoose outputFileName=fromWZLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingIsoWZTight conditions=passingIDWZTight outputFileName=fromWZTight 2>&1 > /dev/null &

# Data Triggers
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingMu17 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingMu17L1Match 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingMu8 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingTkMu8 2>&1 > /dev/null &

# DZ Filter
cmsRun fitter.py isMC=1 inputFileName=TnPTreeDZ_mc.root idName=passingDZ dirName=globalMuonDZTree  outputFileName=globalMuon  2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTreeDZ_mc.root idName=passingDZ dirName=trackerMuonDZTree outputFileName=trackerMuon 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTreeDZ_data.root idName=passingDZ dirName=globalMuonDZTree  outputFileName=globalMuon  2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTreeDZ_data.root idName=passingDZ dirName=trackerMuonDZTree outputFileName=trackerMuon 2>&1 > /dev/null &

wait

hadd -f efficiency-mc.root efficiency-mc-*.root
hadd -f efficiency-data.root efficiency-data-*.root

dumpTagProbeTreeHTML.py --mc efficiency-mc.root --data efficiency-data.root -i muonEffs -o ~/www/TagProbePlots/newmuons
dumpTagProbeLatex.py --mc efficiency-mc.root --data efficiency-data.root -i muonEffs -o ~/www/TagProbePlots/newmuons

dumpTagProbeTreeHTML.py --mc efficiency-mc.root --data efficiency-data.root -i globalMuonDZTree -o ~/www/TagProbePlots/globalMuonDZ
dumpTagProbeLatex.py --mc efficiency-mc.root --data efficiency-data.root -i globalMuonDZTree -o ~/www/TagProbePlots/globalMuonDZ

dumpTagProbeTreeHTML.py --mc efficiency-mc.root --data efficiency-data.root -i trackerMuonDZTree -o ~/www/TagProbePlots/trackerMuonDZ
dumpTagProbeLatex.py --mc efficiency-mc.root --data efficiency-data.root -i trackerMuonDZTree -o ~/www/TagProbePlots/trackerMuonDZ
