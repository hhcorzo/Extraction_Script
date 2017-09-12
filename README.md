# Extraction_Script
Test_Repo

the log file is the file use to test the script. The Excel file is the file generted by the scrip. 
Extraction.py will look for the information in the Gaussian file and extract the info to later report it in a xlsx file.  Extraction.py also could use the info to do new inputs and or some statistical analysis. This Extraction.py is a variation of some old codes done long ago to extract information about binding energies from a Gaussian file. This script is faster than my old codes and is addapted to a normal G16 output file. This scrip does not need the help of bash and needs less memory for searching beacuse I don't need to read the whole file in mem I just read line by line. I also use specific keys for serching information from a log file.  

TODO:
I need to add a routine to make a gjf file for the next calculation and test it with a large set of more files. I also need to dynamically set the variables to search depending on the type of calculation as well as add new keys and add a flag to stop searching when all the kwords where found. I also need to make a function to auto run depending on the shell. I also need to make it more user-friendly.     
