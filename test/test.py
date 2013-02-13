import numpy
import csv
from collections import Counter
features = []

def getStrFeatVal(arraydata, featureArray,subfeat):
	"""
	arraydata: numpy array of the data
	featureArray: string array of all the features for the arraydata
	subfeat: string array of part of the features in the arraydata
	"""
	featIdx = [featureArray.index(x) for x in subfeat]
	tmpArray = list(arraydata[:, featIdx])
	return ['-'.join(x) for x in tmpArray]

def function():
	pass

with open('../../data/UNI_to_WHOLE.csv', 'rb') as f:
	mycsv = csv.reader(f)
	mycsv = list(mycsv)
	features = [x for x in mycsv[0]]

print len(mycsv)
mainfeature = ["age","Weight","Height","PhotoCnt","AnimalSign","NewIncome"]
sfeature = ['s'+x for x in mainfeature]
rfeature = ['r'+x for x in mainfeature]

sfeatIdx = [features.index(x) for x in sfeature]
rfeatIdx = [features.index(x) for x in rfeature]

mycsv = numpy.array(mycsv[1:])

scorpus = list(mycsv[:, sfeatIdx])
sStrVal = ['-'.join(x) for x in scorpus]

rcorpus = list(mycsv[:, rfeatIdx])
rStrVal = ['_'.join(x) for x in rcorpus]
sdistance = sfeature+['distance']
#getStrFeatVal(mycsv,features,sdistance)

def countCommu(dataarray, feats, sfeats, rfeats):
	#use dictionary {}, similar to js object
	commu = {}
	sidx = feats.index('sender')
	ridx = feats.index('receiver')
	for i in xrange(len(dataarray)):
		sid = dataarray[i][sidx]
		rid = dataarray[i][ridx]
		#cannot use if commu[sid] as js. need to use 'in' to check the key
		if not sid in commu:
			commu[sid] ={}
		if not rid in commu[sid]:
			commu[sid][rid]={count:0}
		commu[sid][rid][count] +=1
	return commu

sids = getStrFeatVal(mycsv,features,['sender','receiver'])
countSID = Counter(sids)
print countSID
singsid = [x for x in countSID]
sidCounts = [countSID[x] for x in singsid]
