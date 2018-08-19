#!/usr/bin/env python
import ROOT
import imp
import json
from array import array
wsptools = imp.load_source('wsptools', 'workspaceTools.py')


def GetFromTFile(str):
    f = ROOT.TFile(str.split(':')[0])
    obj = f.Get(str.split(':')[1]).Clone()
    f.Close()
    return obj

# Boilerplate
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.RooWorkspace.imp = getattr(ROOT.RooWorkspace, 'import')
ROOT.TH1.AddDirectory(0)

w = ROOT.RooWorkspace('w')

# IC muon ID, iso, trigger SFs

loc = 'inputs/ICSF/'

# Embedded selection efficiencies

histsToWrap = [
    (loc+'2017/EmbedSel/Mu8/muon_SFs.root:data_trg_eff', 'm_sel_trg8_1_data'),
    (loc+'2017/EmbedSel/Mu17/muon_SFs.root:data_trg_eff', 'm_sel_trg17_1_data')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['gt1_pt', 'expr::gt1_abs_eta("TMath::Abs(@0)",gt1_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

histsToWrap = [
    (loc+'2017/EmbedSel/Mu8/muon_SFs.root:data_trg_eff', 'm_sel_trg8_2_data'),
    (loc+'2017/EmbedSel/Mu17/muon_SFs.root:data_trg_eff', 'm_sel_trg17_2_data')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['gt2_pt', 'expr::gt2_abs_eta("TMath::Abs(@0)",gt2_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

w.factory('expr::m_sel_trg_data("0.9959*(@0*@3+@1*@2-@1*@3)", m_sel_trg8_1_data, m_sel_trg17_1_data, m_sel_trg8_2_data, m_sel_trg17_2_data)')
w.factory('expr::m_sel_trg_ratio("min(1./@0,20)", m_sel_trg_data)')

histsToWrap = [
    (loc+'2017/EmbedSel/Mu8/muon_SFs.root:data_id_eff', 'm_sel_idEmb_data')
]
wsptools.SafeWrapHist(w, ['gt_pt', 'expr::gt_abs_eta("TMath::Abs(@0)",gt_eta[0])'],
                          GetFromTFile(loc+'2017/EmbedSel/Mu8/muon_SFs.root:data_id_eff'), 'm_sel_idEmb_data')

w.factory('expr::m_sel_idEmb_ratio("min(1./@0,20)", m_sel_idEmb_data)')


# trigegr SFs

histsToWrap = [
    (loc+'2017/SingleMuon/muon_SFs.root:data_id_eff', 'm_id_data'),
    (loc+'2017/SingleMuon/muon_SFs.root:ZLL_id_eff', 'm_id_mc'),
    (loc+'2017/SingleMuon/muon_SFs.root:embed_id_eff', 'm_id_embed'),
    (loc+'2017/SingleMuon/muon_SFs.root:data_iso_eff', 'm_iso_data'),
    (loc+'2017/SingleMuon/muon_SFs.root:ZLL_iso_eff', 'm_iso_mc'),
    (loc+'2017/SingleMuon/muon_SFs.root:embed_iso_eff', 'm_iso_embed'),
    (loc+'2017/SingleMuon/muon_SFs.root:data_trg_eff', 'm_trg_data'),
    (loc+'2017/SingleMuon/muon_SFs.root:ZLL_trg_eff', 'm_trg_mc'),
    (loc+'2017/SingleMuon/muon_SFs.root:embed_trg_eff', 'm_trg_embed')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_trg_binned_data', ['m_trg_data', 'm_trg_data', 'm_trg_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_trg_binned_mc', ['m_trg_mc', 'm_trg_mc', 'm_trg_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_trg_binned_embed', ['m_trg_embed', 'm_trg_embed', 'm_trg_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_iso_binned_data', ['m_iso_data', 'm_iso_data', 'm_iso_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_iso_binned_mc', ['m_iso_mc', 'm_iso_mc', 'm_iso_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_iso_binned_embed', ['m_iso_embed', 'm_iso_embed', 'm_iso_embed'])

for t in ['data', 'mc', 'embed']:
    w.factory('expr::m_idiso_%s("@0*@1", m_id_%s, m_iso_%s)' % (t, t, t))
    w.factory('expr::m_idiso_binned_%s("@0*@1", m_id_%s, m_iso_binned_%s)' % (t, t, t))

for t in ['trg', 'trg_binned', 'id', 'iso', 'iso_binned', 'idiso_binned' ]:
    w.factory('expr::m_%s_ratio("@0/@1", m_%s_data, m_%s_mc)' % (t, t, t))
    w.factory('expr::m_%s_embed_ratio("@0/@1", m_%s_data, m_%s_embed)' % (t, t, t))

# EGamma POG ID SFs

loc = 'inputs/EGammaPOG/'

histsToWrap = [
    (loc+'gammaEffi.txt_EGM2D_runBCDEF_passingMVA94Xwp80noiso.root:EGamma_EffData2D', 'e_id_pog_data'),
    (loc+'gammaEffi.txt_EGM2D_runBCDEF_passingMVA94Xwp80noiso.root:EGamma_EffMC2D', 'e_id_pog_mc'),
    (loc+'gammaEffi.txt_EGM2D_runBCDEF_passingMVA94Xwp80iso.root:EGamma_EffData2D', 'e_idiso_pog_data'),
    (loc+'gammaEffi.txt_EGM2D_runBCDEF_passingMVA94Xwp80iso.root:EGamma_EffMC2D', 'e_idiso_pog_mc'),
    (loc+'gammaEffi.txt_EGM2D_runBCDEF_passingMVA94Xwp90noiso.root:EGamma_EffData2D', 'e_looseid_pog_data'),
    (loc+'gammaEffi.txt_EGM2D_runBCDEF_passingMVA94Xwp90noiso.root:EGamma_EffMC2D', 'e_looseid_pog_mc'),
    (loc+'gammaEffi.txt_EGM2D_runBCDEF_passingMVA94Xwp90iso.root:EGamma_EffData2D', 'e_looseidiso_pog_data'),
    (loc+'gammaEffi.txt_EGM2D_runBCDEF_passingMVA94Xwp90iso.root:EGamma_EffMC2D', 'e_looseidiso_pog_mc')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['e_eta', 'e_pt'],
                          GetFromTFile(task[0]), name=task[1])


# IC em trigger SF
loc = 'inputs/ICSF/2017/'

histsToWrap = [
    (loc+'Mu23Ele12/electron_SFs.root:data_trg_eff', 'e_trg_12_data'),
    (loc+'Mu23Ele12/electron_SFs.root:ZLL_trg_eff', 'e_trg_12_mc'),
    (loc+'Mu8Ele23/electron_SFs.root:data_trg_eff', 'e_trg_23_data'),
    (loc+'Mu8Ele23/electron_SFs.root:ZLL_trg_eff', 'e_trg_23_mc')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.30, 0.50],
                                   'e_trg_binned_23_data', ['e_trg_23_data', 'e_trg_23_data', 'e_trg_23_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.30, 0.50],
                                   'e_trg_binned_23_mc', ['e_trg_23_mc', 'e_trg_23_mc', 'e_trg_23_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.30, 0.50],
                                   'e_trg_binned_12_data', ['e_trg_12_data', 'e_trg_12_data', 'e_trg_12_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.30, 0.50],
                                   'e_trg_binned_12_mc', ['e_trg_12_mc', 'e_trg_12_mc', 'e_trg_12_mc'])

for t in ['trg','trg_binned']:
    w.factory('expr::e_%s_12_ratio("@0/@1", e_%s_12_data, e_%s_12_mc)' % (t, t, t))
    w.factory('expr::e_%s_23_ratio("@0/@1", e_%s_23_data, e_%s_23_mc)' % (t, t, t))


histsToWrap = [
    (loc+'Mu23Ele12/muon_SFs.root:data_trg_eff', 'm_trg_23_data'),
    (loc+'Mu23Ele12/muon_SFs.root:ZLL_trg_eff', 'm_trg_23_mc'),
    (loc+'Mu8Ele23/muon_SFs.root:data_trg_eff', 'm_trg_8_data'),
    (loc+'Mu8Ele23/muon_SFs.root:ZLL_trg_eff', 'm_trg_8_mc')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_trg_binned_23_data', ['m_trg_23_data', 'm_trg_23_data', 'm_trg_23_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_trg_binned_23_mc', ['m_trg_23_mc', 'm_trg_23_mc', 'm_trg_23_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_trg_binned_8_data', ['m_trg_8_data', 'm_trg_8_data', 'm_trg_8_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_trg_binned_8_mc', ['m_trg_8_mc', 'm_trg_8_mc', 'm_trg_8_mc'])

for t in ['trg','trg_binned']:
    w.factory('expr::m_%s_23_ratio("@0/@1", m_%s_23_data, m_%s_23_mc)' % (t, t, t))
    w.factory('expr::m_%s_8_ratio("@0/@1", m_%s_8_data, m_%s_8_mc)' % (t, t, t))

# IC EGamma ID, iso, trigger SFs

loc = 'inputs/ICSF/'
        
histsToWrap = [
    (loc+'2017/SingleElectron/electron_SFs.root:data_id_eff', 'e_id_data'),
    (loc+'2017/SingleElectron/electron_SFs.root:ZLL_id_eff', 'e_id_mc'),
    (loc+'2017/SingleElectron/electron_SFs.root:data_iso_eff', 'e_iso_data'),
    (loc+'2017/SingleElectron/electron_SFs.root:ZLL_iso_eff', 'e_iso_mc'),
    (loc+'2017/SingleElectron/electron_SFs.root:data_trg_eff', 'e_trg_data'),
    (loc+'2017/SingleElectron/electron_SFs.root:ZLL_trg_eff', 'e_trg_mc')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.30, 0.50],
                                   'e_trg_binned_data', ['e_trg_data', 'e_trg_data', 'e_trg_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.30, 0.50],
                                   'e_trg_binned_mc', ['e_trg_mc', 'e_trg_mc', 'e_trg_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.30, 0.50],
                                   'e_iso_binned_data', ['e_iso_data', 'e_iso_data', 'e_iso_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.30, 0.50],
                                   'e_iso_binned_mc', ['e_iso_mc', 'e_iso_mc', 'e_iso_mc'])

for t in ['data', 'mc']:
    w.factory('expr::e_idiso_%s("@0*@1", e_id_pog_%s, e_iso_%s)' % (t, t, t))
    w.factory('expr::e_idiso_binned_%s("@0*@1", e_id_pog_%s, e_iso_binned_%s)' % (t, t, t))

for t in ['trg', 'trg_binned', 'id', 'iso', 'iso_binned', 'idiso_binned', 'id_pog', 'idiso_pog', 'looseid_pog', 'looseidiso_pog' ]:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))

## IC em qcd os/ss weights
loc = 'inputs/ICSF/'
wsptools.SafeWrapHist(w, ['expr::m_pt_max100("min(@0,100)",m_pt[0])', 'expr::e_pt_max100("min(@0,100)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_factors_maiso.root:qcd_factors'), 'em_qcd_factors')
wsptools.SafeWrapHist(w, ['expr::m_pt_max100("min(@0,100)",m_pt[0])', 'expr::e_pt_max100("min(@0,100)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_factors_bothaiso.root:qcd_factors'), 'em_qcd_factors_bothaiso')
#wsptools.SafeWrapHist(w, ['expr::dR_max4p5("min(@0,4.5)",dR[0])','expr::njets_max1("min(@0,1)",njets[0])'],  GetFromTFile(loc+'/em_qcd/em_aiso_iso_extrap.root:extrap_uncert'), 'em_qcd_extrap_uncert')
wsptools.SafeWrapHist(w, ['expr::m_pt_max40("min(@0,40)",m_pt[0])','expr::e_pt_max40("min(@0,40)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_isoextrap.root:isoextrap_uncert'), 'em_qcd_extrap_uncert')

w.factory('expr::em_qcd_0jet("(2.162-0.05135*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_1jet("(2.789-0.2712*@0)*@1",dR[0],em_qcd_factors)')

w.factory('expr::em_qcd_0jet_bothaiso("(3.212-0.2186*@0)*@1",dR[0],em_qcd_factors_bothaiso)')
w.factory('expr::em_qcd_1jet_bothaiso("(3.425-0.3629*@0)*@1",dR[0],em_qcd_factors_bothaiso)')

w.factory('expr::em_qcd_0jet_shapeup("(2.162-(0.05135-0.0583)*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_0jet_shapedown("(2.162-(0.05135+0.0583)*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_1jet_shapeup("(2.789-(0.2712-0.0390)*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_1jet_shapedown("(2.789-(0.2712+0.0390)*@0)*@1",dR[0],em_qcd_factors)')

w.factory('expr::em_qcd_0jet_rateup("(2.162+0.192-0.05135*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_0jet_ratedown("(2.162-0.192-0.05135*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_1jet_rateup("(2.789+0.0105-0.2712*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_1jet_ratedown("(2.789-0.0105-0.2712*@0)*@1",dR[0],em_qcd_factors)')

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_binned', ['em_qcd_0jet','em_qcd_1jet'])

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_binned_bothaiso', ['em_qcd_0jet_bothaiso','em_qcd_1jet_bothaiso'])


wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_shapeup_binned', ['em_qcd_0jet_shapeup','em_qcd_1jet_shapeup'])

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_shapedown_binned', ['em_qcd_0jet_shapedown','em_qcd_1jet_shapedown'])

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_rateup_binned', ['em_qcd_0jet_rateup','em_qcd_1jet_rateup'])

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_ratedown_binned', ['em_qcd_0jet_ratedown','em_qcd_1jet_ratedown'])


wsptools.SafeWrapHist(w, ['expr::m_pt_max100("min(@0,100)",m_pt[0])', 'expr::e_pt_max100("min(@0,100)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_factors_2.root:qcd_factors'), 'em_qcd_factors_bothaiso')

w.factory('expr::em_qcd_0jet_bothaiso("(3.208-0.217*@0)*@1",dR[0],em_qcd_factors_bothaiso)')
w.factory('expr::em_qcd_1jet_bothaiso("(3.426-0.3628*@0)*@1",dR[0],em_qcd_factors_bothaiso)')

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_binned_bothaiso', ['em_qcd_0jet_bothaiso','em_qcd_1jet_bothaiso'])

w.factory('expr::em_qcd_extrap_up("@0*@1",em_qcd_osss_binned,em_qcd_extrap_uncert)')
w.factory('expr::em_qcd_extrap_down("@0*(2-@1)",em_qcd_osss_binned,em_qcd_extrap_uncert)')

w.factory('expr::em_qcd_bothaiso_extrap_up("@0*@1",em_qcd_osss_binned_bothaiso,em_qcd_extrap_uncert)')
w.factory('expr::em_qcd_bothaiso_extrap_down("@0*(2-@1)",em_qcd_osss_binned_bothaiso,em_qcd_extrap_uncert)')

em_funcs = ['em_qcd_osss_binned','em_qcd_osss_shapeup_binned','em_qcd_osss_shapedown_binned','em_qcd_osss_rateup_binned','em_qcd_osss_ratedown_binned']
for i in em_funcs:
  w.factory('expr::%s_mva("(@0<=0)*@1 + (@0>0)*1.11632",nbjets[0],%s)' %(i,i))
# add uncertainty on n_bjets>0 bin = +/-36% (11% statistical + 18% background-subtraction + 29% aiso->iso extrapolation added in quadrature)
w.factory('expr::em_qcd_osss_binned_mva_nbjets_up("(@0<=0)*@1 + (@0>0)*1.11632*1.36",nbjets[0],em_qcd_osss_binned)')
w.factory('expr::em_qcd_osss_binned_mva_nbjets_down("(@0<=0)*@1 + (@0>0)*1.11632*0.64",nbjets[0],em_qcd_osss_binned)')



### Muon tracking efficiency scale factor from the muon POG
loc = 'inputs/MuonPOG'

muon_trk_eff_hist = wsptools.TGraphAsymmErrorsToTH1D(GetFromTFile(loc+'/fits.root:ratio_eff_eta3_dr030e030_corr'))
wsptools.SafeWrapHist(w, ['m_eta'], muon_trk_eff_hist, name='m_trk_ratio')

### Electron tracking efficiency scale factor from the egamma POG
loc = 'inputs/EGammaPOG'

electron_trk_eff_hist = GetFromTFile(loc+'/egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root:EGamma_SF2D')
wsptools.SafeWrapHist(w, ['e_eta','e_pt'], electron_trk_eff_hist, name='e_trk_ratio')

### Tau Trigger scale factors from Tau POG

loc = 'inputs/TauTriggerSFs2017/'

tau_id_wps=['medium','tight','vtight']

for wp in tau_id_wps:
  histsToWrap = [
    (loc+'tauTriggerEfficiencies2017_New.root:hist_diTauTriggerEfficiency_%sTauMVA_DATA' % wp,  't_trg_pt_%s_tt_data' % wp),
    (loc+'tauTriggerEfficiencies2017_New.root:hist_diTauTriggerEfficiency_%sTauMVA_MC'% wp,  't_trg_pt_%s_tt_mc' % wp),
    (loc+'tauTriggerEfficiencies2017_New.root:hist_MuTauTriggerEfficiency_%sTauMVA_DATA'% wp,  't_trg_pt_%s_mt_data' % wp),
    (loc+'tauTriggerEfficiencies2017_New.root:hist_MuTauTriggerEfficiency_%sTauMVA_MC' % wp,  't_trg_pt_%s_mt_mc' % wp),
    (loc+'tauTriggerEfficiencies2017_New.root:hist_ETauTriggerEfficiency_%sTauMVA_DATA' % wp,  't_trg_pt_%s_et_data' % wp),
    (loc+'tauTriggerEfficiencies2017_New.root:hist_ETauTriggerEfficiency_%sTauMVA_MC' % wp,  't_trg_pt_%s_et_mc' % wp),

  ]
  for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['t_pt'],
                          GetFromTFile(task[0]), name=task[1])
  
  histsToWrap = [
    (loc+'tauTriggerEfficiencies2017.root:diTau_%s_DATA' % wp,  't_trg_phieta_%s_tt_data' % wp),
    (loc+'tauTriggerEfficiencies2017.root:diTau_%s_MC' % wp,  't_trg_phieta_%s_tt_mc' % wp),
    (loc+'tauTriggerEfficiencies2017.root:diTau_%s_AVG_DATA' % wp,  't_trg_ave_phieta_%s_tt_data' % wp),
    (loc+'tauTriggerEfficiencies2017.root:diTau_%s_AVG_MC' % wp,  't_trg_ave_phieta_%s_tt_mc' % wp),
    (loc+'tauTriggerEfficiencies2017.root:muTau_%s_DATA' % wp,  't_trg_phieta_%s_mt_data' % wp),
    (loc+'tauTriggerEfficiencies2017.root:muTau_%s_MC' % wp,  't_trg_phieta_%s_mt_mc' % wp),
    (loc+'tauTriggerEfficiencies2017.root:muTau_%s_AVG_DATA' % wp,  't_trg_ave_phieta_%s_mt_data' % wp),
    (loc+'tauTriggerEfficiencies2017.root:muTau_%s_AVG_MC' % wp,  't_trg_ave_phieta_%s_mt_mc' % wp),
    (loc+'tauTriggerEfficiencies2017.root:eTau_%s_DATA' % wp,  't_trg_phieta_%s_et_data' % wp),
    (loc+'tauTriggerEfficiencies2017.root:eTau_%s_MC' % wp,  't_trg_phieta_%s_et_mc' % wp),
    (loc+'tauTriggerEfficiencies2017.root:eTau_%s_AVG_DATA' % wp,  't_trg_ave_phieta_%s_et_data' % wp),
    (loc+'tauTriggerEfficiencies2017.root:eTau_%s_AVG_MC' % wp,  't_trg_ave_phieta_%s_et_mc' % wp)

  ]
  for task in histsToWrap:  
    wsptools.SafeWrapHist(w, ['t_eta','t_phi'],
                          GetFromTFile(task[0]), name=task[1])
    
  w.factory('expr::t_trg_%s_tt_data("@0*@1/@2", t_trg_pt_%s_tt_data, t_trg_phieta_%s_tt_data, t_trg_ave_phieta_%s_tt_data)' % (wp, wp, wp, wp))  
  w.factory('expr::t_trg_%s_tt_mc("@0*@1/@2", t_trg_pt_%s_tt_mc, t_trg_phieta_%s_tt_mc, t_trg_ave_phieta_%s_tt_mc)' % (wp, wp, wp, wp))
  
  w.factory('expr::t_trg_%s_et_data("@0*@1/@2", t_trg_pt_%s_et_data, t_trg_phieta_%s_et_data, t_trg_ave_phieta_%s_et_data)' % (wp, wp, wp, wp))  
  w.factory('expr::t_trg_%s_et_mc("@0*@1/@2", t_trg_pt_%s_et_mc, t_trg_phieta_%s_et_mc, t_trg_ave_phieta_%s_et_mc)' % (wp, wp, wp, wp))
  
  w.factory('expr::t_trg_%s_mt_data("@0*@1/@2", t_trg_pt_%s_mt_data, t_trg_phieta_%s_mt_data, t_trg_ave_phieta_%s_mt_data)' % (wp, wp, wp, wp))  
  w.factory('expr::t_trg_%s_mt_mc("@0*@1/@2", t_trg_pt_%s_mt_mc, t_trg_phieta_%s_mt_mc, t_trg_ave_phieta_%s_mt_mc)' % (wp, wp, wp, wp))
  
  w.factory('expr::t_trg_%s_tt_ratio("@0/@1", t_trg_%s_tt_data, t_trg_%s_tt_mc)' % (wp, wp, wp))
  w.factory('expr::t_trg_%s_et_ratio("@0/@1", t_trg_%s_et_data, t_trg_%s_et_mc)' % (wp, wp, wp))
  w.factory('expr::t_trg_%s_mt_ratio("@0/@1", t_trg_%s_mt_data, t_trg_%s_mt_mc)' % (wp, wp, wp))

### Electron leg of etau cross trigger SF -- DESY (for now)
loc = 'inputs/LeptonEfficiencies/Electron/Run2017/'

desyHistsToWrap = [
    (loc+'Electron_EleTau_Ele24.root',           'MC', 'e_trg_EleTau_Ele24Leg_desy_mc'),
    (loc+'Electron_EleTau_Ele24.root',           'Data', 'e_trg_EleTau_Ele24Leg_desy_data'),
]

for task in desyHistsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          wsptools.ProcessDESYLeptonSFs(task[0], task[1], task[2]), name=task[2])

for t in ['trg_EleTau_Ele24Leg_desy']:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))


### LO DYJetsToLL Z mass vs pT correction
#histsToWrap = [
#    ('inputs/DYWeights/dy_weights_2017.root:zptmass_histo'  , 'zptmass_weight_nom'),
#]

#for task in histsToWrap:
#    wsptools.SafeWrapHist(w, ['z_gen_mass', 'z_gen_pt'],
#                          GetFromTFile(task[0]), name=task[1])

histsToWrap = [
    ('inputs/DYWeights/zpt_weights_2017_1D.root:zpt_histo'  , 'zpt_weight_nom'),
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['z_gen_pt'],
                          GetFromTFile(task[0]), name=task[1])

# correction for quark mass dependence to ggH
wsptools.SafeWrapHist(w, ['HpT'],  GetFromTFile('inputs/ICSF/ggH/top_mass_weights.root:pt_weight_toponly'), 'ggH_quarkmass_hist')
w.factory('expr::ggH_quarkmass_corr("1.007*@0", ggH_quarkmass_hist)') # the constant factor is to ensure the normalization doesn't change - it is sample specific
wsptools.SafeWrapHist(w, ['HpT'],  GetFromTFile('inputs/ICSF/ggH/top_mass_weights.root:pt_weight'), 'ggH_fullquarkmass_hist')
w.factory('expr::ggH_fullquarkmass_corr("0.985*@0", ggH_fullquarkmass_hist)') # the constant factor is to ensure the normalization doesn't change - it is sample specific

w.Print()
w.writeToFile('htt_scalefactors_2017_v1.root')
w.Delete()
