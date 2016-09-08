# source me
rm -rf plots/*
./newfitter.py $1
mkdir -p plots/badFits
mv badFit_* plots/badFits
dumpTagProbeTreeHTML.py --data fits.root -i muonFits -o plots
mv plots ~/www/TagProbePlots/Phase2Muons/${1%.root}
