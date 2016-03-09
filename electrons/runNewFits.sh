# source me
rm -rf plots/*
./newfitter.py
mkdir -p plots/badFits
mv badFit_* plots/badFits
dumpTagProbeTreeHTML.py --data fits.root -i muonFits -o plots
./plot.py ZZLoose "Electron Loose ID"
./plot.py ZZTight "Electron Tight ID"
./plot.py ZZIso_wrtLoose "Electron Loose Isolation"
./plot.py ZZIso_wrtTight "Electron Tight Isolation"
