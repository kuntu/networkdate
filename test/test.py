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

with open("./test.csv") as f:
	csvfile = csv.DictReader(f,dialect='excel', delimiter='\t')
	for row in csvfile:
		print row['a']