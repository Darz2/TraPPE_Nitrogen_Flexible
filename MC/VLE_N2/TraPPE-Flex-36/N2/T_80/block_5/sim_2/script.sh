#!/bin/bash

#SBATCH -J 36-N2_T_80_block_5_sim_2
#SBATCH -n 1
#SBATCH -p serial
#SBATCH -t 7-00:00:00
#SBATCH -x c[156,157,160-169,171-200]
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=d.raju@tudelft.nl
 
 ./run -g -o

