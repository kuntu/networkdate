from allData import *
import json
def makeCorpus(config=None):
	featsforWords = None
	sFeatWord = None
	rFeatWord = None
	mod_feats = None
	mod_fMin = None
	mod_fIntv = None
	infile = None
	outfile=None
	if config is None:
		featsforWords = ['age', 'Height', 'weight', 'Gender']
		sFeatWord = ['s'+x for x in featsforWords]
		rFeatWord = ['r'+x for x in featsforWords]
		mod_feats = ['sage', 'sHeight', 'sweight', 'rage', 'rHeight', 'rweight']
		mod_fIntv = [5, 5, 5, 5, 5, 5]
		mod_fMin = [0, 100, 0, 0, 100, 0]
		outfile = '../../data/fakeCorpus.csv'
		infile = '../../data/fakeMsg.csv'
		pass
	else:
		with open(config) as f:
			#f.seek(0)
			cfg = json.load(f)
			sFeatWord = cfg['sfeats']
			rFeatWord = cfg['tfeats']
			mod_feats = [name for name in cfg['feat_mod']]
			mod_fIntv = [cfg['feat_mod'][x][0] for x in cfg['feat_mod']]
			mod_fMin = [cfg['feat_mod'][x][0] for x in cfg['feat_mod']]
			outfile = cfg['outputfile']
			infile = cfg['inputfile']
		pass
	allfeats, data = readcsvfile(infile)
	selected = list(set(sFeatWord) | set(rFeatWord))
	selected.sort()
	selected.insert(len(rFeatWord), 'sender')
	selected.insert(0, 'receiver')
	selected.append('Reply')
	data = subMatrix(data, allfeats, selected)
	data = preprocessDataValue(data, selected, mod_feats, mod_fIntv, mod_fMin)
	dataToCopus(data, selected, sFeatWord, rFeatWord, outfile)
	print selected, '\n', data[0]

makeCorpus('../../data/config.json')


def testData():
	allfeats, data = readcsvfile('../../data/fakeMsg.csv')
	print data[0]
	pref = {}
	stypeIdx = allfeats.index('stype')
	rtypeIdx = allfeats.index('rtype')
	for x in data:
		if x[stypeIdx] not in pref:
			pref[x[stypeIdx]] = {}
		if x[rtypeIdx] in pref[x[stypeIdx]]:
			pref[x[stypeIdx]][x[rtypeIdx]] += 1
		else:
			pref[x[stypeIdx]][x[rtypeIdx]] = 1
	print pref
	pass


#testData()
