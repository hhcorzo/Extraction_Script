#!/usr/bin/python
################################
""" Extraction Utilities""" ####
################################
from urllib2 import urlopen, Request
from urllib2 import quote
from urllib2 import URLError
import json
import re
import sys
import os
#My current path
path=os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

import Mol_data_base



def reverse(xfile):
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



def reversex2(xfile):
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
    

def Extgeom(zline,zfile):
    znline=''
    if 'Redundant' in zline:
        znl=True
        while znl:
         zlineadd=zfile.next().strip()
         if 'Recover' not in zlineadd:
             znline+=zlineadd+'\n'
         elif 'Recover' in zlineadd:    
             znl=False
             break  
    return znline    

    
def getMolResults(name):
    url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/property/IUPACName,MolecularFormula/JSON' % quote(name)
    try:
        response = urlopen(url)
    except URLError as e:
        msg = "\tPubchemError\n%s\n\treceived when trying to open\n\t%s\n" % (str(e), url)
        msg += "\tCheck your internet connection, and the above URL, and try again.\n"
        raise ValidationError(msg)
    data = json.loads(response.read().decode('utf-8'))
    results = []
    for d in data['PropertyTable']['Properties']:
        BaseInfo = Mol_data_base.DataMol(d['CID'], d['IUPACName'], d['IUPACName'])
        results.append(BaseInfo)
    return results


def gjf_gene(zpath,zgeom,zchar,zmult,zmeth,zbasis,zname,zgjfdir,zproc,zextras):
    
    gjf_Dir=zpath+zgjfdir+'/'+str(zchar)+str(zmult)
    zbasis_name=zbasis.replace('-','')
    zN_cores='%nprocshared='+str(zproc)+'\n'
    gjf_name=str(zname)+'_'+zbasis+".gjf"
    zComm='#P '+ zmeth+' '+zbasis+' '+zextras+'\n\n'
    if not os.path.exists(gjf_Dir):
            os.makedirs(gjf_Dir)
            
    file=open(gjf_Dir+'/'+gjf_name,"w")
    file.write(zN_cores+zComm+str(zname)+'\n\n'+str(zchar)+\
    ' '+str(zmult)+'\n'+zgeom+'\n\n')
    file.close()


###Test getMolResults
results = getMolResults("5-aminolevulinic acid")
#results = getMolResults("Anilin")
for r in results:
        print(r) #ID
        print(r.getMoleculeString())   #Coordinates         

    