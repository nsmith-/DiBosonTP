# source me

submit() {
  jobName=$1
  shift
  pythonFile=$1
  shift
  dataset=$1
  shift
  cachefile=$1
  shift
  flags=$@

  if [ ! -f $cachefile ]
  then
    das_client.py --query="file dataset=${dataset}" --format plain --limit 0 > $cachefile
  fi

  farmoutAnalysisJobs $jobName \
    --infer-cmssw-path \
    --input-file-list=${cachefile} \
    --input-dir=root://cmsxrootd.hep.wisc.edu/ \
    --assume-input-files-exist \
    --input-files-per-job=10 \
    ${pythonFile} \
      'inputFiles=$inputFileNames' 'outputFile=$outputFileName' ${flags}
}

submit electronTP makeTree.py /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM DYJetsMC.txt isMC=1
submit electronTPLO makeTree.py /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM DYJetsMC_LO.txt isMC=1
submit electronTPData makeTree.py /SingleElectron/Run2015D-05Oct2015-v1/MINIAOD SingleElectron.txt isMC=0
submit electronTPDataPrompt makeTree.py /SingleElectron/Run2015D-PromptReco-v4/MINIAOD SingleElectronPrompt.txt isMC=0
submit electronTPDataC makeTree.py /SingleElectron/Run2015C_25ns-05Oct2015-v1/MINIAOD SingleElectronC.txt isMC=0

#submit electronTPMC   makeDZTree.py /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM DYJetsMC.txt isMC=1
#submit electronTPData makeDZTree.py /DoubleEG/Run2015D-05Oct2015-v1/MINIAOD DoubleElectron.txt isMC=0
