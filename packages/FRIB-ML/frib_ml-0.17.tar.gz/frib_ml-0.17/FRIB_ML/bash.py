#This python module contains a set of functions used to mimic bash functions

#Imports
import os
import sys
import numpy as np
import shutil
import subprocess

#Functions:


#Function to count files in specified path (1 layer)
def count_file(path):
	count = 0
	for entry in os.scandir(path):
		if entry.is_file():
			count+=1
	return count

#Function to count directories in specified path (1 layer)
def count_dir(path):
	count = 0
	for entry in os.scandir(path):
		if entry.is_dir():
			count+=1
	return count

#Function to return array of directory names in a specified path
def dir_list(path):
	entries = []
	obj = os.scandir(path)
	for entry in obj:
		if entry.is_dir():
			entries.append(entry.name)
	dirs = np.array(entries)
	return dirs

#Function to make new directory, or clear it if it exist
def make_new(path):
	if os.path.exists(path):
		shutil.rmtree(path)
		os.makedirs(path)
	else:
		os.makedirs(path)


#Function to return array of file names in a specified path
def file_list(path,reorder=False):
	entries = []
	obj = os.scandir(path)
	for entry in obj:
		if entry.is_file():
			entries.append(entry.name)
	files = np.array(entries)

	#Reorder files ( Only deals with file names < 30 characters
	if reorder == True:
		filesl = files
		files = np.empty((np.shape(filesl)), dtype=np.dtype('U30'))
		names = files

		for i in filesl:
			name = i.split("_")[-1] #Get last element of array deliminated by "_" (number and file ext.)
			files[int(name.split(".")[0])] = i #Get number portion of name string
	return files




			
		




