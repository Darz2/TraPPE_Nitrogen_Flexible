#!/bin/bash

src="src"
specie="N2"
temperatures=(300) 
pressures=("100" "120" "140" "160" "180" "200")
size=("500")
iter=1
block=5
sim=2

# Snellius

# module load 2024
# module load OpenMPI/5.0.3-GCC-13.3.0
# export I_MPI_PMI_LIBRARY=/cm/shared/apps/slurm/current/lib64/libpmi2.so

# Delftblue

module load 2024r1
module load openmpi


for T in ${temperatures[@]}
do
    for P in ${pressures[@]}
    do
        for ((i=1; i<=block; i++))
        do
            for ((j=1; j<=sim; j++))
            do
                seed=$(( $iter * 1000))
                fold="T_${T}_1/T_${T}_P_${P}/block_${i}/sim_${j}"

                if [ -d "T_${T}_1/T_${T}_P_${P}/block_${i}/sim_${j}" ]; then
                    rm -r ${fold}
                fi

                mkdir -p ${fold}
                mkdir ${fold}/init

                cp src/simulation.in                       ./
                cp src/Running_Density.py                  ./
                cp src/submit_D_NPT.sh                         ./

                sed -i "s/T_VAL/${T}/g"                     simulation.in  
                sed -i "s/P_VAL/${P}/g"                     simulation.in  
                sed -i "s/R_VAL/${seed}/g"                  simulation.in 

                sed -i "s/T_VAL/${T}/g"                     Running_Density.py
                sed -i "s/P_VAL/${P}/g"                     Running_Density.py
                sed -i "s/MOLECULE_DEF/${specie}/g"         Running_Density.py

                sed -i "s/TEMP/${T}/g"                      submit_D_NPT.sh
                sed -i "s/PRESS/${P}/g"                     submit_D_NPT.sh
                sed -i "s/BLOCK/${i}/g"                     submit_D_NPT.sh
                sed -i "s/SIM/${j}/g"                       submit_D_NPT.sh

                mv simulation.in                            ${fold}
                mv Running_Density.py                       ${fold}
                mv submit_D_NPT.sh                          ${fold}

                cp src/N2.xyz                              ${fold}/init
                cp src/N2.ff                                ${fold}/init

                Density_RP=$(python REFPROP_input.py ${T} ${P} "${specie}") 
                wait
            
                echo "The density calculated by REFPROP is: $Density_RP"
                cd ${fold}/init

                ~/Software/fftool/fftool ${size} ${specie}.xyz -r $Density_RP    > /dev/null
                ~/Software/packmol-20.14.2/packmol < pack.inp > packmol.out
                ~/Software/fftool/fftool ${size} ${specie}.xyz -r $Density_RP -l > /dev/null

                sed -i '13,25d'                             ./data.lmp
                cp data.lmp ..

                cd -

                cd ${fold}
                rm -r init
                cd - 

                iter=$((iter+1))
            done
        done
    done
done