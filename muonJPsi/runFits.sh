# source me
cmsenv

if [[ $1 == 'doMC' ]]; then
  # MC ID/Iso
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingIDZZLoose 2>&1 > /dev/null
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingIDZZTight 2>&1 > /dev/null
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingIsoZZ conditions=passingIDZZLoose outputFileName=passingIDZZLoose 2>&1 > /dev/null
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingIsoZZ conditions=passingIDZZTight outputFileName=passingIDZZTight 2>&1 > /dev/null
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingIDWZLoose 2>&1 > /dev/null
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingIDWZTight 2>&1 > /dev/null
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingIsoWZLoose conditions=passingIDWZLoose outputFileName=fromWZLoose 2>&1 > /dev/null
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingIsoWZTight conditions=passingIDWZTight outputFileName=fromWZTight 2>&1 > /dev/null

fi

# Make MC templates for data fit
commonTemplateFlags="-d muonEffs --var2Name=probe_pt --var1Name=probe_abseta --var2Bins=5,15,25,100 --var1Bins=0,1.5,2.5 --weightVarName=totWeight --massWindow=2.5,3.5"
dataFitSeq() {
  idName=$1
  shift
  conditions=$1

  if [[ $conditions ]]; then
    condFileSafe=$(echo ${conditions}|tr ',' '_')
    if [[ ! -f mcTemplates-${idName}-${condFileSafe}.root ]]; then
      getTemplatesFromMC.py ${commonTemplateFlags} -i TnPTree_mc.root -o mcTemplates-${idName}-${condFileSafe}.root --idprobe=${idName} --conditions="${conditions}"
    fi
    cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=${idName} conditions=${conditions} outputFileName=${condFileSafe} mcTemplateFile=mcTemplates-${idName}-${condFileSafe}.root 2>&1 > /dev/null &
  else
    if [[ ! -f mcTemplates-${idName}.root ]]; then
      getTemplatesFromMC.py ${commonTemplateFlags} -i TnPTree_mc.root -o mcTemplates-${idName}.root --idprobe=${idName}
    fi
    cmsRun fitter.py isMC=0 inputFileName=TnPTree_data.root idName=${idName} mcTemplateFile=mcTemplates-${idName}.root 2>&1 > /dev/null &
  fi
}

# rm -rf mcTemplates-*.root

# Data ID/Iso
dataFitSeq passingIDZZLoose
dataFitSeq passingIDZZTight
dataFitSeq passingIsoZZ passingIDZZLoose
dataFitSeq passingIsoZZ passingIDZZTight
dataFitSeq passingIDWZLoose
dataFitSeq passingIDWZTight
dataFitSeq passingIsoWZLoose passingIDWZLoose
dataFitSeq passingIsoWZTight passingIDWZTight

wait

hadd -f efficiency-mc.root efficiency-mc-*.root
hadd -f efficiency-data.root efficiency-data-*.root

mkdir -p ~/www/TagProbePlots/muonJPsi
dumpTagProbeTreeHTML.py --mc efficiency-mc.root --data efficiency-data.root -i muonEffs -o ~/www/TagProbePlots/muonJPsi
dumpTagProbeLatex.py --mc efficiency-mc.root --data efficiency-data.root -i muonEffs -o ~/www/TagProbePlots/muonJPsi --count
