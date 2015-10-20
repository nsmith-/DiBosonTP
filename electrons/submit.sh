# source me

submit() {
  dataset=$1
  cachefile=$2
  isMC=$3
  jobName=$4

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
    makeTree.py \
      'inputFiles=$inputFileNames' 'outputFile=$outputFileName' isMC=$isMC
}

submit /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM DYJetsMC.txt 1 electronTP
submit /SingleElectron/Run2015D-05Oct2015-v1/MINIAOD SingleElectron.txt 0 electronTPData

