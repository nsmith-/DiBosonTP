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

submit muonJPsiTPData makeTree.py /SingleMuon/Run2015D-05Oct2015-v1/MINIAOD SingleMuon.txt isMC=0
