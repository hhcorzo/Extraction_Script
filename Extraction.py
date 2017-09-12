#!/usr/bin/env python

""" Data Extraction"""

_author_ ="Hector H Corzo"
_copyright_ = "Copyright 2017, Auburn, AL"

import os
import re
import openpyxl
import sys

#My current path
path=os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
#

################################################################################
""" Inf. to search in a typical Gaussian 17 log file""" ########################
################################################################################
#Keys for search in a typical Gaussian 17 log file
Gen_keys = {'Stoichiometry','(AMU),','basis:','Multiplicity'}
Status_keys={'Normal termination','Job cpu','Elapsed'}
Energy_keys={'HF=','MP2=','PG=','State='}

#Dic for data
Gen_Data={'Molecule':0,'Charge':0,'Multy':0,'Basisset':0,'Symm':0, 'Frequencies':0}
Energy_Data={'HF':0,'CCSD':0,'CCSD(T)':0,'State':0,'MP2':0, 'PG':0}
Status_Data={'Normal':0,'Days':0,'Hrs':0,'Min':0,'Sec':0, 'Date':0}

#Attributes
Molecule=('Molecule',0,1,'S')
Freq=('Frequencies',3,2,'R')
Basis=('Basisset',0,2,'S')
Charg=('Charge',0,2,'R')
Mult=('Multy',0,5,'R')
Symmt=('Symm',0,0,'S')
Day=('Days',0,2,'R')
Hrs=('Hrs',0,4,'R')
Min=('Min',0,6,'R')
Sect=('Sec',0,8,'R')
E_HF=('HF',0,1,'R')
PG=('PG',0,1,'S')
E_MP2=('MP2',0,1,'R')
State=('State',0,1,'S')

#General Dic of keys
Kserch={'State=':(1,State),'MP2=':(1,E_MP2),'HF=':(1,E_HF),'PG=':(1,PG),'Stoichiometry':(1,Molecule),'(AMU),':(1,Freq),'basis:':(1,Basis),'Multiplicity':(2,(Charg,Mult)),'Elapsed':(4,(Day,Hrs,Min,Sect))}
# !Kserch need to be dynamic and depend on the type of calculation 

##### Columns Assignation for each variable in workbook !This need to be dynamic aloc 

colLoca='A'
colfilename='B'
colMolecule='C'
colCharge='D'
colMultiplicity='E'
colBasis='F'
colPG='G'
colState='H'
colHF='I'
colStatus='J'
colDate='K'


################################
""" Extraction Utilities""" ####
################################


def readlinesreverse(xfile):
        xfile.seek(0, os.SEEK_END)
        position = xfile.tell()
        line = ''
        while position >= 0:
            xfile.seek(position)
            next_char = xfile.read(1)
            if next_char == "\n":
                yield line[::-1]
                line = ''
            else:
                line += next_char
            position -= 1
        yield line[::-1]



def readlinesreversex2(xfile):
        xfile.seek(0, os.SEEK_END)
        position = xfile.tell()
        line = ''
        L2=False
        while position >= 0:
            xfile.seek(position)
            next_char = xfile.read(1)
            if next_char == "\n":
                if L2:
                   yield line[::-1]
                   line = ''
                   L2=False
                else:
                   L2=True 
            elif next_char == " ": 
                line +=''  
            else:
                line += next_char 
            position -= 1
        yield line[::-1]        

def Jump_Line(JN,xfile):
    for i in xrange(JN):
        xfile.next().strip()
    XLine=xfile.next().strip()   
    NewLine=XLine.split()    
    return NewLine


def Ext_X(Xword,Xwords,xfile,Kserch,DicData):
    (INo,Elems)=Kserch[Xword]
    if INo==1:
        (name,y,x,Type)=Elems
        if y!=0:
           Xwords=Jump_Line(y,xfile)  
        if Type=='R':
            DicData[name]=float(Xwords[x])
        elif Type=='S':    
            DicData[name]=Xwords[x]
    elif INo>1:    
      for elem in Elems:
        (name,y,x,Type)=elem
        if y!=0:
           Xwords=Jump_Line(y,xfile)
        if Type=='R':
            DicData[name]=float(Xwords[x])
        elif Type=='S':    
            DicData[name]=Xwords[x]



def Ext_Data(Logfile):
   with open(Logfile, 'r') as f:
# Status data    
       for no,line in enumerate(readlinesreverse(f)):
            if any(x in line for x in Status_keys):
               if 'Normal termination' in line:
                   Status_keys.remove('Normal termination')
                   words=line.split()
                   Status_Data['Normal']='Yes'
                   valuesBlock='/'.join(words[6:])  
                   Status_Data['Date']=valuesBlock                 
               words=line.split()
               for word in words:
                     if word in Status_keys:
                        Status_keys.remove(word)
                        Ext_X(word,words,f,Kserch,Status_Data)
# Energy Data
       for no,line in enumerate(readlinesreversex2(f)):
            valuesBlock=''.join(line)
            if any(x in valuesBlock for x in Energy_keys): 
                valuesBlock=re.split(r'[\\\s]\s*',valuesBlock)
                for word in valuesBlock :
                    for xkey in Energy_keys:
                       if xkey in word:
                           words = word.split(xkey,1)
                           Ext_X(xkey,words,f,Kserch,Energy_Data)
                           Energy_keys.remove(xkey)
                           break  
                           
# General Data                                 
       for no, line in enumerate(f):
           words = line.split()
           for word in words:
               if word in Gen_keys:
                   Gen_keys.remove(word)
                   Ext_X(word,words,f,Kserch,Gen_Data)
   return 'extraxtion done'

## List of files to extract              
def List_Files(path,log_files_folder):
    logfiles=[]
    for path, subdirs, files in os.walk(path+log_files_folder):
        for name in files:
            file_name,extrnsion=os.path.splitext(name)
            if extrnsion=='.log':
                logfiles.append(os.path.join(path, name))
    return logfiles   
              

################################                    
"""Excel file rutines"""  ######
################################                                        
##### Prepare Excel file 
def  workbook_prep(path,Sheet_title,Exc_title):
    
    workbook = openpyxl.Workbook()  #creates openpyxl workbook




    #prepare openpyxl first
    worksheet=workbook.active
    worksheet.title=Sheet_title
    #creates worksheet Data

    #add headings to each column !This need to be dynamic and a function of de Calc. type
    worksheet[colLoca+'1']='Location'
    worksheet[colfilename+'1']='File name'
    worksheet[colMolecule+'1']='Molecule'
    worksheet[colCharge+'1']='Charge'
    worksheet[colMultiplicity+'1']='Multiplicity'
    worksheet[colBasis+'1']='Basis'
    worksheet[colPG+'1']='Point Group'
    worksheet[colState+'1']='Elec State'
    worksheet[colHF+'1']='HF'
    worksheet[colStatus+'1']='Normal Termination'
    worksheet[colDate+'1']='Date' 
    workbook.save(path+'/'+Exc_title)     #saves file
    return workbook,worksheet








def write_into_excel(path,Exc_title,workbook,worksheet,row,fileLoc,StatusD,EnergyD,GenD):
    fltion=fileLoc.split("/")
    fLoc='/'.join(fltion[:-1])
    fileName=fltion[-1]
    worksheet[colLoca+str(row)]=fLoc
    worksheet[colfilename+str(row)]=fileName
    worksheet[colMolecule+str(row)]=GenD['Molecule']
    worksheet[colCharge+str(row)]=GenD['Charge']
    worksheet[colMultiplicity+str(row)]=GenD['Multy']
    worksheet[colBasis+str(row)]=GenD['Basisset']
    worksheet[colPG+str(row)]=EnergyD['PG']
    worksheet[colState+str(row)]=EnergyD['State']
    worksheet[colHF+str(row)]=EnergyD['HF']
    worksheet[colStatus+str(row)]=StatusD['Normal']
    worksheet[colDate+str(row)]=StatusD['Date'] 
    workbook.save(path+'/'+Exc_title)
    return


    
                                                                                                                                                                        
#### Here everything working now we need to do a loop for N files and to create N files                                                                                                
files=List_Files(path,'')  
workbook,worksheet=workbook_prep(path,'first','test.xlsx')  
row=2
for currentfile in files:
  Ext_Data(currentfile)
  #write_into_excel(worksheet,row,currentfile,fileName,Status_Data,Energy_Data,Gen_Data)   
  write_into_excel(path,'test.xlsx',workbook,worksheet,row,currentfile,Status_Data,Energy_Data,Gen_Data)
  row+=1   
print  Gen_Data,Energy_Data,Status_Data






