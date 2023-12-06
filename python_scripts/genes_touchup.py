###################################
# Date: 12/04/23
# Purpose: creates figures outlining unique counts vs core counts
###################################

import matplotlib.pyplot as plt
import numpy as np

## The reference file should be a CSV with 2 columns. The first column contains
##      what should be displayed on the chart (ie. gene name), and the second column
##      should contain a unique ID that should be searched in the summary file.
reference_file = "heatmap/kegg_reference_file.txt"

## Anvio generated summary file below
summary_file = "/Users/maxhomm/Documents/biol_469/final_project/pipeline_data/Erwinia2_gene_clusters_summary.txt"
unique_core_file = "/Users/maxhomm/Documents/biol_469/final_project/pipeline_data/Erwinia2/SUMMARY_unique_and_core/unique_and_core"

protein_dict = {}
species_list = ['pyrifoliae', 'unknown_DE2', 'sorbitola', 'toletana', 'amylovora',
                'unknown_Ejp617', 'beijingensis', 'tracheiphila', 'unknown_QL_Z3',
                'tasmaniensis', 'unknown_E602', 'persicina', 'billingiae', 'rhapontici']

## Step 1 -> Take the protein file input and iteratively add its contents to protein_dict
with open(reference_file) as protein_file:
    for protein_line in protein_file:
        protein_name = protein_line.split(',')[0].rstrip()
        protein_id = protein_line.split(',')[1].rstrip()
        protein_dict[protein_id] = protein_name

## Dictionary of dictionaries
##      outer dict -> species name
##      inner dict -> core: count, unique: count

## make empty dict
big_dict = {}
for item in species_list:
     big_dict[item] = {'unique': 0, 'core': 0, 'other': 0}

## list of lines in file
with open(summary_file) as sum_file:
    kegg = sum_file.readlines()

## main file
with open(unique_core_file) as uc_file:
    uc = uc_file.readlines()

for line in uc:
    species_name = line.split('\t')[3].strip()
    bin_id = line.split('\t')[2].strip()
    for kegg in protein_dict:
        if kegg in line:
            if bin_id == "core_genome":
                big_dict[species_name]['core'] += 1
            if bin_id.endswith("_only"):
                big_dict[species_name]['unique'] += 1
            if bin_id == (''):
                big_dict[species_name]['other'] += 1

count = 0
for item in big_dict:
    for item2 in big_dict[item]:
        count += big_dict[item][item2]

print(count)
