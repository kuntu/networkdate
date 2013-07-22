#psmX = c("sage",  "sHeight", "sWeight", "sBodyType", "sBloodType", "sNewOccupation", "sAnimalSign",  "sNewDegree", "sNewIncome", "sNewHousing", "sMarriage",  "sPhysicalLooking", "sLoveType",  "sNewCar", "sPhotoCnt", "rage",  "rHeight", "rWeight", "rBodyType", "rBloodType", "rNewOccupation", "rAnimalSign", "rAstrology",  "rNewDegree", "rNewIncome", "rNewHousing", "rMarriage", "rHaveChildren", "rPhysicalLooking", "rNewCar", "rNewProfessional",   "rPhotoCnt",  "distance", "AgeFit", "HeightFit", "IncomeFit", "DegreeFit", "MarriageFit", "HaveChildrenFit", "HouseFit", "LocationFit",  "ageDif", "heightDif", "weightDif", "boddyTypeDif",  "incomeDif", "housingDif", "marriageDif")
#psmD = c("sHaveChildren")
#psMY = c("Reply")

DataPrepare = list()

## For LDA model
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
	vocab = as.character(vocabidx)
	
	#define the parameters
	#define phi for word frequence for topics
	phis = list()
	#pick top words for each of the T topics, then add topic Lable to the word
	for(type in 1:T){
		phis[[letters[type]]] = rep(0.01, n)
		topnum = sample(5:min(260,n/T),1)
		topwords = sample(n,size=topnum)
		vocab[topwords] = paste(vocab[topwords],letters[type],sep='')
		phis[[letters[type]]] = phis[[letters[type]]] + sample(0:5,replace=T,size=n)
		phis[[letters[type]]][topwords] = phis[[letters[type]]][topwords] + sample(100:300, replace=T, size=topnum)		
	} 

	#assign D documents to topics
	docTypes = sample(letters[1:T], size=D, replace=T)
	corpus = data.frame(id=1:D, words='',stringsAsFactors=F)
	for(doc in 1:D){
		corpus[doc,'words'] = paste(sample(vocab,size=sample(dlen,size=1),replace=T,prob=phis[[docTypes[doc]]]/sum(phis[[docTypes[doc]]])),collapse=' ')
	}
	model = list()
	model$T=T
	model$D = D
	model$phis = phis
	model$docTypes = docTypes
	model$corpus = corpus
	model$vocab = vocab

	return(model)

}


##Reading and Writing for file
DataPrepare$file=list()

DataPrepare$file$readcfg = function(cfgfile){
	cfg = fromJSON(paste(readLines(cfgfile),collapse=''))
	#cfg = fromJSON(file='xxx')
	return(cfg)
}

##filter data
DataPrepare$filter = list()

#filter rows
DataPrepare$filter$selRowsByCnd = function(data, cfg){
	#filter rows with the conditions in cfg.
	#returns:
	#	subset of rows from data,
	#Paras:
	#	data: data.frame: 
	#	cfg:	list. conditions
	#			cfg$filterLarge: an array of variable names, which require to be larger than some value
	#			cfg$filterLarVal: an array of variable value, 
	#				example: cfg$filterLarge=["age"], cfg$filterLarVal = [19], would use filter data[,"age"]>19 to filter
	#			cfg$filterEq
	#			cfg$filterEqVal
	#			cfg$filterSmall
	#			cfg$filterSmVal
	##
	if(!is.null(cfg[['filterLarge']])){
		valIdx = 0
		for(var in cfg[['filterLarge']]){
			valIdx = valIdx +1
			data = data[which(data[,var]>cfg[['filterLarVal']][valIdx]),]
		}
	}

	#equal condition
	if(!is.null(cfg[['filterEq']])){
		valIdx = 0
		for(var in cfg[['filterEq']]){
			valIdx = valIdx +1
			data = data[which(data[,var]==cfg[['filterEqVal']][valIdx]),]
		}
	}
	#smaller condition
	if(!is.null(cfg[['filterSmall']])){
		valIdx = 0
		for(var in cfg[['filterSmall']]){
			valIdx = valIdx +1
			data = data[which(data[,var]<cfg[['filterSmVal']][valIdx]),]
		}
	}
	return(data)
}

##processing data value
DataPrepare$Disc = list()

##just the script for LDA model
#x = DataPrepare$lda$randomCorpus(4,500,5000,20)
#write.table(x$corpus,file='./corp.csv',sep=',',row.names=F,col.names=F,quote=F)
#write.table(as.data.frame(x$phis),file='./preference.csv',sep=',')
#write(x$docTypes,file='./userType.txt')
#write(x$vocab, file='./receivers.txt')

##scripts for pipe process
rDataToCorpus = function(cfgfile){
	print('loading config file...')
	cfg = DataPrepare$file$readcfg(cfgfile)
	load(cfg$RData)
	data = indata[,cfg$selVar]
	data = DataPrepare$filter$selRowsByCnd(data,cfg)
	summary(data)
#	return(data)
}