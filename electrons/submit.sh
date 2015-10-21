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
    --input-dir=root://cmsxrootd.fnal.gov/ \
    --assume-input-files-exist \
    --input-files-per-job=10 \
    ${pythonFile} \
      'inputFiles=$inputFileNames' 'outputFile=$outputFileName' ${flags}
}

#submit electronTP makeTree.py /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM DYJetsMC.txt isMC=1
#submit electronTPData makeTree.py /SingleElectron/Run2015D-05Oct2015-v1/MINIAOD SingleElectron.txt isMC=0

submit electronTPMC   makeDZTree.py /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM DYJetsMC.txt isMC=1
submit electronTPData makeDZTree.py /DoubleEG/Run2015D-05Oct2015-v1/MINIAOD DoubleElectron.txt isMC=0
