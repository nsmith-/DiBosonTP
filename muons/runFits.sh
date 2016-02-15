# source me
cmsenv

if [[ $1 == 'doMC' ]]; then
  # MC ID/Iso
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingIDZZLoose 2>&1 > /dev/null &
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingIDZZTight 2>&1 > /dev/null &
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingIsoZZ conditions=passingIDZZLoose outputFileName=passingIDZZLoose 2>&1 > /dev/null &
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingIsoZZ conditions=passingIDZZTight outputFileName=passingIDZZTight 2>&1 > /dev/null &

  # MC Triggers
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingMu17 2>&1 > /dev/null &
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingMu17L1Match 2>&1 > /dev/null &
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingMu8 2>&1 > /dev/null &
  cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTree_mc.root idName=passingTkMu8 2>&1 > /dev/null &

  # DZ
  #cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTreeDZ_mc.root idName=passingDZ dirName=globalMuonDZTree  outputFileName=globalMuon  2>&1 > /dev/null
  #cmsRun fitter.py isMC=1 doCutAndCount=1 inputFileName=TnPTreeDZ_mc.root idName=passingDZ dirName=trackerMuonDZTree outputFileName=trackerMuon 2>&1 > /dev/null
fi

# Make MC templates for data fit
commonTemplateFlags="-d muonEffs --var2Name=probe_pt --var1Name=probe_abseta --var2Bins=5,10,20,30,40,50,100,1000 --var1Bins=0,1.5,2.5 --weightVarName=totWeight"
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

# Data Triggers
dataFitSeq passingMu17
dataFitSeq passingMu17L1Match
dataFitSeq passingMu8
dataFitSeq passingTkMu8

# DZ filters
#getTemplatesFromMC.py -i TnPTreeDZ_mc.root -o mcTemplates-globalMuonPassingDZ.root --idprobe=passingDZ \
#  -d globalMuonDZTree --var2Name=probe_pt --var1Name=probe_abseta --var2Bins=10,20,30,40,50,100,1000 --var1Bins=0,1.5,2.5 --weightVarName=totWeight
#cmsRun fitter.py isMC=0 inputFileName=TnPTreeDZ_data.root idName=passingDZ dirName=globalMuonDZTree  outputFileName=globalMuon mcTemplateFile=mcTemplates-globalMuonPassingDZ.root 2>&1 > /dev/null &
#
#getTemplatesFromMC.py -i TnPTreeDZ_mc.root -o mcTemplates-trackerMuonPassingDZ.root --idprobe=passingDZ \
#  -d trackerMuonDZTree --var2Name=probe_pt --var1Name=probe_abseta --var2Bins=10,20,30,40,50,100,1000 --var1Bins=0,1.5,2.5 --weightVarName=totWeight
#cmsRun fitter.py isMC=0 inputFileName=TnPTreeDZ_data.root idName=passingDZ dirName=trackerMuonDZTree outputFileName=trackerMuon mcTemplateFile=mcTemplates-trackerMuonPassingDZ.root 2>&1 > /dev/null &

wait

hadd -f efficiency-mc.root efficiency-mc-*.root
hadd -f efficiency-data.root efficiency-data-*.root

outDir=~/www/TagProbePlots/$(git describe)

dumpTagProbeTreeHTML.py --mc efficiency-mc.root --data efficiency-data.root -i muonEffs -o ${outDir}/muons
dumpTagProbeLatex.py --mc efficiency-mc.root --data efficiency-data.root -i muonEffs -o ${outDir}/muons --count

#dumpTagProbeTreeHTML.py --mc efficiency-mc.root --data efficiency-data.root -i globalMuonDZTree -o ${outDir}/globalMuonDZ
#dumpTagProbeLatex.py --mc efficiency-mc.root --data efficiency-data.root -i globalMuonDZTree -o ${outDir}/globalMuonDZ --count

#dumpTagProbeTreeHTML.py --mc efficiency-mc.root --data efficiency-data.root -i trackerMuonDZTree -o ~/www/TagProbePlots/trackerMuonDZ
#dumpTagProbeLatex.py --mc efficiency-mc.root --data efficiency-data.root -i trackerMuonDZTree -o ~/www/TagProbePlots/trackerMuonDZ --count
