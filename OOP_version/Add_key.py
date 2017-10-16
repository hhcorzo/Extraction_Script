#!/usr/bin/python
import os
import json
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
#My current path
path=os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
import Gen_Datakeys


def Newkey():
    d={}
    new_key = Gen_Datakeys.Datakeys.create_from_rawinput()
    d[Gen_Datakeys.Datakeys.dataname(new_key)]=dict(new_key)   
    if not os.path.exists('ksearch.json'):    
         with open('ksearch.json', mode='w') as kfile:        
                json.dump(d, kfile)
    else:
        with open('ksearch.json') as kfile:
            json_decoded = json.load(kfile)
            for key in d:
              print key,d[key]
              json_decoded[key] = d[key]
        with open('ksearch.json', 'w') as kfile:
              json.dump(json_decoded, kfile)      


Newkey()
