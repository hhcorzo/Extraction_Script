"""Database wrapper"""
from urllib2 import urlopen, Request
from urllib2 import quote
from urllib2 import URLError
import xml.etree.ElementTree as ET
import json
import re
import sys
import os


class DataMol(object):

    def __init__(self, cid, mf, iupac):
        self.url = 'http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi'
        self.cid = cid
        self.mf = mf
        self.iupac = iupac
        self.natom = 0
        self.dataSDF = ''

    def __str__(self):
        return "%17d   %s\n" % (self.cid, self.iupac)

    def getSDF(self):
        if (len(self.dataSDF) == 0):
            def extract_xml_keyval(xml, key):

                matches = list(xml.iter(key))
                if len(matches) == 0:
                    return None
                elif len(matches) == 1:
                    return matches[0].text
                else:
                    print(matches)
                    raise ValidationError("""PubChem: too many matches found %d""" % (len(matches)))

            url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%d/SDF?record_type=3d' % self.cid
            req = Request(url, headers={'Accept' : 'chemical/x-mdl-sdfile'})
            try:
                self.dataSDF = urlopen(req).read().decode('utf-8')
            except URLError as e:
                msg = "Unable to open\n\n%s\n\ndue to the error\n\n%s\n\n" %(url, e)
                msg += "It is possible that 3D information does not exist for this molecule in the PubChem database\n"
                print(msg)
                raise ValidationError(msg)
        return self.dataSDF

    def name(self):
        return self.iupac

    def getCartesian(self):
        try:
            sdfText = self.getSDF()
        except Exception as e:
            raise e
        m = re.search(r'^\s*(\d+)\s+(?:\d+\s+){8}V2000$', sdfText, re.MULTILINE)
        self.natom = 0
        if (m):
            self.natom = int(m.group(1))

        if self.natom == 0:
            raise ValidationError("PubChem: Cannot find the number of atoms.  3D data doesn't appear\n" +
                            "to be available for %s.\n" % self.iupac)

        lines = re.split('\n', sdfText)
        NUMBER = "((?:[-+]?\\d*\\.\\d+(?:[DdEe][-+]?\\d+)?)|(?:[-+]?\\d+\\.\\d*(?:[DdEe][-+]?\\d+)?))"
        atom_re = re.compile(r'^\s*' + NUMBER + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*(\w+)(?:\s+\d+){12}')

        molecule_string = '{}\n\n'.format(self.iupac)

        atom_count = 0
        for line in lines:
            if (not line or line.isspace()):
                continue

            atom_match = atom_re.match(line)
            if atom_match:
                x = float(atom_match.group(1))
                y = float(atom_match.group(2))
                z = float(atom_match.group(3))
                sym = atom_match.group(4)
                atom_count = atom_count + 1
                molecule_string += "%s %10.6f %10.6f %10.6f\n" % (sym, x, y, z)
                if (atom_count == self.natom):
                    break

        return molecule_string

    def getXYZFile(self):
        try:
            temp = self.getCartesian()
        except Exception as e:
            raise
        molstr = "%d\n%s\n%s" % (self.natom, self.iupac, temp)
        return molstr

    def getMoleculeString(self):
        try:
            return self.getCartesian()
        except Exception as e:
            return e.message
            
