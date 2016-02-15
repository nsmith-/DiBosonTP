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

submit muonTP makeTree.py /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM DYJetsMC.txt isMC=1
submit muonTPData makeTree.py       /SingleMuon/Run2015D-05Oct2015-v1/MINIAOD      SingleMuon.txt isMC=0
submit muonTPDataPrompt makeTree.py /SingleMuon/Run2015D-PromptReco-v4/MINIAOD     SingleMuonPrompt.txt isMC=0
submit muonTPDataC makeTree.py      /SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD SingleMuonC.txt isMC=0

submit muonTPMC   makeDZTree.py /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM DYJetsMC.txt isMC=1
submit muonTPData makeDZTree.py       /DoubleMuon/Run2015D-05Oct2015-v1/MINIAOD       DoubleMuon.txt isMC=0
submit muonTPDataPrompt makeDZTree.py /DoubleMuon/Run2015D-PromptReco-v4/MINIAOD      DoubleMuonPrompt.txt isMC=0
submit muonTPDataC makeDZTree.py      /DoubleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD  DoubleMuonC.txt isMC=0
