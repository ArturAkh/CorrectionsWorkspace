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
    (loc+'2017/SingleMuon/muon_SFs.root:embed_trg_eff', 'm_trg_embed'),
    (loc+'2017/Mu20/muon20_cross_B/muon_SFs.root:data_trg_eff', 'm_trg20_runB_data'),
    (loc+'2017/Mu20/muon20_cross_B/muon_SFs.root:ZLL_trg_eff', 'm_trg20_runB_mc'),
    (loc+'2017/Mu20/muon20_cross_B/muon_SFs.root:embed_trg_eff', 'm_trg20_runB_embed'),
    (loc+'2017/Mu20/muon20_noB/muon_SFs.root:data_trg_eff', 'm_trg20_runCtoF_data'),
    (loc+'2017/Mu20/muon20_noB/muon_SFs.root:ZLL_trg_eff', 'm_trg20_runCtoF_mc'),
    (loc+'2017/Mu20/muon20_noB/muon_SFs.root:embed_trg_eff', 'm_trg20_runCtoF_embed')
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
    w.factory('expr::m_trg20_%s("0.1145*@0+0.8855*@1", m_trg20_runB_%s, m_trg20_runCtoF_%s)' % (t, t, t))



for t in ['trg', 'trg20', 'trg_binned', 'id', 'iso', 'iso_binned', 'idiso_binned' ]:
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
    (loc+'2017/SingleElectron/electron_SFs.root:embed_id_eff', 'e_id_embed'),
    (loc+'2017/SingleElectron/electron_SFs.root:data_iso_eff', 'e_iso_data'),
    (loc+'2017/SingleElectron/electron_SFs.root:ZLL_iso_eff', 'e_iso_mc'),
    (loc+'2017/SingleElectron/electron_SFs.root:embed_iso_eff', 'e_iso_embed'),
    (loc+'2017/SingleElectron/electron_SFs.root:data_trg_eff', 'e_trg_data'),
    (loc+'2017/SingleElectron/electron_SFs.root:ZLL_trg_eff', 'e_trg_mc'),
    (loc+'2017/SingleElectron/electron_SFs.root:embed_trg_eff', 'e_trg_embed'),
    (loc+'2017/Ele24/electron_SFs.root:data_trg_eff', 'e_trg24_data'),
    (loc+'2017/Ele24/electron_SFs.root:ZLL_trg_eff', 'e_trg24_mc'),
    (loc+'2017/Ele24/electron_SFs.root:embed_trg_eff', 'e_trg24_embed'),
    (loc+'2017/Ele24/fromDoubleE/electron_SFs.root:data_trg_eff', 'e_trg24_fromDoubleE_data'),
    (loc+'2017/Ele24/fromDoubleE/electron_SFs.root:ZLL_trg_eff', 'e_trg24_fromDoubleE_mc'),
    (loc+'2017/Ele24/fromDoubleE/electron_SFs.root:embed_trg_eff', 'e_trg24_fromDoubleE_embed'),
    (loc+'2017/SingleElectron_27_32single_35/electron_SFs.root:data_trg_eff','e_trg_27_32_35_data'),
    (loc+'2017/SingleElectron_27_32single_35/electron_SFs.root:ZLL_trg_eff','e_trg_27_32_35_mc'),
    (loc+'2017/SingleElectron_27_32single_35/electron_SFs.root:embed_trg_eff','e_trg_27_32_35_embed')
]
for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.30, 0.50],
                                   'e_trg_binned_data', ['e_trg_data', 'e_trg_data', 'e_trg_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.30, 0.50],
                                   'e_trg_binned_mc', ['e_trg_mc', 'e_trg_mc', 'e_trg_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.30, 0.50],
                                   'e_trg_binned_embed', ['e_trg_embed', 'e_trg_embed', 'e_trg_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.30, 0.50],
                                   'e_iso_binned_data', ['e_iso_data', 'e_iso_data', 'e_iso_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.30, 0.50],
                                   'e_iso_binned_mc', ['e_iso_mc', 'e_iso_mc', 'e_iso_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.30, 0.50],
                                   'e_iso_binned_embed', ['e_iso_embed', 'e_iso_embed', 'e_iso_embed'])

for t in ['data', 'mc']:
    w.factory('expr::e_idiso_%s("@0*@1", e_id_pog_%s, e_iso_%s)' % (t, t, t))
    w.factory('expr::e_idiso_binned_%s("@0*@1", e_id_pog_%s, e_iso_binned_%s)' % (t, t, t))
w.factory('expr::e_idiso_embed("@0*@1", e_id_embed, e_iso_embed)')
w.factory('expr::e_idiso_binned_embed("@0*@1", e_id_embed, e_iso_binned_embed)')

for t in ['trg', 'trg24', 'trg_27_32_35', 'trg24_fromDoubleE', 'trg_binned', 'id', 'iso', 'iso_binned', 'idiso_binned', 'id_pog', 'idiso_pog', 'looseid_pog', 'looseidiso_pog' ]:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))
for t in ['trg', 'trg24', 'trg_27_32_35', 'trg_binned', 'id', 'iso', 'iso_binned', 'idiso_binned']:
    w.factory('expr::e_%s_embed_ratio("@0/@1", e_%s_data, e_%s_embed)' % (t, t, t))


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

## Tau Trigger efficiencies for embedded samples from IC

loc = 'inputs/ICSF/2017/TauTrg/'
tau_id_wps=['vloose','loose','medium','tight']
channels=['tt','et','mt']

for chan in channels:
  for wp in tau_id_wps:
    histsToWrap = [
      (loc+'embed_tau_trig_eff_%s.root:eff_%siso_pt' % (chan,wp), 't_trg_pt_%s_%s_embed' % (wp,chan))
    ]
  
    for task in histsToWrap:
      wsptools.SafeWrapHist(w, ['t_pt'],
                            GetFromTFile(task[0]), name=task[1])
  
    histsToWrap = [
      (loc+'embed_tau_trig_eff_%s.root:eff_%siso_eta' % (chan,wp), 't_trg_phieta_%s_%s_embed' % (wp,chan)),
      (loc+'embed_tau_trig_eff_%s.root:eff_%siso_aveeta' % (chan,wp),'t_trg_ave_phieta_%s_%s_embed' % (wp,chan))
    ]
  
    for task in histsToWrap:
      wsptools.SafeWrapHist(w, ['t_eta'],
                            GetFromTFile(task[0]), name=task[1])
  
    w.factory('expr::t_trg_%s_%s_embed("@0*@1/@2", t_trg_pt_%s_%s_embed, t_trg_phieta_%s_%s_embed, t_trg_ave_phieta_%s_%s_embed)' % (wp, chan, wp, chan, wp, chan, wp, chan))
  
# MC effieicies for closure tests
histsToWrap = [
    (loc+'embed_tau_trig_eff_tt_tightiso_mcfull.root:eff_tightiso_pt' , 't_trg_pt_tight_tt_mcfull' ),
    (loc+'embed_tau_trig_eff_tt_tightiso_mc.root:eff_tightiso_pt' , 't_trg_pt_tight_tt_mccalo' )
]

for task in histsToWrap:
  wsptools.SafeWrapHist(w, ['t_pt'],
                        GetFromTFile(task[0]), name=task[1])

histsToWrap = [
  (loc+'embed_tau_trig_eff_tt_tightiso_mcfull.root:eff_tightiso_eta', 't_trg_phieta_tight_tt_mcfull'),
  (loc+'embed_tau_trig_eff_tt_tightiso_mcfull.root:eff_tightiso_aveeta','t_trg_ave_phieta_tight_tt_mcfull'),
  (loc+'embed_tau_trig_eff_tt_tightiso_mc.root:eff_tightiso_eta', 't_trg_phieta_tight_tt_mccalo'),
  (loc+'embed_tau_trig_eff_tt_tightiso_mc.root:eff_tightiso_aveeta','t_trg_ave_phieta_tight_tt_mccalo' )
]

for task in histsToWrap:
  wsptools.SafeWrapHist(w, ['t_eta'],
                        GetFromTFile(task[0]), name=task[1])

w.factory('expr::t_trg_tight_tt_mcfull("@0*@1/@2", t_trg_pt_tight_tt_mcfull, t_trg_phieta_tight_tt_mcfull, t_trg_ave_phieta_tight_tt_mcfull)')
w.factory('expr::t_trg_tight_tt_mccalo("@0*@1/@2", t_trg_pt_tight_tt_mccalo, t_trg_phieta_tight_tt_mccalo, t_trg_ave_phieta_tight_tt_mccalo)') 
w.factory('expr::t_trg_tight_tt_mcclose("@0/@1", t_trg_tight_tt_mcfull, t_trg_tight_tt_mccalo)')


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
histsToWrap = [
    ('inputs/zpt_weights_2017.root:zptmass_histo'  , 'zptmass_weight_nom'),
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['z_gen_mass', 'z_gen_pt'],
                          GetFromTFile(task[0]), name=task[1])

histsToWrap = [
    ('inputs/DYWeights/zpt_weights_2017_1D.root:zpt_weight'  , 'zpt_weight_nom'),
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['z_gen_pt'],
                          GetFromTFile(task[0]), name=task[1])

# correction for quark mass dependence to ggH
wsptools.SafeWrapHist(w, ['HpT'],  GetFromTFile('inputs/ICSF/ggH/quarkmass_uncerts.root:nom'), 'ggH_quarkmass_hist')
w.factory('expr::ggH_quarkmass_corr("1.007*@0", ggH_quarkmass_hist)') # the constant factor is to ensure the normalization doesn't change - it is sample specific

wsptools.SafeWrapHist(w, ['HpT'],  GetFromTFile('inputs/ICSF/ggH/quarkmass_uncerts.root:qup'), 'ggH_quarkmass_hist_up')
w.factory('expr::ggH_quarkmass_corr_up("1.007*@0", ggH_quarkmass_hist_up)')
wsptools.SafeWrapHist(w, ['HpT'],  GetFromTFile('inputs/ICSF/ggH/quarkmass_uncerts.root:qdown'), 'ggH_quarkmass_hist_down')
w.factory('expr::ggH_quarkmass_corr_down("1.007*@0", ggH_quarkmass_hist_down)')

wsptools.SafeWrapHist(w, ['HpT'],  GetFromTFile('inputs/ICSF/ggH/top_mass_weights.root:pt_weight'), 'ggH_fullquarkmass_hist')
w.factory('expr::ggH_fullquarkmass_corr("0.985*@0", ggH_fullquarkmass_hist)') # the constant factor is to ensure the normalization doesn't change - it is sample specific

loc = 'inputs/ICSF/ggH/MG_ps_uncerts.root:'
histsToWrap = [
    (loc + 'ps_0jet_up', 'ps_0jet_up'),
    (loc + 'ps_0jet_down', 'ps_0jet_down'),
    (loc + 'ps_1jet_up', 'ps_1jet_up'),
    (loc + 'ps_1jet_down', 'ps_1jet_down'),
    (loc + 'ps_2jet_up', 'ps_2jet_up'),
    (loc + 'ps_2jet_down', 'ps_2jet_down'),
    (loc + 'ps_3jet_up', 'ps_3jet_up'),
    (loc + 'ps_3jet_down', 'ps_3jet_down')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['HpT'],
                          GetFromTFile(task[0]), name=task[1])

for shift in ['up', 'down']:
  wsptools.MakeBinnedCategoryFuncMap(w, 'ngenjets', [0, 1, 2, 3, 1000],
                                     'ggH_mg_ps_%s' % shift, ['ps_0jet_%s' % shift, 'ps_1jet_%s' % shift, 'ps_2jet_%s' % shift, 'ps_3jet_%s' % shift])


histsToWrap = [
    (loc + 'ue_up', 'ggH_mg_ue_up'),
    (loc + 'ue_down', 'ggH_mg_ue_down')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['ngenjets'],
                          GetFromTFile(task[0]), name=task[1])

### KIT electron/muon tag and probe results

# triggr SFs Muons from KIT
loc = 'inputs/KIT/v17_5/'


histsToWrap = [
    (loc+'ZmmTP_Data_sm_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',                'm_id_kit_data'),
    (loc+'ZmmTP_DY_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',                  'm_id_kit_mc'),
    (loc+'ZmmTP_Embedding_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',           'm_id_kit_embed'),

    (loc+'ZmmTP_Data_sm_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',              'm_iso_kit_data'),
    (loc+'ZmmTP_DY_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',                'm_iso_kit_mc'),
    (loc+'ZmmTP_Embedding_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',         'm_iso_kit_embed'),

    (loc+'ZmmTP_Data_sm_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',              'm_aiso1_kit_data'),
    (loc+'ZmmTP_DY_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',                'm_aiso1_kit_mc'),
    (loc+'ZmmTP_Embedding_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',         'm_aiso1_kit_embed'),

    (loc+'ZmmTP_Data_sm_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',              'm_aiso2_kit_data'),
    (loc+'ZmmTP_DY_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',                'm_aiso2_kit_mc'),
    (loc+'ZmmTP_Embedding_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',         'm_aiso2_kit_embed'),

    (loc+'ZmmTP_Data_sm_Fits_Trg_IsoMu24_pt_eta_bins.root:Trg_IsoMu24_pt_eta_bins',      'm_trg24_kit_data'),
    (loc+'ZmmTP_DY_Fits_Trg_IsoMu24_pt_eta_bins.root:Trg_IsoMu24_pt_eta_bins',        'm_trg24_kit_mc'),
    (loc+'ZmmTP_Embedding_Fits_Trg_IsoMu24_pt_eta_bins.root:Trg_IsoMu24_pt_eta_bins', 'm_trg24_kit_embed'),
    (loc+'ZmmTP_Data_sm_Fits_Trg_IsoMu24_AIso1_pt_bins_inc_eta.root:Trg_IsoMu24_AIso1_pt_bins_inc_eta',      'm_trg24_aiso1_kit_data'),
    (loc+'ZmmTP_DY_Fits_Trg_IsoMu24_AIso1_pt_bins_inc_eta.root:Trg_IsoMu24_AIso1_pt_bins_inc_eta',        'm_trg24_aiso1_kit_mc'),
    (loc+'ZmmTP_Embedding_Fits_Trg_IsoMu24_AIso1_pt_bins_inc_eta.root:Trg_IsoMu24_AIso1_pt_bins_inc_eta', 'm_trg24_aiso1_kit_embed'),
    (loc+'ZmmTP_Data_sm_Fits_Trg_IsoMu24_AIso2_pt_bins_inc_eta.root:Trg_IsoMu24_AIso2_pt_bins_inc_eta',      'm_trg24_aiso2_kit_data'),
    (loc+'ZmmTP_DY_Fits_Trg_IsoMu24_AIso2_pt_bins_inc_eta.root:Trg_IsoMu24_AIso2_pt_bins_inc_eta',        'm_trg24_aiso2_kit_mc'),
    (loc+'ZmmTP_Embedding_Fits_Trg_IsoMu24_AIso2_pt_bins_inc_eta.root:Trg_IsoMu24_AIso2_pt_bins_inc_eta', 'm_trg24_aiso2_kit_embed'),

    (loc+'ZmmTP_Data_sm_Fits_Trg_IsoMu27_pt_eta_bins.root:Trg_IsoMu27_pt_eta_bins',      'm_trg27_kit_data'),
    (loc+'ZmmTP_DY_Fits_Trg_IsoMu27_pt_eta_bins.root:Trg_IsoMu27_pt_eta_bins',        'm_trg27_kit_mc'),
    (loc+'ZmmTP_Embedding_Fits_Trg_IsoMu27_pt_eta_bins.root:Trg_IsoMu27_pt_eta_bins', 'm_trg27_kit_embed'),
    (loc+'ZmmTP_Data_sm_Fits_Trg_IsoMu27_AIso1_pt_bins_inc_eta.root:Trg_IsoMu27_AIso1_pt_bins_inc_eta',      'm_trg27_aiso1_kit_data'),
    (loc+'ZmmTP_DY_Fits_Trg_IsoMu27_AIso1_pt_bins_inc_eta.root:Trg_IsoMu27_AIso1_pt_bins_inc_eta',        'm_trg27_aiso1_kit_mc'),
    (loc+'ZmmTP_Embedding_Fits_Trg_IsoMu27_AIso1_pt_bins_inc_eta.root:Trg_IsoMu27_AIso1_pt_bins_inc_eta', 'm_trg27_aiso1_kit_embed'),
    (loc+'ZmmTP_Data_sm_Fits_Trg_IsoMu27_AIso2_pt_bins_inc_eta.root:Trg_IsoMu27_AIso2_pt_bins_inc_eta',      'm_trg27_aiso2_kit_data'),
    (loc+'ZmmTP_DY_Fits_Trg_IsoMu27_AIso2_pt_bins_inc_eta.root:Trg_IsoMu27_AIso2_pt_bins_inc_eta',        'm_trg27_aiso2_kit_mc'),
    (loc+'ZmmTP_Embedding_Fits_Trg_IsoMu27_AIso2_pt_bins_inc_eta.root:Trg_IsoMu27_AIso2_pt_bins_inc_eta', 'm_trg27_aiso2_kit_embed'),

    (loc+'ZmmTP_Data_sm_Fits_Trg_IsoMu27_or_IsoMu24_pt_eta_bins.root:Trg_IsoMu27_or_IsoMu24_pt_eta_bins',      'm_trg24_27_kit_data'),
    (loc+'ZmmTP_DY_Fits_Trg_IsoMu27_or_IsoMu24_pt_eta_bins.root:Trg_IsoMu27_or_IsoMu24_pt_eta_bins',        'm_trg24_27_kit_mc'),
    (loc+'ZmmTP_Embedding_Fits_Trg_IsoMu27_or_IsoMu24_pt_eta_bins.root:Trg_IsoMu27_or_IsoMu24_pt_eta_bins', 'm_trg24_27_kit_embed'),
    (loc+'ZmmTP_Data_sm_Fits_Trg_IsoMu27_or_IsoMu24_AIso1_pt_bins_inc_eta.root:Trg_IsoMu27_or_IsoMu24_AIso1_pt_bins_inc_eta',      'm_trg24_27_aiso1_kit_data'),
    (loc+'ZmmTP_DY_Fits_Trg_IsoMu27_or_IsoMu24_AIso1_pt_bins_inc_eta.root:Trg_IsoMu27_or_IsoMu24_AIso1_pt_bins_inc_eta',        'm_trg24_27_aiso1_kit_mc'),
    (loc+'ZmmTP_Embedding_Fits_Trg_IsoMu27_or_IsoMu24_AIso1_pt_bins_inc_eta.root:Trg_IsoMu27_or_IsoMu24_AIso1_pt_bins_inc_eta', 'm_trg24_27_aiso1_kit_embed'),
    (loc+'ZmmTP_Data_sm_Fits_Trg_IsoMu27_or_IsoMu24_AIso2_pt_bins_inc_eta.root:Trg_IsoMu27_or_IsoMu24_AIso2_pt_bins_inc_eta',      'm_trg24_27_aiso2_kit_data'),
    (loc+'ZmmTP_DY_Fits_Trg_IsoMu27_or_IsoMu24_AIso2_pt_bins_inc_eta.root:Trg_IsoMu27_or_IsoMu24_AIso2_pt_bins_inc_eta',        'm_trg24_27_aiso2_kit_mc'),
    (loc+'ZmmTP_Embedding_Fits_Trg_IsoMu27_or_IsoMu24_AIso2_pt_bins_inc_eta.root:Trg_IsoMu27_or_IsoMu24_AIso2_pt_bins_inc_eta', 'm_trg24_27_aiso2_kit_embed'),
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg24_binned_kit_data', ['m_trg24_kit_data', 'm_trg24_aiso1_kit_data', 'm_trg24_aiso2_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg24_binned_kit_mc', ['m_trg24_kit_mc', 'm_trg24_aiso1_kit_mc', 'm_trg24_aiso2_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg24_binned_kit_embed', ['m_trg24_kit_embed', 'm_trg24_aiso1_kit_embed', 'm_trg24_aiso2_kit_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg27_binned_kit_data', ['m_trg27_kit_data', 'm_trg27_aiso1_kit_data', 'm_trg27_aiso2_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg27_binned_kit_mc', ['m_trg27_kit_mc', 'm_trg27_aiso1_kit_mc', 'm_trg27_aiso2_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg27_binned_kit_embed', ['m_trg27_kit_embed', 'm_trg27_aiso1_kit_embed', 'm_trg27_aiso2_kit_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg24_27_binned_kit_data', ['m_trg24_27_kit_data', 'm_trg24_27_aiso1_kit_data', 'm_trg24_27_aiso2_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg24_27_binned_kit_mc', ['m_trg24_27_kit_mc', 'm_trg24_27_aiso1_kit_mc', 'm_trg24_27_aiso2_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg24_27_binned_kit_embed', ['m_trg24_27_kit_embed', 'm_trg24_27_aiso1_kit_embed', 'm_trg24_27_aiso2_kit_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_iso_binned_kit_data', ['m_iso_kit_data', 'm_aiso1_kit_data', 'm_aiso2_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_iso_binned_kit_mc', ['m_iso_kit_mc', 'm_aiso1_kit_mc', 'm_aiso2_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_iso_binned_kit_embed', ['m_iso_kit_embed', 'm_aiso1_kit_embed', 'm_aiso2_kit_embed'])

for t in ['data', 'mc', 'embed']:
    w.factory('expr::m_idiso_kit_%s("@0*@1", m_id_kit_%s, m_iso_kit_%s)' % (t, t, t))
    w.factory('expr::m_idiso_binned_kit_%s("@0*@1", m_id_kit_%s, m_iso_binned_kit_%s)' % (t, t, t))

for t in ['trg24', 'trg24_binned', 'trg27', 'trg27_binned', 'trg24_27', 'trg24_27_binned', 'id', 'iso', 'iso_binned', 'idiso_binned' ]:
    w.factory('expr::m_%s_kit_ratio("min(10.,(@0/@1))", m_%s_kit_data, m_%s_kit_mc)' % (t, t, t))
    w.factory('expr::m_%s_embed_kit_ratio("min(10.,(@0/@1))", m_%s_kit_data, m_%s_kit_embed)' % (t, t, t))

# trigger SFs Electrons from KIT
loc = 'inputs/KIT/v17_6/'

histsToWrap = [
    (loc+'ZeeTP_Data_Fits_ID90_pt_eta_bins.root:ID90_pt_eta_bins',                'e_id90_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_ID90_pt_eta_bins.root:ID90_pt_eta_bins',                  'e_id90_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_ID90_pt_eta_bins.root:ID90_pt_eta_bins',           'e_id90_kit_embed'),
    (loc+'ZeeTP_Data_Fits_ID80_pt_eta_bins.root:ID80_pt_eta_bins',                'e_id80_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_ID80_pt_eta_bins.root:ID80_pt_eta_bins',                  'e_id80_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_ID80_pt_eta_bins.root:ID80_pt_eta_bins',           'e_id80_kit_embed'),

    (loc+'ZeeTP_Data_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',              'e_iso_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',                'e_iso_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',         'e_iso_kit_embed'),
    (loc+'ZeeTP_Data_Fits_AIso_pt_eta_bins.root:AIso_pt_eta_bins',              'e_aiso_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_AIso_pt_eta_bins.root:AIso_pt_eta_bins',                'e_aiso_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_AIso_pt_eta_bins.root:AIso_pt_eta_bins',         'e_aiso_kit_embed'),
    # (loc+'ZeeTP_Data_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',              'e_aiso2_kit_data'),
    # (loc+'ZeeTP_DYJetsToLL_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',                'e_aiso2_kit_mc'),
    # (loc+'ZeeTP_Embedding_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',         'e_aiso2_kit_embed'),

    (loc+'ZeeTP_Data_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',      'e_trg_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',        'e_trg_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins', 'e_trg_kit_embed'),
    (loc+'ZeeTP_Data_Fits_Trg_AIso_pt_bins_inc_eta.root:Trg_AIso_pt_bins_inc_eta',      'e_trg_aiso_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg_AIso_pt_bins_inc_eta.root:Trg_AIso_pt_bins_inc_eta',        'e_trg_aiso_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg_AIso_pt_bins_inc_eta.root:Trg_AIso_pt_bins_inc_eta', 'e_trg_aiso_kit_embed'),
    # (loc+'ZeeTP_Data_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',      'e_trg_aiso2_kit_data'),
    # (loc+'ZeeTP_DYJetsToLL_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',        'e_trg_aiso2_kit_mc'),
    # (loc+'ZeeTP_Embedding_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta', 'e_trg_aiso2_kit_embed'),

    (loc+'ZeeTP_Data_Fits_Trg27_Iso_pt_eta_bins.root:Trg27_Iso_pt_eta_bins',      'e_trg27_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg27_Iso_pt_eta_bins.root:Trg27_Iso_pt_eta_bins',        'e_trg27_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg27_Iso_pt_eta_bins.root:Trg27_Iso_pt_eta_bins', 'e_trg27_kit_embed'),
    (loc+'ZeeTP_Data_Fits_Trg27_AIso_pt_bins_inc_eta.root:Trg27_AIso_pt_bins_inc_eta',      'e_trg27_aiso_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg27_AIso_pt_bins_inc_eta.root:Trg27_AIso_pt_bins_inc_eta',        'e_trg27_aiso_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg27_AIso_pt_bins_inc_eta.root:Trg27_AIso_pt_bins_inc_eta', 'e_trg27_aiso_kit_embed'),

    (loc+'ZeeTP_Data_Fits_Trg32_Iso_pt_eta_bins.root:Trg32_Iso_pt_eta_bins',      'e_trg32_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg32_Iso_pt_eta_bins.root:Trg32_Iso_pt_eta_bins',        'e_trg32_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg32_Iso_pt_eta_bins.root:Trg32_Iso_pt_eta_bins', 'e_trg32_kit_embed'),
    (loc+'ZeeTP_Data_Fits_Trg32_AIso_pt_bins_inc_eta.root:Trg32_AIso_pt_bins_inc_eta',      'e_trg32_aiso_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg32_AIso_pt_bins_inc_eta.root:Trg32_AIso_pt_bins_inc_eta',        'e_trg32_aiso_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg32_AIso_pt_bins_inc_eta.root:Trg32_AIso_pt_bins_inc_eta', 'e_trg32_aiso_kit_embed'),

    (loc+'ZeeTP_Data_Fits_Trg32_fb_Iso_pt_eta_bins.root:Trg32_fb_Iso_pt_eta_bins',      'e_trg32fb_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg32_fb_Iso_pt_eta_bins.root:Trg32_fb_Iso_pt_eta_bins',        'e_trg32fb_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg32_fb_Iso_pt_eta_bins.root:Trg32_fb_Iso_pt_eta_bins', 'e_trg32fb_kit_embed'),
    (loc+'ZeeTP_Data_Fits_Trg32_fb_AIso_pt_bins_inc_eta.root:Trg32_fb_AIso_pt_bins_inc_eta',      'e_trg32fb_aiso_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg32_fb_AIso_pt_bins_inc_eta.root:Trg32_fb_AIso_pt_bins_inc_eta',        'e_trg32fb_aiso_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg32_fb_AIso_pt_bins_inc_eta.root:Trg32_fb_AIso_pt_bins_inc_eta', 'e_trg32fb_aiso_kit_embed'),

    (loc+'ZeeTP_Data_Fits_Trg35_Iso_pt_eta_bins.root:Trg35_Iso_pt_eta_bins',      'e_trg35_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg35_Iso_pt_eta_bins.root:Trg35_Iso_pt_eta_bins',        'e_trg35_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg35_Iso_pt_eta_bins.root:Trg35_Iso_pt_eta_bins', 'e_trg35_kit_embed'),
    (loc+'ZeeTP_Data_Fits_Trg35_AIso_pt_bins_inc_eta.root:Trg35_AIso_pt_bins_inc_eta',      'e_trg35_aiso_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg35_AIso_pt_bins_inc_eta.root:Trg35_AIso_pt_bins_inc_eta',        'e_trg35_aiso_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg35_AIso_pt_bins_inc_eta.root:Trg35_AIso_pt_bins_inc_eta', 'e_trg35_aiso_kit_embed'),

    (loc+'ZeeTP_Data_Fits_Trg27_or_Trg32_Iso_pt_eta_bins.root:Trg27_or_Trg32_Iso_pt_eta_bins',      'e_trg27_trg32_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg27_or_Trg32_Iso_pt_eta_bins.root:Trg27_or_Trg32_Iso_pt_eta_bins',        'e_trg27_trg32_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg27_or_Trg32_Iso_pt_eta_bins.root:Trg27_or_Trg32_Iso_pt_eta_bins', 'e_trg27_trg32_kit_embed'),
    (loc+'ZeeTP_Data_Fits_Trg27_or_Trg32_AIso_pt_bins_inc_eta.root:Trg27_or_Trg32_AIso_pt_bins_inc_eta',      'e_trg27_trg32_aiso_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg27_or_Trg32_AIso_pt_bins_inc_eta.root:Trg27_or_Trg32_AIso_pt_bins_inc_eta',        'e_trg27_trg32_aiso_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg27_or_Trg32_AIso_pt_bins_inc_eta.root:Trg27_or_Trg32_AIso_pt_bins_inc_eta', 'e_trg27_trg32_aiso_kit_embed'),

    (loc+'ZeeTP_Data_Fits_Trg27_or_Trg35_Iso_pt_eta_bins.root:Trg27_or_Trg35_Iso_pt_eta_bins',      'e_trg27_trg35_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg27_or_Trg35_Iso_pt_eta_bins.root:Trg27_or_Trg35_Iso_pt_eta_bins',        'e_trg27_trg35_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg27_or_Trg35_Iso_pt_eta_bins.root:Trg27_or_Trg35_Iso_pt_eta_bins', 'e_trg27_trg35_kit_embed'),
    (loc+'ZeeTP_Data_Fits_Trg27_or_Trg35_AIso_pt_bins_inc_eta.root:Trg27_or_Trg35_AIso_pt_bins_inc_eta',      'e_trg27_trg35_aiso_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg27_or_Trg35_AIso_pt_bins_inc_eta.root:Trg27_or_Trg35_AIso_pt_bins_inc_eta',        'e_trg27_trg35_aiso_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg27_or_Trg35_AIso_pt_bins_inc_eta.root:Trg27_or_Trg35_AIso_pt_bins_inc_eta', 'e_trg27_trg35_aiso_kit_embed'),


    (loc+'ZeeTP_Data_Fits_Trg32_or_Trg35_Iso_pt_eta_bins.root:Trg32_or_Trg35_Iso_pt_eta_bins',      'e_trg32_trg35_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg32_or_Trg35_Iso_pt_eta_bins.root:Trg32_or_Trg35_Iso_pt_eta_bins',        'e_trg32_trg35_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg32_or_Trg35_Iso_pt_eta_bins.root:Trg32_or_Trg35_Iso_pt_eta_bins', 'e_trg32_trg35_kit_embed'),
    (loc+'ZeeTP_Data_Fits_Trg32_or_Trg35_AIso_pt_bins_inc_eta.root:Trg32_or_Trg35_AIso_pt_bins_inc_eta',      'e_trg32_trg35_aiso_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg32_or_Trg35_AIso_pt_bins_inc_eta.root:Trg32_or_Trg35_AIso_pt_bins_inc_eta',        'e_trg32_trg35_aiso_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg32_or_Trg35_AIso_pt_bins_inc_eta.root:Trg32_or_Trg35_AIso_pt_bins_inc_eta', 'e_trg32_trg35_aiso_kit_embed'),

    (loc+'ZeeTP_Data_Fits_Trg27_or_Trg32_or_Trg35_Iso_pt_eta_bins.root:Trg27_or_Trg32_or_Trg35_Iso_pt_eta_bins',      'e_trg27_trg32_trg35_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg27_or_Trg32_or_Trg35_Iso_pt_eta_bins.root:Trg27_or_Trg32_or_Trg35_Iso_pt_eta_bins',        'e_trg27_trg32_trg35_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg27_or_Trg32_or_Trg35_Iso_pt_eta_bins.root:Trg27_or_Trg32_or_Trg35_Iso_pt_eta_bins', 'e_trg27_trg32_trg35_kit_embed'),
    (loc+'ZeeTP_Data_Fits_Trg27_or_Trg32_or_Trg35_AIso_pt_bins_inc_eta.root:Trg27_or_Trg32_or_Trg35_AIso_pt_bins_inc_eta',      'e_trg27_trg32_trg35_aiso_kit_data'),
    (loc+'ZeeTP_DYJetsToLL_Fits_Trg27_or_Trg32_or_Trg35_AIso_pt_bins_inc_eta.root:Trg27_or_Trg32_or_Trg35_AIso_pt_bins_inc_eta',        'e_trg27_trg32_trg35_aiso_kit_mc'),
    (loc+'ZeeTP_Embedding_Fits_Trg27_or_Trg32_or_Trg35_AIso_pt_bins_inc_eta.root:Trg27_or_Trg32_or_Trg35_AIso_pt_bins_inc_eta', 'e_trg27_trg32_trg35_aiso_kit_embed'),


]
for task in histsToWrap:
    print task
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])


wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg_binned_kit_data', ['e_trg_kit_data', 'e_trg_aiso_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg_binned_kit_mc', ['e_trg_kit_mc', 'e_trg_aiso_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg_binned_kit_embed', ['e_trg_kit_embed', 'e_trg_aiso_kit_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg27_binned_kit_data', ['e_trg27_kit_data', 'e_trg27_aiso_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg27_binned_kit_mc', ['e_trg27_kit_mc', 'e_trg27_aiso_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg27_binned_kit_embed', ['e_trg27_kit_embed', 'e_trg27_aiso_kit_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg32_binned_kit_data', ['e_trg32_kit_data', 'e_trg32_aiso_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg32_binned_kit_mc', ['e_trg32_kit_mc', 'e_trg32_aiso_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg32_binned_kit_embed', ['e_trg32_kit_embed', 'e_trg32_aiso_kit_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg32fb_binned_kit_data', ['e_trg32fb_kit_data', 'e_trg32fb_aiso_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg32fb_binned_kit_mc', ['e_trg32fb_kit_mc', 'e_trg32fb_aiso_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg32fb_binned_kit_embed', ['e_trg32fb_kit_embed', 'e_trg32fb_aiso_kit_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg35_binned_kit_data', ['e_trg35_kit_data', 'e_trg35_aiso_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg35_binned_kit_mc', ['e_trg35_kit_mc', 'e_trg35_aiso_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg35_binned_kit_embed', ['e_trg35_kit_embed', 'e_trg35_aiso_kit_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg27_trg32_binned_kit_data', ['e_trg27_trg32_kit_data', 'e_trg27_trg32_aiso_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg27_trg32_binned_kit_mc', ['e_trg27_trg32_kit_mc', 'e_trg27_trg32_aiso_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg27_trg32_binned_kit_embed', ['e_trg27_trg32_kit_embed', 'e_trg27_trg32_aiso_kit_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg27_trg35_binned_kit_data', ['e_trg27_trg35_kit_data', 'e_trg27_trg35_aiso_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg27_trg35_binned_kit_mc', ['e_trg27_trg35_kit_mc', 'e_trg27_trg35_aiso_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg27_trg35_binned_kit_embed', ['e_trg27_trg35_kit_embed', 'e_trg27_trg35_aiso_kit_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg32_trg35_binned_kit_data', ['e_trg32_trg35_kit_data', 'e_trg32_trg35_aiso_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg32_trg35_binned_kit_mc', ['e_trg32_trg35_kit_mc', 'e_trg32_trg35_aiso_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg32_trg35_binned_kit_embed', ['e_trg32_trg35_kit_embed', 'e_trg32_trg35_aiso_kit_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg27_trg32_trg35_binned_kit_data', ['e_trg27_trg32_trg35_kit_data', 'e_trg27_trg32_trg35_aiso_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg27_trg32_trg35_binned_kit_mc', ['e_trg27_trg32_trg35_kit_mc', 'e_trg27_trg32_trg35_aiso_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_trg27_trg32_trg35_binned_kit_embed', ['e_trg27_trg32_trg35_kit_embed', 'e_trg27_trg32_trg35_aiso_kit_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_iso_binned_kit_data', ['e_iso_kit_data', 'e_aiso_kit_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_iso_binned_kit_mc', ['e_iso_kit_mc', 'e_aiso_kit_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15,  0.50],
                                   'e_iso_binned_kit_embed', ['e_iso_kit_embed', 'e_aiso_kit_embed'])


for t in ['data', 'mc', 'embed']:
    w.factory('expr::e_id80iso_kit_%s("@0*@1", e_id80_kit_%s, e_iso_kit_%s)' % (t, t, t))
    w.factory('expr::e_id80iso_binned_kit_%s("@0*@1", e_id80_kit_%s, e_iso_binned_kit_%s)' % (t, t, t))
    w.factory('expr::e_id90iso_kit_%s("@0*@1", e_id90_kit_%s, e_iso_kit_%s)' % (t, t, t))
    w.factory('expr::e_id90iso_binned_kit_%s("@0*@1", e_id90_kit_%s, e_iso_binned_kit_%s)' % (t, t, t))

for t in ['trg', 'trg_binned', 'trg27_trg32', 'trg27_trg32_binned', 'trg27_trg35', 'trg27_trg35_binned', 'trg32_trg35', 'trg32_trg35_binned', 'trg27_trg32_trg35', 'trg27_trg32_trg35_binned', 'trg27', 'trg32', 'trg32fb', 'trg35','id90', 'id80', 'iso', 'iso_binned', 'id90iso_binned', 'id80iso_binned']:
    w.factory('expr::e_%s_kit_ratio("min(10.,(@0/@1))", e_%s_kit_data, e_%s_kit_mc)' % (t, t, t))
    w.factory('expr::e_%s_embed_kit_ratio("min(10.,(@0/@1))", e_%s_kit_data, e_%s_kit_embed)' % (t, t, t))

w.Print()
w.writeToFile('htt_scalefactors_2017_v3.root')
w.Delete()
