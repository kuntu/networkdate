import numpy
import csv
import pylab
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
repPre = get_repPre()
sendPre = get_senderPreference()
