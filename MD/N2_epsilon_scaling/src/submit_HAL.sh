#!/bin/bash

#SBATCH --job-name=N2_T_TEMP_P_PRESS
#SBATCH -p highmem
#SBATCH -n 8
#SBATCH --mem-per-cpu=2G
#SBATCH -t 2-00:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=d.raju.tudelft.nl

spack load lammps/d

mpirun -np $SLURM_NTASKS --map-by core --bind-to core lmp -in simulation.in -sf omp -pk omp 1
# srun --distribution=block:cyclic --cpu-bind=cores lmp -in simulation.in -sf omp -pk omp 1