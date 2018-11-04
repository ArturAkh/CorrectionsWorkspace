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
ROOT.gROOT.LoadMacro("CrystalBallEfficiency.cxx+")

w = ROOT.RooWorkspace('w')


### KIT electron/muon tag and probe results
loc = 'inputs/KIT/v16_3'

histsToWrap = [
    (loc+'/ZmmTP_Data_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',                    'm_id_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',              'm_id_mc'),
    (loc+'/ZmmTP_Data_Fits_IDIso_pt_eta_bins.root:IDIso_pt_eta_bins',                    'm_idiso_singlefit_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_IDIso_pt_eta_bins.root:IDIso_pt_eta_bins',              'm_idiso_singlefit_mc'),
    (loc+'/ZmmTP_Data_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',                        'm_iso_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',                  'm_iso_mc'),
    (loc+'/ZmmTP_Data_Fits_ID_pt_eta_finebins.root:ID_pt_eta_finebins',                    'm_id_finebins_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_ID_pt_eta_finebins.root:ID_pt_eta_finebins',              'm_id_finebins_mc'),
    (loc+'/ZmmTP_Data_Fits_Iso_pt_eta_finebins.root:Iso_pt_eta_finebins',                        'm_iso_finebins_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_Iso_pt_eta_finebins.root:Iso_pt_eta_finebins',                  'm_iso_finebins_mc'),
    (loc+'/ZmmTP_Data_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',                    'm_aiso1_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',              'm_aiso1_mc'),
    (loc+'/ZmmTP_Data_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',                    'm_aiso2_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',              'm_aiso2_mc'),
    (loc+'/ZmmTP_Data_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',                'm_trg_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',                'm_trg_mc'),
    #(loc+'/ZmmTP_Data_Fits_Trg_AIso1_pt_bins_inc_eta.root:Trg_AIso1_pt_bins_inc_eta',    'm_trg_aiso1_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_Trg_AIso1_pt_bins_inc_eta.root:Trg_AIso1_pt_bins_inc_eta',    'm_trg_aiso1_mc'),
    #(loc+'/ZmmTP_Data_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',    'm_trg_aiso2_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',    'm_trg_aiso2_mc'),
    #(loc+'/ZmmTP_Data_Fits_TrgOR_Iso_pt_eta_bins.root:TrgOR_Iso_pt_eta_bins',              'm_trgOR_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR_Iso_pt_eta_bins.root:TrgOR_Iso_pt_eta_bins',              'm_trgOR_mc'),
    #(loc+'/ZmmTP_Data_Fits_TrgOR_AIso1_pt_bins_inc_eta.root:TrgOR_AIso1_pt_bins_inc_eta',  'm_trgOR_aiso1_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR_AIso1_pt_bins_inc_eta.root:TrgOR_AIso1_pt_bins_inc_eta',  'm_trgOR_aiso1_mc'),
    #(loc+'/ZmmTP_Data_Fits_TrgOR_AIso2_pt_bins_inc_eta.root:TrgOR_AIso2_pt_bins_inc_eta',  'm_trgOR_aiso2_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR_AIso2_pt_bins_inc_eta.root:TrgOR_AIso2_pt_bins_inc_eta',  'm_trgOR_aiso2_mc'),
    #(loc+'/ZmmTP_Data_Fits_TrgOR3_Iso_pt_eta_bins.root:TrgOR3_Iso_pt_eta_bins',              'm_trgOR3_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR3_Iso_pt_eta_bins.root:TrgOR3_Iso_pt_eta_bins',              'm_trgOR3_mc'),
    (loc+'/ZmmTP_Data_Fits_Trg24_Iso_pt_eta_bins.root:Trg24_Iso_pt_eta_bins',                'm_trg24_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_Trg24_Iso_pt_eta_bins.root:Trg24_Iso_pt_eta_bins',                'm_trg24_mc'),
    (loc+'/ZmmTP_Data_Fits_Trg24OR_Iso_pt_eta_bins.root:Trg24OR_Iso_pt_eta_bins',                'm_trg24OR_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_Trg24OR_Iso_pt_eta_bins.root:Trg24OR_Iso_pt_eta_bins',                'm_trg24OR_mc'),
    #(loc+'/ZmmTP_Data_Fits_Trg24OR3_Iso_pt_eta_bins.root:Trg24OR3_Iso_pt_eta_bins',                'm_trg24OR3_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_Trg24OR3_Iso_pt_eta_bins.root:Trg24OR3_Iso_pt_eta_bins',                'm_trg24OR3_mc')
    (loc+'/ZmmTP_Data_Fits_TrgOR4_Iso_pt_eta_bins.root:TrgOR4_Iso_pt_eta_bins',                'm_trgOR4_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR4_Iso_pt_eta_bins.root:TrgOR4_Iso_pt_eta_bins',                'm_trgOR4_mc'),
    (loc+'/ZmmTP_Data_Fits_TrgOR4_AIso1_pt_bins_inc_eta.root:TrgOR4_AIso1_pt_bins_inc_eta',    'm_trgOR4_aiso1_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR4_AIso1_pt_bins_inc_eta.root:TrgOR4_AIso1_pt_bins_inc_eta',    'm_trgOR4_aiso1_mc'),
    (loc+'/ZmmTP_Data_Fits_TrgOR4_AIso2_pt_bins_inc_eta.root:TrgOR4_AIso2_pt_bins_inc_eta',    'm_trgOR4_aiso2_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR4_AIso2_pt_bins_inc_eta.root:TrgOR4_AIso2_pt_bins_inc_eta',    'm_trgOR4_aiso2_mc'),
    (loc+'/ZmmTP_Data_Fits_TrgOR5_Iso_pt_eta_bins.root:TrgOR5_Iso_pt_eta_bins',                'm_trgOR5_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR5_Iso_pt_eta_bins.root:TrgOR5_Iso_pt_eta_bins',                'm_trgOR5_mc'),
    (loc+'/ZmmTP_Data_Fits_TrgOR5_AIso1_pt_bins_inc_eta.root:TrgOR5_AIso1_pt_bins_inc_eta',    'm_trgOR5_aiso1_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR5_AIso1_pt_bins_inc_eta.root:TrgOR5_AIso1_pt_bins_inc_eta',    'm_trgOR5_aiso1_mc'),
    (loc+'/ZmmTP_Data_Fits_TrgOR5_AIso2_pt_bins_inc_eta.root:TrgOR5_AIso2_pt_bins_inc_eta',    'm_trgOR5_aiso2_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR5_AIso2_pt_bins_inc_eta.root:TrgOR5_AIso2_pt_bins_inc_eta',    'm_trgOR5_aiso2_mc')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])


wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_iso_binned_data', ['m_iso_data', 'm_aiso1_data', 'm_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_iso_binned_mc', ['m_iso_mc', 'm_aiso1_mc', 'm_aiso2_mc'])
'''
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trgOR_binned_data', ['m_trgOR_data', 'm_trgOR_aiso1_data', 'm_trgOR_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trgOR_binned_mc', ['m_trgOR_mc', 'm_trgOR_aiso1_mc', 'm_trgOR_aiso2_mc'])
'''
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trgOR4_binned_data', ['m_trgOR4_data', 'm_trgOR4_aiso1_data', 'm_trgOR4_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trgOR4_binned_mc', ['m_trgOR4_mc', 'm_trgOR4_aiso1_mc', 'm_trgOR4_aiso2_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trgOR5_binned_data', ['m_trgOR5_data', 'm_trgOR5_aiso1_data', 'm_trgOR5_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trgOR5_binned_mc', ['m_trgOR5_mc', 'm_trgOR5_aiso1_mc', 'm_trgOR5_aiso2_mc'])


for t in ['id', 'id_finebins', 'idiso_singlefit', 'iso', 'aiso1', 'aiso2', 'iso_binned', 'iso_finebins', 'iso_finebins_binned', 'trg', 'trg_binned', 'trg24', 'trg24_binned', 'trg24OR', 'trg24OR_binned', 'trgOR4', 'trgOR4_aiso1', 'trgOR4_aiso2', 'trgOR4_binned', 'trgOR5', 'trgOR5_aiso1', 'trgOR5_aiso2', 'trgOR5_binned']:
    w.factory('expr::m_%s_ratio("@0/@1", m_%s_data, m_%s_mc)' % (t, t, t))

for t in ['data', 'mc', 'ratio']:
    w.factory('expr::m_idiso_%s("@0*@1", m_id_%s, m_iso_%s)' % (t, t, t))
    w.factory('expr::m_idiso_finebins_%s("@0*@1", m_id_finebins_%s, m_iso_finebins_%s)' % (t, t, t))

loc = 'inputs/KIT/v16_3'

histsToWrap = [
    (loc+'/ZeeTP_Data_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',                          'e_id_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',                    'e_id_mc'),
    (loc+'/ZeeTP_Data_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',                        'e_iso_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',                  'e_iso_mc'),
    (loc+'/ZeeTP_Data_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',                    'e_aiso1_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',              'e_aiso1_mc'),
    (loc+'/ZeeTP_Data_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',                    'e_aiso2_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',              'e_aiso2_mc'),
    (loc+'/ZeeTP_Data_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',                'e_trg_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',                'e_trg_mc'),
    (loc+'/ZeeTP_Data_Fits_Trg_AIso1_pt_bins_inc_eta.root:Trg_AIso1_pt_bins_inc_eta',    'e_trg_aiso1_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_Trg_AIso1_pt_bins_inc_eta.root:Trg_AIso1_pt_bins_inc_eta',    'e_trg_aiso1_mc'),
    (loc+'/ZeeTP_Data_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',    'e_trg_aiso2_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',    'e_trg_aiso2_mc'),
    (loc+'/ZeeTP_Data_Fits_TrgOR_Iso_pt_eta_bins.root:TrgOR_Iso_pt_eta_bins',                'e_trgOR_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_TrgOR_Iso_pt_eta_bins.root:TrgOR_Iso_pt_eta_bins',                'e_trgOR_mc'),
    (loc+'/ZeeTP_Data_Fits_TrgOR_AIso1_pt_bins_inc_eta.root:TrgOR_AIso1_pt_bins_inc_eta',    'e_trgOR_aiso1_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_TrgOR_AIso1_pt_bins_inc_eta.root:TrgOR_AIso1_pt_bins_inc_eta',    'e_trgOR_aiso1_mc'),
    (loc+'/ZeeTP_Data_Fits_TrgOR_AIso2_pt_bins_inc_eta.root:TrgOR_AIso2_pt_bins_inc_eta',    'e_trgOR_aiso2_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_TrgOR_AIso2_pt_bins_inc_eta.root:TrgOR_AIso2_pt_bins_inc_eta',    'e_trgOR_aiso2_mc'),
    #(loc+'/ZeeTP_Data_Fits_Trg27_Iso_pt_eta_bins.root:Trg27_Iso_pt_eta_bins',                'e_trg27_data'),
    #(loc+'/ZeeTP_DYJetsToLL_Fits_Trg27_Iso_pt_eta_bins.root:Trg27_Iso_pt_eta_bins',                'e_trg27_mc'),
    #(loc+'/ZeeTP_Data_Fits_Trg27_AIso1_pt_bins_inc_eta.root:Trg27_AIso1_pt_bins_inc_eta',    'e_trg27_aiso1_data'),
    #(loc+'/ZeeTP_DYJetsToLL_Fits_Trg27_AIso1_pt_bins_inc_eta.root:Trg27_AIso1_pt_bins_inc_eta',    'e_trg27_aiso1_mc'),
    #(loc+'/ZeeTP_Data_Fits_Trg27_AIso2_pt_bins_inc_eta.root:Trg27_AIso2_pt_bins_inc_eta',    'e_trg27_aiso2_data'),
    #(loc+'/ZeeTP_DYJetsToLL_Fits_Trg27_AIso2_pt_bins_inc_eta.root:Trg27_AIso2_pt_bins_inc_eta',    'e_trg27_aiso2_mc'),
    #(loc+'/ZeeTP_Data_Fits_Trg27OR_Iso_pt_eta_bins.root:Trg27OR_Iso_pt_eta_bins',                'e_trg27OR_data'),
    #(loc+'/ZeeTP_DYJetsToLL_Fits_Trg27OR_Iso_pt_eta_bins.root:Trg27OR_Iso_pt_eta_bins',                'e_trg27OR_mc'),
    #(loc+'/ZeeTP_Data_Fits_Trg27OR_AIso1_pt_bins_inc_eta.root:Trg27OR_AIso1_pt_bins_inc_eta',    'e_trg27OR_aiso1_data'),
    #(loc+'/ZeeTP_DYJetsToLL_Fits_Trg27OR_AIso1_pt_bins_inc_eta.root:Trg27OR_AIso1_pt_bins_inc_eta',    'e_trg27OR_aiso1_mc'),
    #(loc+'/ZeeTP_Data_Fits_Trg27OR_AIso2_pt_bins_inc_eta.root:Trg27OR_AIso2_pt_bins_inc_eta',    'e_trg27OR_aiso2_data'),
    #(loc+'/ZeeTP_DYJetsToLL_Fits_Trg27OR_AIso2_pt_bins_inc_eta.root:Trg27OR_AIso2_pt_bins_inc_eta',    'e_trg27OR_aiso2_mc')
    (loc+'/ZeeTP_Data_Fits_DESYtag_ID_pt_eta_bins.root:DESYtag_ID_pt_eta_bins',                          'e_DESYtag_id_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtag_ID_pt_eta_bins.root:DESYtag_ID_pt_eta_bins',                    'e_DESYtag_id_mc'),
    (loc+'/ZeeTP_Data_Fits_DESYtag_Iso_pt_eta_bins.root:DESYtag_Iso_pt_eta_bins',                        'e_DESYtag_iso_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtag_Iso_pt_eta_bins.root:DESYtag_Iso_pt_eta_bins',                  'e_DESYtag_iso_mc'),
    (loc+'/ZeeTP_Data_Fits_DESYtag_Trg_Iso_pt_eta_bins.root:DESYtag_Trg_Iso_pt_eta_bins',                'e_DESYtag_trg_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtag_Trg_Iso_pt_eta_bins.root:DESYtag_Trg_Iso_pt_eta_bins',                'e_DESYtag_trg_mc'),
    (loc+'/ZeeTP_Data_Fits_DESYtagNonSC_ID_pt_eta_bins.root:DESYtagNonSC_ID_pt_eta_bins',                          'e_DESYtagNonSC_id_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtagNonSC_ID_pt_eta_bins.root:DESYtagNonSC_ID_pt_eta_bins',                    'e_DESYtagNonSC_id_mc'),
    (loc+'/ZeeTP_Data_Fits_DESYtagNonSC_IDIso_pt_eta_bins.root:DESYtagNonSC_IDIso_pt_eta_bins',                          'e_DESYtagNonSC_idiso_singlefit_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtagNonSC_IDIso_pt_eta_bins.root:DESYtagNonSC_IDIso_pt_eta_bins',                    'e_DESYtagNonSC_idiso_singlefit_mc'),
    (loc+'/ZeeTP_Data_Fits_DESYtagNonSC_Iso_pt_eta_bins.root:DESYtagNonSC_Iso_pt_eta_bins',                        'e_DESYtagNonSC_iso_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtagNonSC_Iso_pt_eta_bins.root:DESYtagNonSC_Iso_pt_eta_bins',                  'e_DESYtagNonSC_iso_mc'),
    (loc+'/ZeeTP_Data_Fits_DESYtagNonSC_Trg_Iso_pt_eta_bins.root:DESYtagNonSC_Trg_Iso_pt_eta_bins',                'e_DESYtagNonSC_trg_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtagNonSC_Trg_Iso_pt_eta_bins.root:DESYtagNonSC_Trg_Iso_pt_eta_bins',                'e_DESYtagNonSC_trg_mc'),
    
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])


wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_iso_binned_data', ['e_iso_data', 'e_aiso1_data', 'e_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_iso_binned_mc', ['e_iso_mc', 'e_aiso1_mc', 'e_aiso2_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg_binned_data', ['e_trg_data', 'e_trg_aiso1_data', 'e_trg_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg_binned_mc', ['e_trg_mc', 'e_trg_aiso1_mc', 'e_trg_aiso2_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trgOR_binned_data', ['e_trgOR_data', 'e_trgOR_aiso1_data', 'e_trgOR_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trgOR_binned_mc', ['e_trgOR_mc', 'e_trgOR_aiso1_mc', 'e_trgOR_aiso2_mc'])
'''
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg27_binned_data', ['e_trg27_data', 'e_trg27_aiso1_data', 'e_trg27_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg27_binned_mc', ['e_trg27_mc', 'e_trg27_aiso1_mc', 'e_trg27_aiso2_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg27OR_binned_data', ['e_trg27OR_data', 'e_trg27OR_aiso1_data', 'e_trg27OR_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg27OR_binned_mc', ['e_trg27OR_mc', 'e_trg27OR_aiso1_mc', 'e_trg27OR_aiso2_mc'])
'''


for t in ['id', 'iso', 'aiso1', 'aiso2', 'iso_binned', 'trg', 'trg_aiso1', 'trg_aiso2', 'trg_binned', 'trgOR', 'trgOR_aiso1', 'trgOR_aiso2', 'trgOR_binned', 'DESYtag_id', 'DESYtag_iso', 'DESYtag_iso_binned', 'DESYtag_trg', 'DESYtag_trg_binned', 'DESYtag_trgOR', 'DESYtag_trgOR_binned', 'DESYtagNonSC_id', 'DESYtagNonSC_idiso_singlefit', 'DESYtagNonSC_iso', 'DESYtagNonSC_iso_binned', 'DESYtagNonSC_trg', 'DESYtagNonSC_trg_binned', 'DESYtagNonSC_trgOR', 'DESYtagNonSC_trgOR_binned']:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))

for t in ['data', 'mc', 'ratio']:
    w.factory('expr::e_idiso_%s("@0*@1", e_id_%s, e_iso_%s)' % (t, t, t))
    w.factory('expr::e_DESYtag_idiso_%s("@0*@1", e_DESYtag_id_%s, e_DESYtag_iso_%s)' % (t, t, t))
    w.factory('expr::e_DESYtagNonSC_idiso_%s("@0*@1", e_DESYtagNonSC_id_%s, e_DESYtagNonSC_iso_%s)' % (t, t, t))

### Muon tracking efficiency scale factor from the muon POG
loc = 'inputs/MuonPOG'

muon_trk_eff_hist = wsptools.TGraphAsymmErrorsToTH1D(GetFromTFile(loc+'/Tracking_EfficienciesAndSF_BCDEFGH.root:ratio_eff_eta3_dr030e030_corr'))
wsptools.SafeWrapHist(w, ['m_eta'], muon_trk_eff_hist, name='m_trk_ratio')

### Electron tracking efficiency scale factor from the egamma POG
loc = 'inputs/EGammaPOG'

electron_trk_eff_hist = GetFromTFile(loc+'/egammaEffi.txt_EGM2D.root:EGamma_SF2D')
wsptools.SafeWrapHist(w, ['e_eta','e_pt'], electron_trk_eff_hist, name='e_trk_ratio')


### DESY electron/muon tag and probe results
loc = 'inputs/LeptonEfficiencies'
loc2 = 'inputs/DESYsyncSF'

desyHistsToWrap = [
    (loc+'/Muon/Run2016BtoH/Muon_IdIso_IsoLt0p15_2016BtoH_eff.root',            'MC',   'm_idiso0p15_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_IdIso_IsoLt0p15_2016BtoH_eff.root',            'Data', 'm_idiso0p15_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_IdIso_IsoLt0p2_2016BtoH_eff.root',            'MC',   'm_idiso0p20_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_IdIso_IsoLt0p2_2016BtoH_eff.root',            'Data', 'm_idiso0p20_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_IdIso_antiisolated_Iso0p15to0p3_eff_rb.root',            'MC',   'm_idiso_aiso0p15to0p3_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_IdIso_antiisolated_Iso0p15to0p3_eff_rb.root',            'Data',   'm_idiso_aiso0p15to0p3_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p05to0p15_IdIso_eff.root',            'MC',   'm_idiso_aiso0p05to0p15_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p05to0p15_IdIso_eff.root',            'Data',   'm_idiso_aiso0p05to0p15_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p15to0p25_IdIso_eff.root',            'MC',   'm_idiso_aiso0p15to0p25_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p15to0p25_IdIso_eff.root',            'Data',   'm_idiso_aiso0p15to0p25_desy_data'),
    
    (loc+'/Muon/Run2016BtoH/Muon_IsoMu24_2016BtoH_eff.root',              'MC', 'm_trgIsoMu24_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_IsoMu24_2016BtoH_eff.root',              'Data', 'm_trgIsoMu24_desy_data'),
    
    (loc+'/Muon/Run2016BtoH/Muon_IsoMu24_OR_TkIsoMu24_2016BtoH_eff.root', 'MC', 'm_trgIsoMu24orTkIsoMu24_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_IsoMu24_OR_TkIsoMu24_2016BtoH_eff.root', 'Data', 'm_trgIsoMu24orTkIsoMu24_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p05to0p15_IsoMu24ORTkIsoMu24_eff_rb.root', 'MC', 'm_trgIsoMu24orTkIsoMu24_aiso0p05to0p15_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p05to0p15_IsoMu24ORTkIsoMu24_eff_rb.root', 'Data', 'm_trgIsoMu24orTkIsoMu24_aiso0p05to0p15_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p15to0p25_IsoMu24ORTkIsoMu24_eff_rb.root', 'MC', 'm_trgIsoMu24orTkIsoMu24_aiso0p15to0p25_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p15to0p25_IsoMu24ORTkIsoMu24_eff_rb.root', 'Data', 'm_trgIsoMu24orTkIsoMu24_aiso0p15to0p25_desy_data'),
    
    (loc+'/Muon/Run2016BtoH/Muon_Mu8leg_2016BtoH_eff.root',               'MC', 'm_trgMu8leg_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu8leg_2016BtoH_eff.root',               'Data', 'm_trgMu8leg_desy_data'),
    
    (loc+'/Muon/Run2016BtoH/Muon_Mu23leg_2016BtoH_eff.root',              'MC', 'm_trgMu23leg_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu23leg_2016BtoH_eff.root',              'Data', 'm_trgMu23leg_desy_data'),
    
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_2016BtoH_eff.root',              'MC', 'm_trgMu19leg_eta2p1_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_2016BtoH_eff.root',              'Data', 'm_trgMu19leg_eta2p1_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_eta2p1_antiisolated_Iso0p05to0p15_eff_rb.root',              'MC', 'm_trgMu19leg_eta2p1_aiso0p05to0p15_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_eta2p1_antiisolated_Iso0p05to0p15_eff_rb.root',              'Data', 'm_trgMu19leg_eta2p1_aiso0p05to0p15_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_eta2p1_antiisolated_Iso0p15to0p25_eff_rb.root',              'MC', 'm_trgMu19leg_eta2p1_aiso0p15to0p25_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_eta2p1_antiisolated_Iso0p15to0p25_eff_rb.root',              'Data', 'm_trgMu19leg_eta2p1_aiso0p15to0p25_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_eta2p1_antiisolated_Iso0p15to0p3_eff_rb.root',              'MC', 'm_trgMu19leg_eta2p1_aiso0p15to0p3_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_eta2p1_antiisolated_Iso0p15to0p3_eff_rb.root',              'Data', 'm_trgMu19leg_eta2p1_aiso0p15to0p3_desy_data'),
    
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_eff.root',              'MC', 'm_trgMu22OR_eta2p1_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_eff.root',              'Data', 'm_trgMu22OR_eta2p1_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_antiisolated_Iso0p05to0p15_eff_rb.root',              'MC', 'm_trgMu22OR_eta2p1_aiso0p05to0p15_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_antiisolated_Iso0p05to0p15_eff_rb.root',              'Data', 'm_trgMu22OR_eta2p1_aiso0p05to0p15_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_antiisolated_Iso0p15to0p25_eff_rb.root',              'MC', 'm_trgMu22OR_eta2p1_aiso0p15to0p25_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_antiisolated_Iso0p15to0p25_eff_rb.root',              'Data', 'm_trgMu22OR_eta2p1_aiso0p15to0p25_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_antiisolated_Iso0p15to0p3_eff_rb.root',              'MC', 'm_trgMu22OR_eta2p1_aiso0p15to0p3_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_antiisolated_Iso0p15to0p3_eff_rb.root',              'Data', 'm_trgMu22OR_eta2p1_aiso0p15to0p3_desy_data'),
]

for task in desyHistsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          wsptools.ProcessDESYLeptonSFs(task[0], task[1], task[2]), name=task[2])
for t in ['idiso0p15_desy', 'idiso0p20_desy', 'idiso_aiso0p15to0p3_desy', 'idiso_aiso0p05to0p15_desy', 'idiso_aiso0p15to0p25_desy', 'trgIsoMu24_desy', 'trgIsoMu24orTkIsoMu24_desy',    'trgIsoMu24orTkIsoMu24_aiso0p05to0p15_desy', 'trgIsoMu24orTkIsoMu24_aiso0p15to0p25_desy', 'trgMu8leg_desy', 'trgMu23leg_desy', 'trgMu19leg_eta2p1_desy', 'trgMu19leg_eta2p1_aiso0p05to0p15_desy', 'trgMu19leg_eta2p1_aiso0p15to0p25_desy', 'trgMu19leg_eta2p1_aiso0p15to0p3_desy', 'trgMu22OR_eta2p1_desy', 'trgMu22OR_eta2p1_aiso0p05to0p15_desy', 'trgMu22OR_eta2p1_aiso0p15to0p25_desy', 'trgMu22OR_eta2p1_aiso0p15to0p3_desy']:
    w.factory('expr::m_%s_ratio("@0/@1", m_%s_data, m_%s_mc)' % (t, t, t))

desyHistsToWrap = [
    (loc2+'/Electron_IdIso_IsoLt0p1_2016BtoH_eff.root',          'MC',   'e_idiso0p10_KITbins_desy_mc'),
    (loc2+'/Electron_IdIso_IsoLt0p1_2016BtoH_eff.root',          'Data', 'e_idiso0p10_KITbins_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_IdIso_IsoLt0p1_eff.root',          'MC',   'e_idiso0p1_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_IdIso_IsoLt0p1_eff.root',          'Data', 'e_idiso0p1_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_IdIso_IsoLt0p15_eff.root',          'MC',   'e_idiso0p15_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_IdIso_IsoLt0p15_eff.root',          'Data', 'e_idiso0p15_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_antiisolated_0p05to0p15_IdIso_eff.root',          'MC',   'e_idiso_aiso0p05to0p15_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_antiisolated_0p05to0p15_IdIso_eff.root',          'Data', 'e_idiso_aiso0p05to0p15_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_antiisolated_0p10to0p20_IdIso_eff.root',          'MC',   'e_idiso_aiso0p1to0p2_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_antiisolated_0p10to0p20_IdIso_eff.root',          'Data', 'e_idiso_aiso0p1to0p2_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_IdIso_antiisolated_Iso0p1to0p3_eff.root',          'MC',   'e_idiso_aiso0p1to0p3_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_IdIso_antiisolated_Iso0p1to0p3_eff.root',          'Data', 'e_idiso_aiso0p1to0p3_desy_data'),
    
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_eff.root',          'MC',   'e_trgEle24_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_eff.root',          'Data', 'e_trgEle24_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_antiisolated_Iso0p05to0p15_eff_rb.root',          'MC',   'e_trgEle24_aiso0p05to0p15_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_antiisolated_Iso0p05to0p15_eff_rb.root',          'Data', 'e_trgEle24_aiso0p05to0p15_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_antiisolated_Iso0p1to0p2_eff_rb.root',          'MC',   'e_trgEle24_aiso0p1to0p2_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_antiisolated_Iso0p1to0p2_eff_rb.root',          'Data', 'e_trgEle24_aiso0p1to0p2_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_antiisolated_Iso0p1to0p3_eff_rb.root',          'MC',   'e_trgEle24_aiso0p1to0p3_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_antiisolated_Iso0p1to0p3_eff_rb.root',          'Data', 'e_trgEle24_aiso0p1to0p3_desy_data'),
    
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_eff.root',          'MC',   'e_trgEle25eta2p1WPTight_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_eff.root',          'Data', 'e_trgEle25eta2p1WPTight_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_antiisolated_Iso0p05to0p15_eff_rb.root',          'MC',   'e_trgEle25eta2p1WPTight_aiso0p05to0p15_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_antiisolated_Iso0p05to0p15_eff_rb.root',          'Data', 'e_trgEle25eta2p1WPTight_aiso0p05to0p15_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_antiisolated_Iso0p1to0p2_eff_rb.root',          'MC',   'e_trgEle25eta2p1WPTight_aiso0p1to0p2_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_antiisolated_Iso0p1to0p2_eff_rb.root',          'Data', 'e_trgEle25eta2p1WPTight_aiso0p1to0p2_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_antiisolated_Iso0p1to0p3_eff_rb.root',          'MC',   'e_trgEle25eta2p1WPTight_aiso0p1to0p3_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_antiisolated_Iso0p1to0p3_eff_rb.root',          'Data', 'e_trgEle25eta2p1WPTight_aiso0p1to0p3_desy_data'),
    
    (loc2+'/Electron_Ele25_eta2p1_WPTight_2016BtoH_eff.root', 'MC', 'e_trgEle25eta2p1WPTight_KITbins_desy_mc'),
    (loc2+'/Electron_Ele25_eta2p1_WPTight_2016BtoH_eff.root', 'Data', 'e_trgEle25eta2p1WPTight_KITbins_desy_data'),
    
    (loc+'/Electron/Run2016BtoH/Electron_Ele12leg_eff.root',           'MC', 'e_trgEle12leg_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele12leg_eff.root',           'Data', 'e_trgEle12leg_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele23leg_eff.root',           'MC', 'e_trgEle23leg_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele23leg_eff.root',           'Data', 'e_trgEle23leg_desy_data')
]

for task in desyHistsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          wsptools.ProcessDESYLeptonSFs(task[0], task[1], task[2]), name=task[2])

for t in ['idiso0p10_KITbins_desy', 'idiso0p1_desy', 'idiso0p15_desy', 'idiso_aiso0p05to0p15_desy', 'idiso_aiso0p1to0p2_desy', 'idiso_aiso0p1to0p3_desy', 'trgEle24_desy', 'trgEle24_aiso0p05to0p15_desy', 'trgEle24_aiso0p1to0p2_desy', 'trgEle24_aiso0p1to0p3_desy', 'trgEle25eta2p1WPTight_desy', 'trgEle25eta2p1WPTight_aiso0p05to0p15_desy', 'trgEle25eta2p1WPTight_aiso0p1to0p2_desy', 'trgEle25eta2p1WPTight_aiso0p1to0p3_desy', 'trgEle25eta2p1WPTight_KITbins_desy', 'trgEle12leg_desy', 'trgEle23leg_desy']:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))

### IC electron/muon embedded scale factors

loc = 'inputs/ICSF/'

histsToWrap = [
    (loc+'TauTau/MC_trig_correction.root:hist', 'doubletau_corr')
]
for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['dR'],
                          GetFromTFile(task[0]), name=task[1])

histsToWrap = [
    (loc+'MuMu8/muon_SFs.root:trg_data', 'm_sel_trg8_1_data'),
    (loc+'MuMu17/muon_SFs.root:trg_data', 'm_sel_trg17_1_data')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['gt1_pt', 'expr::gt1_abs_eta("TMath::Abs(@0)",gt1_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

histsToWrap = [
    (loc+'MuMu8/muon_SFs.root:trg_data', 'm_sel_trg8_2_data'),
    (loc+'MuMu17/muon_SFs.root:trg_data', 'm_sel_trg17_2_data')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['gt2_pt', 'expr::gt2_abs_eta("TMath::Abs(@0)",gt2_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])
    
    w.factory('expr::m_sel_trg_data("0.9461*(@0*@3+@1*@2-@1*@3)", m_sel_trg8_1_data, m_sel_trg17_1_data, m_sel_trg8_2_data, m_sel_trg17_2_data)')
    w.factory('expr::m_sel_trg_ratio("min(1./@0,2)", m_sel_trg_data)')


histsToWrap = [
    (loc+'SingleLepton/muon_SFs.root:trg_data', 'm_trg22_ic_data'),
    (loc+'SingleLepton/muon_SFs.root:trg_mc', 'm_trg22_ic_mc'),
    (loc+'SingleLepton/muon_SFs.root:trg_embed', 'm_trg22_ic_embed'),
    (loc+'SingleLepton/aiso1/muon_SFs.root:trg_data', 'm_trg22_aiso1_ic_data'),
    (loc+'SingleLepton/aiso1/muon_SFs.root:trg_mc', 'm_trg22_aiso1_ic_mc'),
    (loc+'SingleLepton/aiso1/muon_SFs.root:trg_embed', 'm_trg22_aiso1_ic_embed'),
    (loc+'SingleLepton/aiso2/muon_SFs.root:trg_data', 'm_trg22_aiso2_ic_data'),
    (loc+'SingleLepton/aiso2/muon_SFs.root:trg_mc', 'm_trg22_aiso2_ic_mc'),
    (loc+'SingleLepton/aiso2/muon_SFs.root:trg_embed', 'm_trg22_aiso2_ic_embed'),
    (loc+'MuTau/muon_SFs.root:trg_data', 'm_trg19_ic_data'),
    (loc+'MuTau/muon_SFs.root:trg_mc', 'm_trg19_ic_mc'),
    (loc+'MuTau/muon_SFs.root:trg_embed', 'm_trg19_ic_embed'),
    (loc+'MuTau/aiso1/muon_SFs.root:trg_data', 'm_trg19_aiso1_ic_data'),
    (loc+'MuTau/aiso1/muon_SFs.root:trg_mc', 'm_trg19_aiso1_ic_mc'),
    (loc+'MuTau/aiso1/muon_SFs.root:trg_embed', 'm_trg19_aiso1_ic_embed'),
    (loc+'MuTau/aiso2/muon_SFs.root:trg_data', 'm_trg19_aiso2_ic_data'),
    (loc+'MuTau/aiso2/muon_SFs.root:trg_mc', 'm_trg19_aiso2_ic_mc'),
    (loc+'MuTau/aiso2/muon_SFs.root:trg_embed', 'm_trg19_aiso2_ic_embed'),
    (loc+'El23Mu8/muon_SFs.root:trg_data', 'm_trg8_ic_data'),
    (loc+'El23Mu8/muon_SFs.root:trg_mc', 'm_trg8_ic_mc'),
    (loc+'El23Mu8/muon_SFs.root:trg_embed', 'm_trg8_ic_embed'),
    (loc+'El23Mu8/aiso1/muon_SFs.root:trg_data', 'm_trg8_aiso1_ic_data'),
    (loc+'El23Mu8/aiso1/muon_SFs.root:trg_mc', 'm_trg8_aiso1_ic_mc'),
    (loc+'El23Mu8/aiso1/muon_SFs.root:trg_embed', 'm_trg8_aiso1_ic_embed'),
    (loc+'El23Mu8/aiso2/muon_SFs.root:trg_data', 'm_trg8_aiso2_ic_data'),
    (loc+'El23Mu8/aiso2/muon_SFs.root:trg_mc', 'm_trg8_aiso2_ic_mc'),
    (loc+'El23Mu8/aiso2/muon_SFs.root:trg_embed', 'm_trg8_aiso2_ic_embed'),
    (loc+'El12Mu23/muon_SFs.root:trg_data', 'm_trg23_ic_data'),
    (loc+'El12Mu23/muon_SFs.root:trg_mc', 'm_trg23_ic_mc'),
    (loc+'El12Mu23/muon_SFs.root:trg_embed', 'm_trg23_ic_embed'),
    (loc+'El12Mu23/aiso1/muon_SFs.root:trg_data', 'm_trg23_aiso1_ic_data'),
    (loc+'El12Mu23/aiso1/muon_SFs.root:trg_mc', 'm_trg23_aiso1_ic_mc'),
    (loc+'El12Mu23/aiso1/muon_SFs.root:trg_embed', 'm_trg23_aiso1_ic_embed'),
    (loc+'El12Mu23/aiso2/muon_SFs.root:trg_data', 'm_trg23_aiso2_ic_data'),
    (loc+'El12Mu23/aiso2/muon_SFs.root:trg_mc', 'm_trg23_aiso2_ic_mc'),
    (loc+'El12Mu23/aiso2/muon_SFs.root:trg_embed', 'm_trg23_aiso2_ic_embed')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg22_binned_ic_data', ['m_trg22_ic_data', 'm_trg22_aiso1_ic_data', 'm_trg22_aiso2_ic_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg22_binned_ic_mc', ['m_trg22_ic_mc', 'm_trg22_aiso1_ic_mc', 'm_trg22_aiso2_ic_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg22_binned_ic_embed', ['m_trg22_ic_embed', 'm_trg22_aiso1_ic_embed', 'm_trg22_aiso2_ic_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg19_binned_ic_data', ['m_trg19_ic_data', 'm_trg19_aiso1_ic_data', 'm_trg19_aiso2_ic_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg19_binned_ic_mc', ['m_trg19_ic_mc', 'm_trg19_aiso1_ic_mc', 'm_trg19_aiso2_ic_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg19_binned_ic_embed', ['m_trg19_ic_embed', 'm_trg19_aiso1_ic_embed', 'm_trg19_aiso2_ic_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.20, 0.3, 0.50],
                                   'm_trg8_binned_ic_data', ['m_trg8_ic_data', 'm_trg8_aiso1_ic_data', 'm_trg8_aiso2_ic_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.20, 0.3, 0.50],
                                   'm_trg8_binned_ic_mc', ['m_trg8_ic_mc', 'm_trg8_aiso1_ic_mc', 'm_trg8_aiso2_ic_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.20, 0.3, 0.50],
                                   'm_trg8_binned_ic_embed', ['m_trg8_ic_embed', 'm_trg8_aiso1_ic_embed', 'm_trg8_aiso2_ic_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.20, 0.3, 0.50],
                                   'm_trg23_binned_ic_data', ['m_trg23_ic_data', 'm_trg23_aiso1_ic_data', 'm_trg23_aiso2_ic_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.20, 0.3, 0.50],
                                   'm_trg23_binned_ic_mc', ['m_trg23_ic_mc', 'm_trg23_aiso1_ic_mc', 'm_trg23_aiso2_ic_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.20, 0.3, 0.50],
                                   'm_trg23_binned_ic_embed', ['m_trg23_ic_embed', 'm_trg23_aiso1_ic_embed', 'm_trg23_aiso2_ic_embed'])


for t in ['trg22_ic', 'trg22_aiso1_ic', 'trg22_aiso2_ic', 'trg22_binned_ic', 'trg19_ic', 'trg19_aiso1_ic', 'trg19_aiso2_ic', 'trg19_binned_ic', 'trg8_ic', 'trg8_aiso1_ic', 'trg8_aiso2_ic', 'trg8_binned_ic', 'trg23_ic', 'trg23_aiso1_ic', 'trg23_aiso2_ic', 'trg23_binned_ic']:
    w.factory('expr::m_%s_ratio("@0/@1", m_%s_data, m_%s_mc)' % (t, t, t))
    w.factory('expr::m_%s_embed_ratio("@0/@1", m_%s_data, m_%s_embed)' % (t, t, t))
    
    

histsToWrap = [
    (loc+'SingleLepton/electron_SFs.root:trg_data', 'e_trg25_ic_data'),
    (loc+'SingleLepton/electron_SFs.root:trg_mc', 'e_trg25_ic_mc'),
    (loc+'SingleLepton/electron_SFs.root:trg_embed', 'e_trg25_ic_embed'),
    (loc+'SingleLepton/aiso1/electron_SFs.root:trg_data', 'e_trg25_aiso1_ic_data'),
    (loc+'SingleLepton/aiso1/electron_SFs.root:trg_mc', 'e_trg25_aiso1_ic_mc'),
    (loc+'SingleLepton/aiso1/electron_SFs.root:trg_embed', 'e_trg25_aiso1_ic_embed'),
    (loc+'SingleLepton/aiso2/electron_SFs.root:trg_data', 'e_trg25_aiso2_ic_data'),
    (loc+'SingleLepton/aiso2/electron_SFs.root:trg_mc', 'e_trg25_aiso2_ic_mc'),
    (loc+'SingleLepton/aiso2/electron_SFs.root:trg_embed', 'e_trg25_aiso2_ic_embed'),
    (loc+'El12Mu23/electron_SFs.root:trg_data', 'e_trg12_ic_data'),
    (loc+'El12Mu23/electron_SFs.root:trg_mc', 'e_trg12_ic_mc'),
    (loc+'El12Mu23/electron_SFs.root:trg_embed', 'e_trg12_ic_embed'),
    (loc+'El12Mu23/aiso1/electron_SFs.root:trg_data', 'e_trg12_aiso1_ic_data'),
    (loc+'El12Mu23/aiso1/electron_SFs.root:trg_mc', 'e_trg12_aiso1_ic_mc'),
    (loc+'El12Mu23/aiso1/electron_SFs.root:trg_embed', 'e_trg12_aiso1_ic_embed'),
    (loc+'El12Mu23/aiso2/electron_SFs.root:trg_data', 'e_trg12_aiso2_ic_data'),
    (loc+'El12Mu23/aiso2/electron_SFs.root:trg_mc', 'e_trg12_aiso2_ic_mc'),
    (loc+'El12Mu23/aiso2/electron_SFs.root:trg_embed', 'e_trg12_aiso2_ic_embed'),
    (loc+'El23Mu8/electron_SFs.root:trg_data', 'e_trg23_ic_data'),
    (loc+'El23Mu8/electron_SFs.root:trg_mc', 'e_trg23_ic_mc'),
    (loc+'El23Mu8/electron_SFs.root:trg_embed', 'e_trg23_ic_embed'),
    (loc+'El23Mu8/aiso1/electron_SFs.root:trg_data', 'e_trg23_aiso1_ic_data'),
    (loc+'El23Mu8/aiso1/electron_SFs.root:trg_mc', 'e_trg23_aiso1_ic_mc'),
    (loc+'El23Mu8/aiso1/electron_SFs.root:trg_embed', 'e_trg23_aiso1_ic_embed'),
    (loc+'El23Mu8/aiso2/electron_SFs.root:trg_data', 'e_trg23_aiso2_ic_data'),
    (loc+'El23Mu8/aiso2/electron_SFs.root:trg_mc', 'e_trg23_aiso2_ic_mc'),
    (loc+'El23Mu8/aiso2/electron_SFs.root:trg_embed', 'e_trg23_aiso2_ic_embed')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.1, 0.25, 0.50],
                                   'e_trg25_binned_ic_data', ['e_trg25_ic_data', 'e_trg25_aiso1_ic_data', 'e_trg25_aiso2_ic_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.1, 0.25, 0.50],
                                   'e_trg25_binned_ic_mc', ['e_trg25_ic_mc', 'e_trg25_aiso1_ic_mc', 'e_trg25_aiso2_ic_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.1, 0.25, 0.50],
                                   'e_trg25_binned_ic_embed', ['e_trg25_ic_embed', 'e_trg25_aiso1_ic_embed', 'e_trg25_aiso2_ic_embed'])


wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.3, 0.50],
                                   'e_trg12_binned_ic_data', ['e_trg12_ic_data', 'e_trg12_aiso1_ic_data', 'e_trg12_aiso2_ic_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.3, 0.50],
                                   'e_trg12_binned_ic_mc', ['e_trg12_ic_mc', 'e_trg12_aiso1_ic_mc', 'e_trg12_aiso2_ic_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.3, 0.50],
                                   'e_trg12_binned_ic_embed', ['e_trg12_ic_embed', 'e_trg12_aiso1_ic_embed', 'e_trg12_aiso2_ic_embed'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.3, 0.50],
                                   'e_trg23_binned_ic_data', ['e_trg23_ic_data', 'e_trg23_aiso1_ic_data', 'e_trg23_aiso2_ic_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.3, 0.50],
                                   'e_trg23_binned_ic_mc', ['e_trg23_ic_mc', 'e_trg23_aiso1_ic_mc', 'e_trg23_aiso2_ic_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.3, 0.50],
                                   'e_trg23_binned_ic_embed', ['e_trg23_ic_embed', 'e_trg23_aiso1_ic_embed', 'e_trg23_aiso2_ic_embed'])


for t in ['trg25_ic', 'trg25_aiso1_ic', 'trg25_aiso2_ic', 'trg25_binned_ic', 'trg12_ic', 'trg12_aiso1_ic', 'trg12_aiso2_ic', 'trg12_binned_ic', 'trg23_ic', 'trg23_aiso1_ic', 'trg23_aiso2_ic', 'trg23_binned_ic']:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))
    w.factory('expr::e_%s_embed_ratio("@0/@1", e_%s_data, e_%s_embed)' % (t, t, t))

## IC em qcd os/ss weights
wsptools.SafeWrapHist(w, ['expr::m_pt_max100("min(@0,100)",m_pt[0])', 'expr::e_pt_max100("min(@0,100)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_factors_maiso.root:qcd_factors'), 'em_qcd_factors')
wsptools.SafeWrapHist(w, ['expr::m_pt_max100("min(@0,100)",m_pt[0])', 'expr::e_pt_max100("min(@0,100)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_factors_bothaiso.root:qcd_factors'), 'em_qcd_factors_bothaiso')
#wsptools.SafeWrapHist(w, ['expr::dR_max4p5("min(@0,4.5)",dR[0])','expr::njets_max1("min(@0,1)",njets[0])'],  GetFromTFile(loc+'/em_qcd/em_aiso_iso_extrap.root:extrap_uncert'), 'em_qcd_extrap_uncert')
wsptools.SafeWrapHist(w, ['expr::m_pt_max40("min(@0,40)",m_pt[0])','expr::e_pt_max40("min(@0,40)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_isoextrap.root:isoextrap_uncert'), 'em_qcd_extrap_uncert')

w.factory('expr::em_qcd_0jet("(2.162-0.05135*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_1jet("(2.789-0.2712*@0)*@1",dR,em_qcd_factors)')

w.factory('expr::em_qcd_0jet_bothaiso("(3.212-0.2186*@0)*@1",dR,em_qcd_factors_bothaiso)')
w.factory('expr::em_qcd_1jet_bothaiso("(3.425-0.3629*@0)*@1",dR,em_qcd_factors_bothaiso)')

w.factory('expr::em_qcd_0jet_shapeup("(2.162-(0.05135-0.0583)*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_0jet_shapedown("(2.162-(0.05135+0.0583)*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_1jet_shapeup("(2.789-(0.2712-0.0390)*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_1jet_shapedown("(2.789-(0.2712+0.0390)*@0)*@1",dR,em_qcd_factors)')

w.factory('expr::em_qcd_0jet_rateup("(2.162+0.192-0.05135*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_0jet_ratedown("(2.162-0.192-0.05135*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_1jet_rateup("(2.789+0.0105-0.2712*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_1jet_ratedown("(2.789-0.0105-0.2712*@0)*@1",dR,em_qcd_factors)')

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

w.factory('expr::em_qcd_0jet_bothaiso("(3.208-0.217*@0)*@1",dR,em_qcd_factors_bothaiso)')
w.factory('expr::em_qcd_1jet_bothaiso("(3.426-0.3628*@0)*@1",dR,em_qcd_factors_bothaiso)')

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

## IC jet->tau SFs

loc = 'inputs/ICSF/faketaus/'

dy_fit_data =  GetFromTFile(loc+'/taufakes_zmm.root:data_eff_fit')
dy_fit_mc =  GetFromTFile(loc+'/taufakes_zmm.root:mc_eff_fit')
params_data = dy_fit_data.GetParameters()
params_mc = dy_fit_mc.GetParameters()
w.factory('expr::t_pt_max400("min(400,@0)",t_pt[0])')
w.factory('expr::t_jetfake_dy_data("%f*exp(%f*@0)+%f+%f/(@0+%f)",t_pt_max400)' % (params_data[0],params_data[1],params_data[2],params_data[3],params_data[4]))
w.factory('expr::t_jetfake_dy_mc("%f*exp(%f*@0)+%f+%f/(@0+%f)",t_pt_max400)' % (params_mc[0],params_mc[1],params_mc[2],params_mc[3],params_mc[4]))
w.factory('expr::t_jetfake_dy_ratio("@0/@1",t_jetfake_dy_data,t_jetfake_dy_mc)')

ttbar_fit = GetFromTFile(loc+'/taufakes_em.root:ratio_pol1')
params = ttbar_fit.GetParameters()
w.factory('expr::t_pt_max80("min(80,@0)",t_pt[0])')
w.factory('expr::t_jetfake_ttbar_ratio("%f+%f*@0",t_pt_max80)' % (params[0],params[1]))

wjet_fit = GetFromTFile(loc+'/taufakes_mt.root:ratio_pol1')
params = wjet_fit.GetParameters()
w.factory('expr::t_jetfake_wjet_ratio("%f+%f*@0",t_pt_max400)' % (params[0],params[1]))


### KIT tau ID scale factors
loc = 'inputs/KIT/tau_id_sfs_2016.root:'
histsToWrap = [
    (loc + 'mva_m_dm0_pt30', 't_iso_mva_m_dm0_pt30_sf'),
    (loc + 'mva_m_dm1_pt30', 't_iso_mva_m_dm1_pt30_sf'),
    (loc + 'mva_m_dm10_pt30', 't_iso_mva_m_dm10_pt30_sf'),
    (loc + 'mva_t_dm0_pt40_eta2p1', 't_iso_mva_t_dm0_pt40_eta2p1_sf'),
    (loc + 'mva_t_dm1_pt40_eta2p1', 't_iso_mva_t_dm1_pt40_eta2p1_sf'),
    (loc + 'mva_t_dm10_pt40_eta2p1', 't_iso_mva_t_dm10_pt40_eta2p1_sf'),
]
for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['t_pt', 'expr::t_abs_eta("TMath::Abs(@0)",t_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                   't_iso_mva_m_pt30_sf', ['t_iso_mva_m_dm0_pt30_sf', 't_iso_mva_m_dm1_pt30_sf', 't_iso_mva_m_dm10_pt30_sf'])

wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                   't_iso_mva_t_pt40_eta2p1_sf', ['t_iso_mva_t_dm0_pt40_eta2p1_sf', 't_iso_mva_t_dm1_pt40_eta2p1_sf', 't_iso_mva_t_dm10_pt40_eta2p1_sf'])

### Hadronic tau trigger efficiencies for embedded samples by IC

with open('inputs/ICSF/TauTau/embed_trg_fits.json') as jsonfile:
    pars = json.load(jsonfile)
    for iso in ['Vloose','Loose','Medium','Tight']:
      for dm in ['dm0', 'dm1', 'dm10']:
        label = '%sIso_%s' % (iso,dm)
        x = pars['embed_%s' % (label)]
        w.factory('CrystalBallEfficiency::t_%s_tt_embed(t_pt[0],%g,%g,%g,%g,%g)' % (
                      label, x['m_{0}'], x['sigma'], x['alpha'], x['n'], x['norm']
                  ))
      label = '%sIso' % iso
      wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                                 't_%s_tt_embed' % label, ['t_%s_dm0_tt_embed' % label, 't_%s_dm1_tt_embed' % label, 't_%s_dm10_tt_embed' % label])

for p in ['full', 'calo']:
  with open('inputs/ICSF/TauTau/mc_trg_fits_%s.json' % p) as jsonfile:
    pars = json.load(jsonfile)
    for iso in ['Tight']:
      for dm in ['dm0', 'dm1', 'dm10']:
        label = '%sIso_%s' % (iso,dm)
        x = pars['embed_%s' % (label)]
        w.factory('CrystalBallEfficiency::t_%s_tt_%s(t_pt[0],%g,%g,%g,%g,%g)' % (
                      label, p, x['m_{0}'], x['sigma'], x['alpha'], x['n'], x['norm']
                  ))
      label = '%sIso' % iso
      wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                                 't_%s_tt_%s' % (label,p), ['t_%s_dm0_tt_%s' % (label,p), 't_%s_dm1_tt_%s' % (label,p), 't_%s_dm10_tt_%s' % (label,p)])

w.factory('expr::t_trg_tight_tt_mcclose("@0/@1", t_TightIso_tt_full, t_TightIso_tt_calo)')


interpOrder = 1
tau_mt_file = ROOT.TFile('inputs/ICSF/TauTau/embed_tau_trig_eff_mt.root')

for iso in ['Vloose', 'Loose', 'Medium', 'Tight']:
  for region in ['barrel', 'endcap']:
      label = '%s_%sIso' % (region,iso)
  
      wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
          tau_mt_file.Get('eff_%siso_%s' % (iso.lower(),region))), name='t_%s_mt_embed' % label)
  
      w.function('t_%s_mt_embed' % label).setInterpolationOrder(interpOrder)
  
  w.factory('expr::t_%sIso_mt_embed("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_barrel_%sIso_mt_embed, t_endcap_%sIso_mt_embed)' % (iso,iso,iso))
tau_mt_file.Close()    


### Hadronic tau trigger efficiencies
with open('inputs/triggerSF-Moriond17/di-tau/fitresults_tt_moriond2017.json') as jsonfile:
    pars = json.load(jsonfile)
    for tautype in ['genuine', 'fake']:
        for iso in ['VLooseIso','LooseIso','MediumIso','TightIso','VTightIso','VVTightIso']:
            for dm in ['dm0', 'dm1', 'dm10']:
                label = '%s_%s_%s' % (tautype, iso, dm)
                x = pars['data_%s' % (label)]
                w.factory('CrystalBallEfficiency::t_%s_tt_data(t_pt[0],%g,%g,%g,%g,%g)' % (
                    label, x['m_{0}'], x['sigma'], x['alpha'], x['n'], x['norm']
                ))

                x = pars['mc_%s' % (label)]
                w.factory('CrystalBallEfficiency::t_%s_tt_mc(t_pt[0],%g,%g,%g,%g,%g)' % (
                    label, x['m_{0}'], x['sigma'], x['alpha'], x['n'], x['norm']
                ))
            label = '%s_%s' % (tautype, iso)
            wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                               't_%s_tt_data' % label, ['t_%s_dm0_tt_data' % label, 't_%s_dm1_tt_data' % label, 't_%s_dm10_tt_data' % label])
            wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                               't_%s_tt_mc' % label, ['t_%s_dm0_tt_mc' % label, 't_%s_dm1_tt_mc' % label, 't_%s_dm10_tt_mc' % label])
            w.factory('expr::t_%s_tt_ratio("@0/@1", t_%s_tt_data, t_%s_tt_mc)' % (label, label, label))

interpOrder = 1
tau_mt_file = ROOT.TFile('inputs/triggerSF-Moriond17/mu-tau/trigger_sf_mt.root')
for tautype in ['genuine', 'fake']:
    for iso in ['NoIso',
                'VLooseIso',
                'LooseIso',
                'MediumIso',
                'TightIso',
                'VTightIso',
                'VVTightIso']:
        for region in ['barrel', 'endcap']:
            label = '%s_%s_%s' % (tautype, region, iso)

            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_mt_file.Get('data_%s' % label)), name='t_%s_mt_data' % label)
            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_mt_file.Get('mc_%s' % label)), name='t_%s_mt_mc' % label)

            w.function('t_%s_mt_data' % label).setInterpolationOrder(interpOrder)
            w.function('t_%s_mt_mc' % label).setInterpolationOrder(interpOrder)

            w.factory('expr::t_%s_mt_ratio("@0/@1", t_%s_mt_data, t_%s_mt_mc)' % (label, label, label))

        w.factory('expr::t_%s_%s_mt_ratio("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_mt_ratio, t_%s_endcap_%s_mt_ratio)' %
            (tautype, iso, tautype, iso, tautype, iso))
        w.factory('expr::t_%s_%s_mt_data("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_mt_data, t_%s_endcap_%s_mt_data)' %
            (tautype, iso, tautype, iso, tautype, iso))
        w.factory('expr::t_%s_%s_mt_mc("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_mt_mc, t_%s_endcap_%s_mt_mc)' %
            (tautype, iso, tautype, iso, tautype, iso))

tau_mt_file.Close()

tau_et_file = ROOT.TFile('inputs/triggerSF-Moriond17/ele-tau/trigger_sf_et.root')
for tautype in ['genuine', 'fake']:
    for iso in ['NoIso',
                'VLooseIso',
                'LooseIso',
                'MediumIso',
                'TightIso',
                'VTightIso',
                'VVTightIso']:
        for region in ['barrel', 'endcap']:
            label = '%s_%s_%s' % (tautype, region, iso)

            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_et_file.Get('data_%s_dm0' % label)), name='t_%s_dm0_et_data' % label)
            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_et_file.Get('data_%s_dm1' % label)), name='t_%s_dm1_et_data' % label)
            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_et_file.Get('data_%s_dm10' % label)), name='t_%s_dm10_et_data' % label)

            wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                               't_%s_et_data' % label, ['t_%s_dm0_et_data' % label, 't_%s_dm1_et_data' % label, 't_%s_dm10_et_data' % label])

            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_et_file.Get('mc_%s' % label)), name='t_%s_et_mc' % label)

            w.function('t_%s_dm0_et_data' % label).setInterpolationOrder(interpOrder)
            w.function('t_%s_dm1_et_data' % label).setInterpolationOrder(interpOrder)
            w.function('t_%s_dm10_et_data' % label).setInterpolationOrder(interpOrder)
            w.function('t_%s_et_mc' % label).setInterpolationOrder(interpOrder)

            w.factory('expr::t_%s_et_ratio("@0/@1", t_%s_et_data, t_%s_et_mc)' % (label, label, label))

        w.factory('expr::t_%s_%s_et_data("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_et_data, t_%s_endcap_%s_et_data)' %
            (tautype, iso, tautype, iso, tautype, iso))
        w.factory('expr::t_%s_%s_et_mc("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_et_mc, t_%s_endcap_%s_et_mc)' %
            (tautype, iso, tautype, iso, tautype, iso))
        w.factory('expr::t_%s_%s_et_ratio("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_et_ratio, t_%s_endcap_%s_et_ratio)' %
            (tautype, iso, tautype, iso, tautype, iso))


tau_et_file.Close()


### LO DYJetsToLL Z mass vs pT correction
histsToWrap = [
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo'                 , 'zpt_weight_nom'         ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_ESUp'            , 'zpt_weight_esup'        ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_ESDown'          , 'zpt_weight_esdown'      ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_TTUp'            , 'zpt_weight_ttup'        ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_TTDown'          , 'zpt_weight_ttdown'      ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_StatM400pT0Up'   , 'zpt_weight_statpt0up'   ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_StatM400pT0Down' , 'zpt_weight_statpt0down' ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_StatM400pT40Up'  , 'zpt_weight_statpt40up'  ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_StatM400pT40Down', 'zpt_weight_statpt40down'),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_StatM400pT80Up'  , 'zpt_weight_statpt80up'  ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_StatM400pT80Down', 'zpt_weight_statpt80down')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['z_gen_mass', 'z_gen_pt'],
                          GetFromTFile(task[0]), name=task[1])

# correction for quark mass dependence to ggH
wsptools.SafeWrapHist(w, ['HpT'],  GetFromTFile('inputs/ICSF/ggH/quarkmass_uncerts_hnnlo.root:nom'), 'ggH_quarkmass_hist')
w.factory('expr::ggH_quarkmass_corr("1.006*@0", ggH_quarkmass_hist)') # the constant factor is to ensure the normalization doesn't change - it is sample specific

wsptools.SafeWrapHist(w, ['HpT'],  GetFromTFile('inputs/ICSF/ggH/quarkmass_uncerts_hnnlo.root:up'), 'ggH_quarkmass_hist_up')
w.factory('expr::ggH_quarkmass_corr_up("1.006*@0", ggH_quarkmass_hist_up)')
wsptools.SafeWrapHist(w, ['HpT'],  GetFromTFile('inputs/ICSF/ggH/quarkmass_uncerts_hnnlo.root:down'), 'ggH_quarkmass_hist_down')
w.factory('expr::ggH_quarkmass_corr_down("1.006*@0", ggH_quarkmass_hist_down)')

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

w.importClassCode('CrystalBallEfficiency')

w.Print()
w.writeToFile('htt_scalefactors_v16_5_1.root')
w.Delete()
