#This python module contains a class of static functions used for machine learning 

#Imports
import numpy as np
import sys
import h5py
import skimage.transform
import os
import math as m
import tensorflow as tf
import FRIB_ML as ML
from FRIB_ML.data_process import h5_process

#Functions:
	
#Python generator zips together data and label images. Takes two numpy arrays of h5 file names
def data_generator(h5_data,h5_labels):
	for i,j in zip(h5_data, h5_labels):
		a = h5_process(i)
		b = h5_process(j)
		
		yield a,b

#Function that takes path to a directory containing training and label data in foders and returns arrays of strings of h5 file names 
def fetch_data(data_path):
	#Define train/test percentage
	train_perc = .8
	#Access sim and label directories
	sim_path = data_path + "/sim_out"
	label_path = data_path + "/label_out"
	
	#Confirm that they are of the same size
	if ML.count_file(label_path) != ML.count_file(sim_path):
		raise ValueError(f"{label_path} and {sim_path} must be the same size")
	
	#Store number of files in training set
	num_files = ML.count_file(label_path)
	#Generate array of range between 1-len(training_set)
	index_arr = np.arange(1,num_files+1,1)
	#Shuffle array to yield random set order
	np.random.shuffle(index_arr)
	#Generate 2 arrays (label and sim data) filled with file names based on index arrays
	h5_labels = np.zeros(num_files)
	h5_sim = np.zeros(num_files)
	for i in range(num_files):
		h5_labels[i] = f"{label_path}/label_{index_arr[i]}.h5"
		h5_sim[i] = f"{sim_path}/sim_out_{index_arr[i]}.h5"	
	
	#Divide arrays into training and testing based on a percentage (floored integer value)
	train_size = m.floor(train_perc * num_files)
	train_files = h5_sim[:train_size]
	test_files = h5_sim[train_size:]
	train_labels = h5_labels[:train_size]
	test_labels = h5_labels[train_size:]

	return train_files, test_files, train_labels, test_labels 
	
#Function to normalize a tensorflow dataset using min/max normalization
def mm_norm(dataset):
	min_val = tf.reduce_min(dataset)
	max_val = tf.reduce_max(dataset)
	
	return (dataset - min_val) / (max_val-min_val)

#Function to normalize a tensorflow dataset using z-score normalization
def z_norm(dataset):
	mean = tf.reduce_mean(dataset)
	std = tf.reduce_std(dataset)

	norm_set = (dataset - mean) / std
	
	return(norm_set)

#Function to seperate features from input labels
def extract_features(features, label):
	return features

#Function to seperate labels from input features
def extract_labels(features, label):
	return label




	

