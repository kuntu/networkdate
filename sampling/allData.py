
import numpy as np
import csv


def readcsvfile(filename):
	with open(filename, 'rb') as f:
		mycsv = list(csv.reader(f))
		feature = [x for x in mycsv[0]]
		#data = np.array(mycsv[1:])
		return feature, np.array(mycsv[1:])


def getFeaFrq(allFeat, feat, dataDrray):
	idx = allFeat.index(feat)
	freq = {}
	for row in dataDrray:
		if not row[idx] in freq:
			freq[row[idx]] = 1
		freq[row[idx]] += 1
	return freq


def dataToCopus(file, sfeat, rfeat, newcsvfile):
	with open(file, 'rb') as f:
		rawdata = csv.reader(f)
		rawdata = list(rawdata)
		feat = [x for x in rawdata[0]]
		arraydata = np.array(rawdata[1:])
		with open(newcsvfile, 'wb') as outfile:
			sfidx = [feat.index(x) for x in sfeat]
			rfidx = [feat.index(x) for x in rfeat]
			outData = {}
			for row in arraydata:
				sender = '_'.join(list(row[sfidx]))
				if not sender in outData:
					outData[sender] = sender+'\t'
				receiver = '_'.join(list(row[rfidx]))
				outData[sender] = ' '.join([outData[sender], receiver])
			for key in outData:
				outfile.write(outData[key]+'\n')


dataToCopus('../../data/receiveMsg.csv',['sender','sage'], ['receiver','rage'], '../../data/testout.txt')
