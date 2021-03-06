# Marco Mravic DeGrado Lab 2016


# input 1: pdb to input, oriented in the membrane.. auto grabs resfile and span file  
# input 2: protocol xml file
# input 3: path to rosetta 
# input 4: path to constraints file


# output: directory called 'designs' to store output files for design trajactories

## example command line
# python ~/CHAMP/bin/champDesign_rosMem.py ~/CHAMP/a5/bb2Design/match_1/match_1.pdb ~/CHAMP/bin/helix_Design.xml ~/rosetta/



import sys, os, subprocess as sp, time
start = time.time()

# I/O

inPdb 		= sys.argv[1]
inSpan		= os.path.basename( inPdb)[:-4] + '.span'
inXML		= sys.argv[2]
inResF		= os.path.join( os.path.dirname(inPdb), 'resfile' )
inCst 		= sys.argv[3]

rosiBase 	= sys.argv[4]
rosiScrps	= os.path.join( rosiBase, 'source/bin/rosetta_scripts.linuxgccrelease' )
rosiDB 		= os.path.join( rosiBase, 'database/' )

oDir 		= os.path.join( os.path.dirname(inPdb), 'outputs_%s/' % os.path.basename( inCst )[:-4] )

if not os.path.exists( oDir ):
	os.mkdir( oDir )

if not os.path.exists( inSpan ):
	rosiSpanGen = os.path.join( rosiBase, 'source/bin/spanfile_from_pdb.linuxgccrelease')

	cmdSpan = [ rosiSpanGen, 
	'-database', rosiDB, 
	'-in:file:s', inPdb
	]

	sp.call( cmdSpan )
#

n = '20'

cmd = [  rosiScrps, 
'-parser:protocol', inXML, 					# Path to Rosetta script (see above)
'-in:file:s', inPdb,						# Input PDB structure
'-nstruct', n, 								# Generate 1000 models
'-mp:setup:spanfiles', inSpan,				# Input spanfile
'-mp:scoring:hbond', 						# Turn on membrane hydrogen bonding
'-relax:jump_move', 'true', 				# Allow jumps to move during relax
'-out:prefix', oDir,
'-packing:resfile', inResF,
'-parser:script_vars', 'cst_file=' + inCst,
'-out:overwrite',
'-packing:pack_missing_sidechains', '0' ]

print 
print cmd
print 

sp.call( cmd )

print 
print 'Entire run took this many seconds:', time.time() - start