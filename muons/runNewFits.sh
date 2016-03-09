# source me
rm -rf plots/*
./newfitter.py
mkdir -p plots/badFits
mv badFit_* plots/badFits
dumpTagProbeTreeHTML.py --data fits.root -i muonFits -o plots
./plot.py ZZLoose "Muon Loose ID"
./plot.py ZZTight "Muon Tight ID"
./plot.py ZZIso_wrtLoose "Muon Loose Isolation"
./plot.py ZZIso_wrtTight "Muon Tight Isolation"
