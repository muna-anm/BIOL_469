############################
## Date: 12/06/23
## Purpose: Extraction of Marker Genes and 16sRNA from PROKKA Files
############################

#!/bin/bash

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

## For extracting the 16sRNA

makeblastdb -in *.fna -dbtype 'nucl' -parse_seqids
cat *.gff | grep "barrnap" | awk '{ if ($7 == "-") {print $1" "$4"-"$5" minus"} else {print $1" "$4"-"$5" plus"} }' > ${dir}_rRNAs.txt
blastdbcmd -db *.fna -entry_batch ${dir}_rRNAs.txt > ${dir}_rRNAs.fa


## For extracting the 8 marker genes

makeblastdb -in *.ffn -dbtype 'nucl' -parse_seqids

atpD=$(grep "atpD" *.tsv | awk '{print $1}')
carA=$(grep "carA" *.tsv | awk '{print $1}')
infB=$(grep "infB" *.tsv | awk '{print $1}')
gyrB=$(grep "gyrB" *.tsv | awk '{print $1}')
recA=$(grep "recA" *.tsv | awk '{print $1}')
rpoB=$(grep "rpoB" *.tsv | awk '{print $1}')
acnB=$(grep "acnB" *.tsv | awk '{print $1}')
gltA=$(grep "gltA" *.tsv | awk '{print $1}')

declare -A gene_titles=(["atpD"]=$atpD, ["carA"]=$carA, ["infB"]=$infB, ["gyrB"]=$gyrB, ["recA"]=$recA, ["rpoB"]=$rpoB, ["acnB"]=$acnB, ["gltA"]=$gltA)

echo "" > ${dir}_marker.fa

for key in "${!gene_titles[@]}"
do
  value="${gene_titles[$key]}"
  value="$(echo "$value" | tr -d ',[:space:]')"  # Remove commas and leading/trailing spaces

  if [ -z "$value" ]
  then
    echo "$key is missing in genome" >> ${dir}_marker.fa
  else
    echo "Trying to retrieve entry '$value' for gene '$key'"
    echo "The following is the $key gene:" >> ${dir}_marker.fa
    blastdbcmd -entry "$value" -db *.ffn >> ${dir}_marker.fa
    if [ $? -ne 0 ]; then
      echo "Error retrieving entry '$value' for gene '$key'"  # Provides an error message if the gene is not present
    fi
  fi
done