'''
Created on May 4, 2013

@author: Kun
'''
from allData import *
import collections
import matplotlib as mpl
import scipy as sp
import json
import os
import matplotlib
import random as rnd
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime


def getFeatDistr(ar, featIdx):
    return collections.Counter(ar[:, featIdx].astype(int))


def randomSelect(cfgfile=None):
    inpufile = None
    outputfile = None
    selectedFeats = None
    selectedVals = None
    featOfDist = None
    selCondition = False
    ourdir = '.'
    if cfgfile is not None:
        f = open(cfgfile)
        cfg = json.load(f)
        print cfg
        inputfile = cfg['indir']+'/'+cfg['infile']
        selectedFeats = cfg['selected_feats']
        selectedVals = cfg['selected_vals']
        featOfDist = cfg['key_feat']
        outdir = cfg['outdir']
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        pass
    allfeats, data = readcsvfile(inputfile)
    selFeatIdxes = [allfeats.index(i) for i in selectedFeats]
    data = selectRowsByVal(data, selFeatIdxes[0], str(selectedVals[0]))
    selectedData = selectRowsByMultiVal(data, selFeatIdxes, selectedVals)
    print len(data), len(selectedData)
    #sp.array([data[i] for i in xrange(len(data)) if data[i][selFeatIdxes[0]]==str(selectedVals[0])])
    for it in xrange(len(featOfDist)):
        idx = allfeats.index(featOfDist[it])
        randCounts = getFeatDistr(data, idx)
        randX = [x for x in randCounts]
        randX.sort()
        randYtmp = list([randCounts[x] for x in randX])
        selCounts = getFeatDistr(selectedData, idx)
        selX = [x for x in selCounts]
        selX.sort()
        selYtmp = list([selCounts[x] for x in selX])
        xaxis = xrange(randX[0], randX[-1]+1)
        selY = sp.zeros(len(xaxis))
        randY = sp.zeros(len(xaxis))
        for x in xrange(len(selX)):
            selY[selX[x]-xaxis[0]] = selYtmp[x]
        for x in xrange(len(randX)):
            randY[randX[x]-xaxis[0]] = randYtmp[x]
        #yaxis = [counts[x] for x in xaxis]
        plt.figure(it)
        plt.xlabel(featOfDist[it])
        plt.ylabel('distribution')
        plt.plot(xaxis, selY/selY.sum(), 'r--', label='with pref')
        plt.plot(xaxis, randY/randY.sum(), 'b-', label='random selection')
        plt.legend()
        plt.savefig(outdir+'/'+featOfDist[it]+'.png')
    plt.show()
    #print os.getcwd()
#randomSelect('../../data/randsel.json')


def getMarRplRate(cfgfile=None):
    inpufile = None
    outputfile = None
    selectedFeats = None
    selectedVals = None
    featOfDist = None
    selCondition = False
    ourdir = '.'
    if cfgfile is not None:
        f = open(cfgfile)
        cfg = json.load(f)
        print cfg
        inputfile = cfg['indir']+'/'+cfg['infile']
        selectedFeats = cfg['selected_feats']
        selectedVals = cfg['selected_vals']
        featOfDist = cfg['key_feat']
        outdir = cfg['outdir']
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        pass
    allfeats, data = readcsvfile(inputfile)
    selFeatIdxes = [allfeats.index(i) for i in selectedFeats]
    data = selectRowsByVal(data, selFeatIdxes[0], str(selectedVals[0]))
    selectedData = selectRowsByMultiVal(data, selFeatIdxes, selectedVals)
    print len(data), len(selectedData)
    # do sampling with reply probability, sample n times and use average
    N = 5
    sampleIdxes = {}
    sampleSet = set(xrange(len(data)))
    for x in xrange(N):
        sampleIdxes[x] = rnd.sample(sampleSet, len(selectedData))
    #sp.array([data[i] for i in xrange(len(data)) if data[i][selFeatIdxes[0]]==str(selectedVals[0])])
    for it in xrange(len(featOfDist)):
        idx = allfeats.index(featOfDist[it])
        totalCounts = getFeatDistr(data, idx)
        totalX = [x for x in totalCounts]
        totalX.sort()
        xaxis = xrange(totalX[0], totalX[-1]+1)
        # for random sender
        sampleCounts = getFeatDistr(data[sampleIdxes[0]], idx)
        for x in xrange(1, N):
            sampleCounts += getFeatDistr(data[sampleIdxes[x]], idx)
        samX = [x for x in sampleCounts]
        samX.sort()
        samY = sp.zeros(len(xaxis))
        for x in xrange(len(samX)):
            samY[samX[x]-xaxis[0]] = float(sampleCounts[samX[x]])/totalCounts[samX[x]]
        # for selected sender
        samY /= N
        selCounts = getFeatDistr(selectedData, idx)
        selX = [x for x in selCounts]
        selX.sort()
        print featOfDist[it], '-selcounts:', selCounts
        print 'sampleCounts:', sampleCounts
        selY = sp.zeros(len(xaxis))
        for x in xrange(len(selX)):
            selY[selX[x]-xaxis[0]] = float(selCounts[selX[x]])/totalCounts[selX[x]]
        plt.figure(it)
        plt.xlabel(featOfDist[it])
        plt.ylabel('distribution')
        plt.plot(xaxis, selY, 'r--', label='with pref')
        # plt.plot(xaxis, samY, 'b-', label='random selection')
        plt.bar(xaxis, samY, color='r', yerr='reply Probability')
        plt.bar(xaxis, 1-samY, color='y', bottom=samY, yerr='reject Probability')
        plt.legend()
        plt.savefig(outdir+'/'+featOfDist[it]+'.png')
    plt.show()
#getMarRplRate("../../data/exp/randsel.json")


def test1(cfgfile=None):
    inpufile = None
    outputfile = None
    selectedFeats = None
    selectedVals = None
    featOfDist = None
    selCondition = False
    ourdir = '.'
    if cfgfile is not None:
        f = open(cfgfile)
        cfg = json.load(f)
        print cfg
        inputfile = cfg['indir']+'/'+cfg['infile']
        selectedFeats = cfg['selected_feats']
        selectedVals = cfg['selected_vals']
        featOfDist = cfg['key_feat']
        outdir = cfg['outdir']
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        pass
    allfeats, data = readcsvfile(inputfile)
    selFeatIdxes = [allfeats.index(i) for i in selectedFeats]
    data = selectRowsByVal(data, selFeatIdxes[0], str(selectedVals[0]))
    checkcor = [data[x] for x in xrange(len(data)) if data[x][allfeats.index('sAnimalSign')]== str(0)]
    print checkcor




def getTimePro(cfgfile=None):
    data = None
    timeFeats = None
    regtime = None
    logtime = None
    sendtime = None
    pass  # cfg here
    seldata = None    
    for row in xrange(len(data)):
        for col in xrange(len(timeFeats)):
            seldata[row][col] = datetime.strptime(seldata[row][col], '%Y-%m-%d %H:%M:%S')