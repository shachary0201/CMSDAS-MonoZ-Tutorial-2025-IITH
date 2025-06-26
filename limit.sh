#!/bin/bash

# Create output directory if not exists
mkdir -p limit_results

# Loop over all root files matching the pattern
for file in workspace_TEST_DMSimp_MonoZLL_*.root; do
    # Extract base name without 'workspace_TEST_' prefix and '.root' suffix
    base_name=$(echo "$file" | sed 's/^workspace_TEST_//' | sed 's/\.root$//')

    # Define output text file name
    out_txt="limit_results/${base_name}.txt"

    echo "Running combine for: $file"
    
    # Run combine and redirect both stdout and stderr to the output file
    combine -M AsymptoticLimits \
        --datacard "$file" \
        -m 125 \
        --name "$base_name" \
        --rMax=5 \
        --rMin=-10 \
        --cminFallbackAlgo Minuit2,Migrad,0:0.05 \
        --X-rtd MINIMIZER_analytic \
        --X-rtd FAST_VERTICAL_MORPH &> "$out_txt"

    echo "Output saved to $out_txt"
done
