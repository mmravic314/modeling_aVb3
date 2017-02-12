# find helical axis of chain A and rotate all atoms around this axis in 60 degree increments 
# print our those pdbs

from prody import *
import sys, os, numpy as np
from numpy import linalg as LA
from numpy import roll, diag, identity 
from math import *

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

def ang2rad( ang ):
	return ang*np.pi/180.0

def rotation_matrix( axis, angle ):
    """Generate the rotation matrix from the axis-angle notation.

    Conversion equations
    ====================

    From Wikipedia (http://en.wikipedia.org/wiki/Rotation_matrix), the conversion is given by::

        c = cos(angle); s = sin(angle); C = 1-c
        xs = x*s;   ys = y*s;   zs = z*s
        xC = x*C;   yC = y*C;   zC = z*C
        xyC = x*yC; yzC = y*zC; zxC = z*xC
        [ x*xC+c   xyC-zs   zxC+ys ]
        [ xyC+zs   y*yC+c   yzC-xs ]
        [ zxC-ys   yzC+xs   z*zC+c ]


    @param matrix:  The 3x3 rotation matrix to update.
    @type matrix:   3x3 numpy array
    @param axis:    The 3D rotation axis.
    @type axis:     numpy array, len 3
    @param angle:   The rotation angle.
    @type angle:    float
    """

    # Trig factors.
    ca = cos(angle)
    sa = sin(angle)
    C = 1 - ca

    # Depack the axis.
    x, y, z = tuple( axis )

    # Multiplications (to remove duplicate calculations).
    xs = x*sa
    ys = y*sa
    zs = z*sa
    xC = x*C
    yC = y*C
    zC = z*C
    xyC = x*yC
    yzC = y*zC
    zxC = z*xC

    # Update the rotation matrix.
    matrix  	 = np.zeros( (3,3) )
    matrix[0, 0] = x*xC + ca
    matrix[0, 1] = xyC - zs
    matrix[0, 2] = zxC + ys
    matrix[1, 0] = xyC + zs
    matrix[1, 1] = y*yC + ca
    matrix[1, 2] = yzC - xs
    matrix[2, 0] = zxC - ys
    matrix[2, 1] = yzC + xs
    matrix[2, 2] = z*zC + ca
    return matrix


inPDB 	= parsePDB( sys.argv[1] )
helixA 	= inPDB.select('chain A').copy()
helixB 	= inPDB.select('chain B').copy()

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


####### Now helix is aligned, make rotations about the z axis, then transform back to approximate helical axis 
for i in [0,60,120,180,240,300]:
	filePath 	= 'input_aV_B3-%s.pdb' % str(i)
	rotMat		= rotation_matrix( zN, ang2rad(i) )
	turned		= applyTransformation( Transformation( rotMat, np.zeros(3) ), helixA.copy() )
	inv_trans   = Transformation( LA.inv( transform.getMatrix() ) )
	final 		= applyTransformation( inv_trans, turned )
	final += helixB
	final.setTitle(filePath)
	writePDB( filePath, final )