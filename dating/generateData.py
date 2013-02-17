import numpy
import csv
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
		senderID, 
		groupe=senderType, 
		rec={
				receiver1ID={
					count: # message from sender
					group: receiver Type}
			}
	"""
	#use dictionary {}, similar to js object
	commu = {}
	doc_group = {}
	sidx = feats.index('sender')
	ridx = feats.index('receiver')
	sfeaIdx = [feats.index(x) for x in sfeats]
	rfeaIdx = [feats.index(x) for x in rfeats]	
	for i in xrange(len(dataarray)):
		sid = dataarray[i][sidx]
		rid = dataarray[i][ridx]
		#cannot use if commu[sid] as js. need to use 'in' to check the key
		if not sid in commu:
			commu[sid] ={'rec':{}}
			commu[sid]['group'] = '_'.join(list(dataarray[i][sfeaIdx]))
		"""
		if not rid in commu:
			commu[rid] ={'rec':{}}
			commu[rid]['group'] = '_'.join(list(dataarray[i][rfeaIdx]))
		"""
		if not rid in commu[sid]['rec']:
			commu[sid]['rec'][rid]={'count':0}
			commu[sid]['rec'][rid]['group'] = '_'.join(list(dataarray[i][rfeaIdx]))
			#commu[sid]['rec'][rid]['rpl'] = 0
		commu[sid]['rec'][rid]['count'] +=1
	return commu

features = []
with open('../../data/UNI_to_WHOLE.csv', 'rb') as f:
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

mycsv = numpy.array(mycsv[1:])

mycsv = preprocessDataValue(mycsv, features,\
						 createFeatures(["sage", "sWeight", "sHeight", "rage", \
										"rWeight"],\
									 [5,10,5,5,10]))
									 
#print mycsv[1:200,features.index("sWeight")]
cc = countCommu(mycsv, features, sfeature, rfeature)
keys = [x for x in cc]
for i in xrange(10):
	print keys[i], cc[keys[i]]

with open('newdata.csv','wb') as csvfile:
	for x in cc:
		row = x+'\t'+cc[x]['group']+'\t'
		for i in cc[x]['rec']:
			row = row + (cc[x]['rec'][i]['group']+' ')*cc[x]['rec'][i]['count']
		csvfile.write(row+'\n')

def generateCSVData(infile, outfile,givenFields, predictFields,allfields=None):
	"""
	generate csv
	"""