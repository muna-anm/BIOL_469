###################################
# Date: 11/15/23
# Purpose: creates a heat map highlighting counts for relevant genes found
#           within species_list
###################################

import matplotlib.pyplot as plt
import numpy as np

## The reference file should be a CSV with 2 columns. The first column contains
##      what should be displayed on the chart (ie. gene name), and the second column
##      should contain a unique ID that should be searched in the summary file.
reference_file = "heatmap/kegg_reference_file.txt"

## Anvio generated summary file below
summary_file = "/Users/maxhomm/Documents/biol_469/final_project/pipeline_data/Erwinia2_gene_clusters_summary.txt"

protein_dict = {}
species_list = ['pyrifoliae', 'unknown_DE2', 'sorbitola', 'toletana', 'amylovora',
                'unknown_Ejp617', 'beijingensis', 'tracheiphila', 'unknown_QL_Z3',
                'tasmaniensis', 'unknown_E602', 'persicina', 'billingiae', 'rhapontici']

## Step 1 -> Take the protein file input and iteratively add its contents to protein_dict
with open(reference_file) as protein_file:
    for protein_line in protein_file:
        protein_name = protein_line.split(',')[0].rstrip()
        protein_id = protein_line.split(',')[1].rstrip()
        protein_dict[protein_name] = protein_id

## Step 2 -> Create an empty dictionary of dictionaries
outer_dict = {}
for element in species_list:
    outer_dict[element] = {}
    for protein in protein_dict:
        outer_dict[element][protein] = 0

## Step 3 -> Create a dictionary of dictionaries
##      outer dict: strain names
##      inner dict: genes and their respective counts
with open(summary_file) as sum_file:
        lines = sum_file.readlines()

for species_name_big in species_list:
    for sum_file_line in lines:
        species_name = sum_file_line.split('\t')[3].strip()
        if species_name_big == species_name:
            for protein_pair in protein_dict:
                if protein_dict[protein_pair] in sum_file_line:
                    outer_dict[species_name_big][protein_pair] += 1

## Step 4 -> Use this dictionary of dictionaries to create/display the heatmap
# Extract labels and values
outer_labels = list(outer_dict.keys())
inner_labels = list(outer_dict[outer_labels[0]].keys())
values = np.array([[outer_dict[word][inner_word] for inner_word in inner_labels] for word in outer_labels])

# Create the actual heatmap
fig, ax = plt.subplots(figsize=(20, 18))
cax = ax.imshow(values, cmap='viridis', aspect='auto')

# Set labels
ax.set_xticks(np.arange(len(inner_labels)))
ax.set_yticks(np.arange(len(outer_labels)))
ax.set_xticklabels(inner_labels)
ax.set_yticklabels(outer_labels)

# Rotate the tick labels and set their alignment to 45 degrees
plt.setp(ax.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")

# Display the values on the heatmap
for i in range(len(outer_labels)):
    for j in range(len(inner_labels)):
        text = ax.text(j, i, str(values[i, j]), ha='center', va='center', color='w', fontsize=6)

# Adjust the position of the x-axis labels
ax.xaxis.set_ticks_position('top')
ax.set_xticks(np.arange(len(inner_labels)))
ax.set_xticklabels(inner_labels, rotation=60, ha="left", rotation_mode="anchor")

cbar = fig.colorbar(cax)

# Display the plot
plt.show()