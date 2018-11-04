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

loc = 'inputs/ICSF/FFFracs/'

histsToWrap = [
    (loc+'/ff_fracs_et.root:bin_2_W_fracs', 'w_et_0jet'),
    (loc+'/ff_fracs_et.root:bin_3_W_fracs', 'w_et_boosted_low'),
    (loc+'/ff_fracs_et.root:bin_4_W_fracs', 'w_et_boosted_high'),
    (loc+'/ff_fracs_et.root:bin_5_W_fracs', 'w_et_dijet_lowboost'),
    (loc+'/ff_fracs_et.root:bin_6_W_fracs', 'w_et_dijet_boosted'),
    (loc+'/ff_fracs_et.root:bin_7_W_fracs', 'w_et_btag'),
    (loc+'/ff_fracs_et.root:bin_2_TT_fracs', 'ttbar_et_0jet'),
    (loc+'/ff_fracs_et.root:bin_3_TT_fracs', 'ttbar_et_boosted_low'),
    (loc+'/ff_fracs_et.root:bin_4_TT_fracs', 'ttbar_et_boosted_high'),
    (loc+'/ff_fracs_et.root:bin_5_TT_fracs', 'ttbar_et_dijet_lowboost'),
    (loc+'/ff_fracs_et.root:bin_6_TT_fracs', 'ttbar_et_dijet_boosted'),
    (loc+'/ff_fracs_et.root:bin_7_TT_fracs', 'ttbar_et_btag'),
    (loc+'/ff_fracs_et.root:bin_2_QCD_fracs', 'qcd_et_0jet'),
    (loc+'/ff_fracs_et.root:bin_3_QCD_fracs', 'qcd_et_boosted_low'),
    (loc+'/ff_fracs_et.root:bin_4_QCD_fracs', 'qcd_et_boosted_high'),
    (loc+'/ff_fracs_et.root:bin_5_QCD_fracs', 'qcd_et_dijet_lowboost'),
    (loc+'/ff_fracs_et.root:bin_6_QCD_fracs', 'qcd_et_dijet_boosted'),
    (loc+'/ff_fracs_et.root:bin_7_QCD_fracs', 'qcd_et_btag'),
    (loc+'/ff_fracs_et.root:bin_2_realtau_sf', 'realtau_et_0jet'),
    (loc+'/ff_fracs_et.root:bin_3_realtau_sf', 'realtau_et_boosted_low'),
    (loc+'/ff_fracs_et.root:bin_4_realtau_sf', 'realtau_et_boosted_high'),
    (loc+'/ff_fracs_et.root:bin_5_realtau_sf', 'realtau_et_dijet_lowboost'),
    (loc+'/ff_fracs_et.root:bin_6_realtau_sf', 'realtau_et_dijet_boosted'),
    (loc+'/ff_fracs_et.root:bin_7_realtau_sf', 'realtau_et_btag'),
    (loc+'/ff_fracs_mt.root:bin_2_W_fracs', 'w_mt_0jet'),
    (loc+'/ff_fracs_mt.root:bin_3_W_fracs', 'w_mt_boosted_low'),
    (loc+'/ff_fracs_mt.root:bin_4_W_fracs', 'w_mt_boosted_high'),
    (loc+'/ff_fracs_mt.root:bin_5_W_fracs', 'w_mt_dijet_lowboost'),
    (loc+'/ff_fracs_mt.root:bin_6_W_fracs', 'w_mt_dijet_boosted'),
    (loc+'/ff_fracs_mt.root:bin_7_W_fracs', 'w_mt_btag'),
    (loc+'/ff_fracs_mt.root:bin_2_TT_fracs', 'ttbar_mt_0jet'),
    (loc+'/ff_fracs_mt.root:bin_3_TT_fracs', 'ttbar_mt_boosted_low'),
    (loc+'/ff_fracs_mt.root:bin_4_TT_fracs', 'ttbar_mt_boosted_high'),
    (loc+'/ff_fracs_mt.root:bin_5_TT_fracs', 'ttbar_mt_dijet_lowboost'),
    (loc+'/ff_fracs_mt.root:bin_6_TT_fracs', 'ttbar_mt_dijet_boosted'),
    (loc+'/ff_fracs_mt.root:bin_7_TT_fracs', 'ttbar_mt_btag'),
    (loc+'/ff_fracs_mt.root:bin_2_QCD_fracs', 'qcd_mt_0jet'),
    (loc+'/ff_fracs_mt.root:bin_3_QCD_fracs', 'qcd_mt_boosted_low'),
    (loc+'/ff_fracs_mt.root:bin_4_QCD_fracs', 'qcd_mt_boosted_high'),
    (loc+'/ff_fracs_mt.root:bin_5_QCD_fracs', 'qcd_mt_dijet_lowboost'),
    (loc+'/ff_fracs_mt.root:bin_6_QCD_fracs', 'qcd_mt_dijet_boosted'),
    (loc+'/ff_fracs_mt.root:bin_7_QCD_fracs', 'qcd_mt_btag'),
    (loc+'/ff_fracs_mt.root:bin_2_realtau_sf', 'realtau_mt_0jet'),
    (loc+'/ff_fracs_mt.root:bin_3_realtau_sf', 'realtau_mt_boosted_low'),
    (loc+'/ff_fracs_mt.root:bin_4_realtau_sf', 'realtau_mt_boosted_high'),
    (loc+'/ff_fracs_mt.root:bin_5_realtau_sf', 'realtau_mt_dijet_lowboost'),
    (loc+'/ff_fracs_mt.root:bin_6_realtau_sf', 'realtau_mt_dijet_boosted'),
    (loc+'/ff_fracs_mt.root:bin_7_realtau_sf', 'realtau_mt_btag'),
    (loc+'/ff_fracs_tt.root:bin_2_W_fracs', 'w_tt_0jet_1'),
    (loc+'/ff_fracs_tt.root:bin_3_W_fracs', 'w_tt_boosted_low_1'),
    (loc+'/ff_fracs_tt.root:bin_4_W_fracs', 'w_tt_boosted_high_1'),
    (loc+'/ff_fracs_tt.root:bin_5_W_fracs', 'w_tt_dijet_lowboost_1'),
    (loc+'/ff_fracs_tt.root:bin_6_W_fracs', 'w_tt_dijet_boosted_1'),
    (loc+'/ff_fracs_tt.root:bin_2_TT_fracs', 'ttbar_tt_0jet_1'),
    (loc+'/ff_fracs_tt.root:bin_3_TT_fracs', 'ttbar_tt_boosted_low_1'),
    (loc+'/ff_fracs_tt.root:bin_4_TT_fracs', 'ttbar_tt_boosted_high_1'),
    (loc+'/ff_fracs_tt.root:bin_5_TT_fracs', 'ttbar_tt_dijet_lowboost_1'),
    (loc+'/ff_fracs_tt.root:bin_6_TT_fracs', 'ttbar_tt_dijet_boosted_1'),
    (loc+'/ff_fracs_tt.root:bin_2_QCD_fracs', 'qcd_tt_0jet_1'),
    (loc+'/ff_fracs_tt.root:bin_3_QCD_fracs', 'qcd_tt_boosted_low_1'),
    (loc+'/ff_fracs_tt.root:bin_4_QCD_fracs', 'qcd_tt_boosted_high_1'),
    (loc+'/ff_fracs_tt.root:bin_5_QCD_fracs', 'qcd_tt_dijet_lowboost_1'),
    (loc+'/ff_fracs_tt.root:bin_6_QCD_fracs', 'qcd_tt_dijet_boosted_1'),
    (loc+'/ff_fracs_tt.root:bin_2_DY_fracs', 'dy_tt_0jet_1'),
    (loc+'/ff_fracs_tt.root:bin_3_DY_fracs', 'dy_tt_boosted_low_1'),
    (loc+'/ff_fracs_tt.root:bin_4_DY_fracs', 'dy_tt_boosted_high_1'),
    (loc+'/ff_fracs_tt.root:bin_5_DY_fracs', 'dy_tt_dijet_lowboost_1'),
    (loc+'/ff_fracs_tt.root:bin_6_DY_fracs', 'dy_tt_dijet_boosted_1'),
    (loc+'/ff_fracs_tt.root:bin_2_realtau_sf', 'realtau_tt_0jet_1'),
    (loc+'/ff_fracs_tt.root:bin_3_realtau_sf', 'realtau_tt_boosted_low_1'),
    (loc+'/ff_fracs_tt.root:bin_4_realtau_sf', 'realtau_tt_boosted_high_1'),
    (loc+'/ff_fracs_tt.root:bin_5_realtau_sf', 'realtau_tt_dijet_lowboost_1'),
    (loc+'/ff_fracs_tt.root:bin_6_realtau_sf', 'realtau_tt_dijet_boosted_1'),
    (loc+'/ff_fracs_tt.root:bin_8_W_fracs', 'w_tt_0jet_2'),
    (loc+'/ff_fracs_tt.root:bin_9_W_fracs', 'w_tt_boosted_low_2'),
    (loc+'/ff_fracs_tt.root:bin_10_W_fracs', 'w_tt_boosted_high_2'),
    (loc+'/ff_fracs_tt.root:bin_11_W_fracs', 'w_tt_dijet_lowboost_2'),
    (loc+'/ff_fracs_tt.root:bin_12_W_fracs', 'w_tt_dijet_boosted_2'),
    (loc+'/ff_fracs_tt.root:bin_8_TT_fracs', 'ttbar_tt_0jet_2'),
    (loc+'/ff_fracs_tt.root:bin_9_TT_fracs', 'ttbar_tt_boosted_low_2'),
    (loc+'/ff_fracs_tt.root:bin_10_TT_fracs', 'ttbar_tt_boosted_high_2'),
    (loc+'/ff_fracs_tt.root:bin_11_TT_fracs', 'ttbar_tt_dijet_lowboost_2'),
    (loc+'/ff_fracs_tt.root:bin_12_TT_fracs', 'ttbar_tt_dijet_boosted_2'),
    (loc+'/ff_fracs_tt.root:bin_8_QCD_fracs', 'qcd_tt_0jet_2'),
    (loc+'/ff_fracs_tt.root:bin_9_QCD_fracs', 'qcd_tt_boosted_low_2'),
    (loc+'/ff_fracs_tt.root:bin_10_QCD_fracs', 'qcd_tt_boosted_high_2'),
    (loc+'/ff_fracs_tt.root:bin_11_QCD_fracs', 'qcd_tt_dijet_lowboost_2'),
    (loc+'/ff_fracs_tt.root:bin_12_QCD_fracs', 'qcd_tt_dijet_boosted_2'),
    (loc+'/ff_fracs_tt.root:bin_8_DY_fracs', 'dy_tt_0jet_2'),
    (loc+'/ff_fracs_tt.root:bin_9_DY_fracs', 'dy_tt_boosted_low_2'),
    (loc+'/ff_fracs_tt.root:bin_10_DY_fracs', 'dy_tt_boosted_high_2'),
    (loc+'/ff_fracs_tt.root:bin_11_DY_fracs', 'dy_tt_dijet_lowboost_2'),
    (loc+'/ff_fracs_tt.root:bin_12_DY_fracs', 'dy_tt_dijet_boosted_2'),
    (loc+'/ff_fracs_tt.root:bin_8_realtau_sf', 'realtau_tt_0jet_2'),
    (loc+'/ff_fracs_tt.root:bin_9_realtau_sf', 'realtau_tt_boosted_low_2'),
    (loc+'/ff_fracs_tt.root:bin_10_realtau_sf', 'realtau_tt_boosted_high_2'),
    (loc+'/ff_fracs_tt.root:bin_11_realtau_sf', 'realtau_tt_dijet_lowboost_2'),
    (loc+'/ff_fracs_tt.root:bin_12_realtau_sf', 'realtau_tt_dijet_boosted_2')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['expr::mvis_max240("min(@0,240)",mvis[0])'],
                          GetFromTFile(task[0]), name=task[1])

procs = ['w','qcd','ttbar','realtau']
for chan in ['mt','et']:
  for proc in procs: 
    wsptools.MakeBinnedCategoryFuncMap(w, 'pt_tt', [0., 200., 100000.],
                                       '%s_%s_dijet' % (proc,chan), ['%s_%s_dijet_lowboost' % (proc,chan), '%s_%s_dijet_boosted' % (proc,chan)])
    wsptools.MakeBinnedCategoryFuncMap(w, 'pt_tt', [0., 100., 100000.],
                                       '%s_%s_1jet' % (proc,chan), ['%s_%s_boosted_low' % (proc,chan), '%s_%s_boosted_high' % (proc,chan)])   

    wsptools.MakeBinnedCategoryFuncMap(w, 'mjj', [0., 300., 100000.],
                                       '%s_%s_2jet' % (proc,chan), ['%s_%s_1jet' % (proc,chan), '%s_%s_dijet' % (proc,chan)])
    
    if proc == 'realtau': extra = 'sf'
    else: extra = 'fracs'
    
    wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0, 1, 2, 100000],
                                       '%s_%s_0bjet' % (proc,chan), ['%s_%s_0jet' % (proc,chan), '%s_%s_1jet' % (proc,chan), '%s_%s_2jet' % (proc,chan)])

    wsptools.MakeBinnedCategoryFuncMap(w, 'nbjets', [0, 1, 100000],
                                       '%s_%s_%s' % (proc,chan,extra), ['%s_%s_0bjet' % (proc,chan), '%s_%s_btag' % (proc,chan)])

procs = ['w','qcd','ttbar','dy','realtau']    
for proc in procs: 
    wsptools.MakeBinnedCategoryFuncMap(w, 'pt_tt', [0., 200., 100000.],
                                       '%s_tt_dijet_1' % (proc), ['%s_tt_dijet_lowboost_1' % (proc), '%s_tt_dijet_boosted_1' % (proc)])
    wsptools.MakeBinnedCategoryFuncMap(w, 'pt_tt', [0., 200., 100000.],
                                       '%s_tt_dijet_2' % (proc), ['%s_tt_dijet_lowboost_2' % (proc), '%s_tt_dijet_boosted_2' % (proc)])
    wsptools.MakeBinnedCategoryFuncMap(w, 'pt_tt', [0., 100., 100000.],
                                       '%s_tt_1jet_1' % (proc), ['%s_tt_boosted_low_1' % (proc), '%s_tt_boosted_high_1' % (proc)])    
    wsptools.MakeBinnedCategoryFuncMap(w, 'pt_tt', [0., 100., 100000.],
                                       '%s_tt_1jet_2' % (proc), ['%s_tt_boosted_low_2' % (proc), '%s_tt_boosted_high_2' % (proc)]) 

    wsptools.MakeBinnedCategoryFuncMap(w, 'mjj', [0., 300., 100000.],
                                       '%s_tt_2jet_1' % (proc), ['%s_tt_1jet_1' % (proc), '%s_tt_dijet_1' % (proc)])
    
    wsptools.MakeBinnedCategoryFuncMap(w, 'mjj', [0., 300., 100000.],
                                       '%s_tt_2jet_2' % (proc), ['%s_tt_1jet_2' % (proc), '%s_tt_dijet_2' % (proc)])
    
    if proc == 'realtau': extra = 'sf'
    else: extra = 'fracs'
    
    wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0, 1, 2, 100000],
                                       '%s_tt_%s_1' % (proc,extra), ['%s_tt_0jet_1' % (proc), '%s_tt_1jet_1' % (proc), '%s_tt_2jet_1' % (proc)])
    wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0, 1, 2, 100000],
                                       '%s_tt_%s_2' % (proc,extra), ['%s_tt_0jet_2' % (proc), '%s_tt_1jet_2' % (proc), '%s_tt_2jet_2' % (proc)])


w.Print()
w.writeToFile('ff_fracs_2016.root')
w.Delete()
