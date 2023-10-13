###################################
# Date: 10/01/23
# Purpose: Create contig databases for each sequence, as well as an external genomes file.
# Requirements from the user:
#   - you change the value of TRIAL to the genus/species you're working with
#   - you change fasta_filepath to wherever your fasta files are located
#   - ensure that the assembled fasta sequences are within fasta_filepath
#   - ensure that conda is used to activate anvio, and anvio is up to date (7.1)
###################################

import glob #Creates a list of strings of all files within a directory
import subprocess #Lets you run command-line commands in python
import os #Good module for working with files

## Constants
TRIAL = "Erwinia"# fill this in with the name of the genus when running

## Global Variables
## fasta_filepath is the absolute path where the fasta files are located
fasta_filepath = os.path.expanduser(f"/Users/maxhomm/Documents/biol_469/final_project/pipeline_data")
files_list = glob.glob(f"{fasta_filepath}/*")

def create_databases():
    '''
    Creates a db for each element in files_list, which should be a filename of a
        fasta sequence.
    create_database: (listof Str) -> None
    Effects:
        Every filename in lst has its own db created
    '''
    for i in range(len(files_list)):
        index = files_list[i]
        if index.endswith(".fna"):
            with open(index) as current_file:
                species_id = current_file.readline().split(' ')[2]
                file_id = index.split("/")[-1]
                subprocess.run(f"anvi-script-reformat-fasta -o {species_id}.fna --simplify-names {file_id}", shell=True)
                subprocess.run(f"anvi-gen-contigs-database -f {fasta_filepath}/{species_id}.fna -o {species_id}.db", shell= True)
                subprocess.run(f"anvi-run-hmms -c {species_id}.db", shell= True)

def create_external_genomes_file():
    '''
    Creates a TSV file so that anvio knows exactly which databases correspond to
        which genome.
    '''
    with open(f"{TRIAL}_external-GENOMES.txt", 'w') as external_file:
        external_file.write("name" + '\t' + "contigs_db_path" + '\n')
        files_list = glob.glob(f"{fasta_filepath}/*")
        for subject in files_list:
            if not subject.endswith("genomic.fna") and subject.endswith(".fna"):
                species_id = subject.split('/')[-1].split('.')[0]
                external_file.write(f"{species_id}\t{species_id}.db\n")

