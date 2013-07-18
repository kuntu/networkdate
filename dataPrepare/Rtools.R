psmX = c("sage",  "sHeight", "sWeight", "sBodyType", "sBloodType", "sNewOccupation", "sAnimalSign",  "sNewDegree", "sNewIncome", "sNewHousing", "sMarriage",  "sPhysicalLooking", "sLoveType",  "sNewCar", "sPhotoCnt", "rage",  "rHeight", "rWeight", "rBodyType", "rBloodType", "rNewOccupation", "rAnimalSign", "rAstrology",  "rNewDegree", "rNewIncome", "rNewHousing", "rMarriage", "rHaveChildren", "rPhysicalLooking", "rNewCar", "rNewProfessional",   "rPhotoCnt",  "distance", "AgeFit", "HeightFit", "IncomeFit", "DegreeFit", "MarriageFit", "HaveChildrenFit", "HouseFit", "LocationFit",  "ageDif", "heightDif", "weightDif", "boddyTypeDif",  "incomeDif", "housingDif", "marriageDif")
psmD = c("sHaveChildren")
psMY = c("Reply")

DataPrepare = list()

DataPrepare$lda = list()

DataPrepare$lda$randomCorpus = function(T,n,D,dlen){
	##create a random corpus for lda model and test whether it can recover the topics
	#the generated corpus contains T topics and D Documents, with the vocaburary of size n.
	#
	#frequency of a words in a topic are randomly generated and hopefully distinguishes 
	#from one topic to another.
	#documents are randomly assigned with a topic and then generate maximun dlen words
	#
	#returns
	#	a csv file. each row represents a documents, column1 is document ID and column2 are words 
	#	joint with ' '.
	#
	#parameter
	#
	#	T:	int,	number of topic in the corpus, maximun 26 for convenience
	#	n:	int,	size of vocaburary in the random corpus
	#	D:	int,	number of documents
	#	dlen:	int,	maximum legth of a doc
	
	##generate a vocaburary with n words. 
	if(T>26) T = 26
	vocabidx = 1:n
	vocab = as.character(vocab)
	
	#define the parameters
	#define phi for word frequence for topics
	phis = list()
	#pick top words for each of the T topics, then add topic Lable to the word
	for(type in T){
		phis[[letters[type]]] = rep(0.01, n)
		topnum = sample(5:as.integer(n/T),1)
		topwords = sample(n,size=topnum)
		vocab[topwords] = paste(vocab[topwords],'type',sep='')
		phis[[letters[type]]][topwords] = phis[[letters[type]]][topwords] + sample(100:300, size=topnum)
		
	} 
}