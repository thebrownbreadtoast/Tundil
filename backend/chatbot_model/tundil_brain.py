import nltk
import numpy as np
from backend.chatbot_model import load_model
import gc

class Tundil_bot(object):

	def __init__(self):
		self.word_embedding_size = 100
		self.sentence_embedding_size = 300
		self.dictionary_size = 7000
		self.maxlen_input = 50
		self.name_of_computer = 'tundil'
		self.model, self.vocabulary = load_model.Tundil_model().load_model()
		
	def tokenize(self,sentence):
	    tokenized_sentences = nltk.word_tokenize(sentence)
	    index_to_word = [x[0] for x in self.vocabulary]
	    word_to_index = dict([(w,i) for i,w in enumerate(index_to_word)])
	    tokenized_sentences = [w if w in word_to_index else 'something' for w in tokenized_sentences]
	    X = np.asarray([word_to_index[w] for w in tokenized_sentences])
	    s = X.size
	    Q = np.zeros((1,self.maxlen_input))
	    if s < (self.maxlen_input + 1):
	        Q[0,- s:] = X
	    else:
	        Q[0,:] = X[- maxlen_input:]
	    
	    return Q

	def greedy_decoder(self,input):
		flag = 0
		prob = 1
		ans_partial = np.zeros((1,self.maxlen_input))
		ans_partial[0, -1] = 2
		for k in range(self.maxlen_input - 1):
			ye = self.model.predict([input, ans_partial])
			yel = ye[0,:]
			p = np.max(yel)
			mp = np.argmax(ye)
			ans_partial[0, 0:-1] = ans_partial[0, 1:]
			ans_partial[0, -1] = mp
			if mp == 3:
				flag = 1
			if flag == 0:
				prob = prob * p
		text = ''
		for k in ans_partial[0]:
			k = k.astype(int)
			if k < (self.dictionary_size-2):
				w = self.vocabulary[k]
				text = text + w[0] + ' '
		return(text, prob)

	def preprocess(self,raw_word):
	    l1 = ['won’t','won\'t','wouldn’t','wouldn\'t','’m', '’re', '’ve', '’ll', '’s','’d', 'n’t', '\'m', '\'re', '\'ve', '\'ll', '\'s', '\'d', 'can\'t', 'n\'t', 'B: ', 'A: ', ',', ';', '.', '?', '!', ':', '. ?', ',   .', '. ,', 'EOS', 'BOS', 'eos', 'bos']
	    l2 = ['will not','will not','would not','would not',' am', ' are', ' have', ' will', ' is', ' had', ' not', ' am', ' are', ' have', ' will', ' is', ' had', 'can not', ' not', '', '', ' ,', ' ;', ' .', ' ?', ' !', ' :', '? ', '.', ',', '', '', '', '']
	    l3 = ['-', '_', ' *', ' /', '* ', '/ ', '\"', ' \\"', '\\ ', '--', '...', '. . .']
	    raw_word = raw_word.lower()
	    raw_word = raw_word.replace(', ' + self.name_of_computer, '')
	    raw_word = raw_word.replace(self.name_of_computer + ' ,', '')

	    for j, term in enumerate(l1):
	        raw_word = raw_word.replace(term,l2[j])
	        
	    for term in l3:
	        raw_word = raw_word.replace(term,' ')
	    
	    for j in range(30):
	        raw_word = raw_word.replace('. .', '')
	        raw_word = raw_word.replace('.  .', '')
	        raw_word = raw_word.replace('..', '')
	       
	    for j in range(5):
	        raw_word = raw_word.replace('  ', ' ')
	          
	    return raw_word

	def inference_reply(self,user_query):
		prob = 0
		last_query  = ' '
		last_text = ''
		if prob > 0.2:
			user_query = last_text + ' ' + user_query
		
		tokenize_user_query = self.tokenize(user_query)
		predout, prob = self.greedy_decoder(tokenize_user_query[0:1])
		start_index = predout.find('BOS')
		end_index = predout.find('EOS')
		processed_reply = self.preprocess(predout[start_index:end_index])
		last_text = user_query
		return processed_reply
