import numpy
import csv
import operator
from datafeature import * #self defined class
from collections import Counter


def getStrFeatVal(arraydata, featureArray,subfeat):
	"""
	arraydata: numpy array of the data
	featureArray: string array of all the features for the arraydata
	subfeat: string array of part of the features in the arraydata
	"""
	featIdx = [featureArray.index(x) for x in subfeat]
	tmpArray = list(arraydata[:, featIdx])
	return ['-'.join(x) for x in tmpArray]





def createFeatures(fNameArray, valueInterval=None, valueMin = None):
	"""
	create an array of DataFeature objects
	"""
	features = []
	if valueInterval is None:
		features = [DataFeature(x) for x in fNameArray]
	else:
		if valueMin is None:
			valueMin = [0 for x in fNameArray]
		
		for i in xrange(len(fNameArray)):
			print i, len(fNameArray), len(valueMin), len(valueInterval)
			features.append( DataFeature(fNameArray[i],valueMin[i],valueInterval[i]))
	return features

def preprocessDataValue(dataarray,allFeatNameArray, modiFeat):
	"""
	This function modify the values of features-column in the dataarray, e.g. the age 18 could be mapped
	 to type 1, age 24 mapped to type 2 ...
	 
	dataarray: multi-dimestion array data
	allFeatNameArray: a string array containing the names of all features
	modiFeat: a DataFeature-object array, each element in the array
	"""
	newData = None
	for x in modiFeat:
		idx = allFeatNameArray.index(x.name)		
		dataarray[:, idx] = (dataarray[:, idx].astype(int) - x.minVal)/x.intv
	return dataarray


def countCommu(dataarray, feats, sfeats, rfeats):
	"""
	refine data
	1.for each sender, has such following structure:
		sgroup={ #type of the person who receive a message,  
		
				sender1Type={
					accept: # message reply to the sender who has sender1Type
					reject: # message didn't reply}
			}
	"""
	#use dictionary {}, similar to js object
	commu = {}
	#in the reply, receiver is viewed as sender:
	sfeaIdx = [feats.index(x) for x in sfeats]
	rfeaIdx = [feats.index(x) for x in rfeats]
	repIdx = feats.index("Reply")
	for i in xrange(len(dataarray)):
		sgroup = '_'.join(list(dataarray[i][sfeaIdx]))
		if not sgroup in commu:
			commu[sgroup] ={}
		rgroup = '_'.join(list(dataarray[i][rfeaIdx]))		
		if not rgroup in commu[sgroup]:			
			commu[sgroup][rgroup]={'accept':0.001,'reject':0.001}
			#commu[sid]['rec'][rid]['rpl'] = 0
		if dataarray[i][repIdx]=='0':
			commu[sgroup][rgroup]['reject'] +=1
		else:
			commu[sgroup][rgroup]['accept'] +=1
	return commu

features = []
with open('../../data/sendMsg.txt', 'rb') as f:
	mycsv = csv.reader(f)
	mycsv = list(mycsv)
	features = [x for x in mycsv[0]]

"""
sids = getStrFeatVal(mycsv,features,['sender','receiver'])
countSID = Counter(sids)
print countSID
singsid = [x for x in countSID]
sidCounts = [countSID[x] for x in singsid]
"""

"""
set up features here
"""
mainfeature = ["age","Weight","Height","PhotoCnt","AnimalSign","NewIncome"]
sfeature = ['s'+x for x in mainfeature]
#rfeature = ['r'+x for x in mainfeature]
rfeature = ["rPhotoCnt","rage","rNewIncome","rWeight"]
sfeatIdx = [features.index(x) for x in sfeature]
rfeatIdx = [features.index(x) for x in rfeature]
#alternative way to set up feature by setting feature value

"""
organize data here
"""
mycsv = numpy.array(mycsv[1:])
#aggregate values
mycsv = preprocessDataValue(mycsv, features,\
						 createFeatures(["rage", "rWeight", "rHeight", "sage", \
										"sWeight"],\
									 [5,10,5,5,10]))
#mycsv = preprocessDataValue(mycsv, features,\
#						createFeatures(['rWeight','rHeight','sWeight'], [10,5,10]))

cc = countCommu(mycsv, features, sfeature, rfeature)
keys = [x for x in cc]
sorting = {}
for i in xrange(len(keys)):
	sorting[keys[i]] = len(cc[keys[i]])

sortedkey = sorted(sorting.iteritems(),key = operator.itemgetter(1),reverse=True)
order = [x[0] for x in sortedkey]
for i in xrange(10):
	#sorting[keys[i]]=len(cc[keys[i]])
	print order[i],':'
	for j in cc[order[i]]:
		print '\t', j,':', cc[order[i]][j]['accept']/(cc[order[i]][j]['accept']+cc[order[i]][j]['reject'])
		
	#print keys[i], cc[keys[i]]
	pass
"""
with open('replydata.csv','wb') as csvfile:
	for x in cc:
		row = x+'\t'+cc[x]['group']
		for i in cc[x]['rec']:
			row = row +' '+ cc[x]['rec'][i]['group']+':'+("%.4f" % \
			(cc[x]['rec'][i]['accept']/(cc[x]['rec'][i]['accept']+cc[x]['rec'][i]['reject'])))
		csvfile.write(row+'\n')
"""

with open('senderFreq.csv','wb') as csvfile:
	for i in xrange(len(order)):
		row = order[i]+'\t'+str(len(cc[order[i]]))+'\t'
		for j in cc[order[i]]:
			row +=j+':'+('%.5f' % (cc[order[i]][j]['accept']/(cc[order[i]][j]['accept']+cc[order[i]][j]['reject'])))+' '
		#print row
		csvfile.write(row+'\n')
print 'done'
				

