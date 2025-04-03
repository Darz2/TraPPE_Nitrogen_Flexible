#!/bin/bash

src="files_src"
directory=$(pwd)

specie=("N2")
Temp=( $(seq 70 10 110) )

block=5
sim=2
iter=1

for T in ${Temp[@]}
do
    for ((i=1; i<=block; i++))
    do
        for ((j=1; j<=sim; j++))
        do

            fold="${specie}/T_${T}/block_${i}/sim_${j}"
            foldIn="${fold}/INPUT"

            echo ${fold}
            mkdir -p ${foldIn}

            seed=$(expr $iter \* 1000)

            cp ${src}/settings.in     ./  
            cp ${src}/topology.in     ./   
            cp ${src}/forcefield.in   ./
            cp ${src}/script.sh       ./

            sed -i "2s/K/${T}/g"                        settings.in
            sed -i "11s/seed/${seed}/g"                 settings.in
            
            sed -i "3s/name/45-${specie}_T_${T}_block_${i}_sim_${j}/g"        script.sh

            mv settings.in         ${foldIn}/
            mv topology.in         ${foldIn}/
            mv forcefield.in       ${foldIn}/
            mv script.sh           ${fold}/

            cp ${src}/run          ${fold}/
            cp ${src}/N2           ${foldIn}/

            iter=$((iter+1))
        done
    done
done
wait

# ./submit.sh

# wait