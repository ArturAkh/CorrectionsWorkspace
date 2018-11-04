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

loc = 'inputs/ICSF/FFFracs/new_fracs'

histsToWrap = [
    (loc+'/ff_fracs_new_et.root:bin_0jet_W_fracs', 'w_et_0jet'),
    (loc+'/ff_fracs_new_et.root:bin_0jet_TT_fracs', 'ttbar_et_0jet'),
    (loc+'/ff_fracs_new_et.root:bin_0jet_QCD_fracs', 'qcd_et_0jet'),
    (loc+'/ff_fracs_new_mt.root:bin_0jet_W_fracs', 'w_mt_0jet'),
    (loc+'/ff_fracs_new_mt.root:bin_0jet_TT_fracs', 'ttbar_mt_0jet'),
    (loc+'/ff_fracs_new_mt.root:bin_0jet_QCD_fracs', 'qcd_mt_0jet'),
    (loc+'/ff_fracs_new_tt.root:bin_0jet_1_W_fracs', 'w_tt_0jet_1'),
    (loc+'/ff_fracs_new_tt.root:bin_0jet_1_TT_fracs', 'ttbar_tt_0jet_1'),
    (loc+'/ff_fracs_new_tt.root:bin_0jet_1_QCD_fracs', 'qcd_tt_0jet_1'),
    (loc+'/ff_fracs_new_tt.root:bin_0jet_1_DY_fracs', 'dy_tt_0jet_1'), 
    (loc+'/ff_fracs_new_tt.root:bin_0jet_2_W_fracs', 'w_tt_0jet_2'),
    (loc+'/ff_fracs_new_tt.root:bin_0jet_2_TT_fracs', 'ttbar_tt_0jet_2'),
    (loc+'/ff_fracs_new_tt.root:bin_0jet_2_QCD_fracs', 'qcd_tt_0jet_2'),
    (loc+'/ff_fracs_new_tt.root:bin_0jet_2_DY_fracs', 'dy_tt_0jet_2')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['m_sv'],
                          GetFromTFile(task[0]), name=task[1])


histsToWrap = [
    (loc+'/ff_fracs_new_et.root:bin_boosted_W_fracs',        'w_et_boosted'),
    (loc+'/ff_fracs_new_et.root:bin_boosted_TT_fracs',   'ttbar_et_boosted'),
    (loc+'/ff_fracs_new_et.root:bin_boosted_QCD_fracs',    'qcd_et_boosted'),
    (loc+'/ff_fracs_new_mt.root:bin_boosted_W_fracs',        'w_mt_boosted'),
    (loc+'/ff_fracs_new_mt.root:bin_boosted_TT_fracs',   'ttbar_mt_boosted'),
    (loc+'/ff_fracs_new_mt.root:bin_boosted_QCD_fracs',    'qcd_mt_boosted'),
    (loc+'/ff_fracs_new_tt.root:bin_boosted_1_W_fracs',      'w_tt_boosted_1'),
    (loc+'/ff_fracs_new_tt.root:bin_boosted_1_TT_fracs', 'ttbar_tt_boosted_1'),
    (loc+'/ff_fracs_new_tt.root:bin_boosted_1_QCD_fracs',  'qcd_tt_boosted_1'),
    (loc+'/ff_fracs_new_tt.root:bin_boosted_1_DY_fracs',    'dy_tt_boosted_1'),
    (loc+'/ff_fracs_new_tt.root:bin_boosted_2_W_fracs',      'w_tt_boosted_2'),
    (loc+'/ff_fracs_new_tt.root:bin_boosted_2_TT_fracs', 'ttbar_tt_boosted_2'),
    (loc+'/ff_fracs_new_tt.root:bin_boosted_2_QCD_fracs',  'qcd_tt_boosted_2'),
    (loc+'/ff_fracs_new_tt.root:bin_boosted_2_DY_fracs',    'dy_tt_boosted_2')
]


for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['m_sv','pt_tt'],
                          GetFromTFile(task[0]), name=task[1],incOF=True)

histsToWrap = [
    (loc+'/ff_fracs_new_et.root:bin_dijet_loosemjj_lowboost_W_fracs',        'w_et_dijet_loosemjj_lowboost'),
    (loc+'/ff_fracs_new_et.root:bin_dijet_loosemjj_lowboost_TT_fracs',   'ttbar_et_dijet_loosemjj_lowboost'),
    (loc+'/ff_fracs_new_et.root:bin_dijet_loosemjj_lowboost_QCD_fracs',    'qcd_et_dijet_loosemjj_lowboost'),
    (loc+'/ff_fracs_new_mt.root:bin_dijet_loosemjj_lowboost_W_fracs',        'w_mt_dijet_loosemjj_lowboost'),
    (loc+'/ff_fracs_new_mt.root:bin_dijet_loosemjj_lowboost_TT_fracs',   'ttbar_mt_dijet_loosemjj_lowboost'),
    (loc+'/ff_fracs_new_mt.root:bin_dijet_loosemjj_lowboost_QCD_fracs',    'qcd_mt_dijet_loosemjj_lowboost'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_lowboost_1_W_fracs',      'w_tt_dijet_loosemjj_lowboost_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_lowboost_1_TT_fracs', 'ttbar_tt_dijet_loosemjj_lowboost_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_lowboost_1_QCD_fracs',  'qcd_tt_dijet_loosemjj_lowboost_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_lowboost_1_DY_fracs',    'dy_tt_dijet_loosemjj_lowboost_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_lowboost_2_W_fracs',      'w_tt_dijet_loosemjj_lowboost_2'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_lowboost_2_TT_fracs', 'ttbar_tt_dijet_loosemjj_lowboost_2'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_lowboost_2_QCD_fracs',  'qcd_tt_dijet_loosemjj_lowboost_2'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_lowboost_2_DY_fracs',    'dy_tt_dijet_loosemjj_lowboost_2'),

    (loc+'/ff_fracs_new_et.root:bin_dijet_loosemjj_boosted_W_fracs',        'w_et_dijet_loosemjj_boosted'),
    (loc+'/ff_fracs_new_et.root:bin_dijet_loosemjj_boosted_TT_fracs',   'ttbar_et_dijet_loosemjj_boosted'),
    (loc+'/ff_fracs_new_et.root:bin_dijet_loosemjj_boosted_QCD_fracs',    'qcd_et_dijet_loosemjj_boosted'),
    (loc+'/ff_fracs_new_mt.root:bin_dijet_loosemjj_boosted_W_fracs',        'w_mt_dijet_loosemjj_boosted'),
    (loc+'/ff_fracs_new_mt.root:bin_dijet_loosemjj_boosted_TT_fracs',   'ttbar_mt_dijet_loosemjj_boosted'),
    (loc+'/ff_fracs_new_mt.root:bin_dijet_loosemjj_boosted_QCD_fracs',    'qcd_mt_dijet_loosemjj_boosted'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_boosted_1_W_fracs',      'w_tt_dijet_loosemjj_boosted_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_boosted_1_TT_fracs', 'ttbar_tt_dijet_loosemjj_boosted_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_boosted_1_QCD_fracs',  'qcd_tt_dijet_loosemjj_boosted_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_boosted_1_DY_fracs',    'dy_tt_dijet_loosemjj_boosted_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_boosted_2_W_fracs',      'w_tt_dijet_loosemjj_boosted_2'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_boosted_2_TT_fracs', 'ttbar_tt_dijet_loosemjj_boosted_2'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_boosted_2_QCD_fracs',  'qcd_tt_dijet_loosemjj_boosted_2'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_loosemjj_boosted_2_DY_fracs',    'dy_tt_dijet_loosemjj_boosted_2'),

    (loc+'/ff_fracs_new_et.root:bin_dijet_tightmjj_lowboost_W_fracs',        'w_et_dijet_tightmjj_lowboost'),
    (loc+'/ff_fracs_new_et.root:bin_dijet_tightmjj_lowboost_TT_fracs',   'ttbar_et_dijet_tightmjj_lowboost'),
    (loc+'/ff_fracs_new_et.root:bin_dijet_tightmjj_lowboost_QCD_fracs',    'qcd_et_dijet_tightmjj_lowboost'),
    (loc+'/ff_fracs_new_mt.root:bin_dijet_tightmjj_lowboost_W_fracs',        'w_mt_dijet_tightmjj_lowboost'),
    (loc+'/ff_fracs_new_mt.root:bin_dijet_tightmjj_lowboost_TT_fracs',   'ttbar_mt_dijet_tightmjj_lowboost'),
    (loc+'/ff_fracs_new_mt.root:bin_dijet_tightmjj_lowboost_QCD_fracs',    'qcd_mt_dijet_tightmjj_lowboost'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_lowboost_1_W_fracs',      'w_tt_dijet_tightmjj_lowboost_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_lowboost_1_TT_fracs', 'ttbar_tt_dijet_tightmjj_lowboost_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_lowboost_1_QCD_fracs',  'qcd_tt_dijet_tightmjj_lowboost_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_lowboost_1_DY_fracs',    'dy_tt_dijet_tightmjj_lowboost_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_lowboost_2_W_fracs',      'w_tt_dijet_tightmjj_lowboost_2'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_lowboost_2_TT_fracs', 'ttbar_tt_dijet_tightmjj_lowboost_2'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_lowboost_2_QCD_fracs',  'qcd_tt_dijet_tightmjj_lowboost_2'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_lowboost_2_DY_fracs',    'dy_tt_dijet_tightmjj_lowboost_2'),

    (loc+'/ff_fracs_new_et.root:bin_dijet_tightmjj_boosted_W_fracs',        'w_et_dijet_tightmjj_boosted'),
    (loc+'/ff_fracs_new_et.root:bin_dijet_tightmjj_boosted_TT_fracs',   'ttbar_et_dijet_tightmjj_boosted'),
    (loc+'/ff_fracs_new_et.root:bin_dijet_tightmjj_boosted_QCD_fracs',    'qcd_et_dijet_tightmjj_boosted'),
    (loc+'/ff_fracs_new_mt.root:bin_dijet_tightmjj_boosted_W_fracs',        'w_mt_dijet_tightmjj_boosted'),
    (loc+'/ff_fracs_new_mt.root:bin_dijet_tightmjj_boosted_TT_fracs',   'ttbar_mt_dijet_tightmjj_boosted'),
    (loc+'/ff_fracs_new_mt.root:bin_dijet_tightmjj_boosted_QCD_fracs',    'qcd_mt_dijet_tightmjj_boosted'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_boosted_1_W_fracs',      'w_tt_dijet_tightmjj_boosted_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_boosted_1_TT_fracs', 'ttbar_tt_dijet_tightmjj_boosted_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_boosted_1_QCD_fracs',  'qcd_tt_dijet_tightmjj_boosted_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_boosted_1_DY_fracs',    'dy_tt_dijet_tightmjj_boosted_1'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_boosted_2_W_fracs',      'w_tt_dijet_tightmjj_boosted_2'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_boosted_2_TT_fracs', 'ttbar_tt_dijet_tightmjj_boosted_2'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_boosted_2_QCD_fracs',  'qcd_tt_dijet_tightmjj_boosted_2'),
    (loc+'/ff_fracs_new_tt.root:bin_dijet_tightmjj_boosted_2_DY_fracs',    'dy_tt_dijet_tightmjj_boosted_2')
]


for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['expr::abs_sjdphi("TMath::Abs(@0)",sjdphi[0])','m_sv'],
                          GetFromTFile(task[0]), name=task[1],incOF=True)

procs = ['w','qcd','ttbar']
for chan in ['mt','et']:
  for proc in procs:
    w.factory('expr::%s_%s_dijet_lowboost("(@0>300 && @0<=500)*@1 + (@0>500)*@2",mjj[0], %s_%s_dijet_loosemjj_lowboost, %s_%s_dijet_tightmjj_lowboost)' %(proc, chan, proc, chan, proc, chan))
    w.factory('expr::%s_%s_dijet_boosted("(@0>300 && @0<=500)*@1 + (@0>500)*@2",mjj[0], %s_%s_dijet_loosemjj_boosted, %s_%s_dijet_tightmjj_boosted)' %(proc, chan, proc, chan, proc, chan))

    w.factory('expr::%s_%s_dijet("(@0<150)*@1 + (@0>=150)*@2", pt_tt[0], %s_%s_dijet_lowboost, %s_%s_dijet_boosted)' % (proc, chan, proc, chan, proc, chan))

    w.factory('expr::%s_%s_fracs("(@0==0)*@2 + (@0==1 || (@0>1&&@1<=300))*@3 + (@0>1&&@1>=300)*@4", njets[0], mjj[0], %s_%s_0jet, %s_%s_boosted, %s_%s_dijet)' % (proc, chan, proc, chan, proc, chan, proc, chan))

procs= ['w','qcd','ttbar','dy']
chan='tt'
for proc in procs:
    w.factory('expr::%s_%s_dijet_lowboost_1("(@0>300 && @0<=500)*@1 + (@0>500)*@2",mjj[0], %s_%s_dijet_loosemjj_lowboost_1, %s_%s_dijet_tightmjj_lowboost_1)' %(proc, chan, proc, chan, proc, chan))
    w.factory('expr::%s_%s_dijet_boosted_1("(@0>300 && @0<=500)*@1 + (@0>500)*@2",mjj[0], %s_%s_dijet_loosemjj_boosted_1, %s_%s_dijet_tightmjj_boosted_1)' %(proc, chan, proc, chan, proc, chan))

    w.factory('expr::%s_%s_dijet_1("(@0<150)*@1 + (@0>=150)*@2", pt_tt[0], %s_%s_dijet_lowboost_1, %s_%s_dijet_boosted_1)' % (proc, chan, proc, chan, proc, chan))

    w.factory('expr::%s_%s_fracs_1("(@0==0)*@2 + (@0==1 || (@0>1&&@1<=300))*@3 + (@0>1&&@1>=300)*@4", njets[0], mjj[0], %s_%s_0jet_1, %s_%s_boosted_1, %s_%s_dijet_1)' % (proc, chan, proc, chan, proc, chan, proc, chan))

    w.factory('expr::%s_%s_dijet_lowboost_2("(@0>300 && @0<=500)*@1 + (@0>500)*@2",mjj[0], %s_%s_dijet_loosemjj_lowboost_2, %s_%s_dijet_tightmjj_lowboost_2)' %(proc, chan, proc, chan, proc, chan))
    w.factory('expr::%s_%s_dijet_boosted_2("(@0>300 && @0<=500)*@1 + (@0>500)*@2",mjj[0], %s_%s_dijet_loosemjj_boosted_2, %s_%s_dijet_tightmjj_boosted_2)' %(proc, chan, proc, chan, proc, chan))

    w.factory('expr::%s_%s_dijet_2("(@0<150)*@1 + (@0>=150)*@2", pt_tt[0], %s_%s_dijet_lowboost_2, %s_%s_dijet_boosted_2)' % (proc, chan, proc, chan, proc, chan))

    w.factory('expr::%s_%s_fracs_2("(@0==0)*@2 + (@0==1 || (@0>1&&@1<=300))*@3 + (@0>1&&@1>=300)*@4", njets[0], mjj[0], %s_%s_0jet_2, %s_%s_boosted_2, %s_%s_dijet_2)' % (proc, chan, proc, chan, proc, chan, proc, chan))


w.writeToFile('ff_fracs_new_2016.root')
w.Delete()
