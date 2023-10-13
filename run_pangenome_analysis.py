###################################
# Date: 10/01/23
# Purpose: Runs a pan genome analysis on sequences of interest.
# Requirements from the user:
#   - ensure you adhere to the requirements from create_databases.py
###################################

import subprocess
from create_databases import *

## Constants:
THREADS = 6

def pangenomic_analysis():
    '''
    Runs the actual analysis on genomes with the help of db.
    pangenomic_analysis: Str Str -> None
    '''
    subprocess.run(f"anvi-gen-genomes-storage -e {TRIAL}_external-GENOMES.txt -o {TRIAL}-GENOMES.db", shell=True)
    subprocess.run(f"anvi-pan-genome -g {TRIAL}-GENOMES.db --project-name {TRIAL} --num-threads {THREADS}", shell=True)

def display_pangenome():
    '''
    Opens up your default web browser to view the results of the analysis. pangenome
    should be the output file of the pangenomic_analysis function.
    pangenome: Str Str -> None
    '''
    subprocess.run(f"anvi-migrate {fasta_filepath}/{TRIAL}/{TRIAL}-PAN.db --migrate-safely", shell=True)
    subprocess.run(f"anvi-display-pan -g {TRIAL}-GENOMES.db -p {fasta_filepath}/{TRIAL}/{TRIAL}-PAN.db", shell=True)

## Run the pipeline below
if __name__ == '__main__':
    display_pangenome()