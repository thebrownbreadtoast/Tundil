from keras.layers import Input, Embedding, LSTM, Dense,concatenate
from keras.optimizers import Adam
from keras.models import Model
from keras.layers import Activation, Dense
from keras.preprocessing.text import Tokenizer
import numpy as np
import pickle
import os
import nltk
import pickle


class Tundil_bot(object):

	def __init__(self):
		self.word_embedding_size = 100
		self.sentence_embedding_size = 300
		self.dir_path = os.path.dirname(os.path.realpath(__file__))
		self.weights_file = self.dir_path+'/trained_model.h5'
		self.dictionary_size = 7000
		self.maxlen_input = 50
		self.name_of_computer = 'Tundil'
		

	def model_initialization(self):
		optimizer = Adam(lr=0.000001)
		input_context = Input(shape=(self.maxlen_input,), dtype='int32', name='input_context')
		input_answer = Input(shape=(self.maxlen_input,), dtype='int32', name='input_answer')
		LSTM_encoder = LSTM(self.sentence_embedding_size, kernel_initializer= 'lecun_uniform', name = 'encoder_memory')
		LSTM_decoder = LSTM(self.sentence_embedding_size, kernel_initializer= 'lecun_uniform', name = 'decoder_memory')
		Shared_Embedding = Embedding(output_dim=self.word_embedding_size, input_dim=self.dictionary_size, input_length=self.maxlen_input, name='Shared')

		word_embedding_context = Shared_Embedding(input_context)
		context_embedding = LSTM_encoder(word_embedding_context)

		word_embedding_answer = Shared_Embedding(input_answer)
		answer_embedding = LSTM_decoder(word_embedding_answer)

		merge_layer = concatenate([context_embedding, answer_embedding], axis=1, name='merge')
		out = Dense(self.dictionary_size//2, activation="relu", name='relu_activation')(merge_layer)
		out = Dense(self.dictionary_size, activation="softmax", name='output')(out)
		model = Model(inputs=[input_context, input_answer], outputs = [out])
		model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer)
		model.load_weights(self.weights_file)
		return model
		
class Inference(Tundil_bot):

	def __init__(self):
		self.maxlen_input = 50
		self.dictionary_size = 7000
		self.dir_path = os.path.dirname(os.path.realpath(__file__))
		self.vocabulary_file = self.dir_path+'/vocabulary'
		self.vocabulary = pickle.load(open(self.vocabulary_file, 'rb'))
		
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
		conversation_bot = Tundil_bot().model_initialization()
		flag = 0
		prob = 1
		ans_partial = np.zeros((1,self.maxlen_input))
		ans_partial[0, -1] = 2
		for k in range(self.maxlen_input - 1):
			ye = conversation_bot.predict([input, ans_partial])
			yel = ye[0,:]
			p = np.max(yel)
			mp = np.argmax(ye)
			ans_partial[0, 0:-1] = ans_partial[0, 1:]
			ans_partial[0, -1] = mp
			if mp == 3:  #  he index of the symbol EOS (end of sentence)
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
	    raw_word = raw_word.replace(', ' + Tundil_bot().name_of_computer, '')
	    raw_word = raw_word.replace(Tundil_bot().name_of_computer + ' ,', '')

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
		tokenize_user_query = self.tokenize(user_query)
		predout, prob = self.greedy_decoder(tokenize_user_query[0:1])
		start_index = predout.find('BOS')
		end_index = predout.find('EOS')
		processed_reply = self.preprocess(predout[start_index:end_index])
		return processed_reply

if __name__ == '__main__':
	inference = Inference()
	while True:
		query = input('You: ')
		print(inference.inference_reply(query))

