#!/bin/bash

#SBATCH --job-name=N2_T_TEMP_P_PRESS
#SBATCH -p parallel-28
#SBATCH -n 8
#SBATCH --mem-per-cpu=2G
#SBATCH -t 5-00:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=d.raju.tudelft.nl

lmp=~/Software/lammps/src/
mpirun -np $SLURM_NTASKS $lmp/lmp_mpi < simulation.in

wait