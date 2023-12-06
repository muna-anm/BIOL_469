############################
## Date: 12/06/23
## Purpose: Script to Run PROKKA on Multiple Genomes in a Directory
############################

#!/bin/bash

for file in *.fna; do prokka $file --outdir "$file".prokka.output --prefix PROKKA_$file; echo $file; done