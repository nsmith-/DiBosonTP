#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import argparse, json, pickle, os, re, subprocess

__gitversion__ = subprocess.check_output(["git", "describe", "--always"]).strip()

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
    if not plotsDir :
        return
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
        
        index.write(HTML.footer.format(
                version=__gitversion__
            ))

def parseEfficiencyDir(effDir, outputDirectory, index) :
    effName = effDir.GetName()
    rows = ''
    codeRows = []

    for effBinDir in fitSubDirs(effDir) :
        binName = effBinDir.GetName()

        if not effBinDir.Get('fitresults') :
            continue

        (row, code) = parseEfficiencyBin(effBinDir, outputDirectory)
        codeRows.append(code)
        rows += row

    plot = get2DPlot(effDir)
    plotName = 'efficiency2DPtEta.png'
    if plot :
        plot.Print(os.path.join(outputDirectory, plotName))

    macroVariables = effDir.Get('variables').GetTitle()
    with open(os.path.join(outputDirectory, effName+'.C'), 'w') as fout :
        fout.write("// Made with love by DiBosonTP version: %s\n" % __gitversion__)
        fout.write("float %s(%s) {\n" % (effName, macroVariables))
        for row in codeRows :
            fout.write(row+"\n")
        fout.write("    return 1.; // Default\n")
        fout.write("}\n")

    index.write(HTML.effDirItem.format(
        effName=effName,
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

    if effValue.getVal()+effValue.getErrorHi() > 1. :
        print "Found one! :"
        effValue.Print()

    canvas = effBinDir.Get('fit_canvas')
    passing = canvas.FindObject('fit_canvas_1')
    firstPlot = passing.GetListOfPrimitives()[0]
    firstPlot.SetTitle('Passing '+effBinDir.GetName())
    fullPlot = os.path.join(outputDirectory, effBinDir.GetName()+'.png')
    canvas.Print(fullPlot)
    smallPlot = fullPlot.replace('.png','_small.png')
    subprocess.call(['convert', '-gravity', 'north', '-crop', '100%x50%', fullPlot, smallPlot])

    nll = fitResults.minNll()

    mcHist = effBinDir.Get('mc_cutCount')
    mcPass = mcHist.GetBinContent(1)
    mcTotal= mcHist.GetBinContent(2)
    mcEff = mcPass/mcTotal

    with open(os.path.join(outputDirectory, effBinDir.GetName()+'.parameters.txt'), 'w') as paramOut :
        #paramOut.write("# Fit chi2/dof: %f / %d\n" % (chi2, dof))
        params = fitResults.floatParsFinal()
        for p in xrange(params.getSize()):
            myPar = params.at(p)
            paramOut.write("%s[%.3f,%.3f,%.3f]\n"%(myPar.GetName(), myPar.getVal(), myPar.getMin(), myPar.getMax()))

    colors = ['#79ff00', '#ffff00', '#ff7700', '#ff0000']
    thresholds = [1., 5., 10., 100.]
    fitStatusColor = '#00ff00' 
    for i in range(4) :
        if nll > thresholds[i] :
            fitStatusColor = colors[i]

    binName = effBinDir.GetName()

    row = HTML.effTableRow.format(
            fitStatusColor=fitStatusColor,
            efficiencyNice='%.4f +%.4f %.4f' % (effBinInfo['efficiency'], effBinInfo['error_hi'], effBinInfo['error_lo']),
            mcEfficiency='%.4f (%d/%d)' % (mcEff, mcPass, mcTotal),
            effName=effBinDir.GetDirectory('..').GetName(),
            binName=binName,
            binNameNice=re.sub('__pdfSignal.*', '', binName),
            numSignalAll=fitResults.floatParsFinal().find('numSignalAll').getVal(),
            nll=nll,
            fitStatus=':'.join(['%d' % fitResults.statusCodeHistory(i) for i in range(fitResults.numStatusHistory())]),
        )
    row += '''<tr><td colspan="6" style="text-align: center;"><img src="{effName}/{binName}_small.png"></td></tr>'''.format(
            effName=effBinDir.GetDirectory('..').GetName(),
            binName=binName,
        )

    codeRow = '    '+effBinDir.Get('cutString').GetTitle()

    return (row, codeRow)

def subDirs(dir) :
    for key in dir.GetListOfKeys() :
        if key.IsFolder() :
            yield key.ReadObj()

def fitSubDirs(dir) :
    for key in dir.GetListOfKeys() :
        if key.IsFolder() :
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
    Function: <a href="{effName}/{effName}.C">{effName}.C</a><br />
    <table>
        <tr style="background: #cccccc">
            <td>Bin name</td>
            <td>Data Value</td>
            <td>MC Value</td>
            <td>Data fit status</td>
            <td>Data fit signal yield</td>
            <td>NLL</td>
        </tr>
        {tableRows}
    </table>
    <!-- <img src="{eff2DPtEtaImage}" /><br /> -->
</div>'''

    effTableRow = '''
        <tr style="background: {fitStatusColor}">
            <td><a href="{effName}/{binName}.png">{binNameNice}</a></td>
            <td><a href="{effName}/{binName}.parameters.txt">{efficiencyNice}</a></td>
            <td>{mcEfficiency}</td>
            <td>{fitStatus}</td>
            <td>{numSignalAll:.0f}</td>
            <td>{nll:.0f}</td>
        </tr>'''


    footer = '''</table>
Generated using DiBosonTP version {version}<br />
</body>
</html>
'''

def main() :
    parser = argparse.ArgumentParser(description='Dumps fit info generated by TagProbeFitTreeAnalyzer into HTML summary')
    parser.add_argument('--data', help='Data fit tree name', type=rootFileType)
    parser.add_argument('--output', '-o', help='Directory name for output', required=True)
    parser.add_argument('--input', '-i', help='Directory name in root files to load', default='muonEffs')
    args = parser.parse_args()
    
    ROOT.gStyle.SetPaintTextFormat('0.4f')
    ROOT.gStyle.SetOptTitle(True)

    mkdirP(args.output)

    parseFitTree(args.data.Get(args.input), args.output)

if __name__ == '__main__' :
    main()
