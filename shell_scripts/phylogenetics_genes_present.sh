############################
## Date: 12/06/23
## Purpose: Determines Whether Marker Genes are Present in Genome
############################

#!/bin/bash

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "" > "$dir"_genespresent

genes=("atpD" "carA" "infB" "gyrB" "recA" "rpoB" "acnB" "gltA")

for gene in "${genes[@]}"; do
    gene_match=$(grep "$gene" *.tsv | awk '{print $1}')
    if [ -n "$gene_match" ]; then
        echo "$gene" >> "$dir"_genespresent
    fi
done

## Directly tells user how many genes are present

grep -v '^$' "$dir"_genespresent | wc -l