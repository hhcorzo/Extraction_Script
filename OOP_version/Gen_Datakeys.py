#!/usr/bin/python
class Datakeys(object):
    
  def __init__(self, Dname, Kserch, Xline, Yline,Vtype) :
    self.Dname = Dname
    self.Kserch = Kserch
    self.Xline = Xline
    self.Yline= Yline
    self.Vtype= Vtype
  @staticmethod
  def create_from_rawinput():
        return Datakeys(
        raw_input("Data name:"),
        raw_input("Keyword to search:"),
        raw_input("Position in x:"),
        raw_input("Position in y:"),
        raw_input("Data type (R,S,I) :")
        )
        

  def dataname(self):
      return '{}'.format(self.Dname)  
      
  def __str__(self) :
     return"Data name: {}\n  Keyword: {}\n  Loc-x: {}\n  Loc-y: {}\n  Data type: {}\n"\
     .format(self.Dname,self.Kserch,self.Xline,self.Yline,self.Vtype)
     
    
       
  def __iter__(self):
    yield 'k', self.Kserch
    yield 'x', self.Xline
    yield 'y', self.Yline
    yield 't', self.Vtype
    

    
    
  
