#!/usr/bin/env python

""" Collector"""


import os
import re
import openpyxl
import sys
import stat
import json  
#My current path
path=os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

import Mol_data_base
import h_utilities 


class Gen_Data:
    def __init__(self,Molecule,Charge,Multy,Basisset,Symm,Frequencies):
     self.Molecule=Molecule
     self.Charge=Charge
     self.Multy=Multy
     self.Basisset=Basisset
     self.Symm=Symm
     self.Frequencies=Frequencies

class Energy_Data:
     def __init__(self,HF,CCSD,CCSD_T,State,MP2,PG):
        self.HF=HF
        self.CCSD=CCSD
        self.CCSD_T=CCSD_T
        self.State=State
        self.MP2=MP2
        self.PG=PG 
         
class Status_Data:
    def __init__(self,Normal,Days,Hrs,Min,Sec,Date):
        self.Normal=Normal
        self.Days=Days
        self.Hrs=Hrs
        self.Min=Min
        self.Sec=Sec
        self.Date=Date 
        
Energy_keys={'HF','State','MP2','PG'}

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

def Ener_Collector(Logpath,Logfile):
     Ekeys=[]
     with open('ksearch.json') as kfile:
            json_decoded = json.load(kfile)
            for i in Energy_keys:
                Ekeys.appen(json_decoded[i][k]) 
     with open(Logfile, 'r') as f:  
         for no,line in enumerate(h_utilities.reversex2(f)):
            if len(Energy_keys)==0:
               break 
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
                       if len(Energy_keys)==0:
                            break         
Ekeys=[]
with open('ksearch.json') as kfile:
            json_decoded = json.load(kfile)
            for i in Energy_keys:
                Ekeys.append(json_decoded[i]['k'])          
print( Ekeys)               