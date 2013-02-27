import numpy
import csv
import pylab
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
data=[]
with open('./replyFreq.csv', 'rb') as f:
    data = csv.reader(f)
    data = list(data)
#process the 3rd element and split them into type:
print data[0]