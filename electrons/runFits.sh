# source me
cmsenv

# MC ID/Iso
cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingLoose 2>&1 > /dev/null
cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingMedium 2>&1 > /dev/null
cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingTight 2>&1 > /dev/null
cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingVeto 2>&1 > /dev/null
cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingZZLoose 2>&1 > /dev/null
cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingZZTight 2>&1 > /dev/null
cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingZZIso conditions=passingZZLoose outputFileName=passingZZLoose 2>&1 > /dev/null
cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingZZIso conditions=passingZZTight outputFileName=passingZZTight 2>&1 > /dev/null

# MC Triggers
cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root dirName=GsfElectronToTrigger idName=passingHLTEle17Ele12Leg1 2>&1 > /dev/null
cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root dirName=GsfElectronToTrigger idName=passingHLTEle17Ele12Leg1L1Match 2>&1 > /dev/null
cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root dirName=GsfElectronToTrigger idName=passingHLTEle17Ele12Leg2 2>&1 > /dev/null

# Make MC templates for data fit
commonTemplateFlags="-d GsfElectronToRECO --var2Name=probe_Ele_pt --var1Name=probe_Ele_abseta --var2Bins=10,20,30,40,50,100,1000 --var1Bins=0,1.5,2.5 --weightVarName=totWeight"
dataFitSeq() {
  dirName=$1
  shift
  idName=$1
  shift
  conditions=$1

  if [[ $conditions ]]; then
    condFileSafe=$(echo ${conditions}|tr ',' '_')
    getTemplatesFromMC.py ${commonTemplateFlags} -d ${dirName} -i TnPTree_mc.root -o mcTemplates-${idName}-${condFileSafe}.root --idprobe=${idName} --conditions="${conditions}"
    cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root dirName=${dirName} idName=${idName} conditions=${conditions} outputFileName=${condFileSafe} mcTemplateFile=mcTemplates-${idName}-${condFileSafe}.root 2>&1 > /dev/null &
  else
    getTemplatesFromMC.py ${commonTemplateFlags} -d ${dirName} -i TnPTree_mc.root -o mcTemplates-${idName}.root --idprobe=${idName}
    cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root dirName=${dirName} idName=${idName} mcTemplateFile=mcTemplates-${idName}.root  2>&1 > /dev/null &
  fi
}

# Data ID/Iso
dataFitSeq GsfElectronToRECO passingLoose
dataFitSeq GsfElectronToRECO passingMedium
dataFitSeq GsfElectronToRECO passingTight
dataFitSeq GsfElectronToRECO passingVeto
dataFitSeq GsfElectronToRECO passingZZLoose
dataFitSeq GsfElectronToRECO passingZZTight
dataFitSeq GsfElectronToRECO passingZZIso passingZZLoose
dataFitSeq GsfElectronToRECO passingZZIso passingZZTight

# Data Triggers
dataFitSeq GsfElectronToTrigger passingHLTEle17Ele12Leg1
dataFitSeq GsfElectronToTrigger passingHLTEle17Ele12Leg1L1Match
dataFitSeq GsfElectronToTrigger passingHLTEle17Ele12Leg2

# DZ Filter
cmsRun fitter.py isMC=1 inputFileName=TnPTreeDZ_mc.root idName=passingHLTDZFilter dirName=GsfElectronToTrigger 2>&1 > /dev/null
getTemplatesFromMC.py -i TnPTreeDZ_mc.root -o mcTemplates-passingDZ.root --idprobe=passingHLTDZFilter  \
  -d GsfElectronToTrigger --var2Name=probe_Ele_pt --var1Name=probe_Ele_abseta --var2Bins=10,20,30,40,50,100,1000 --var1Bins=0,1.5,2.5 --weightVarName=totWeight
cmsRun fitter.py isMC=0 inputFileName=TnPTreeDZ_data.root idName=passingHLTDZFilter dirName=GsfElectronToTrigger mcTemplateFile=mcTemplates-passingDZ.root 2>&1 > /dev/null &

wait

hadd -f efficiency-mc.root efficiency-mc-*.root
hadd -f efficiency-data.root efficiency-data-*.root

dumpTagProbeTreeHTML.py --mc efficiency-mc.root --data efficiency-data.root -i GsfElectronToRECO -o ~/www/TagProbePlots/electrons
dumpTagProbeLatex.py --mc efficiency-mc.root --data efficiency-data.root -i GsfElectronToRECO -o ~/www/TagProbePlots/electrons --count

dumpTagProbeTreeHTML.py --mc efficiency-mc.root --data efficiency-data.root -i GsfElectronToTrigger -o ~/www/TagProbePlots/electronTrigger
dumpTagProbeLatex.py --mc efficiency-mc.root --data efficiency-data.root -i GsfElectronToTrigger -o ~/www/TagProbePlots/electronTrigger --count
