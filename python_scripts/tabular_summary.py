###################################
# Date: 11/17/23
# Purpose: parses through the summary file to create a tsv file with some relevent
#           information for each species (Number of COG, KEGG annotations, genes,
#           genome size, GC content, etc).
###################################

## interest file should be the summary file produced by anvio. update the variable below accordingly
interest_file = ""

def count_unique_and_core_genes():
    '''
    Prints a dictionary of all counts for the species and core genes. This dictionary
    will be manually copied into a summary table.
    '''
    species_dict = {'core': 0}
    with open(interest_file) as file:
        for line in file:
            if not line.startswith('unique_id'): #excludes the first line
                bin_name = line.split('\t')[2]
                if bin_name != "":
                    if bin_name == 'core_genome':
                        species_dict['core'] += 1
                    else:
                        species_name = line.split('\t')[3]
                        if species_name not in species_dict:
                            species_dict[species_name] = 1
                        else:
                            species_dict[species_name] += 1
    print(f"Unique and core genes: {species_dict}")

def count_total_genes():
    '''
    Counts the total number of genes in each strain. This dictionary will only
    be printed as it will be manually copied into a summary table.
    '''
    count_dict = {}
    with open(interest_file) as file:
        for line in file:
            if not line.startswith('unique_id'): #excludes the first line
                species_name = line.split('\t')[3]
                if species_name not in count_dict:
                    count_dict[species_name] = 1
                else:
                    count_dict[species_name] += 1
    print(f"Total genes: {count_dict}")

if __name__ == '__main__':
    count_unique_and_core_genes()
    count_total_genes()