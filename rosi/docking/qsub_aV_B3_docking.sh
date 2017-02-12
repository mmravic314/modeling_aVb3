#!/bin/bash                         #-- what is the language of this shell
#                                  #-- Any line that starts with #$ is an instruction to SGE
#$ -S /bin/bash                     #-- the shell for the job
#$ -o /netapp/home/mmravic/CHAMP/modeling_aVb3/rosi/docking #-- output directory (fill in)
#$ -cwd                            #-- tell the job that it should start in your working directory
#$ -r y                            #-- tell the system that if a job crashes, it should be restarted
#$ -j y                            #-- tell the system that the STDERR and STDOUT should be joined
#$ -l mem_free=1G                  #-- submits on nodes with enough free memory (required)
#$ -l arch=linux-x64               #-- SGE resources (CPU type)
#$ -l netapp=1G,scratch=1G         #-- SGE resources (home and scratch disks)
#$ -l h_rt=60:00:00                #-- runtime limit (see above; this requests 24 hours)
#$ -t 1-20                        #-- remove first '#' to specify the number of
                                   #-- tasks if desired (see Tips section)

# start fom job #1
inx=1

#Determine which job/index to stop on
taskID=$SGE_TASK_ID
#taskID=10

## Loop through a list, incrementing $inx each time. 
# Here, list is an array of directory pathes: ms1_trial_1, ms1_trial_2, ...etc
# The looping variable is the path to each directory
for pdb in /netapp/home/mmravic/CHAMP/modeling_aVb3/rosi/docking/prepack*.pdb
	
	do 
	
	# stop the loop and execute command when the increment, $inx, is equal to the job/task number 
	if [ $inx -eq $taskID ]
			then
				echo $pdb
				## Perform job script... here a python script that calles rosetta... 
				# but this line can more simply be the command line calling rosetta itself
				/netapp/home/mmravic/bin/Rosetta/source/bin/mp_dock.linuxgccrelease -in:file:s $pdb -score:weights mpframework_docking_fa_2015.wts -mp:setup:spanfiles aV_B3_apart.span -mp:scoring:hbond -packing:pack_missing_sidechains 0 -docking:partners A_B -nstruct 3000 -out:overwrite -out:prefix outputs/ -ignore_zero_occupancy false > std.txt
                                rm std.txt
				break 

			fi
			# Increment 
			inx=$(( inx + 1))
	
	done
	
exit


########### ALTERNATIVE !!  ##########
# You can look through lines of a list file with:
# > qsub_script.sh list_of_stuff.txt 

while read -r line
	do 
		
			if [ $inx -eq $SGE_TASK_ID ]
			then
				
				echo $line
				
				break

			fi
			inx=$(( inx + 1))

done < $1	
	
