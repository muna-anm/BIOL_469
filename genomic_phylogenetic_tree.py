###################################
# Date: 10/12/23
# Purpose: Create a phylogenetic tree based on 16s rRNA protein sequences
# Requirements from the user:
#   - the create_databases.py script is run, specifically the function
#       create_external_genomes_file
###################################

import subprocess
from create_databases import *
import glob

def migrate_older_databases():
    '''
    Ensures that the files are up to date and using Anvio version 8.
    '''
    for filepath in glob.glob(f"{fasta_filepath}/*.db"):
        if not filepath.startswith("G"):
            subprocess.run(f"anvi-migrate {filepath} --migrate-safely", shell=True)


def create_concat_proteins_file():
    '''
    Creates a fasta file based on the rRNA sequences found within the external
    genomes file. If alternative genes are desired, the --gene-names tag can
    be changed.
    '''
    external_genomes_file = f"{TRIAL}_external-GENOMES.txt"
    output = f"{TRIAL}_concatenated-proteins.fa"
    subprocess.run(f"anvi-get-sequences-for-hmm-hits --external-genomes {external_genomes_file} \
                                                      -o {output} \
                                                      --hmm-source Bacteria_71 \
                                                      --gene-names Ribosomal_L1,Ribosomal_L2,Ribosomal_L3,Ribosomal_L4,Ribosomal_L5,Ribosomal_L6 \
                                                      --return-best-hit \
                                                      --get-aa-sequences \
                                                      --concatenate" , shell=True)

def run_msa():
    '''
    Uses famsa software to run a multiple sequence alignment on the protein
    fasta file created above. Ensure that all fasta entries are of the same
    length (it should just do this by default).
    '''
    concat_proteins = f"{TRIAL}_concatenated-proteins.fa"
    famsa_file = f"{TRIAL}_famsalignment.fa"
    subprocess.run(f"famsa {concat_proteins} {famsa_file}", shell=True)

def create_tree():
    '''
    Creates a phylogenetic tree in newick format.
    '''
    famsa_file = f"{TRIAL}_famsalignment.fa"
    tree = f"{TRIAL}_phylogenomic-tree.txt"
    subprocess.run(f"anvi-gen-phylogenomic-tree -f {famsa_file} \
                                                -o {tree}", shell=True)

def display_tree():
    '''
    Displays the phylogenetic tree in Anvio.
    '''
    tree_file = f"{TRIAL}_phylogenomic-tree.txt"
    subprocess.run(f"anvi-interactive -p phylogenomic-profile.db \
                                      -t {tree_file} \
                                      --title '{TRIAL} Phylogenetic Tree' \
                                      --manual", shell=True)

if __name__ == '__main__':
    migrate_older_databases()
    create_concat_proteins_file()
    run_msa()
    create_tree()
    display_tree()
