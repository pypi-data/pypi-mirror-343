#Configuration file for ML_package
#This file may be ran to add this package directory to the user's python site packages, allowing for future imports of this package in python scripts. 

#Imports
import sys
import os

print("This configuration file must be ran from the ML_package directory on your system")

#Retrieve location of python site packages from user input
while True:
	site_path = input("Please enter the full path to your python site packages directory:")

	if os.path.isdir(site_path):
		print(f"Site packages located at {site_path}")
		break

	else:
		print("Directory not found")
exit
		
#Add ML package to user site packages 
custom_file = site_path + '/usercustomize.py'
package_dir = os.getcwd()
print(package_dir)

#Open or create usercustomize.py in site package path. append to file if existing
if os.path.isfile(custom_file):
	f = open(custom_file,"a")
	f.write("sys.path.extend([\""+str(package_dir)+"\",])")
	f.close()
else:
	f = open(custom_file,"w")
	f.write("import sys")
	f.write("\n")
	f.write("sys.path.extend([\""+str(package_dir)+"\",])")
	f.close()

print("ML_package may now be imported in python files")


