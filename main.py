import nltk
from nltk.corpus import stopwords




custom_words=['band','they','them']

p=open("postweets.txt","r")
postxt=p.readlines()


n=open("negtweets.txt","r")
negtxt=n.readlines()


neglist=[]
poslist=[]

for i in range(0,len(negtxt)):
	neglist.append('negative')

for i in range(0,len(postxt)):
	poslist.append('positive')


negtagged=zip(negtxt,neglist)
postagged=zip(postxt,poslist)

taggedtweets=postagged+negtagged

tweets=[]

for (word,sentiment) in taggedtweets:
	word_filter=[i.lower() for i in word.split()]
	tweets.append((word_filter,sentiment))


def getwords(tweets):
    allwords=[]
    for(words,sentiment) in tweets:
        allwords.extend(words)
    return allwords    

def getwordfeatures(listoftweets):
    wordfreq=nltk.FreqDist(listoftweets)
    words=wordfreq.keys()
    return words

wordlist=getwordfeatures(getwords(tweets))

wordlist=[i for i in wordlist if i not in stopwords.words('english')]
wordlist=[i for i in wordlist if i not in custom_words]

def feature_extractor(doc):
	docwords=set(doc)
	features={}
	for i in wordlist:
		features['contains(%s)'%i]=(i in docwords)
	return features
	
training_set=nltk.classify.apply_features(feature_extractor,tweets)

print (training_set)

classifier=nltk.NaiveBayesClassifier.train(training_set)	


while 1:
	input=raw_input("Enter any sentence to estimate the sentiment")
	if input=='exit':
		break
	else:
	    input=input.lower()
	    input=input.split()	
	    print '\nWe think that sentiment was '+classifier.classify(feature_extractor(input))+' in that sentence'


