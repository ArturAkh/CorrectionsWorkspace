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

loc = 'inputs/ICSF/FFFracs/pt_fracs/'

histsToWrap = [
    (loc+'/ff_fracs_pt_et.root:bin_0jet_W_fracs', 'w_et_0jet'),
    (loc+'/ff_fracs_pt_et.root:bin_0jet_TT_fracs', 'ttbar_et_0jet'),
    (loc+'/ff_fracs_pt_et.root:bin_0jet_QCD_fracs', 'qcd_et_0jet'),
    (loc+'/ff_fracs_pt_et.root:bin_1jet_W_fracs', 'w_et_1jet'),
    (loc+'/ff_fracs_pt_et.root:bin_1jet_TT_fracs', 'ttbar_et_1jet'),
    (loc+'/ff_fracs_pt_et.root:bin_1jet_QCD_fracs', 'qcd_et_1jet'),
    (loc+'/ff_fracs_pt_et.root:bin_2jet_W_fracs', 'w_et_2jet'),
    (loc+'/ff_fracs_pt_et.root:bin_2jet_TT_fracs', 'ttbar_et_2jet'),
    (loc+'/ff_fracs_pt_et.root:bin_2jet_QCD_fracs', 'qcd_et_2jet'),
    (loc+'/ff_fracs_pt_et.root:bin_btag_W_fracs', 'w_et_btag'),
    (loc+'/ff_fracs_pt_et.root:bin_btag_TT_fracs', 'ttbar_et_btag'),
    (loc+'/ff_fracs_pt_et.root:bin_btag_QCD_fracs', 'qcd_et_btag'),
    (loc+'/ff_fracs_pt_et.root:bin_0jet_ss_W_fracs', 'w_et_0jet_ss'),
    (loc+'/ff_fracs_pt_et.root:bin_0jet_ss_TT_fracs', 'ttbar_et_0jet_ss'),
    (loc+'/ff_fracs_pt_et.root:bin_0jet_ss_QCD_fracs', 'qcd_et_0jet_ss'),
    (loc+'/ff_fracs_pt_et.root:bin_1jet_ss_W_fracs', 'w_et_1jet_ss'),
    (loc+'/ff_fracs_pt_et.root:bin_1jet_ss_TT_fracs', 'ttbar_et_1jet_ss'),
    (loc+'/ff_fracs_pt_et.root:bin_1jet_ss_QCD_fracs', 'qcd_et_1jet_ss'),
    (loc+'/ff_fracs_pt_et.root:bin_2jet_ss_W_fracs', 'w_et_2jet_ss'),
    (loc+'/ff_fracs_pt_et.root:bin_2jet_ss_TT_fracs', 'ttbar_et_2jet_ss'),
    (loc+'/ff_fracs_pt_et.root:bin_2jet_ss_QCD_fracs', 'qcd_et_2jet_ss'),
    (loc+'/ff_fracs_pt_et.root:bin_btag_ss_W_fracs', 'w_et_btag_ss'),
    (loc+'/ff_fracs_pt_et.root:bin_btag_ss_TT_fracs', 'ttbar_et_btag_ss'),
    (loc+'/ff_fracs_pt_et.root:bin_btag_ss_QCD_fracs', 'qcd_et_btag_ss'),
    (loc+'/ff_fracs_pt_et.root:bin_0jet_highmt_W_fracs', 'w_et_0jet_highmt'),
    (loc+'/ff_fracs_pt_et.root:bin_0jet_highmt_TT_fracs', 'ttbar_et_0jet_highmt'),
    (loc+'/ff_fracs_pt_et.root:bin_0jet_highmt_QCD_fracs', 'qcd_et_0jet_highmt'),
    (loc+'/ff_fracs_pt_et.root:bin_1jet_highmt_W_fracs', 'w_et_1jet_highmt'),
    (loc+'/ff_fracs_pt_et.root:bin_1jet_highmt_TT_fracs', 'ttbar_et_1jet_highmt'),
    (loc+'/ff_fracs_pt_et.root:bin_1jet_highmt_QCD_fracs', 'qcd_et_1jet_highmt'),
    (loc+'/ff_fracs_pt_et.root:bin_2jet_highmt_W_fracs', 'w_et_2jet_highmt'),
    (loc+'/ff_fracs_pt_et.root:bin_2jet_highmt_TT_fracs', 'ttbar_et_2jet_highmt'),
    (loc+'/ff_fracs_pt_et.root:bin_2jet_highmt_QCD_fracs', 'qcd_et_2jet_highmt'),
    (loc+'/ff_fracs_pt_et.root:bin_btag_highmt_W_fracs', 'w_et_btag_highmt'),
    (loc+'/ff_fracs_pt_et.root:bin_btag_highmt_TT_fracs', 'ttbar_et_btag_highmt'),
    (loc+'/ff_fracs_pt_et.root:bin_btag_highmt_QCD_fracs', 'qcd_et_btag_highmt'),
    (loc+'/ff_fracs_pt_mt.root:bin_0jet_W_fracs', 'w_mt_0jet'),
    (loc+'/ff_fracs_pt_mt.root:bin_0jet_TT_fracs', 'ttbar_mt_0jet'),
    (loc+'/ff_fracs_pt_mt.root:bin_0jet_QCD_fracs', 'qcd_mt_0jet'),
    (loc+'/ff_fracs_pt_mt.root:bin_1jet_W_fracs', 'w_mt_1jet'),
    (loc+'/ff_fracs_pt_mt.root:bin_1jet_TT_fracs', 'ttbar_mt_1jet'),
    (loc+'/ff_fracs_pt_mt.root:bin_1jet_QCD_fracs', 'qcd_mt_1jet'),
    (loc+'/ff_fracs_pt_mt.root:bin_2jet_W_fracs', 'w_mt_2jet'),
    (loc+'/ff_fracs_pt_mt.root:bin_2jet_TT_fracs', 'ttbar_mt_2jet'),
    (loc+'/ff_fracs_pt_mt.root:bin_2jet_QCD_fracs', 'qcd_mt_2jet'),
    (loc+'/ff_fracs_pt_mt.root:bin_btag_W_fracs', 'w_mt_btag'),
    (loc+'/ff_fracs_pt_mt.root:bin_btag_TT_fracs', 'ttbar_mt_btag'),
    (loc+'/ff_fracs_pt_mt.root:bin_btag_QCD_fracs', 'qcd_mt_btag'),
    (loc+'/ff_fracs_pt_mt.root:bin_0jet_ss_W_fracs', 'w_mt_0jet_ss'),
    (loc+'/ff_fracs_pt_mt.root:bin_0jet_ss_TT_fracs', 'ttbar_mt_0jet_ss'),
    (loc+'/ff_fracs_pt_mt.root:bin_0jet_ss_QCD_fracs', 'qcd_mt_0jet_ss'),
    (loc+'/ff_fracs_pt_mt.root:bin_1jet_ss_W_fracs', 'w_mt_1jet_ss'),
    (loc+'/ff_fracs_pt_mt.root:bin_1jet_ss_TT_fracs', 'ttbar_mt_1jet_ss'),
    (loc+'/ff_fracs_pt_mt.root:bin_1jet_ss_QCD_fracs', 'qcd_mt_1jet_ss'),
    (loc+'/ff_fracs_pt_mt.root:bin_2jet_ss_W_fracs', 'w_mt_2jet_ss'),
    (loc+'/ff_fracs_pt_mt.root:bin_2jet_ss_TT_fracs', 'ttbar_mt_2jet_ss'),
    (loc+'/ff_fracs_pt_mt.root:bin_2jet_ss_QCD_fracs', 'qcd_mt_2jet_ss'),
    (loc+'/ff_fracs_pt_mt.root:bin_btag_ss_W_fracs', 'w_mt_btag_ss'),
    (loc+'/ff_fracs_pt_mt.root:bin_btag_ss_TT_fracs', 'ttbar_mt_btag_ss'),
    (loc+'/ff_fracs_pt_mt.root:bin_btag_ss_QCD_fracs', 'qcd_mt_btag_ss'),
    (loc+'/ff_fracs_pt_mt.root:bin_0jet_highmt_W_fracs', 'w_mt_0jet_highmt'),
    (loc+'/ff_fracs_pt_mt.root:bin_0jet_highmt_TT_fracs', 'ttbar_mt_0jet_highmt'),
    (loc+'/ff_fracs_pt_mt.root:bin_0jet_highmt_QCD_fracs', 'qcd_mt_0jet_highmt'),
    (loc+'/ff_fracs_pt_mt.root:bin_1jet_highmt_W_fracs', 'w_mt_1jet_highmt'),
    (loc+'/ff_fracs_pt_mt.root:bin_1jet_highmt_TT_fracs', 'ttbar_mt_1jet_highmt'),
    (loc+'/ff_fracs_pt_mt.root:bin_1jet_highmt_QCD_fracs', 'qcd_mt_1jet_highmt'),
    (loc+'/ff_fracs_pt_mt.root:bin_2jet_highmt_W_fracs', 'w_mt_2jet_highmt'),
    (loc+'/ff_fracs_pt_mt.root:bin_2jet_highmt_TT_fracs', 'ttbar_mt_2jet_highmt'),
    (loc+'/ff_fracs_pt_mt.root:bin_2jet_highmt_QCD_fracs', 'qcd_mt_2jet_highmt'),
    (loc+'/ff_fracs_pt_mt.root:bin_btag_highmt_W_fracs', 'w_mt_btag_highmt'),
    (loc+'/ff_fracs_pt_mt.root:bin_btag_highmt_TT_fracs', 'ttbar_mt_btag_highmt'),
    (loc+'/ff_fracs_pt_mt.root:bin_btag_highmt_QCD_fracs', 'qcd_mt_btag_highmt'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_1_W_fracs', 'w_tt_0jet_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_1_TT_fracs', 'ttbar_tt_0jet_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_1_QCD_fracs', 'qcd_tt_0jet_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_1_DY_fracs', 'dy_tt_0jet_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_1_W_fracs', 'w_tt_1jet_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_1_TT_fracs', 'ttbar_tt_1jet_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_1_QCD_fracs', 'qcd_tt_1jet_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_1_DY_fracs', 'dy_tt_1jet_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_1_W_fracs', 'w_tt_2jet_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_1_TT_fracs', 'ttbar_tt_2jet_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_1_QCD_fracs', 'qcd_tt_2jet_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_1_DY_fracs', 'dy_tt_2jet_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_1_W_fracs', 'w_tt_btag_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_1_TT_fracs', 'ttbar_tt_btag_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_1_QCD_fracs', 'qcd_tt_btag_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_1_DY_fracs', 'dy_tt_btag_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_ss_1_W_fracs', 'w_tt_0jet_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_ss_1_TT_fracs', 'ttbar_tt_0jet_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_ss_1_QCD_fracs', 'qcd_tt_0jet_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_ss_1_DY_fracs', 'dy_tt_0jet_ss_1'), 
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_ss_1_W_fracs', 'w_tt_1jet_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_ss_1_TT_fracs', 'ttbar_tt_1jet_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_ss_1_QCD_fracs', 'qcd_tt_1jet_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_ss_1_DY_fracs', 'dy_tt_1jet_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_ss_1_W_fracs', 'w_tt_2jet_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_ss_1_TT_fracs', 'ttbar_tt_2jet_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_ss_1_QCD_fracs', 'qcd_tt_2jet_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_ss_1_DY_fracs', 'dy_tt_2jet_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_ss_1_W_fracs', 'w_tt_btag_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_ss_1_TT_fracs', 'ttbar_tt_btag_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_ss_1_QCD_fracs', 'qcd_tt_btag_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_ss_1_DY_fracs', 'dy_tt_btag_ss_1'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_2_W_fracs', 'w_tt_0jet_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_2_TT_fracs', 'ttbar_tt_0jet_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_2_QCD_fracs', 'qcd_tt_0jet_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_2_DY_fracs', 'dy_tt_0jet_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_2_W_fracs', 'w_tt_1jet_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_2_TT_fracs', 'ttbar_tt_1jet_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_2_QCD_fracs', 'qcd_tt_1jet_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_2_DY_fracs', 'dy_tt_1jet_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_2_W_fracs', 'w_tt_2jet_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_2_TT_fracs', 'ttbar_tt_2jet_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_2_QCD_fracs', 'qcd_tt_2jet_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_2_DY_fracs', 'dy_tt_2jet_2'), 
    (loc+'/ff_fracs_pt_tt.root:bin_btag_2_W_fracs', 'w_tt_btag_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_2_TT_fracs', 'ttbar_tt_btag_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_2_QCD_fracs', 'qcd_tt_btag_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_2_DY_fracs', 'dy_tt_btag_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_ss_2_W_fracs', 'w_tt_0jet_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_ss_2_TT_fracs', 'ttbar_tt_0jet_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_ss_2_QCD_fracs', 'qcd_tt_0jet_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_0jet_ss_2_DY_fracs', 'dy_tt_0jet_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_ss_2_W_fracs', 'w_tt_1jet_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_ss_2_TT_fracs', 'ttbar_tt_1jet_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_ss_2_QCD_fracs', 'qcd_tt_1jet_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_1jet_ss_2_DY_fracs', 'dy_tt_1jet_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_ss_2_W_fracs', 'w_tt_2jet_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_ss_2_TT_fracs', 'ttbar_tt_2jet_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_ss_2_QCD_fracs', 'qcd_tt_2jet_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_2jet_ss_2_DY_fracs', 'dy_tt_2jet_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_ss_2_W_fracs', 'w_tt_btag_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_ss_2_TT_fracs', 'ttbar_tt_btag_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_ss_2_QCD_fracs', 'qcd_tt_btag_ss_2'),
    (loc+'/ff_fracs_pt_tt.root:bin_btag_ss_2_DY_fracs', 'dy_tt_btag_ss_2'),

]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['expr::pt_max250("min(@0,250)",pt[0])'],
                          GetFromTFile(task[0]), name=task[1])

procs = ['w','qcd','ttbar']
for chan in ['mt','et']:
  for proc in procs: 
    wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0, 1, 2, 100000],
                                       '%s_%s_0bjet' % (proc,chan), ['%s_%s_0jet' % (proc,chan), '%s_%s_1jet' % (proc,chan), '%s_%s_2jet' % (proc,chan)])

    wsptools.MakeBinnedCategoryFuncMap(w, 'nbjets', [0, 1, 100000],
                                       '%s_%s_fracs' % (proc,chan), ['%s_%s_0bjet' % (proc,chan), '%s_%s_btag' % (proc,chan)])

    wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0, 1, 2, 100000],
                                       '%s_%s_0bjet_ss' % (proc,chan), ['%s_%s_0jet_ss' % (proc,chan), '%s_%s_1jet_ss' % (proc,chan), '%s_%s_2jet_ss' % (proc,chan)])

    wsptools.MakeBinnedCategoryFuncMap(w, 'nbjets', [0, 1, 100000],
                                       '%s_%s_ss_fracs' % (proc,chan), ['%s_%s_0bjet_ss' % (proc,chan), '%s_%s_btag_ss' % (proc,chan)])

    wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0, 1, 2, 100000],
                                       '%s_%s_0bjet_highmt' % (proc,chan), ['%s_%s_0jet_highmt' % (proc,chan), '%s_%s_1jet_highmt' % (proc,chan), '%s_%s_2jet_highmt' % (proc,chan)])

    wsptools.MakeBinnedCategoryFuncMap(w, 'nbjets', [0, 1, 100000],
                                       '%s_%s_highmt_fracs' % (proc,chan), ['%s_%s_0bjet_highmt' % (proc,chan), '%s_%s_btag_highmt' % (proc,chan)])

procs = ['w','qcd','ttbar','dy']    
for proc in procs: 
    chan='tt'
    wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0, 1, 2, 100000],
                                       '%s_%s_0bjet_1' % (proc,chan), ['%s_%s_0jet_1' % (proc,chan), '%s_%s_1jet_1' % (proc,chan), '%s_%s_2jet_1' % (proc,chan)])
    
    wsptools.MakeBinnedCategoryFuncMap(w, 'nbjets', [0, 1, 100000],
                                       '%s_%s_fracs_1' % (proc,chan), ['%s_%s_0bjet_1' % (proc,chan), '%s_%s_btag_1' % (proc,chan)])
    
    wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0, 1, 2, 100000],
                                       '%s_%s_0bjet_2' % (proc,chan), ['%s_%s_0jet_2' % (proc,chan), '%s_%s_1jet_2' % (proc,chan), '%s_%s_2jet_2' % (proc,chan)])

    wsptools.MakeBinnedCategoryFuncMap(w, 'nbjets', [0, 1, 100000],
                                       '%s_%s_fracs_2' % (proc,chan), ['%s_%s_0bjet_2' % (proc,chan), '%s_%s_btag_2' % (proc,chan)])

    wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0, 1, 2, 100000],
                                       '%s_%s_0bjet_ss_1' % (proc,chan), ['%s_%s_0jet_ss_1' % (proc,chan), '%s_%s_1jet_ss_1' % (proc,chan), '%s_%s_2jet_ss_1' % (proc,chan)])

    wsptools.MakeBinnedCategoryFuncMap(w, 'nbjets', [0, 1, 100000],
                                       '%s_%s_ss_fracs_1' % (proc,chan), ['%s_%s_0bjet_ss_1' % (proc,chan), '%s_%s_btag_ss_1' % (proc,chan)])

    wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0, 1, 2, 100000],
                                       '%s_%s_0bjet_ss_2' % (proc,chan), ['%s_%s_0jet_ss_2' % (proc,chan), '%s_%s_1jet_ss_2' % (proc,chan), '%s_%s_2jet_ss_2' % (proc,chan)])

    wsptools.MakeBinnedCategoryFuncMap(w, 'nbjets', [0, 1, 100000],
                                       '%s_%s_ss_fracs_2' % (proc,chan), ['%s_%s_0bjet_ss_2' % (proc,chan), '%s_%s_btag_ss_2' % (proc,chan)])

w.Print()
w.writeToFile('ff_fracs_pt_2016.root')
w.Delete()
