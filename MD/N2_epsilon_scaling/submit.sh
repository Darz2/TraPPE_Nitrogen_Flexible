#!/bin/bash

folder="N2_TRAPPE_FLEX-8"
temperature=("300")
pressure=("120" "140" "160" "180" "200")

for T in ${temperature[@]}
do  
    for P in ${pressure[@]}
    do  

        fold="$folder/T_${T}_P_${P}"

        if [ -d "$folder/T_${T}_P_${P}" ]; then
            cd ${fold}
            sbatch submit_H.sh
            cd -
        else 
            echo "The file location is not available"
        fi

    done
done