import numpy
import csv
from collections import Counter
features = []


def getStrFeatVal(arraydata, featureArray, subfeat):
	"""
	arraydata: numpy array of the data
	featureArray: string array of all the features for the arraydata
	subfeat: string array of part of the features in the arraydata
	"""
	featIdx = [featureArray.index(x) for x in subfeat]
	tmpArray = list(arraydata[:, featIdx])
	return ['-'.join(x) for x in tmpArray]

with open("./test.csv") as f:
	csvfile = csv.DictReader(f, dialect='excel', delimiter='\t')
	for row in csvfile:
		print row['a']


class GrowingHash(object):
	def __init__(self):
		self._mapping = {}
		self._reverse = {}
		self._growth = True
		self._idx = 0

	def __getitem__(self, s):
		try:
			return self._mapping[s]
		except KeyError:
			if not isinstance(s, basestring):
				raise ValueError('%s must be a basestring' % (s,))
			if not self._growth:
				return None
			self._mapping[s] = self._idx
			self._reverse[self._idx] = s
			self._idx += 1
			return self._mapping[s]

	def freeze(self):
		self._growth = False


