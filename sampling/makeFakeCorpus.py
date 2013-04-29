from allData import *

featsforWords = [ 'age', 'Height', 'weight', 'Gender', 'type']
sFeatWord = ['s'+x for x in featsforWords]
rFeatWord = ['r'+x for x in featsforWords]
allfeats, data = readcsvfile('../../data/fakeMsg.csv')
print allfeats
selected = list(set(sFeatWord) | set(rFeatWord))
selected.sort()
selected.insert(len(rFeatWord), 'sender')
selected.insert(0, 'receiver')
selected.append('Reply')
data = subMatrix(data, allfeats, selected)
data = preprocessDataValue(data, selected, ['sage', 'sHeight', 'rage', \
	'rHeight'],	[5, 5, 5, 5], [0, 100, 0, 100])
dataToCopus(data, selected, sFeatWord, rFeatWord, '../../data/fakeCorpus.csv')
print selected, '\n', data[0]
