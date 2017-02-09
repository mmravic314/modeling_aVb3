# find helical axis of chain A and rotate all atoms around this axis in 60 degree increments 
# print our those pdbs

from prody import *
import sys, os, numpy as np
from numpy import linalg as LA
from numpy import roll, diag, identity 

def skew(v):
	if len(v) == 4: v = v[:3]/v[3]
	skv = roll(roll(diag(v.flatten()), 1, 1), -1, 0)
	return skv - skv.T

def VectorAlign(a,b):
	u = np.cross(a,b)
	s = LA.norm(u)
	c = np.dot(a,b)
	# skew-symetric by hand
	skw = skew(u)

	return identity(3) + skw + (1/(1+c)) * np.dot(skw, skw)


inPDB 	= parsePDB( sys.argv[1] )
helixA 	= inPDB.select('chain A').copy()


botAtom = helixA.select('ca resnum 33 to 36').copy()
bottoms = botAtom.getCoords()
topAtom = helixA.select('ca resnum 5 6 7 8').copy()
tops 	= topAtom.getCoords()



both 	= botAtom + topAtom

# move bundle bottom to Z axis
bottCen = calcCenter( bottoms )
overall = calcCenter(both)

moveAtoms( both, to=np.zeros(3), ag=True)

# calculate approximate helical axis vector and find rotation matrix to align it to Z & translation to put center of mass at 0
topCen 	= calcCenter( tops )
axis 	= topCen - bottCen
axisN 	= axis / LA.norm(axis)
zN 		= np.array([0,0,1])

rotation  =	VectorAlign( axisN, zN)
transform = Transformation( rotation , -overall )

applyTransformation( transform, helixA )


####### Now helix is aligned, make rotations about the z axis 