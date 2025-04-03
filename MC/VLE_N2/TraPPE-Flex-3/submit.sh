#!/bin/bash

directory=$(pwd)

specie=("N2")
Temp=( $(seq 70 10 110) )

block=5
sim=2

for T in ${Temp[@]}
do
    for ((i=1; i<=block; i++))
    do
        for ((j=1; j<=sim; j++))
        do

            fold="${specie}/T_${T}/block_${i}/sim_${j}"
            foldIn="${fold}/INPUT"

            cd ${fold}

            sbatch script.sh  &

            cd ${directory}

        done
    done
done
wait