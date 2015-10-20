# source me
cmsenv

# MC ID/Iso
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingMedium 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingTight 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingVeto 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingZZLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingZZTight 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingZZIso conditions=passingZZLoose outputFileName=fromZZLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root idName=passingZZIso conditions=passingZZTight outputFileName=fromZZTight 2>&1 > /dev/null &

# MC Triggers
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root dirName=GsfElectronToTrigger idName=passingHLTEle17Ele12Leg1 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root dirName=GsfElectronToTrigger idName=passingHLTEle17Ele12Leg1L1Match 2>&1 > /dev/null &
cmsRun fitter.py isMC=1 inputFileName=TnPTree_mc.root dirName=GsfElectronToTrigger idName=passingHLTEle17Ele12Leg2 2>&1 > /dev/null &

# Data ID/Iso
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingMedium 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingTight 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingVeto 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingZZLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingZZTight 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingZZIso conditions=passingZZLoose outputFileName=fromZZLoose 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=passingZZIso conditions=passingZZTight outputFileName=fromZZTight 2>&1 > /dev/null &

# Data Triggers
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root dirName=GsfElectronToTrigger idName=passingHLTEle17Ele12Leg1 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root dirName=GsfElectronToTrigger idName=passingHLTEle17Ele12Leg1L1Match 2>&1 > /dev/null &
cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root dirName=GsfElectronToTrigger idName=passingHLTEle17Ele12Leg2 2>&1 > /dev/null &

wait

hadd -f efficiency-mc.root efficiency-mc-*.root
hadd -f efficiency-data.root efficiency-data-*.root

dumpTagProbeTreeHTML.py --mc efficiency-mc.root --data efficiency-data.root -i GsfElectronToRECO -o ~/www/TagProbePlots/newelectrons
dumpTagProbeLatex.py --mc efficiency-mc.root --data efficiency-data.root -i GsfElectronToRECO -o ~/www/TagProbePlots/newelectrons

dumpTagProbeTreeHTML.py --mc efficiency-mc.root --data efficiency-data.root -i GsfElectronToTrigger -o ~/www/TagProbePlots/electronTrigger
dumpTagProbeLatex.py --mc efficiency-mc.root --data efficiency-data.root -i GsfElectronToTrigger -o ~/www/TagProbePlots/electronTrigger
