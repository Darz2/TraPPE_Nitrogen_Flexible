#!/bin/bash
#SBATCH -J name
#SBATCH -e error.log
#SBATCH --partition=compute-p1
#SBATCH --time=5-00:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=d.raju@tudelft.nl
#SBATCH --account=research-me-pe

module load 2022r2
srun ./run -g -o 
