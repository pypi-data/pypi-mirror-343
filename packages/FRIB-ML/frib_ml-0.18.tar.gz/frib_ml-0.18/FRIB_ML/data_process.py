#This module is used for processing training data for training the machine learning model
import h5py
import skimage.transform
import numpy as np
import tensorflow as tf
import FRIB_ML as ML

class process:
	#Function that takes h5 file and returns a processed numpy array
	@staticmethod
	def h5_process(file_name):
		with h5py.File(file_name, 'r') as f:
			dataset = list(f.keys())[0]
			a = np.array(f[dataset])
			#Process array
			array = skimage.transform.downscale_local_mean(a,(5,5))
			f.close()
			
		return array

	#Function that uses a data generator to get data from h5 files
	@staticmethod
	def get_data(train_files, test_files, train_labels, test_labels, BUFFER_SIZE, BATCH_SIZE):
		train_set = tf.data.Dataset.from_generator(ML.data_generator(train_files, train_labels),(tf.float32,tf.float32)).shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
		test_set = tf.data.Dataset.from_generator(ML.data_generator(test_files, test_labels),(tf.float32,tf.float32)).shuffle(BUFFER_SIZE).batch(BATCH_SIZE)

		return train_set, test_set, train_labels, test_labels