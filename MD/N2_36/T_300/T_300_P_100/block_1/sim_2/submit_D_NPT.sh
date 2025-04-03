#!/bin/bash

#SBATCH --job-name=T_300_P_100_B_1_S_2
#SBATCH --time 1-00:00:00
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --partition=compute-p1
#SBATCH --account=research-me-pe

module load 2024r1
module load fftw openmpi
export NUM_OMP_THREADS=1

lmp=~/Software/LAMMPS/omp_lammps/build
srun --cpu-bind=verbose $lmp/lmp -in simulation.in -sf omp -pk omp 1 > slurm.out
wait
