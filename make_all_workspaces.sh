#!/bin/bash

for dir in cards-*; do
    # Since thesre datcard are in their respevctive directoiries therfoee 
    if [ -d "$dir" ] && [ -f "$dir/combined.dat" ]; then
        # Depending upon the type of partcile
        if [[ "$dir" == *"Axial"* ]]; then
            MODEL="Axial"
        elif [[ "$dir" == *"Vector"* ]]; then
            MODEL="Vector"
        elif [[ "$dir" == *"Scalar"* ]]; then
            MODEL="Scalar"
        elif [[ "$dir" == *"Pseudo"* ]]; then
            MODEL="Pseudo"
        else
            echo "Model is is not correct $dir"
            continue
        fi

        
        
        Mmed=$(echo $dir | sed -n 's/.*_\([0-9]\+\)_MXd.*/\1/p')
        Mxd=$(echo $dir | sed -n 's/.*MXd-\([0-9]\+\)/\1/p')

        
        if [[ "$MODEL" == "Scalar" || "$MODEL" == "Pseudo" ]]; then
            Mmed=$(echo $dir | sed -n 's/.*_\([0-9]\+\)_mxd.*/\1/p')
            Mxd=$(echo $dir | sed -n 's/.*mxd-\([0-9]\+\)/\1/p')
        fi

       
        outfile="workspace_TEST_DMSimp_MonoZLL_${MODEL}_${Mmed}_MXd-${Mxd}.root"

        
        echo "Generating workspace for $dir"
        text2workspace.py $dir/combined.dat -o $outfile
    fi
done
