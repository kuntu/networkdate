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
"""
# change features to string for sender and receiver
scorpus = list(mycsv[:, sfeatIdx])
sStrVal = ['-'.join(x) for x in scorpus]

rcorpus = list(mycsv[:, rfeatIdx])
rStrVal = ['_'.join(x) for x in rcorpus]
sdistance = sfeature+['distance']
#getStrFeatVal(mycsv,features,sdistance)
"""
def countCommu(dataarray, feats, sfeats, rfeats):
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
"""
sids = getStrFeatVal(mycsv,features,['sender','receiver'])
countSID = Counter(sids)
print countSID
singsid = [x for x in countSID]
sidCounts = [countSID[x] for x in singsid]
"""
cc = countCommu(mycsv, features, sfeature, rfeature)
keys = [x for x in cc]
for i in xrange(1):
	print keys[i], cc[keys[i]]
	
with open('data.csv','wb') as csvfile:
	for x in cc:
		row = x+'\t'+cc[x]['group']+'\t'
		for i in cc[x]['rec']:
			row = row + (cc[x]['rec'][i]['group']+' ')*cc[x]['rec'][i]['count']
		csvfile.write(row+'\n')
	
