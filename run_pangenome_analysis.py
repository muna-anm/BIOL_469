###################################
# Date: 10/01/23
# Purpose: Creates and runs a pangenome for each contigs db.
# Requirements from the user:
#   - ensure you adhere to the requirements from create_databases.py
###################################

import subprocess
from create_databases import *

## Constants:
THREADS = 6

def pangenomic_analysis():
    '''
    Creates a pangenome for all contig db files in the directory
    pangenomic_analysis: Str Str -> None
    '''
    subprocess.run(f"anvi-gen-genomes-storage -e {TRIAL}_external-GENOMES.txt -o {TRIAL}2-GENOMES.db", shell=True)
    subprocess.run(f"anvi-pan-genome -g {TRIAL}2-GENOMES.db --project-name {TRIAL}2 --num-threads {THREADS}", shell=True)

def display_pangenome():
    '''
    Opens up your default web browser to view the results of the analysis. pangenome
    should be the output file of the pangenomic_analysis function.
    pangenome: Str Str -> None
    '''
    ## if the anvio version is updated, un-comment below
    #subprocess.run(f"anvi-migrate {fasta_filepath}/{TRIAL}/{TRIAL}-PAN.db --migrate-safely", shell=True)

    subprocess.run(f"anvi-display-pan -g {TRIAL}2-GENOMES.db -p {fasta_filepath}/{TRIAL}2/{TRIAL}2-PAN.db", shell=True)

def display_cogs_pangenome():
    '''
    Displays the functions pangenome for cog with all annotations showing up at their
    respective locations within the various gene clusters
    '''
    ## un-comment below and run instead if you receive an error
    # subprocess.run(f"anvi-display-functions -e {TRIAL}_external-GENOMES.txt " +\
    #                 "--annotation-source COG20_FUNCTION " +\
    #                 "--profile-db COGS-PROFILE.db", shell=True)
    subprocess.run("anvi-interactive --profile-db COGS-PROFILE.db --manual", shell=True)

def display_kegg_pangenome():
    '''
    Displays the functions pangenome for kegg with all annotations showing up at their
    respective locations within the various gene clusters
    '''
    ## un-comment below and run instead if you receive an error
    subprocess.run(f"anvi-display-functions -e {TRIAL}_external-GENOMES.txt " +\
                     "--annotation-source KOfam " +\
                     "--profile-db KOFAM-PROFILE.db", shell=True)

    ##un-comment after running the above command for the first time
    #subprocess.run("anvi-interactive --profile-db KOFAM-PROFILE.db --manual", shell=True)