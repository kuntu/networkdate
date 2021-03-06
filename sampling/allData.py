
import numpy as np
import csv


def readcsvfile(filename):
	"""
	read a csv file and return the fieldname and matrix
	filename: the filename
	"""
	with open(filename, 'rb') as f:
		mycsv = list(csv.reader(f))
		feature = [x for x in mycsv[0]]
		#data = np.array(mycsv[1:])
		return feature, np.array(mycsv[1:])


def getFeaFrq(allFeat, feat, dataDrray):
	"""
	get the frequency of each value of a single feature.
	allFeat: the fieldnames of the dataToCopus
	feat: the name of the feature whose value frequency is to count
	"""
	idx = allFeat.index(feat)
	freq = {}
	for row in dataDrray:
		if not row[idx] in freq:
			freq[row[idx]] = 1
		freq[row[idx]] += 1
	return freq


def getStrFeatVal(arraydata, featureArray, subfeat):
	tmpArray = list(subMatrix(arraydata, featureArray, subfeat))
	return ['-'.join(x) for x in tmpArray]


def subMatrix(arraydata, allFeat, subfeat):
	"""
	arraydata: numpy array of the data
	featureArray: string array of all the features for the arraydata
	subfeat: string array of part of the features in the arraydata
	"""
	featIdx = [allFeat.index(x) for x in subfeat]
	return arraydata[:, featIdx]


def getPercentSample(percent, len):
	"""
	return an list store the idx of sampled row with a probability
	equal to 'percent'
	"""
	sampList = []
	for x in xrange(len):
		if np.random() < percent:
			sampList.append(x)
	return sampList


def dataToCopus(arraydata, feat, sfeat, rfeat, newcsvfile):
	"""
	"""
	with open(newcsvfile, 'wb') as outfile:
		sfidx = [feat.index(x) for x in sfeat]
		rfidx = [feat.index(x) for x in rfeat]
		outData = {}
		typeCount = {}
		senderID = {}
		for row in arraydata:
			sender = '_'.join(list(row[sfidx]))
			sendername = row[feat.index('sender')]
			if not sender in outData:
				outData[sender] = sender+'\t'
				typeCount[sender] = 1
				senderID[sendername] = 1
			elif not sendername in senderID:
				senderID[sendername] = 1
				typeCount[sender] += 1
			receiver = '_'.join(list(row[rfidx]))
			outData[sender] = ' '.join([outData[sender], receiver])
		keys = [x for x in outData]
		keys.sort()
		with open(newcsvfile+'.csv', 'wb') as outfile_count:
			for key in keys:
				outfile.write(outData[key]+'\n')
				outfile_count.write(key+'\t'+str(typeCount[key])+'\t'+str(typeCount[key])+'\n')


def preprocessDataValue(dataarray, allFeatNameArray, modiFeatName, intervals, minVals):
	"""
	This function modify the values of features-column in the dataarray,
	e.g. the age 18 could be mapped	 to type 1, age 24 mapped to type 2 ...
	dataarray: multi-dimestion array data
	allFeatNameArray: a string array containing the names of all features
	modiFeatName: a array of fieldnames to modify
	intervals: an array of intervals for the modiFeatures.
	minVals: for the fields
	"""
	for i in xrange(len(modiFeatName)):
		idx = allFeatNameArray.index(modiFeatName[i])
		dataarray[:, idx] = (dataarray[:, idx].astype(int) - minVals[i])/intervals[i]
	return dataarray


def selectRowsByVal(dataArray, featIdx, val):
    return np.array([dataArray[i] for i in xrange(len(dataArray)) if dataArray[i][featIdx] == val])
   

def isRowMatchVals(row, idxes, vals):
	ar = row[idxes]==np.array(vals).astype(str)
	return ar.all()


def selectRowsByMultiVal(dataArray,featIdxes, vals):
	return np.array([dataArray[i] for i in xrange(len(dataArray)) if isRowMatchVals(dataArray[i], featIdxes, vals)])
#dataToCopus('../../data/receiveMsg.csv',['sender','sage'], ['receiver','rage'], '../../data/testout.txt')
#age height education city photocnt income career house lovetype
