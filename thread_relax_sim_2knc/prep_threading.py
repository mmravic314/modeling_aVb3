import sys, os, numpy as np
from prody import *

inPdb = parsePDB( sys.argv[1] )

seqs, totalSeq, stp = {1:'', 2:''}, '', 0
with open(sys.argv[2]) as fin:
	for i in fin:
		if i[0]=='>':
			stp +=1
		elif len(i) < 20: continue
		else:
			print i
			totalSeq +=i.strip()
			seqs[stp] = i.strip()


for k,v in seqs.items():
	print k, v, len(v)

stp, txt = 1, 'start\n'
for res in inPdb.iterResidues():
	resN, ch, rName = res.getResnum(), res.getChid(), res.getResname()
	
	newRes = totalSeq[stp-1]
	res.setResnum( stp )

	print resN, ch, rName, stp, newRes
	txt += '%d %s PIKAA %s\n' % ( stp, ch, newRes )
	stp +=1

oFile = open('resfile', 'w')
oFile.write(txt)
oFile.close()

writePDB( 'aVb3_2kncModel.pdb', inPdb )