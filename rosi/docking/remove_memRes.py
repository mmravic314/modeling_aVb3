#! /usr/bin/python
from prody import *
import sys

pdb = parsePDB( sys.argv[1], chain='AB' )
writePDB( sys.argv[1], pdb )