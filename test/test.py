import numpy
import csv
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

with open('dating_small.csv', 'rb') as f:
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
print getStrFeatVal(mycsv,features,sfeature.extend(['distance']))


