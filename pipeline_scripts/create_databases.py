###################################
# Date: 10/01/23
## Purpose: Create contig databases for each sequence, as well as an external genomes file
##          for all sequences.
# Requirements from the user:
#   - you change the value of TRIAL to the genus/species you're working with
#   - you change fasta_filepath to wherever your fasta files are located
#   - ensure that the assembled fasta sequences are within fasta_filepath
#   - ensure that conda is used to activate anvio, and anvio is up to date (version 8)
###################################

from run_pangenome_analysis import *
import glob #Creates a list of strings of all files within a directory
import subprocess #Lets you run command-line commands in python
import os #Good module for working with files

## change TRIAL accordingly with the genus name
TRIAL = "Erwinia"

## Display where the fasta files are stored
fasta_filepath = os.path.expanduser(f"/Users/maxhomm/Documents/biol_469/final_project/pipeline_data")

## Creates a list of strings of all fasta files in fasta_filepath
files_list = glob.glob(f"{fasta_filepath}/*fa")

def create_databases():
    '''
    Creates a db for each element in files_list, which should be a filename of a
    fasta sequence.
    '''
    for i in range(len(files_list)):
        index = files_list[i]
        if index.endswith(".fna"):
            with open(index) as current_file:
                species_id = current_file.readline().split(' ')[2]
                file_id = index.split("/")[-1]
                subprocess.run(
                    f"anvi-script-reformat-fasta -o {species_id}.fna --simplify-names {file_id}",
                    shell=True)
                subprocess.run(
                    f"anvi-gen-contigs-database -f {fasta_filepath}/{species_id}.fna -o {species_id}.db",
                    shell=True)
                subprocess.run(f"anvi-run-hmms -c {species_id}.db", shell=True)

def run_cogs():
    '''
    Updates each of the previously made contig databases for the 8 strains
    in create_database.py to include COG functions
    '''
    for filepath in glob.glob(f"{fasta_filepath}/*.db"):
        if not subject.endswith("genomic.fna") and subject.endswith(".fna"):
            subprocess.run(f"anvi-run-ncbi-cogs -c {filepath} -T {THREADS}", shell=True)

def run_keggs():
    '''
    Updates each of the previously made contig databases for the 8 strains
    in create_database.py to include KEGG functions
    '''
    for filepath in glob.glob(f"{fasta_filepath}/*.db"):
        if not subject.endswith("genomic.fna") and subject.endswith(".fna"):
            subprocess.run(f"anvi-run-kegg-kofams -c {filepath} -T {THREADS}", shell=True)

def create_external_genomes_file():
    '''
    Creates a TSV file so that anvio knows exactly which databases correspond to
        which genome.
    '''
    with open(f"{TRIAL}_external-GENOMES.txt", 'w') as external_file:
        external_file.write("name" + '\t' + "contigs_db_path" + '\n')
        for subject in files_list:
            if not subject.endswith("genomic.fna") and subject.endswith(".fna"):
                species_id = subject.split('/')[-1].split('.')[0]
                external_file.write(f"{species_id}\t{species_id}.db\n")