'''
Created on May 4, 2013

@author: Kun
'''
from allData import *
import collections
import matplotlib as mpl
import scipy as sp
import json
import matplotlib.pyplot as plt
#import os

def getFeatDistr(ar, featIdx):
    return collections.Counter(ar[:,featIdx].astype(int))

def randomSelect(cfgfile=None):
    inpufile = None
    outputfile = None
    selectedFeats = None
    selectedVals = None
    featOfDist = None
    selCondition = False
    if cfgfile is not None:
        f = open(cfgfile)
        cfg = json.load(f)
        print cfg
        inputfile = cfg['indir']+'/'+cfg['infile']
        selectedFeats = cfg['selected_feats']
        selectedVals = cfg['selected_vals']
        featOfDist = cfg['key_feat']
        pass
    allfeats, data = readcsvfile(inputfile)    
    selFeatIdxes = [allfeats.index(i) for i in selectedFeats]
    data = selectRowsByVal(data,selFeatIdxes[0],str(selectedVals[0]))
    selectedData = selectRowsByMultiVal(data,selFeatIdxes,selectedVals)
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
        xaxis = xrange(randX[0],randX[-1]+1)
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
        plt.plot(xaxis, randY/randY.sum(),'b-', label='random selection')
        plt.legend()
    plt.show()
    #print os.getcwd()
randomSelect('../../data/randsel.json')