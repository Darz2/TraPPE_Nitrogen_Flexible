#!/bin/bash

src="src"
specie="N2"
temperatures=(300) 
pressures=("100" "120" "140" "160" "180" "200")
block=5
sim=2

for T in ${temperatures[@]}
do
    for P in ${pressures[@]}
    do
        for ((i=1; i<=block; i++))
        do  
            for ((j=1; j<=sim; j++))
            do
                fold="T_${T}_1/T_${T}_P_${P}/block_${i}/sim_${j}"

                if [ -d "T_${T}_1/T_${T}_P_${P}/block_${i}/sim_${j}" ]; then
                    
                    cd ${fold}

                    sbatch submit_D_NPT.sh

                    cd - 

                else
                    echo "The file is not located in the destination directory"
                fi

            done
        done
    done
done