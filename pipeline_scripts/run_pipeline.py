###################################
# Date: 11/19/23
# Purpose: Uses Anvio to run through all
###################################

from create_databases import *
from run_pangenome_analysis import *

if __name__ == '__main__':
    create_databases()
    run_cogs()
    run_keggs()
    create_external_genomes_file()
    pangenomic_analysis()
    display_pangenome()