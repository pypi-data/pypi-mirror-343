import FRIB_ML as ML
import os
import plotly.graph_objects as go
import random
import subprocess
import numpy as np
import h5py

class generate:
	def __init__(self,path,levels,trans,runs,PEs,min_E,max_E):
		self.levels = levels
		self.trans = trans
		self.runs = runs
		self.PEs = PEs
		self.min_E = min_E
		self.max_E = max_E
		self.path = path
		

		self.root = path + "/Training_data"
		self.root_dump = self.root + "/root_dump"
		self.hist = self.root + "/hist_dump"
		self.label_dump = self.root + "/label_dump"
		self.train_sets = self.root + "/Training_sets"

		self.mac_dump = self.label_dump + "/macs"
		self.rad_dump = self.label_dump + "/rad_decay"
		self.levels_dump = self.label_dump + "/levels_dump"
		self.PE_dump = self.label_dump + "/PE_dump"
		self.trans_dump = self.label_dump + "/trans_matrix_dump"
		self.slurm_dump = self.root + "/slurm_dump"		
		#Define target directory for training set
		self.set_dir = str(self.train_sets) + "/"+str(self.levels)+"_levels/"+str(self.trans)+"_trans/"+str(self.runs)+"_runs"

		print("Training data located at ", self.root)

	#Initialize data directories from desired root data path, and defines names of dump data directories and training set directory
	def initialize(self):
		#Check and see if directories exist, make them if not
		mklist = [self.root_dump,self.hist,self.label_dump,self.slurm_dump,self.mac_dump,self.rad_dump,self.trans_dump,self.PE_dump,self.levels_dump]
		for i in mklist:
			ML.make_new(i)
		os.makedirs(self.train_sets,exist_ok=True)
		os.makedirs(self.set_dir,exist_ok=True)
	#Check and see how many directories are in target training set directory and then make a new one and its sim/label directories
		count = ML.count_dir(self.set_dir) + 1
		self.active_dir = str(self.set_dir)+"/set_"+str(count)
		self.sim_dir = str(self.active_dir)+"/sim_out"
		self.label_dir = str(self.active_dir)+"/label_out"
		
		os.makedirs(self.sim_dir,exist_ok=True)
		os.makedirs(self.label_dir,exist_ok=True)
	
	#Define simulation location and name
	def sim_path(self,sim_path,sim_name):
		self.sim_path = sim_path
		self.sim_name = sim_name
	
	#Clear dump directories
	def clear_dump(self):
		mklist = [self.root_dump,self.hist,self.slurm_dump,self.mac_dump,self.rad_dump,self.trans_dump,self.PE_dump,self.levels_dump]
		for i in mklist:
			ML.make_new(i)

	#Generate PE files
	def generate_PE(self):
		class Transition:
			def __init__(self, transition_number, transition_energy, intensity):
				self.transition_number = transition_number
				self.transition_energy = transition_energy
				self.intensity = intensity


		class Level:
			def __init__(self, level_number, level_energy):
				self.level_number = level_number
				self.level_energy = level_energy
				self.placement = 1
				self.transitions = []

			def add_transition(self, transition_number, transition_energy, intensity):
				transition = Transition(transition_number, transition_energy, intensity)
				self.transitions.append(transition)
		#make random PE file

		# Access the variable values
		number_of_levels = self.levels
		max_transitions = self.trans
		max_energy = self.max_E
		min_energy = self.min_E
		PEs = self.PEs
		sim_outdir = self.root_dump
		sim_name = self.sim_name
		sim_eventnum = self.runs

		output = '''#/gedssd_bc/analysis/dirname
		  /{sim_name}/analysis/filename {sim_outdir}{sim_outname}

		  #Pick the detectors to visualize

		  #
		  #uncommonly used detectors - set to false unless you need
		  #something specific here
		  /e17011_sim/det/Use3Hen false
		  /e17011_sim/det/UseMTC false
		  /e17011_sim/det/UseLENDA false
		  /e17011_sim/det/UseGetest false
		  /e17011_sim/det/UseEXOtest false

		  #more commonly used detectors in beta decay setups
		  /e17011_sim/det/UseSiDSSD false
		  /e17011_sim/det/setGeThickDetectorThickness 15 mm
		  /e17011_sim/det/setGeThinDetectorMate Vacuum
		  /e17011_sim/det/UseGeThickDetector false
		  /e17011_sim/det/UseGeThickDetectorCryo false
		  /e17011_sim/det/UseGeThickDetectorCryoEndCap false
		  /e17011_sim/det/UseGeThinDetector false
		  /e17011_sim/det/UseSega false
		  /e17011_sim/det/UseClover true
		  #/e17011_sim/det/UseCloverBracket false
		  /e17011_sim/det/UseLaBr3 false
		  /e17011_sim/det/UseEJ204Scint false
		  /e17011_sim/det/UseCeBr3Scint false
		  /e17011_sim/det/UsePipe false
		  /e17011_sim/det/UsePSPMT false
		  /e17011_sim/det/UseLaBr3Frame false

		  /run/initialize

		  /grdm/allVolumes

		  /grdm/setRadioactiveDecayFile 27 70 {file_path_rdf}
		  /grdm/setPhotoEvaporationFile 28 70 {file_path}
		  /grdm/nucleusLimits 70 70 27 27


		  /gps/ang/type iso
		  /gps/position 0 0 0.0 cm
		  /gps/particle ion
		  #/gps/ion 28 70 0 {excitation_energy}
		  /gps/ion 27 70 0 0




		  /run/beamOn {sim_eventnum}

		  # Re-establish auto refreshing and verbosity:
		  #/vis/viewer/set/autoRefresh true
		  #/vis/verbose warnings
		'''

		for ii in range(PEs):

			energies = [random.randint(min_energy, max_energy) for _ in range(number_of_levels)]
			fillers = [random.randint(1, 10000) for _ in range(15)]
			fillers[1] = .000000000023
			fillers[2] = 2.0
			fillers[3] = 1
			energies[0] = 0
			energies.sort()

			# Open file for writing
			filename = self.PE_dump + "/photon_evap_" + str(ii) + ".txt"
			filename_rdf = self.rad_dump + "/rad_decay_" + str(ii) + ".txt"
			filename_levels = self.levels_dump + "/levels_" + str(ii) + ".txt"
			filename_trans_matrix = self.trans_dump + "/trans_matrix_" + str(ii) + ".txt"

			#write output file with list of level energies only
			with open(filename_levels,"w") as file:
				for energy in energies:
					file.write(str(energy) + ' ')
				file.close()

			#make a 2D matrix of levels x levels where the element contains 
			#intensity of transition
			# Initialize an empty 2D array with zeros
			array_2d = [[0 for _ in range(0,len(energies))] for _ in range(0,len(energies))]

			#make the photon evaporation file
			with open(filename, "w") as file:
				# Write numbers to file
				for i in range(0,len(energies)):
					if (i != 0):
						remaining = len(energies) -i
						remaining = i
						if max_transitions < remaining:
							transition_num = random.randint(1,max_transitions)
						else:
							transition_num = random.randint(1,remaining)    
						levels_list = []
						transitions = []    
						for j in range(0,transition_num):
							new_level = random.randint(0,i-1)
							intensity = random.randint(1,99)
							if new_level in levels_list:
								break
							else:
								levels_list.append(new_level)
							transitions.append(Transition(new_level, energies[i]-energies[new_level],intensity))
						if len(transitions) > 1:
							highest_intensity = random.randint(0,len(transitions)-1)
							transitions[highest_intensity].intensity = 100
						elif (len(transitions) > 0):
							transitions[0].intensity = 100
						transitions.sort(key=lambda p: p.transition_number, reverse=True)
						#print(f"{len(transitions)}   {transition_num}")
						file.write(f"{i:>4}  -  {energies[i]:>8.2f}  {fillers[1]:>10.2e}  {fillers[2]:>4.1f}  {len(transitions)}\n")
						for j in range(0,len(transitions)):
							#this is confusing as hell but it works
							array_2d[i][transitions[j].transition_number] = transitions[j].intensity
							array_2d[transitions[j].transition_number][i] = transitions[j].intensity
							file.write(f"     {transitions[j].transition_number:>4}    {transitions[j].transition_energy:>8.2f}     {transitions[j].intensity:>3.1f}     4      0 0.000001e-30    0.0000   0.00000 0.0000000 0.0000000  0.000000 0.000e-00 0.000e-00         0         0 0.0000000\n")
					else:
						file.write(f"{i:>4}  -  {energies[i]:>8.2f}  {fillers[1]:>10.2e}  {fillers[2]:>4.1f}  {0}\n")

			#write out file for 2D array
			with open(filename_trans_matrix,"w") as file:
				for row in array_2d:
					row_str = ' '.join(map(str, row))
					file.write(row_str + '\n')
				file.close()

			#make the radioactive decay file
			level_branch = 100.00/len(energies) #equal branches to each level for now
			q_value = max_energy + 100
			with open(filename_rdf, "w") as file:
				file.write("# 70CO ( 10 s )\n")
				file.write("#  Excitation  flag   Halflife  Mode    Daughter Ex flag   Intensity          Q\n")
				file.write("P            0  - 1.00e01\n")
				file.write("                              BetaMinus            0               1\n")
				for i in range(1,len(energies)):
					q_val_text = q_value - energies[i]
					file.write(f"                              BetaMinus     {energies[i]:>8.3f}  -       {level_branch:>6.2f}     {q_val_text:>8.3f}\n")

			#make the highest energy level the excitation energy 
			excitation_energy = energies[-1] #making this 0 for decay file, but this part is commented out in macro
			file_path = filename #for photon evap file
			file_path_rdf = filename_rdf #for radioactive decay file
			sim_outname = "/sim_" + str(ii)

			outputUpdate = output.format(file_path=file_path, file_path_rdf=file_path_rdf, excitation_energy = excitation_energy, sim_outdir = sim_outdir, sim_name = sim_name, sim_outname = sim_outname, sim_eventnum = sim_eventnum)
			outfile = self.mac_dump + "/macro_" +str(ii) + ".mac"

			with open(outfile, 'w') as file:
				file.write(outputUpdate)

				print("File " + outfile + " generated successfully.")

	#Run slurm training script from mac_dump directory files. (Run simulation)
	def run_sim(self):
		print("Running simulations")
		macs = ML.file_list(self.mac_dump)
		exec_path = os.path.dirname(__file__) + "/bash_exec/slurm.sh"
		exec_str = "sh "+exec_path + " "+str(self.PEs)+" "+str(self.sim_path)+" "+str(self.mac_dump)+" "+str(self.slurm_dump)
		os.system(exec_str)
		print("Simulations complete.")

	#Extract root histograms from root_dump directory
	def extract_hist(self):
		print("Performing histogram extraction")
		#Run bash executable to source newer version of root and run python script in subshell
		exec_str = "sh " + os.path.dirname(__file__) + "/bash_exec/hist_extract.sh " + os.path.dirname(__file__) + " " +str(self.root_dump) + " " + str(self.hist)
		os.system(exec_str)
		
		print("Histogram extraction complete.")

	#Convert ROOT histograms to h5 file format and store in proper directory
	def hist2_h5(self):
		import ROOT
		import h5py

		#Get array of filenames in root_dump directory to convert to h5
		prefix = self.hist + "/"
		root_files = np.char.add(prefix,ML.file_list(self.hist))

		#Loop over each file in root_files to access histogram and save as h5 file
		count = 0
		for i in root_files:

			#Define root rile and the proper histogram
			root_file = ROOT.TFile(i)			
			histogram_gg = root_file.Get("hClover_gg")

			#Define number of x and y bins in ROOT histogram
			num_bins_x = histogram_gg.GetNbinsX()
			num_bins_y = histogram_gg.GetNbinsY()

			#Define numpy array to hold histogram
			data_arr = np.zeros((5120,5120))

			#Read histogram data into numpy array
			for x_bin in range(1, num_bins_x +1):
				for y_bin in range(1, num_bins_y +1):
					bin_content = histogram_gg.GetBinContent(x_bin, y_bin)
					data_arr[x_bin - 1, y_bin - 1] = bin_content

			#Define the h5 file and add the histogram to it
			h5_name = self.sim_dir + "/sim_out_" + str(count+1) + ".h5"
			h5_file = h5py.File(h5_name, "w")
			h5_file.create_dataset("histogram_data", data=data_arr)

			#Close the files
			root_file.Close()
			h5_file.close()
			
			#Increase the count by 1
			count+=1

		print("TH2D histogram data has been written to .h5 files.") 

	#Generate h5 files of label arrays that represent level schemes
	def label(self,kernel_size=5):

		#Initialize label matrix
		label_shape = 5120
		label_arr = np.zeros((5120,5120))

		#Get list of file names for level arrays and transition matrices. Here we assume that both lists are of the same size.
		prefix_trans = self.trans_dump + "/"
		prefix_levels = self.levels_dump + "/"
		trans_list = np.char.add(prefix_trans, ML.file_list(self.trans_dump,reorder=True))
		print(trans_list)
		levels_list = np.char.add(prefix_levels, ML.file_list(self.levels_dump,reorder=True))


		#Loop over coupled elements from levels array and trans matrix to generate label data
		for n in range(len(trans_list)):

			#Read in transition matrix and level text files
			trans_mat = np.loadtxt(trans_list[n]).astype(int)
			levels_arr = np.loadtxt(levels_list[n]).astype(int)

			print("trans_list element = ", trans_list[n])
			print("levels_list element = ", levels_list[n])

			#Function that takes an index past an edge of the matrix and converts it to the edge
			def edge_lock(shape,value):
				if value >= shape:
					value = shape
				if value < 0:
					value = 0
				return value

			#Fill label array based on trans_mat and levels_arr. Fills data in a 5x5 kernel around point.
			x = -1
			y = -1
			for i in levels_arr:
				y=-1
				x+=1
				for j in levels_arr:
					y+=1
					label_arr[edge_lock(label_shape,i-2):edge_lock(label_shape,i+3),edge_lock(label_shape,j-2):edge_lock(label_shape,j+3)] = trans_mat[x,y]			

			#Save label matrix as .h5 file in training set
			save_name = self.label_dir + "/" + "label_" + str(n+1) + ".h5"

			#Create and save h5 file
			h5_file = h5py.File(save_name, "w")
			h5_file.create_dataset("label_data", data=label_arr)

			#Close h5 file
			h5_file.close()
		print("Level scheme label data has been written to h5 files.")

		
