#psmX = c("sage",  "sHeight", "sWeight", "sBodyType", "sBloodType", "sNewOccupation", "sAnimalSign",  "sNewDegree", "sNewIncome", "sNewHousing", "sMarriage",  "sPhysicalLooking", "sLoveType",  "sNewCar", "sPhotoCnt", "rage",  "rHeight", "rWeight", "rBodyType", "rBloodType", "rNewOccupation", "rAnimalSign", "rAstrology",  "rNewDegree", "rNewIncome", "rNewHousing", "rMarriage", "rHaveChildren", "rPhysicalLooking", "rNewCar", "rNewProfessional",   "rPhotoCnt",  "distance", "AgeFit", "HeightFit", "IncomeFit", "DegreeFit", "MarriageFit", "HaveChildrenFit", "HouseFit", "LocationFit",  "ageDif", "heightDif", "weightDif", "boddyTypeDif",  "incomeDif", "housingDif", "marriageDif")
#psmD = c("sHaveChildren")
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

#change data.frame to LDA corpus
DataPrepare$lda$dataToCorpus = function(featTb,docF,file='./defaultCorpus.txt'){
	##
	#intro:
	#	concatenate feature values of each row to a string. This kind of String
	#	is regarded as a word in LDA model.
	#	function will return a list. with names as the docID and each doc contains a
	#	supper long string. This long string is the concateneted words seperated by ' '
	#paraM"
	#	featTb: data.frame. contain the refined values of all the features
	#	docF: factor: contain the doc IDs for each row. strings in rows with the same ID will
	#		be group together. The same way as words in the same doc should be group together
	#	file: string: the output file of the 'ready-to-use' corpus. in each row of 
	#		the file. format is 'docID, word1 word2 ...'. words are seperated by space, and 
	#		column is splited by ','
	##
	target = apply(featTb, 1, paste, collapse='_')	
	targUser = docF  #factor(indata[splIdx$mSenderIdx,'sender'])
	tmpcorpus = split(target,targUser)
	#concatenate each element to a long string in the tmpcorpus, with ' '.
	tmpcorpus = lapply(tmpcorpus, paste, collapse=' ')
	#print(levels(docF))
	idx = cbind('ID',paste(names(featTb),collapse='_'))
	write.table(rbind(idx,t(rbind(names(tmpcorpus),tmpcorpus))),file,row.names=F,col.names=F,sep=',')
	return(tmpcorpus)
}

#feature space to number
DataPrepare$lda$featSpace = function(Data, selFeat, discVals){
	data = unique(DataPrepare$Disc$discretize(Data[,selFeat],selFeat,discVals))
	summary(data)
	featSpace = list()
	featSpace$missing = 0
	for(i in 1:length(data[,1])) {
		featSpace[[paste(data[i,],collapse='_')]] = i
	}
	return(featSpace)
}

DataPrepare$lda$getTypeFeatTab = function(Data, selFeat){
	if(is.na(Data)){
		print('data is NA, cannot get type-feature counting table')
		return(NA)
	}
	dataf = factor(apply(Data[,selFeat],1,paste,collapse='_'))
	typef = factor(Data$userType)
	tb = table(typef,dataf)
	tb = tb + 1/length(levels(dataf))
	return(tb)	
}

DataPrepare$lda$getTypeProb = function(tab, feat){
	idx = paste(feat,collapse='_')
	if(idx %in% colnames(tab)){
		return(tab[,idx]/sum(tab[,idx]))
	}else{
		return(rep(1/length(tab[,1], length(tab[,1]))))
	}
	
}

DataPrepare$lda$getFeatProb = function(tab, type){
	
	return(tab[type,]/sum(tab[type,]))
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

# change data type for column variables in data.frame according to the config file
DataPrepare$filter$changeDataType = function(data, dataInfo){
	## 
	#Parameter:
	#	data (data.frame):	the data
	#	dataInfo(list):		contain arrays of variable names, where each array of variable are to be changed to a different type
	#		dataInfo$numeic = ["var_to_be_numeric", "var2"]
	#		dataInfo$datatime = ["var_to_be_datatime","xxxx"]
	#		
	#change to numeric
	for(var in dataInfo$numeric){
		data[[var]] = as.numeric(as.character(data[[var]]))
	}
	#change to time data
	for(var in dataInfo$datetime){
		data[[var]] = as.POSIXct(as.character(data[[var]]), format='%Y-%m-%d %H:%M:%S')
	}

	return(data)
}

DataPrepare$filter$removeCol = function(data, cols){
	if(mode(cols)=='character'){
		return(data[, -na.omit(match(cols,names(data)))])
	}else{
		return(data[, -cols])
	}
}

# detect NA values
DataPrepare$filter$detectNA = function(data, NAdetect){
	for(var in names(NAdetect$smallVar)){
		data[which(data[[var]] < NAdetect$smallVar[[var]]), var] = NA
	}
	for(var in names(NAdetect$largeVar)){
		data[which(data[[var]] > NAdetect$largeVar[[var]]), var] = NA
	}
}

##processing data value
DataPrepare$Disc = list()

#discretize variables
DataPrepare$Disc$discretize = function(data, discVar, discVarVal){
	##discretize variables in the data, given the DiscVar and the intervals in the cfg
	#	use findInterval() to discretize
	#returns
	#	a new data.frame withe discretized values
	#Para:
	#	data: data.frame:	the data where variables are to be discretized
	#	cfg:	list:		the config read from json. should contain the "DiscVar" and "DiscVarVal"
	#			cfg$DiscVar:(vector)	the names of variables that are to discretized
	#			cfg$DiscVarVal:	(list)	intervals for each variables. the names of the element are the names in the DiscVar
	if(!is.null(discVar)){
		if(!is.null(discVarVal)){
			valIdx = 0
			for(var in discVar){
				valIdx = valIdx +1
				if(var %in% names(data)){
					data[[var]] = findInterval(data[[var]],discVarVal[[var]])
				}
			}			
		}
	}else{
		print('Cannot discretize variables')		
	}
	return(data)
}

##just the script for LDA model
#x = DataPrepare$lda$randomCorpus(4,500,5000,20)
#write.table(x$corpus,file='./corp.csv',sep=',',row.names=F,col.names=F,quote=F)
#write.table(as.data.frame(x$phis),file='./preference.csv',sep=',')
#write(x$docTypes,file='./userType.txt')
#write(x$vocab, file='./receivers.txt')

##scripts for pipe process
DataPrepare$rDataToCorpus = function(cfgfile,outfile='./ldacorpus.txt', missing=T){
	print('loading config file...')
	cfg = DataPrepare$file$readcfg(cfgfile)
	load(cfg$RData)
	data = DataPrepare$filter$selRowsByCnd(indata,cfg)
	IDf = factor(data[,cfg$IDVar])
	data = data[,cfg$selVar]
	if(!missing){
		data = na.omit(data)
		print('omitting missing data')
	}
	data = DataPrepare$Disc$discretize(data, cfg[['DiscVar']], cfg[['DiscVarVal']])
	#print(summary(data))
	if(!is.null(cfg[['outfile']])){
		outfile = paste(cfg[['outdir']], cfg[['outfile']], sep='/')
	}
	corpus = DataPrepare$lda$dataToCorpus(data,IDf,outfile)
	return(data)
}