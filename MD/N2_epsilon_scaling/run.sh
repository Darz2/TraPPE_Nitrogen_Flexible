#!/bin/bash

folder="N2_TRAPPE_FLEX-8"
src="src"
specie="N2"
temperature=("300")
pressure=("120" "140" "160" "180" "200")
iter=1
size=("400")
# Boltzmann constant (kcal/(mol·K))
boltzmann_constant=0.0019872041
epsilon_in_K=54


for T in ${temperature[@]}
do  
    for P in ${pressure[@]}
    do
                
        seed=$(( $iter * 1000))

        fold="$folder/T_${T}_P_${P}"

        if [ -d "$folder/T_${T}_P_${P}" ]; then
            rm -r ${fold}
        fi

        mkdir -p ${fold}
        mkdir ${fold}/init

        cp src/simulation.in                       ./
        cp src/Running_Density.py                  ./
        cp src/submit_H.sh                         ./

        energy=$(echo "scale=4; $epsilon_in_K * $boltzmann_constant" | bc)

        sed -i "s/T_VAL/${T}/g"                     simulation.in  
        sed -i "s/P_VAL/${P}/g"                     simulation.in  
        sed -i "s/R_VAL/${seed}/g"                  simulation.in
        sed -i "s/E_VAL/${energy}/g"                simulation.in

        sed -i "s/TEMP/${T}/g"                      submit_H.sh  
        sed -i "s/PRESS/${P}/g"                     submit_H.sh    

        sed -i "s/T_VAL/${T}/g"                     Running_Density.py
        sed -i "s/P_VAL/${P}/g"                     Running_Density.py
        sed -i "s/MOLECULE_DEF/${specie}/g"         Running_Density.py

        mv simulation.in                            ${fold}
        mv Running_Density.py                       ${fold}
        mv submit_H.sh                              ${fold}

        cp src/N2.xyz                              ${fold}/init
        cp src/N2.ff                               ${fold}/init

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