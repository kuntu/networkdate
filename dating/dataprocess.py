
class DataProcess(object):
	def __init__(self):
		pass
		self._mapping = {} # mapping feature strings to  integer
		self._reverse = {} # mapping integer to ferture strings
		self._idx = 0
		self._growing = True

	def __getitem__(self, s):
		try:
			return self._mapping[s];
		except KeyError :
			if not isinstance(s,basestring):				
				raise ValueError("Invalid (%s): must be a valid string ", % (s))
		pass