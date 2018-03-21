import pandas as pd
import re
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import wordnet
from nltk.corpus import stopwords
import spacy
from spacy.lang.en.stop_words import STOP_WORDS


lemmatizer = WordNetLemmatizer()

"""
function used to determine the part-of-speech tagging
"""
def get_lemmatized_word(treebank_tag):
	if treebank_tag is 'V':
		return 'v'
	elif treebank_tag is 'J': # for adjective
		return 'a'
	elif treebank_tag is 'N':
		return 'n'
	elif treebank_tag is 'R': # 
		
		return 'r'
	else:
		return '_NA_'

		
"""
function used to get the root/lemmatized form of any word if it exists.
"""
def lemmatize_func(msg):
	tokens=word_tokenize(msg.lower())
	tag=nltk.pos_tag(tokens)
	c=0
	lemmatized=[]
	size=len(tag)
	for i in tag:
		if c<size:
			# i is the actual tuple ('name', 'NN') , i[0] is 'name' and i[1] is 'NN' i [1][0] is first letter of 'NN' i.e 'N' 
			#print i[1][0],c,'ccccccccc'
			tag_type=get_lemmatized_word(i[1][0])
			#print tag_type,i[0],'zzzzzzzzzz'
			if tag_type is '_NA_':
				#print lemmatizer.lemmatize(i[0])
				lemmatized.append(str(i[0]).upper())
			else:
				
				lem=lemmatizer.lemmatize(str(i[0]),tag_type)
				#print lem,str(i[0]),tag_type
				
				lemmatized.append(lem.upper())
			c=c+1
		
	
	# --------need to check by removing '_NA_' values
	return lemmatized
	#print msg,'xxxxxxxxxx',lemmatized
	#raw_input()

	
"""
function that gets rid of all the noise data and extracts the important data.
"""

def filtered_df_func(df):

	c=0
	nlp = spacy.load('en')
	for idx,row in df.iterrows():
		try:
			filtered_msg_list=[]
			
			msg=row['Question'].lower()
			msg=nlp(msg)
			cleaned_text=''
			
			msg=spacy_filter(msg)
			
			tokens=word_tokenize(msg.upper())
			
			#print tokens
			
			#stop_words = set(stopwords.words('english'))
		
		except Exception as e:
			filtered_msg_list.append(' ')
			print ('error',e)
			continue
		
		try:
		
			for word in tokens:
				match=re.search(r'([A-Z]+)',word.upper())
				#print match.group(),'mmmm',word
				
				if match:
					#for extracting alphabetical keywords
					if match.group() == word and len(word)>1: 
						#print 'oyeehoyeee' 
						#feature_dict[word]=row['MessageType']
						#df.at[idx,'filtered_msg']=word
						#if word.lower() not in stop_words:
							#print word,'stop_word'
							#raw_input()
						#----------------------not removing stopwords as it is to be used during bi-grams	
						
						filtered_msg_list.append(word)
			#if no filtered word is found,append empty space ' ' to the list
			
			if len(filtered_msg_list) is 0: 
				print ('no   matchhhh')
				input()
				filtered_msg_list.append(' ')
				
			#filtered_stopwords_text=' '.join(filtered_msg_list)
			#lemmatized_text=lemmatize_func(filtered_stopwords_text)
			#print lemmatized_text
			#raw_input()
				
			#df.at[idx,'filtered_msg']=' '.join(lemmatized_text)
			df.at[idx,'filtered_msg']=' '.join(filtered_msg_list)
		except Exception as e:
			#df=df.drop(idx)
			filtered_msg_list.append(' ')
			print ('errorrrrr',e)
			continue
		
	print (df)
	input()
	df.to_csv('feature_sampleeee.csv')
	#raw_input()
	return df
	#raw_input()
		
	#feature_list.append((feature_dict,row['MessageType']))
	
	
def spacy_filter(msg):
	list=[w.lemma_ for w in msg if not (w.pos_ in ['DET','ADP','PUNCT','SYM','PRON'] or w in STOP_WORDS)]
	list=[w for w in list if not (w in STOP_WORDS)]
	
	new_msg=' '.join(list)
	#print ('hello',new_msg)
	#input()
	
	return new_msg
