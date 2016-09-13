# source me
rm -rf plots/*
./newfitter.py $1
puVal=${1%.root}
mkdir -p plots/badFits
mv badFit_* plots/badFits
dumpTagProbeTreeHTML.py --data fits.root -i muonFits -o plots
./plot.py WZLoose "WZ Loose ID @${puVal}"
./plot.py Tight "Tight ID @${puVal}"
./plot.py RelIso0p4 "PF Rel. Iso<0.4 @${puVal}"
./plot.py RelIso0p12 "PF Rel. Iso<0.12 @${puVal}"
rm -rf ~/www/TagProbePlots/Phase2Muons/${puVal}
cp -r plots ~/www/TagProbePlots/Phase2Muons/${puVal}
