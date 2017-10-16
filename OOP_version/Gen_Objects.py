
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
        raw_input("molecule name:"),
        raw_input("Propiety need:"),
        raw_input("Method wanted:"),
        raw_input("Ref. value:"),
        raw_input("Diff wanted:")
        ) 
    
    def molecule_name(self):
        return'{}'.format(self.molecule)
        
class Structure_search(Info_needed):

    def __init__(self,molecule=None):
       self.molecule=molecule
       self.prop=prop
       self.method=method
       self.refvalue=refvalue
       self.error=error
       Info_needed.info_need_cnt+= 1


class Molecule_info:
    num_of_molecules=0
    def __init__(self,name,charge,multy,symm,formula):
       self.name=name
       self.charge=charge
       self.multy=multy
       self.symm=symm
       self.formula=formula
       Molecule_info.num_of_molecules += 1
                                      
class Calculation_info(Molecule_info):
    num_of_ctype = 0
    def __init__(self,ctype,method,basis,extras,Molecule_info=None):

          self.Calculation_info=Calculation_info
          self.ctype=ctype
          self.method=method
          self.basis=basis
          self.extras=extras 
          if Molecule_info is None:
             self.Molecule_info=[]
          else:
             self.Molecule_info=Molecule_info      
          Calculation_info.num_of_ctype +=1
       
          
    def CalRev(self):
        return'Type: {}, Method: {}, Base: {}'.format(self.ctype,self.method,self.basis)
    def G16Key(self):
        return '#P {} {} {} {}'.format(self.method,self.basis,self.ctype,self.extras)                                
                                       
          
    def add_molecula_info(self,molinf):
        if molinf not in self.Molecule_info:
            self.Molecule_info.append(molinf)  
               
    def remove_molecula_info(self,molinf):
        if molinf in self.Molecule_info:
            self.Molecule_info.remove(molinf)
    
    def print_molecula(self):
        for molec in self.Molecule_info:
            print('Molecule: ', molec.name)                                                    
                                                         
                                                                  
                                                                           
                                                                                    
                                                                                             
                                                                                                      
                                                                                                               
                                                                                                                        
                                                                                                                                 
                                                                                                                                          
                                                                                                                                                            
 
class Comp_info:

    def __init__(self,nproc,mem):
          self.nproc=nproc
          self.mem=mem

    def G16proc(self):
        return '%nprocshared={}'.format(self.nproc)  
        
    def G16mem(self):
        return '%mem={}'.format(self.mem)       

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
        