import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

process = cms.Process("tnp")
options = VarParsing('analysis')
options.register(
    "isMC",
    True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Compute MC efficiencies"
    )
options.parseArguments()

isolationDef = "(chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/pt"
config = {}
config['MUON_COLL']           = "slimmedMuons"
config['MUON_CUTS']           = "(isTrackerMuon || isGlobalMuon) && abs(eta)<2.5 && pt > 10"
config['DEBUG']               = cms.bool(False)
config['json']                = 'Cert_246908-258714_13TeV_PromptReco_Collisions15_25ns_JSON.txt'

# file dataset=/DoubleMuon/Run2015D-05Oct2015-v1/MINIAOD
# https://cmsweb.cern.ch/das/request?view=plain&limit=50&instance=prod%2Fglobal&input=file+dataset%3D%2FDoubleMuon%2FRun2015D-05Oct2015-v1%2FMINIAOD
inputFilesData = [
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/529E5F9F-5F6F-E511-83C6-0026189438F4.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/52A8BE9F-5F6F-E511-86A9-0025905AA9CC.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/56CC0262-5E6F-E511-B9BD-0025905A613C.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/58051008-616F-E511-9963-0025905A60DE.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/58441703-616F-E511-9B25-002354EF3BE0.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/58933F5C-5E6F-E511-8211-00261894389D.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/5AE4B6F8-656F-E511-B7F0-0025905A6068.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/5C134106-616F-E511-B373-0025905A6132.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/5C5D3202-616F-E511-9103-002618943811.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/5CA25362-5E6F-E511-B217-003048FFCBFC.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/5E996F5C-5E6F-E511-9402-002354EF3BE0.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/5EC7B1CC-646F-E511-9DDE-0025905A6080.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/6406E2A2-5F6F-E511-9F64-0025905A605E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/643154B9-656F-E511-88A8-002618943865.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/66161DB9-656F-E511-BDB3-00261894390A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/66BD3C68-5E6F-E511-97A7-0025905A609E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/68058ED5-646F-E511-A2D7-0026189438DD.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/6A7647D8-626F-E511-AF16-0025905A612E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/6EB2C705-616F-E511-997D-0025905A612E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/6EBBAD13-646F-E511-92BF-0025905964A2.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/72614CCF-646F-E511-BC57-003048FFD7D4.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/72C81ED9-626F-E511-BB83-0025905A60EE.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/72E5EF05-616F-E511-AD8C-0025905B858E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/746F9662-5E6F-E511-8EEE-0025905938D4.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/749CEEFE-646F-E511-8931-002618943918.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/764D5309-616F-E511-8111-0025905A60CE.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/7A637DCF-656F-E511-A942-002590593902.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/7EC502A4-5F6F-E511-9B44-0025905A6066.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/8250F85C-5E6F-E511-A10F-002354EF3BD0.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/847A499D-5F6F-E511-9523-00261894387E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/86E742D7-626F-E511-89CE-0025905A6068.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/88722C80-5C6F-E511-9CEC-0025905A612A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/8A7CE4DD-626F-E511-9541-0026189438CF.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/8C80359E-5F6F-E511-8BF2-003048FFCBFC.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/8CF7D960-5E6F-E511-AA90-003048FFD79C.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/8E2282D2-626F-E511-B94C-00261894394F.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/8EB315A2-5F6F-E511-9744-0025905A6118.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/90194F61-5E6F-E511-A4C9-0025905A497A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/9034A535-646F-E511-93FF-003048FFCC1E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/928277CC-646F-E511-AD98-002618943843.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/92D9CDA1-5F6F-E511-AEC1-0025905A60D6.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/9433E1E5-656F-E511-BA20-0025905A4964.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/9AAD419D-5F6F-E511-9E36-002354EF3BE0.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/9ABDDCBE-656F-E511-82DE-002618943862.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/9C06FF62-5E6F-E511-A74F-0025905B861C.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/9EC796F1-656F-E511-A4EB-002354EF3BDB.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/A08ACBD7-626F-E511-AF31-0025905A612C.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/A0E9185D-5E6F-E511-9912-00261894393B.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/A237AF67-5E6F-E511-A345-0025905A609E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/A6598AD5-626F-E511-8992-0026189438E1.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/A8CDFF5C-5E6F-E511-A443-002618943811.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/B497C462-5E6F-E511-A77D-0025905B85E8.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/B864DAA7-5F6F-E511-B2E1-0025905A60FE.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/B8BDE901-616F-E511-A173-0026189438B1.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/BAFE4602-616F-E511-B1E4-002618943964.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/BC46185D-5E6F-E511-ABDE-00261894394F.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/BEC64BEB-656F-E511-994F-0025905A6080.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/C02CC0C9-646F-E511-8CDE-002618943865.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/C08CF4DF-646F-E511-8333-0025905B85B2.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/C0BFFDD7-626F-E511-9A41-0025905A60A0.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/C264086C-5E6F-E511-BAA3-0025905A6068.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/C2C3179D-5F6F-E511-999A-002354EF3BE0.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/C616B8EF-656F-E511-9761-0025905A6092.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/C83F39D8-626F-E511-B85C-0025905A4964.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/CA3F5FD1-646F-E511-9C06-0025905A6068.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/CA4180CC-646F-E511-BD22-0025905A6090.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/CC3A05D6-626F-E511-B449-0025905964A2.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/CC58B7D1-646F-E511-BD25-0025905A609E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/CCC1D78E-5F6F-E511-BF91-003048FFD728.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/CE1139E5-646F-E511-A47E-0025905A612A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/D41C04E5-656F-E511-9C5A-0025905B85B2.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/D659B9A1-5F6F-E511-90C9-0025905A60D6.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/DA047BD8-626F-E511-A140-003048FFCC1E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/DA71FFD0-646F-E511-8337-002590593902.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/DE7A3708-616F-E511-8FC8-002590593920.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/E0076703-616F-E511-B6FD-002618943935.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/E0B79FDA-646F-E511-A3A1-002618943862.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/E4137862-5E6F-E511-B214-0025905A6136.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/E4A83D62-5E6F-E511-B3B5-003048FFCC1E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/E6581CD7-626F-E511-9918-0025905A608A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/E823D5B7-656F-E511-BE68-0025905A6090.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/E8A7BE8C-5F6F-E511-87C0-0025905B85E8.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/EA1B5CA1-5F6F-E511-94A4-0025905964C2.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/EABA9AE1-646F-E511-AB40-002354EF3BDB.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/ECA8B2D1-626F-E511-B768-002354EF3BE4.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/ECBD2CD4-626F-E511-A54C-0026189438F4.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/EE753202-616F-E511-8932-002618943874.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/F29D5FD6-656F-E511-8BA2-0025905B85AE.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/F2BC2C60-5E6F-E511-9C3A-0025905B859E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/F46A93E8-646F-E511-9651-00261894390A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/F616CECD-646F-E511-9A48-0025905A4964.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/F69EFBD3-626F-E511-AB6D-00261894392F.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/F881DC00-616F-E511-8CDD-002618943913.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/F8FA8E9F-5F6F-E511-BA39-0025905964B6.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/FC1DEBD2-626F-E511-B381-002618943831.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/FC2D8CCA-646F-E511-954A-002618943923.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/FC95F1D6-626F-E511-A558-0025905A6068.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/40000/FCFA1592-5F6F-E511-BA92-003048FFD79C.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/0061FE0B-6B6F-E511-8D34-00261894383B.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/024EA4D2-5F6F-E511-B594-0025905B8562.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/04E3FAC2-686F-E511-A658-0025905AA9F0.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/067AFD10-6B6F-E511-B251-003048FFCBA4.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/069C5F61-6E6F-E511-957A-0025905A6138.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/08E73863-646F-E511-B7C3-0025905A60A0.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/0AFFAA11-6B6F-E511-8637-0025905938A4.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/0CC33129-6B6F-E511-9586-0026189438CB.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/0E2DB966-676F-E511-8543-003048FFCC1E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/0E3F3F2E-626F-E511-9CC4-0025905A611C.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/0EE45ABC-686F-E511-8FE7-00261894394A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/1097FFC1-686F-E511-97BC-0025905A48F0.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/10D6FF63-646F-E511-803E-003048FFD75C.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/12648010-6B6F-E511-A0B6-0025905964BC.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/1485055B-6E6F-E511-9058-002618943901.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/1645F3D4-626F-E511-91B1-002354EF3BD2.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/167CFED1-5F6F-E511-B08D-0025905B855E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/16ED6365-646F-E511-BE20-0025905A60A8.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/1893B1D5-626F-E511-AE22-002618943922.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/1A076CEA-636F-E511-9F88-0025905A607E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/1A227748-6C6F-E511-9415-00261894392F.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/1A5347D1-5F6F-E511-A9E4-0025905A60A8.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/1AF703BC-5F6F-E511-BE71-0025905A60DA.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/1CC0BB68-676F-E511-8DEA-0025905A4964.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/1EA5AA11-6B6F-E511-AC49-0025905938A4.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/2019FB67-676F-E511-B8A0-0025905A497A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/208735DD-626F-E511-BB71-00259059642A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/224C5AE5-5F6F-E511-BCDE-0025905A6090.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/2877EE45-6C6F-E511-9E74-0026189438CF.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/2C15DCB8-5F6F-E511-8F64-00261894380B.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/2CBF0128-626F-E511-8D96-00261894385A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/2E2867D2-5F6F-E511-99B5-0025905A606A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/2E70E9D3-706F-E511-9365-00261894383B.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/2E74A359-646F-E511-AD6C-0026189438E1.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/301F915A-646F-E511-BC48-0025905938A4.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/3278890F-6B6F-E511-AAE5-003048FF9AC6.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/3288262F-626F-E511-9861-00259059642E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/32B0D96A-6E6F-E511-95D8-0025905A607A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/3475754B-6C6F-E511-8585-0025905A6094.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/34A45C6C-676F-E511-B0A9-003048FFD796.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/362E8847-706F-E511-BF07-0025905A612E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/36B2FC5A-6E6F-E511-9234-00261894397F.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/3A0AEDC3-686F-E511-955F-003048FFD736.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/3EAF4F69-676F-E511-A07E-003048FFD728.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/40C9F6FE-636F-E511-8EC8-0025905A60B8.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/4212A861-646F-E511-B850-002618943983.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/424B4BD0-5F6F-E511-8CED-0025905A612E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/42F455D1-5F6F-E511-9AE3-002618943919.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/44A8322D-626F-E511-A82D-0025905964A2.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/44AEC0CD-5F6F-E511-90FF-003048FFCB9E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/462EFE59-6E6F-E511-B390-002618943953.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/46762F60-6C6F-E511-8842-0025905A6136.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/46AA872E-626F-E511-8FD5-0025905A6126.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/46D17411-6B6F-E511-A813-0025905A606A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/480BAACF-686F-E511-8287-0025905A612A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/48A03C5C-6E6F-E511-B649-002618943886.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/4A04C45F-6E6F-E511-9AC5-003048FFCBFC.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/4ADF122E-626F-E511-86DA-0025905A606A.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/4C07A166-676F-E511-851D-0025905A605E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/4C4D0709-646F-E511-A3A9-002590593902.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/4E581156-646F-E511-8E41-002618943874.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/4E852F67-676F-E511-AB40-0025905A605E.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/5021EBDA-626F-E511-AED4-0025905A60E0.root',
        '/store/data/Run2015D/DoubleMuon/MINIAOD/05Oct2015-v1/60000/50C6D3B9-5F6F-E511-8852-0026189438F7.root',
]

# file dataset=/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM
# https://cmsweb.cern.ch/das/request?view=plain&limit=50&instance=prod%2Fglobal&input=file+dataset%3D%2FDYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8%2FRunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3%2FMINIAODSIM
inputFilesMC = [
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/009D49A5-7314-E511-84EF-0025905A605E.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/00C0BECF-6F14-E511-96F8-0025904B739A.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/0260F225-7614-E511-A79F-00A0D1EE8EB4.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/02B810EA-7214-E511-BDAB-0025905964C2.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/02CEA7DD-7714-E511-A93E-00266CFAEA68.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/0453351C-7014-E511-A296-0025905B85AA.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/0679BC6F-7714-E511-945E-0025905B8562.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/0823BF6F-7814-E511-8E48-00A0D1EE8B08.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/08271551-9714-E511-B209-0025907FD2DA.root',
        '/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/08D8E2DA-7014-E511-8875-002590593872.root',
]

if len(options.inputFiles) is 0 :
    if options.isMC :
        options.inputFiles = inputFilesMC
    else :
        options.inputFiles = inputFilesData

if options.isMC :
    config['outputFile'] = 'TnPTreeDZ_mc.root'
else :
    config['outputFile'] = 'TnPTreeDZ_data.root'

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    )

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.hltFilter = hltHighLevel.clone()
process.hltFilter.throw = cms.bool(True)
process.hltFilter.HLTPaths = cms.vstring('HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v*', 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v*')

process.goodMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag(config['MUON_COLL']),
    cut = cms.string(config['MUON_CUTS']),
    filter = cms.bool(True)
)

process.triggerMatchingSequence = cms.Sequence()

process.muonTriggerUpperLeg = cms.EDProducer("PatMuonTriggerCandProducer",
    filterNames = cms.vstring("hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4", "hltL3fL1sDoubleMu103p5L1f0L2f10OneMuL3Filtered17"),
    inputs      = cms.InputTag("goodMuons"),
    bits        = cms.InputTag('TriggerResults::HLT'),
    objects     = cms.InputTag('selectedPatTrigger'),
    dR          = cms.double(0.5),
    isAND       = cms.bool(True)
    )
process.triggerMatchingSequence += process.muonTriggerUpperLeg

process.muonTriggerMu8Leg = process.muonTriggerUpperLeg.clone()
process.muonTriggerMu8Leg.filterNames = cms.vstring("hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4", "hltL3pfL1sDoubleMu103p5L1f0L2pf0L3PreFiltered8")
process.triggerMatchingSequence += process.muonTriggerMu8Leg

process.muonTriggerTkMu8Leg = process.muonTriggerUpperLeg.clone()
process.muonTriggerTkMu8Leg.filterNames = cms.vstring("hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4", "hltDiMuonGlbFiltered17TrkFiltered8")
process.triggerMatchingSequence += process.muonTriggerTkMu8Leg

process.muonDZTriggerMu8Leg = process.muonTriggerUpperLeg.clone()
process.muonDZTriggerMu8Leg.filterNames = cms.vstring("hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4", "hltL3pfL1sDoubleMu103p5L1f0L2pf0L3PreFiltered8", "hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4DzFiltered0p2")
process.triggerMatchingSequence += process.muonDZTriggerMu8Leg

process.muonDZTriggerTkMu8Leg = process.muonTriggerUpperLeg.clone()
process.muonDZTriggerTkMu8Leg.filterNames = cms.vstring("hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4", "hltDiMuonGlbFiltered17TrkFiltered8", "hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4DzFiltered0p2")
process.triggerMatchingSequence += process.muonDZTriggerTkMu8Leg

process.tpPairsMu17Mu8 = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("muonTriggerUpperLeg@+ muonTriggerMu8Leg@-"), # charge coniugate states are implied
    cut   = cms.string("40 < mass < 200")
)

process.tpPairsMu17TkMu8 = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("muonTriggerUpperLeg@+ muonTriggerTkMu8Leg@-"), # charge coniugate states are implied
    cut   = cms.string("40 < mass < 200")
)

process.muMcMatch = cms.EDProducer("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(13),
    src = cms.InputTag(config['MUON_COLL']),
    distMin = cms.double(0.3),
    matched = cms.InputTag("prunedGenParticles"),
    checkCharge = cms.bool(True)
)

process.pileupReweightingProducer = cms.EDProducer("PileupWeightProducer",
    hardcodedWeights = cms.untracked.bool(False),
    PileupMCFile = cms.string('../data/puWeightMC.root'),
    PileupDataFile = cms.string('../data/puWeightData.root'),
    )

ZVariablesToStore = cms.PSet(
    eta = cms.string("eta"),
    abseta = cms.string("abs(eta)"),
    pt  = cms.string("pt"),
    mass  = cms.string("mass"),
    )   

ProbeVariablesToStore = cms.PSet(
    probe_eta    = cms.string("eta"),
    probe_abseta = cms.string("abs(eta)"),
    probe_pt     = cms.string("pt"),
    probe_et     = cms.string("et"),
    probe_e      = cms.string("energy"),
    probe_q      = cms.string("charge"),
    )

TagVariablesToStore = cms.PSet(
    tag_eta    = cms.string("eta"),
    tag_abseta = cms.string("abs(eta)"),
    tag_pt     = cms.string("pt"),
    tag_et     = cms.string("et"),
    tag_e      = cms.string("energy"),
    tag_q      = cms.string("charge"),
    )

CommonStuffForMuonProbe = cms.PSet(
    variables = cms.PSet(ProbeVariablesToStore),
    ignoreExceptions =  cms.bool (True),
    addRunLumiInfo   =  cms.bool (True),
    addEventVariablesInfo   =  cms.bool(True),
    vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    #pfMet = cms.InputTag(""),
    pairVariables =  cms.PSet(ZVariablesToStore),
    pairFlags     =  cms.PSet(
        mass60to120 = cms.string("60 < mass < 120")
        ),
    tagVariables   =  cms.PSet(TagVariablesToStore),
    tagFlags       =  cms.PSet(),    
    )

mcTruthCommonStuff = cms.PSet(
    isMC = cms.bool(False),
    tagMatches = cms.InputTag("muMcMatch"),
    probeMatches = cms.InputTag("muMcMatch"),
    motherPdgId = cms.vint32(22,23),
    #motherPdgId = cms.vint32(443), # JPsi
    #motherPdgId = cms.vint32(553), # Yupsilon
    makeMCUnbiasTree = cms.bool(False),
    checkMotherInUnbiasEff = cms.bool(False),
    mcVariables = cms.PSet(
        probe_eta = cms.string("eta"),
        probe_abseta = cms.string("abs(eta)"),
        probe_et  = cms.string("et"),
        probe_e  = cms.string("energy"),
        ),
    mcFlags     =  cms.PSet(
        probe_flag = cms.string("pt>0")
        ),      
    )

process.globalMuonDZTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
    CommonStuffForMuonProbe, mcTruthCommonStuff,
    tagProbePairs = cms.InputTag("tpPairsMu17Mu8"),
    arbitration   = cms.string("BestMass"),
    massForArbitration = cms.double(91.),
    flags         = cms.PSet(
        passingDZ = cms.InputTag("muonDZTriggerMu8Leg"),
    ),
    allProbes     = cms.InputTag("muonTriggerMu8Leg"),
    )

process.trackerMuonDZTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
    CommonStuffForMuonProbe, mcTruthCommonStuff,
    tagProbePairs = cms.InputTag("tpPairsMu17TkMu8"),
    arbitration   = cms.string("BestMass"),
    massForArbitration = cms.double(91.),
    flags         = cms.PSet(
        passingDZ = cms.InputTag("muonDZTriggerTkMu8Leg"),
    ),
    allProbes     = cms.InputTag("muonTriggerTkMu8Leg"),
    )

process.tpPairSeq = cms.Sequence(
    process.tpPairsMu17Mu8 + process.tpPairsMu17TkMu8
)

if options.isMC :
    process.tpPairSeq += process.muMcMatch 
    process.tpPairSeq += process.pileupReweightingProducer
    process.globalMuonDZTree.isMC = cms.bool(True)
    process.globalMuonDZTree.eventWeight   = cms.InputTag("generator")
    process.globalMuonDZTree.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")
    process.trackerMuonDZTree.isMC = cms.bool(True)
    process.trackerMuonDZTree.eventWeight   = cms.InputTag("generator")
    process.trackerMuonDZTree.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")

if not options.isMC :
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/'+config['json']).getVLuminosityBlockRange()

process.p = cms.Path(
    process.goodMuons *
    process.triggerMatchingSequence *
    process.tpPairSeq *
    (process.globalMuonDZTree + process.trackerMuonDZTree)
    )

process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string('debug.root'),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
                               )
if config['DEBUG'] :
    process.outpath = cms.EndPath(process.out)

process.TFileService = cms.Service("TFileService", fileName = cms.string(config['outputFile']))

