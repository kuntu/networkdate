import re, time
from corpus import *
from csv import reader
from iterview import iterview
from numpy import argsort, array, cumsum, log, ones, searchsorted, zeros
from numpy.random import uniform
from numpy.random.mtrand import dirichlet
from scipy.special import gammaln
from vocabulary import *



def sample(dist, num_samples=1):
    """
    Uses the inverse CDF method to return samples drawn from an
    (unnormalized) discrete distribution.

    Arguments:

    dist -- (unnormalized) distribution

    Keyword arguments:

    num_samples -- number of samples to draw
    """

    cdf = cumsum(dist)
    r = uniform(size=num_samples) * cdf[-1]

    return cdf.searchsorted(r)


def generate_corpus(alpha, m, beta, n, D, Nd):
    """
    Returns a grouped corpus drawn from a mixture of
    Dirichlet--multinomial unigram language models.

    Arguments:

    alpha -- concentration parameter for the Dirichlet prior over theta
    m -- T-dimensional mean of the Dirichlet prior over theta
    beta -- concentration parameter for the Dirichlet prior over phis
    n -- V-dimensional mean of the Dirichlet prior over phis
    D -- number of documents to generate
    Nd -- number of tokens to generate per document
    """
    
    T = len(m)
    V = len(n)
    corpus = GroupedCorpus()
    theta = dirichlet(alpha*m)
    zVector = sample(theta,D)   #generate group type Zd for each docutment d
    allPhis = [dirichlet(beta*n) for t in xrange(T)]
    allWords = zeros(Nd*D)

    for d in xrange(D):
        for n in xrange(Nd):
            allWords[d*Nd+n] = sample(allPhis[zVector[d]])
    print allWords
    return allWords,zVector


def create_stopword_list(f):
    """
    Returns a set of stopwords.

    Arguments:

    f -- list of stopwords or name of file containing stopwords
    """

    if not f:
        return set()

    if isinstance(f, basestring):
        f = file(f)

    return set(word.strip() for word in f)


def tokenize(text, stopwords=set()):
    """
    Returns a list of lowercase tokens corresponding to the specified
    string with stopwords (if any) removed.

    Arguments:

    text -- string to tokenize

    Keyword arguments:

    stopwords -- set of stopwords to remove
    """

    tokens = re.findall('[a-z]+', text.lower())

    return [x for x in tokens if x not in stopwords]

def tokenize2(text, stopwords=set()):
    """
    Returns a list of tokens corresponding to the specified
    string with stopwords (if any) removed. This is for data only

    Arguments:

    text -- string to tokenize

    Keyword arguments:

    stopwords -- set of stopwords to remove
    """

    tokens = re.findall('\S+', text)
    
    return [x for x in tokens if x not in stopwords]

def preprocess(filename, stopword_filename=None, idx=None):
    """
    Preprocesses a CSV file and returns a grouped corpus, where each
    document's group is determined by field number 'idx'. If 'idx' is
    None, all documents are assumed to belong to a single group.

    The idx means the column number in the csv file. the last column in the
    csv table is the statements/contents. the previous columns mean some
    property of the instance. setting the idx means grouping the instances
    by a property.

    Arguments:

    filename -- name of CSV file

    Keyword arguments:

    stopword_filename -- name of file containing stopwords
    idx -- field number (e.g., 0, 1, ...) of the group
    """

    stopwords = create_stopword_list(stopword_filename)

    corpus = GroupedCorpus()

    for fields in reader(open(filename), delimiter='\t'):

        if idx:
            group = fields[idx]
            
        else:
            group = 'group 1'
        corpus.add(fields[0], group, tokenize2(fields[-1], stopwords))
        #corpus.add(fields[0], group, tokenize(fields[-1], stopwords))

    return corpus


def log_evidence_1(corpus, alpha, m, beta, n):
    """
    Returns the log evidence for a grouped corpus (i.e., document
    tokens and groups) according to a mixture of
    Dirichlet--multinomial unigram language models.

    Arguments:

    corpus -- grouped corpus
    alpha -- concentration parameter for the Dirichlet prior over theta
    m -- T-dimensional mean of the Dirichlet prior over theta
    beta -- concentration parameter for the Dirichlet prior over phis
    n -- V-dimensional mean of the Dirichlet prior over phis
    """

    D = len(corpus)
    V = len(corpus.vocab)
    T = len(corpus.group_vocab)

    assert len(m) == T and len(n) == V

    Nvt = zeros((V, T), dtype=int)
    Nt = zeros(T, dtype=int)

    Dt = zeros(T, dtype=int)

    for doc, t in corpus:
        Dt[t] += 1
        for v in doc.w:
            Nvt[v, t] += 1
            Nt[t] += 1
    
    alphas = alpha*m
    betas = beta*n
    wLogNum=0;
    wLogDeno=0;
    zLogNum =gammaln(alpha);
    zLogDeno = gammaln(D+alpha)
    logGammaBeta = gammaln(beta)
    for t in xrange(T):
        zLogNum +=gammaln(Dt[t]+alphas[t])
        zLogDeno += gammaln(alphas[t])
        wLogNum +=logGammaBeta
        wLogDeno += gammaln(Nt[t]+beta)
        for v in xrange(V):
            wLogNum += gammaln(Nvt[v] + betas[v])
            wLogDeno += gammaln(betas[v])
    
    return zLogNum+wLogNum-zLogDeno-wLogDeno
    


def log_evidence_2(corpus, alpha, m, beta, n):

    V = len(corpus.vocab)
    T = len(corpus.group_vocab)

    assert len(m) == T and len(n) == V

    Nvt = zeros((V, T), dtype=int)
    Nt = zeros(T, dtype=int)

    Dt = zeros(T, dtype=int)
    
    
    betas = beta*n
    alphas = alpha*m
    wLogNume=0
    wLogDeno = 0
    zLogNume = 0
    zLogDeno = 0
    N=0
    D=0
    for doc, t in corpus:
        for v in doc.w:   # v is the value? or the lenth?
            wLogNume += log(Nvt[v,t]+betas[v])
            Nvt[v,t] +=1
            wLogDeno += log(Nt[t]+beta)
            Nt[t]+=1
        
        zLogNume += log(Dt[t]+alphas[t])
        Dt[t]+=1
        zLogDeno += log(D+alpha)
        D += 1
    return  wLogNume+zLogNume-wLogDeno-zLogDeno   
    pass # YOUR CODE GOES HERE


def time_taken(func, corpus, alpha, m, beta, n, num_reps):

    avg = 0

    for rep in iterview(xrange(num_reps), inc=1):

        start = time.time()
        func(corpus, alpha, m, beta, n)
        avg += (time.time() - start)

    avg /= float(num_reps)

    return avg


def log_evidence_tokens_1(corpus, beta, n):
    """
    Returns the log evidence for the tokens belonging to a grouped
    corpus given the doucument groups according to a mixture of
    Dirichlet--multinomial unigram language models.

    Arguments:

    corpus -- grouped corpus

    beta -- concentration parameter for the Dirichlet prior over phis
    n -- V-dimensional mean of the Dirichlet prior over phis
    """

    V = len(corpus.vocab)
    T = len(corpus.group_vocab)

    assert len(n) == V

    Nvt = zeros((V, T), dtype=int)
    Nt = zeros(T, dtype=int)

    for doc, t in corpus:
        for v in doc.w:
            Nvt[v, t] += 1
            Nt[t] += 1
    #print 'execute log_evidence_tokens_1()'
    betas = beta*n
    numer=0
    denom=0
    for t in xrange(T):
        numer += gammaln(beta)
        denom += gammaln(Nt[t]+beta)
        for v in xrange(V):
            numer += gammaln(Nvt[v,t]+betas[v])
            denom += gammaln(betas[v])
    return numer-denom
    pass # YOUR CODE GOES HERE


def posterior_mean(corpus, alpha, m, beta, n):
    """
    Returns the mean of the posterior distribution.

    Arguments:

    corpus -- grouped corpus
    alpha -- concentration parameter for the Dirichlet prior over theta
    m -- T-dimensional mean of the Dirichlet prior over theta
    beta -- concentration parameter for the Dirichlet prior over phis
    n -- V-dimensional mean of the Dirichlet prior over phis
    """

    mean_theta = posterior_mean_theta(corpus, alpha, m)
    mean_phis = posterior_mean_phis(corpus, beta, n)

    return mean_theta, mean_phis


def posterior_mean_phis(corpus, beta, n):
    """
    Returns the mean of the posterior distribution over phis.

    Arguments:

    corpus -- grouped corpus
    beta -- concentration parameter for the Dirichlet prior over phis
    n -- V-dimensional mean of the Dirichlet prior over phis
    """

    V = len(corpus.vocab)
    T = len(corpus.group_vocab)

    assert len(n) == V

    Nvt = zeros((V, T), dtype=int)
    Nt = zeros(T, dtype=int)

    for doc, t in corpus:
        for v in doc.w:
            Nvt[v, t] += 1
            Nt[t] += 1
    
    phis = zeros((V,T))
    betas = beta*n
    for t in xrange(T):
        phis[:,t] = betas
        
    phis +=Nvt
    for t in xrange(T):
        phis[:,t] /=Nt[t]+beta
    return phis
    pass # YOUR CODE GOES HERE


def posterior_mean_theta(corpus, alpha, m):
    """
    Returns the mean of the posterior distribution over theta.

    Arguments:

    corpus -- grouped corpus
    alpha -- concentration parameter for the Dirichlet prior over theta
    m -- T-dimensional mean of the Dirichlet prior over theta
    """

    D = len(corpus)
    T = len(corpus.group_vocab)

    assert len(m) == T

    Dt = zeros(T, dtype=int)

    for doc, t in corpus:
        Dt[t] += 1
    
    alphas = alpha *m
    theta = (Dt+alphas)/(D+alpha)
    
    return theta
    pass # YOUR CODE GOES HERE


def print_top_types(corpus, beta, n, num=10):
    """
    Prints the most probable word types according to the mean of the
    posterior distribution over phis.

    Arguments:

    corpus -- grouped corpus
    beta -- concentration parameter for the Dirichlet prior over phis
    n -- V-dimensional mean of the Dirichlet prior over phis

    Keyword arguments:

    num -- number of types to print
    """

    mean_phis = posterior_mean_phis(corpus, beta, n)

    for t in xrange(len(corpus.group_vocab)):
        group = corpus.group_vocab.lookup(t)
        top_types = map(corpus.vocab.lookup, argsort(mean_phis[:, t]))
        print '%s: %s' % (group, ' '.join(top_types[-num:][::-1]))
        
        
    
#corpus = preprocess('ufos.csv','stopwordlist.txt',2)
#-38824961.0869
corpus = preprocess('newdata.csv','stopwordlist.txt',1)
T = len(corpus.group_vocab)
V= len(corpus.vocab)
alpha = T
m=ones(T)/T
beta = V
n = ones(V)/V
print len(corpus.vocab)
#for doc, t in corpus:
#    print doc.w
#import cProfile
#cProfile.run('cor=preprocess(\'ufos.csv\',\'new_stopwordlist.txt\',1)')

#print log_evidence_tokens_1(corpus, V, ones(V) / V)
print_top_types(corpus, V, ones(V) / V)