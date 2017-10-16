#!/usr/bin/env python

""" Setting the first file"""


import os
import re
#import openpyxl
import sys
import stat  
#My current path
path=os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

import Mol_data_base
import h_utilities 


 # Some Basis sets !add to data base
Dunning=('cc-pvDz','cc-pvTz','cc-pvQz','cc-pv5z')
Pople=('STO-3G','3-21G','6-21G','4-31G','6-31G','6-311G')

def getter_setter_gen(name, type_):
    def getter(self):
        return getattr(self, "__" + name)
    def setter(self, value):
        if not isinstance(value, type_):
            raise TypeError("%s attribute must be set to an instance of %s" % (name, type_))
        setattr(self, "__" + name, value)
    return property(getter, setter)

def auto_attr_check(cls):
    new_dct = {}
    for key, value in cls.__dict__.items():
        if isinstance(value, type):
            value = getter_setter_gen(key, value)
        new_dct[key] = value
    # Creates a new class, using the modified dictionary as the class dict:
    return type(cls)(cls.__name__, cls.__bases__, new_dct)

@auto_attr_check
class Info_needed(object):
    molecule = str
    prop=str
    method=str
    refvalue=float
    error=float
    
    info_need_cnt=0
    
    def __init__(self,molecule,prop,method,refvalue,error):
       self.molecule=molecule
       self.prop=prop
       self.method=method
       self.refvalue=refvalue
       self.error=error
       
       Info_needed.info_need_cnt+= 1

    @staticmethod
    def create_from_rawinput():
        return Info_needed(
        str(raw_input("molecule name:")),
        str(raw_input("Propiety needed:")),
        str(raw_input("Method wanted:")),
        float(raw_input("Ref. value:")),
        float(raw_input("Diff wanted:"))
        ) 
    
    def molecule_name(self):
        return '{}'.format(self.molecule)
    def method_wanted(self):
        return'{}'.format(self.method)   
    def prop_wanted(self):
        return'{}'.format(self.prop) 
    def ref_given(self):
        return'{}'.format(self.refvalue)
    def diff_wanted(self):
        return'{}'.format(self.error)           
    def type_wanted(self):
        if Info_needed.prop_wanted=='Energy':
          return ''
        if Info_needed.prop_wanted=='Opt':
            return 'Opt'
        if Info_needed.prop_wanted=='Frequencies': 
             return 'freq'
        else:
            return'{}'.format(self.prop)     

@auto_attr_check        
class Molecule_gjf:
    charge=str
    multy=str
    num_of_molecule_gjf=0
    def __init__(self,name,charge,multy):
       self.name=name
       self.charge=charge
       self.multy=multy
       Molecule_gjf.num_of_molecule_gjf += 1
    @staticmethod
    def create_from_rawinput():
        return Molecule_gjf(
        str(raw_input("what file name do you want? ")),
        str(raw_input("molecule charge:")),
        str(raw_input("molecule multy:"))
        ) 

    def filename_wanted(self):
        return'{}'.format(self.name) 
    def charge_wanted(self):
        return'{}'.format(self.charge) 
    def mult_wanted(self):
        return'{}'.format(self.multy)
    
    def G16_char_mult(self):
         return'{} {}'.format(self.charge,self.multy)           


class gjf_info:

    def __init__(self,ctype,method,basis,extras,geom):
          self.ctype=ctype
          self.method=method
          self.basis=basis
          self.extras=extras
          self.geom=geom

       
          
    def CalRev(self):
        return'Type: {}, Method: {}, Base: {}'.format(self.ctype,self.method,self.basis)
    def G16Key(self):
        return '#P {} {} {} {}'.format(self.method,self.basis,self.ctype,self.extras)                                        
    def G16geom(self):                                  
        return '{}\n'.format(self.geom)   
   

                       
class Quete_info:
    """Typical Queue system"""
    
    def __init__(self,queue,procore,timelim,qmem,runcomm):
          self.queue=queue
          self.procore=procore
          self.timelim=timelim
          self.qmem=qmem
          self.runcomm=runcomm

           
    @staticmethod
    def create_from_rawinput():
        return Quete_info(
        raw_input("Queue name? "),
        raw_input("Number or nodes? "),
        raw_input("Time limit? "),
        raw_input("Memory? "),
        raw_input("Run command? ")
        ) 
                     
    def Runcomm(self):
        return '{}'.format(self.runcomm)                          
    def Runpar(self):                                  
        return '{}\n{}\n{}\n{}'.format(self.queue,self.procore,self.timelim,self.qmem)                                        
                                                                
@auto_attr_check
class Comp_info:
    nproc=int
    mem=int
    units=str
    def __init__(self,nproc,mem,units):
          self.nproc=nproc
          self.mem=mem
          self.units=units
    def G16proc(self):
        return '%nprocshared={}'.format(self.nproc)  
        
    def G16mem(self):
        return '%mem={}'.format(self.mem) 
           
    @staticmethod
    def create_from_rawinput():
        return Comp_info(
        int(raw_input("Cores you want to use? ")),
        int(raw_input("Memory you want to use? ")),
        str(raw_input("Memory Units (eg. mw,gb ...)? "))
        ) 

@auto_attr_check
class Extra_info:
    exc=str
    def __init__(self,exc):
          self.exc=exc
          
    @staticmethod
    def create_from_rawinput():
        return Extra_info(
        str(raw_input("Do you want a report of the calculations? "))
        )  
    
def Ini_code():
    print (30 * '-')
    print ("      Main Menu")
    print (30 * '-')
    print ("1. Job settings")
    print ("2. Cores and Mem settings")
    print ("3. Extra options settings")
    print ("4. Start Calculation")
    print (30 * '-')
 
    is_valid=0  

    while not is_valid :
         try :
                 choice = int ( raw_input('Enter your choice [1-4] : ') )
                 ### Take action as per selected menu-option ###
                 if choice == 1:
                        print ("Let's set the info of what you want")
                        #BaseInfo = Info_needed.create_from_rawinput()
                        #BaseInfo = Info_needed('Anilin','Opt freq','mp2',5.0,2.2)
                        #BaseInfo = Info_needed('1,3,5-hexatriene','Opt','mp2',5.0,2.2)
                        BaseInfo = Info_needed('benzene','Opt','mp2',5.0,2.2)
                        is_valid = 0
                 elif choice == 2:
                        print ("Let's set the memory and cores you want to use")
                        CompInfo=Comp_info.create_from_rawinput()
                        #CompInfo=Comp_info(4,4,'gb')
                        is_valid = 0
                 elif choice == 3:
                        print ("Let's set some extras")
                        Extrainfo=Extra_info.create_from_rawinput()
                        #Extrainfo=Extra_info('YES')
                        is_valid = 0
                 elif choice == 4:
                        print ("Starting Calculations...\n")
                        is_valid = 1
                        return BaseInfo,CompInfo,Extrainfo   
                 else:
        
                        print ("Invalid number. Try again...")
                        is_valid = 0                 
         except ValueError, e :
                 print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])
 











def set_first_str(Name_mole):
     print(Name_mole)
     results = h_utilities.getMolResults(Name_mole)
     Nresults=len(results)
     if Nresults>1:
         i=1
         print Nresults,' were found for this name:\n'
         for r in results:
             
             print i,') ',r
             i+=1
             #print(r)
         is_valid=0
 
         while not is_valid :
            try :
                choice = int ( raw_input('What structure should we use? ') )
                if  0> choice > Nresults : 
                   print ("Invalid option. Try again...")
                   is_valid = 0   
                else:      
                  is_valid = 1 ## set it to 1 to validate input and to terminate the while..not loop
            except ValueError, e :
                 print ("'%s' is not a valid integer." % e.args[0].split(": ")[1]) 
                   
         r=results[choice-1]
         print(r)
         Mol_xyz=r.getMoleculeString()
         print(Mol_xyz)
     else:
         Mol_xyz=results[0].getMoleculeString()
         print(Mol_xyz)   
     return Mol_xyz








def gjf_gene(zpath,zcor,zmem,zcomm,zname,zmol,zchmul,zgeom,zchar,zmult):
    zgjfdir='/gjf_files'
    list_files=[]
    gjf_Dir=zpath+zgjfdir+'/'+str(zchar)+str(zmult)
    if not os.path.exists(gjf_Dir):
            os.makedirs(gjf_Dir)
            
    for zbasis in Dunning:       
        zbasis_name=zbasis.replace('-','')
        gjf_name=zname+'_'+zbasis_name+".gjf"
        list_files.append(gjf_name)
        file=open(gjf_Dir+'/'+gjf_name,"w")  
        file.write(zcor+'\n'+zmem+'\n'+zcomm+'\n\n'+zmol\
        +'\n\n'+zchmul+'\n'+zgeom.split('\n\n',1)[-1]+'\n\n')
        file.close()
    return list_files,gjf_Dir   

def quete_exe(fls,qinf,dir_gene):
    comm=qinf.Runcomm()
    with open(dir_gene+'/param', mode='w') as pfile:
         pfile.write(qinf.Runpar())
    with open(dir_gene+'/Run', mode='w') as kfile: 
         for nn in fls:          
       
          kfile.write(comm +' '+nn+'< param'+'\n')
    st=os.stat(dir_gene+'/Run')      
    os.chmod(dir_gene+'/Run', st.st_mode | stat.S_IEXEC)   


def start_process():
    Queueset=Quete_info.create_from_rawinput()  
    BaseInfo,CompInfo,Extrainfo=Ini_code()
    Look_for=BaseInfo.molecule_name() #name to look for
    #print(Look_for)
    Basexyz=set_first_str(Look_for)#geom
    basegjf=Molecule_gjf.create_from_rawinput() #general information for the imput 
    #basegjf=Molecule_gjf('test','0','1')
    methodgjf=BaseInfo.method_wanted() #method wanted
    mulgjf=basegjf.mult_wanted() #multl wanted
    chargjf=basegjf.charge_wanted() #charge wanted
    typegjf=BaseInfo.type_wanted()  #type of calculation
    procgjf=CompInfo.G16proc() #proc
    memgjf=CompInfo.G16mem() #mem
    namegjf=basegjf.filename_wanted()
    chmulgjf=basegjf.G16_char_mult()
    gjffile=gjf_info(typegjf,methodgjf,'','',Basexyz)
    geomgjf=gjffile.G16geom()
    keygjf=gjffile.G16Key()  
    files_gene,dir_gene=gjf_gene(path,procgjf,memgjf,keygjf,namegjf,Look_for,chmulgjf,geomgjf,chargjf,mulgjf)
    quete_exe(files_gene,Queueset,dir_gene)
    #print(files_gene)
    return dir_gene
    
    
#    "1,3,5-hexatriene"

print(start_process())

  
  
  
  
  
  
  
  
  
