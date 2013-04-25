import numpy as np
import scipy as sp
import random as rnd

def sample(dist, samplesize=1):
	"""
	sameple from the distribution
	"""
	cdf = np.cumsum(dist)
	r = sp.random.uniform(size=samplesize) * cdf[-1]
	return cdf.searchsorted(r)


def log_sample(log_dist, samplesize=1):
	return sample(np.exp(log_dist - log_dist.max()), samplesize)


def generateFake(configFile=None):
	"""
	generate 3 user type and type 3 has 10,000 messages.
	user type 1 2 should have similar messages.
	decisiion tree --- age height and weight
		|---------- age > 40 ----heigth > 180 ---- weight > 90 === type 1
					|			|					|-weight in [50, 90] ==type 2
					|			|					|-weight <50  === type 3
					|			|---height < 180 ---- weight >90 ===type 3
					|			|					|-weight <90 === type 2
					|-- age <40 ----height > 180 ---- weight > 90 ===type 1
								|					|-weight <90 === type 2
								|---height < 180 ---- weight > 90 === type 3
													|-weight <90 === type 1
	"""
	userInfo = {}
	male = {}
	female = {}
	for x in xrange(1, 4):
		male[x] = []
		female[x] = []
	for x in xrange(200):  # create users with types
		userInfo[x] = []
		userInfo[x].append(rnd.randint(18, 60))
		userInfo[x].append(rnd.randint(150, 190))
		userInfo[x].append(rnd.randint(40, 120))
		userInfo[x].append(rnd.randint(0, 1))
		userInfo[x].append(classifyuser(userInfo[x]))
		print userInfo[x][4]
		if userInfo[x][3] == 0:
			male[userInfo[x][4]].append(x)
		else:
			female[userInfo[x][4]].append(x)
		pass  # random create age height and weight fror each user and classi
	prefs = []  # initial the user preferences
	for x in xrange(3):
		prefs.append(sp.random.uniform(size=3))
	with open('../../data/fakePref.txt', 'wb') as prefFile:
		for x in prefs:
			prefFile.write('\t'.join(x.astype('|S7'))+'\n')  # '|Sx'--dtype: x is the length
	# assign user type here
	alluser = set(xrange(100))
	usergroup = []
	for x in xrange(3-1):
		tmp = rnd.sample(alluser, rnd.randint(1, len(alluser)/2))
		usergroup.append(tmp)
		alluser = alluser - set(tmp)
	usergroup.append(list(alluser))
	# generate messages
	with open('../../data/fakeMsg.csv', 'wb') as fakefile:
		fakefile.write('sender\tsage\tsHeight\sweight\tstype\tsGender\treceiver\trage\trHeight\trweight\trtype\trGender\treply')
		for t in xrange(1, 3):
			for x in xrange(len(male[t])):
				sender = '\t'.join(userInfo[male[t][x]])
				msgNum = rnd.randint(0, len(female[1])/2)  # might use power law distribution
				targettypes = sample(prefs[t], msgNum)
				pass  # find the method to get a set like random idx
				tempset = {}
				for idx in xrange(len(female)):
					tempset[idx] = set(female[idx])
				for y in xrange(len(targettypes)):
					receiver = '\t'.join(userInfo[female[y]])
					fakefile.write(str(x)+'\t'+sender+'\t'+receiver+'\t'+str(rnd.randint(0, 1)))
					pass
				pass
	print len(female[1])


def classifyuser(user):
	if user[0] > 40:
		if user[1] > 180:
			if user[2] > 90:
				return (1)
			elif user[2] > 50:
				return (2)
			else:
				return (3)
		if user[1] < 180:
			if user[2] > 90:
				return (3)
			else:
				return (2)
	else:
		if user[1] > 180:
			if user[2] > 90:
				return (1)
			else:
				return (2)
		if user[1] < 180:
			if user[2] > 90:
				return (3)
			else:
				return (1)

#please prepare a config file to run experiments
generateFake()