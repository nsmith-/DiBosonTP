#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import argparse, json, pickle, os, re

# mkdir -p 
def mkdirP(dirname) :
    import errno
    try:
        os.mkdir(dirname)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise e
        pass

def rootFileType(string) :
    file = ROOT.TFile.Open(string)
    if not file :
        raise argparse.ArgumentTypeError(string+' could not be opened!')
    return file

def get2DPlot(effDir) :
    canvas = None
    plotsDir = effDir.Get('fit_eff_plots')
    for key in plotsDir.GetListOfKeys() :
        if re.match('probe_.*abseta.*_probe_.*_PLOT.*', key.GetName()) :
            canvas = key.ReadObj()
            break

    if not canvas :
        raise Exception('No canvas found in %s' % effDir.GetName())
    
    # Stylize?
    canvas.SetLogy(True)
    plot = canvas.GetPrimitive(canvas.GetName())

    ROOT.SetOwnership(canvas, False)
    return canvas

def parseFitTree(baseDirectory, outputDirectory) :
    '''
        Generates HTML files in outputDirectory
    '''

    mkdirP(outputDirectory)
    with open(os.path.join(outputDirectory, 'index.html'), 'w') as index :
        index.write(HTML.header.format(
            rootFile=baseDirectory.GetFile().GetName(),
            baseDirectory=baseDirectory.GetName()
        ))

        for effDir in subDirs(baseDirectory) :
            effName = effDir.GetName()

            effoutDir = os.path.join(outputDirectory, effName)
            mkdirP(effoutDir)

            parseEfficiencyDir(effDir, effoutDir, index)
        
        index.write(HTML.footer)

def parseEfficiencyDir(effDir, outputDirectory, index) :
    effName = effDir.GetName()
    rows = ''

    for effBinDir in fitSubDirs(effDir) :
        binName = effBinDir.GetName()

        if not effBinDir.Get('fitresults') :
            continue

        row = parseEfficiencyBin(effBinDir, outputDirectory)
        rows += row

    plot = get2DPlot(effDir)
    plotName = 'efficiency2DPtEta.png'
    plot.Print(os.path.join(outputDirectory, plotName))

    index.write(HTML.effDirItem.format(
        effName=effName,
        effDefinition='?',
        eff2DPtEtaImage=os.path.join(effName, plotName),
        tableRows=rows
    ))

def makeChi2(rooPad, nFitParam) :
    # This is so fucking stupid
    data = rooPad.FindObject('h_data_binned')
    model = rooPad.FindObject('pdfPass_Norm[mass]')
    chi2 = 0.
    for i in range(data.GetN()) :
        x = ROOT.Double()
        y = ROOT.Double()
        data.GetPoint(i, x, y)
        yerr = data.GetErrorY(i)
        ypred = model.interpolate(x)
        if y > 0 :
            chi2 += (y-ypred)**2 / yerr**2
    return (chi2, data.GetN()-nFitParam)

def makeChi2_roofit(rooPad, nFitParam) :
    data = rooPad.FindObject('h_data_binned')
    model = rooPad.FindObject('pdfPass_Norm[mass]')
    Redchi2 = model.chiSquare(data, nFitParam)
    dof = data.GetN() - nFitParam
    return (Redchi2*dof, dof)

def parseEfficiencyBin(effBinDir, outputDirectory) :
    fitResults = effBinDir.Get('fitresults')
    # https://root.cern.ch/root/html/tutorials/roofit/rf607_fitresult.C.html
    effValue = fitResults.floatParsFinal().find('efficiency')
    effBinInfo = {
            'efficiency' : effValue.getVal(),
            'error_hi' : effValue.getErrorHi(),
            'error_lo' : effValue.getErrorLo()
        }

    canvas = effBinDir.Get('fit_canvas')
    canvas.Print(os.path.join(outputDirectory, effBinDir.GetName()+'.png'))

    with open(os.path.join(outputDirectory, effBinDir.GetName()+'.parameters.txt'), 'w') as paramOut :
        params = fitResults.floatParsFinal()
        for p in xrange(params.getSize()):
            myPar = params.at(p)
            paramOut.write("%s[%.3f,%.3f,%.3f]\n"%(myPar.GetName(), myPar.getVal(), myPar.getMin(), myPar.getMax()))

    passing = canvas.FindObject('fit_canvas_1')
    (chi2, dof) = makeChi2(passing, fitResults.floatParsFinal().getSize())
    (chi2roo, dofroo) = makeChi2_roofit(passing, fitResults.floatParsFinal().getSize())

    colors = ['#79ff00', '#ffff00', '#ff7700', '#ff0000']
    thresholds = [1., 5., 10., 100.]
    fitStatusColor = '#00ff00' 
    for i in range(4) :
        if chi2/dof > thresholds[i] :
            fitStatusColor = colors[i]

    binName = effBinDir.GetName()

    row = HTML.effTableRow.format(
            fitStatusColor=fitStatusColor,
            efficiencyNice='%.4f +%.4f %.4f' % (effBinInfo['efficiency'], effBinInfo['error_hi'], effBinInfo['error_lo']),
            effName=effBinDir.GetDirectory('..').GetName(),
            binName=binName,
            binNameNice=re.sub('__pdfSignal.*', '', binName),
            numSignalAll=fitResults.floatParsFinal().find('numSignalAll').getVal(),
            chi2='%.0f / %d' % (chi2, dof),
            chi2roo='%.0f / %d' % (chi2roo, dofroo),
            fitStatus='-'.join(['%d' % fitResults.statusCodeHistory(i) for i in range(fitResults.numStatusHistory())]),
        )

    return row

def subDirs(dir) :
    for key in dir.GetListOfKeys() :
        if key.IsFolder() :
            yield key.ReadObj()

def fitSubDirs(dir) :
    for key in dir.GetListOfKeys() :
        if key.IsFolder() and re.match('probe.*_bin\d__probe.*_bin\d__.*pdfSignal.*', key.GetName()) :
            yield key.ReadObj()

# HTML Templates
class HTML :
    header = '''<html>
<head>
    <title>Efficiency summary for {rootFile}/{baseDirectory}</title>
    <style type="text/css">
        div.effResult {{
            margin: auto;
            width: 80%;
            border: 2px solid #888888;
        }}

        table {{
            width: 100%;
        }}
    </style>
</head>
<body>
<h2>Efficiency summary for {rootFile}/{baseDirectory}</h2>
'''

    effDirItem = '''<div class="effResult">
    <h3>Efficiency results for {effName}</h3><br />
    Definition: <span class="code">{effDefinition}</span><br />
    <table>
        <tr style="background: #cccccc">
            <td>Bin name</td>
            <td>Value</td>
            <td>Fit status</td>
            <td>Fit signal yield</td>
            <td>Chi2</td>
        </tr>
        {tableRows}
    </table>
    <img src="{eff2DPtEtaImage}" /><br />
</div>'''

    effTableRow = '''
        <tr style="background: {fitStatusColor}">
            <td><a href="{effName}/{binName}.png">{binNameNice}</a></td>
            <td><a href="{effName}/{binName}.parameters.txt">{efficiencyNice}</a></td>
            <td>{fitStatus}</td>
            <td>{numSignalAll:.0f}</td>
            <td>{chi2} (Roo: {chi2roo})</td>
        </tr>'''


    footer = '''</table>
</body>
</html>
'''

def main() :
    parser = argparse.ArgumentParser(description='Dumps fit info generated by TagProbeFitTreeAnalyzer into HTML summary')
    parser.add_argument('--mc', help='MC fit tree name', type=rootFileType)
    parser.add_argument('--data', help='Data fit tree name', type=rootFileType)
    parser.add_argument('--output', '-o', help='Directory name for output', required=True)
    parser.add_argument('--input', '-i', help='Directory name in root files to load', default='muonEffs')
    args = parser.parse_args()
    
    ROOT.gStyle.SetPaintTextFormat('0.4f')

    mkdirP(args.output)

    if args.mc :
        parseFitTree(args.mc.Get(args.input), os.path.join(args.output, 'mc'))
    if args.data :
        parseFitTree(args.data.Get(args.input), os.path.join(args.output, 'data'))

if __name__ == '__main__' :
    main()
