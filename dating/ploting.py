import numpy
import csv
#import pylab
from replyData import *
from senderData import *

#function to build up plotting from the sting
def getPreFromString(num,string):
    typeArray = []
    preference = []
    split=[]
    preStr = string.split(' ');
    for i in xrange(num):
        split = preStr[i].split(':')
        typeArray.append(split[0])
        preference.append(float(split[1]))
    return typeArray,preference

#read file and get array
sendPre = get_senderPreference()
repPre = get_repPre()

comPre = {}
for rp in repPre:
    if rp in sendPre:
        comPre[rp] = {}
        print rp, ':'
        for rp_target in repPre[rp]:
            if rp_target in sendPre[rp]:
                comPre[rp][rp_target] = {'recPre':repPre[rp][rp_target],'sendPre':sendPre[rp][rp_target]}
                print '\t'+comPre[rp][rp_target]