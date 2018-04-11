from keras.models import model_from_json
import numpy as np
import pickle
import os
import gc

class Tundil_model(object):

	def __init__(self):
		self.dir_path = os.path.dirname(os.path.realpath(__file__))
		self.model_file = self.dir_path+'/data/model.json'
		self.weights_file = self.dir_path+'/data/trained_model.h5'
		self.vocabulary_file = self.dir_path+'/data/vocabulary'

	def load_model(self):
		self.vocabulary = pickle.load(open(self.vocabulary_file, 'rb'))
		json_file = open(self.model_file,'r')
		loaded_model_json = json_file.read()
		json_file.close()
		self.model = model_from_json(loaded_model_json)
		self.model.load_weights(self.weights_file)
		self.model.compile(loss='categorical_crossentropy',optimizer='adam')
		return self.model, self.vocabulary

	def free_memory(self):
		del self.model, self.vocabulary
		gc.collect()
