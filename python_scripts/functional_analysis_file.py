###################################
# Date: 11/11/2023
# Purpose: Parse through the anvio summary file and develop matplotlib stacked bar
#           plots outlining COG and KEGG proportions for all genomes, or just
#           amylovora in the case of the just_amylovora() function.
###################################

import matplotlib.pyplot as plt
import pandas as pd

def just_amylovora():
    '''
    Display a matplotlib bar chart with all gene COG categories within the
    unique amylovora only bin from Anvio.
    '''
    amylovora_dict = {}
    summary_file_path = "just_amylovora_summary.txt"
    with open(summary_file_path) as summary_file:

        # creates a dictionary of identifiers to cog functions
        for line in summary_file:
            if line.split('\t')[2] == "amylovora_only":
                unique_id = line.split('\t')[0]
                cog20_category_acc = line.split('\t')[15]
                if cog20_category_acc != "":
                    amylovora_dict[unique_id] = cog20_category_acc

        # creates a dictionary of amylovora function counts
        amylovora_count_dict = {}
        for k,v in amylovora_dict.items():
            if v not in amylovora_count_dict:
                amylovora_count_dict[v] = 1
            else:
                amylovora_count_dict[v] += 1
        sorted_amylovora_count = sorted(amylovora_count_dict.items(), key=lambda item: item[1], reverse=True)
        sorted_amylovora_count_dict = dict(sorted_amylovora_count)

        # sets up the cog categories and counts to be plotted
        amylovora_functions = list(sorted_amylovora_count_dict.keys())
        amylovora_counts = list(sorted_amylovora_count_dict.values())

        fig, ax = plt.subplots(figsize=(6, 4), gridspec_kw={'bottom': 0.5, 'top': 0.9})
        plt.bar(amylovora_functions, amylovora_counts, color='blue')
        plt.xticks(rotation=27, ha='right', fontsize=8)
        plt.xlabel('COG Functions')
        plt.ylabel('Count')
        plt.title('Erwinia Amylovora Unique Genes COG Function Distribution')
        plt.show()

def all_cog_functions():
    '''
    First, parses through the summary_file_path file.
    Create a Dictionary of dictionaries where first key is the species and value
    is an internal dictionary with COG category to count.
    Example: {amylovora: {transcription:10, ...}
    '''
    summary_file_path = "Erwinia2_gene_clusters_summary.txt"
    with open(summary_file_path) as summary_file:

        ## outer_dict should contain the dictionary of dictionaries as described
        ##      above, but unsorted
        outer_dict = {}
        for line in summary_file:
            if not line.startswith("unique_id"):
                species_name = line.split('\t')[3]
                cog_category = line.split('\t')[23] #23 is COG Category
                if species_name not in outer_dict:
                    outer_dict[species_name] = {}
                    if cog_category != "":
                        if cog_category in outer_dict[species_name]:
                            outer_dict[species_name][cog_category] += 1
                        else:
                            outer_dict[species_name][cog_category] = 1
                else:
                    if cog_category != "":
                        if cog_category in outer_dict[species_name]:
                            outer_dict[species_name][cog_category] += 1
                        else:
                            outer_dict[species_name][cog_category] = 1

        ## now it's time to sort each inner dict in order from largest to smallest
        sorted_outer_dict = {}
        for species in outer_dict:
            inner_dict = outer_dict[species]
            sorted_inner = sorted(inner_dict.items(), key=lambda item: item[1], reverse=True)
            sorted_inner_dict = dict(sorted_inner)
            sorted_outer_dict[species] = sorted_inner_dict

        ## Creates a dictionary of counts (required to make a proportion dict)
        gene_count_dict = {}
        for k,v in sorted_outer_dict.items():
            current_key_count = 0
            for k2,v2 in v.items():
                current_key_count += v2
            gene_count_dict[k] = current_key_count

        ## Creates the proportion dict that will be plotted
        proportion_dict = {}
        for k,v in sorted_outer_dict.items():
            number_species_cogs = gene_count_dict[k]
            proportion_dict[k] = {}
            for k2,v2 in v.items():
                proportion_dict[k][k2] = v2 / number_species_cogs

        ## Actually plot the proportions

        ## Creates a pandas dataframe (T refers to its transpose)
        df = pd.DataFrame(proportion_dict).T #change to sorted_outer_dict for numbers instead
        color_palette = ['#FF4500', '#9400D3', '#4FD3B7', '#5DADE2', '#FF9800',
                         '#229954', '#CD6155', '#e377c2', '#5D4037', '#9467bd',
                         '#CA6F1E', '#FFEE58', '#48C9B0', '#1A5276', '#D4AC0D',
                         '#7CB342', '#CC0099', '#BB8FCE', '#8D6E63', '#FF7043',
                         '#1976D2', '#FF0000', '#666600', '#6C3483', '#FF0000',
                         '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF',
                         '#FF8000', '#8000FF', '#0080FF', '#FF0080', '#80FF00',
                         '#00FF80', '#800000', '#008000', '#000080', '#808000',
                         '#800080', '#008080', '#808080', '#FFC0CB', '#FFD700',
                         '#FFA500', '#00FF00', '#00FFFF', '#0000FF', '#800000',
                         '#008000', '#000080', '#808080', '#FF1493']

        ## Plots the data as a stacked bar chart
        ax = df.plot(kind="bar", stacked=True, color=color_palette)

        ## Designs the legend
        pos = ax.get_position()
        ax.set_position([pos.x0, pos.y0, pos.width * 0.9, pos.height])
        handles, labels = ax.get_legend_handles_labels()

        ## Displays only the first 25 COG categories in the legend
        ax.legend(reversed(handles[0:25]), reversed(labels[0:25]),
                  title='25 Largest COG Categories - Proportions',
                  loc='center right', bbox_to_anchor=(1.86, 0.5))

        ## Sorts out the title and the x/y-axis labels
        ax.set_title('Erwinia COG Category Proportions')
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.xlabel('14 Erwinia Species')
        plt.ylabel('Number of Annotated Genes')
        plt.subplots_adjust(bottom=0.15, right=0.55, left = 0.05)
        plt.show()

def all_kegg_functions():
    '''
    First, parses through the summary_file_path file.
    Create a Dictionary of dictionaries where first key is the species and value
    is an internal dictionary with KEGG category to count.
    Example: {amylovora: {transcription:10, ...}
    '''
    summary_file_path = "all_kegg_and_cog.txt"
    with open(summary_file_path) as summary_file:

        ## outer_dict should contain the dictionary of dictionaries as described
        ##      above, but unsorted
        outer_dict = {}
        for line in summary_file:
            try:
                if not line.startswith("unique_id"):
                    species_name = line.split('\t')[3]
                    cog_category = line.split('\t')[-2]
                    if species_name not in outer_dict:
                        outer_dict[species_name] = {}
                        if cog_category != "":
                            if cog_category in outer_dict[species_name]:
                                outer_dict[species_name][cog_category] += 1
                            else:
                                outer_dict[species_name][cog_category] = 1
                    else:
                        if cog_category != "":
                            if cog_category in outer_dict[species_name]:
                                outer_dict[species_name][cog_category] += 1
                            else:
                                outer_dict[species_name][cog_category] = 1
            except:
                continue

        ## now it's time to sort each inner dict in order from largest to smallest
        sorted_outer_dict = {}
        for species in outer_dict:
            inner_dict = outer_dict[species]
            sorted_inner = sorted(inner_dict.items(), key=lambda item: item[1], reverse=True)
            sorted_inner_dict = dict(sorted_inner)
            sorted_outer_dict[species] = sorted_inner_dict

        ## Creates a dictionary of counts (required to make a proportion dict)
        gene_count_dict = {}
        for k,v in sorted_outer_dict.items():
            current_key_count = 0
            for k2,v2 in v.items():
                current_key_count += v2
            gene_count_dict[k] = current_key_count

        ## Creates the proportion dict that will be plotted
        proportion_dict = {}
        for k,v in sorted_outer_dict.items():
            number_species_cogs = gene_count_dict[k]
            proportion_dict[k] = {}
            for k2,v2 in v.items():
                proportion_dict[k][k2] = v2 / number_species_cogs

        ## Actually plot the proportions

        ## Creates a pandas dataframe (T refers to its transpose)
        df = pd.DataFrame(sorted_outer_dict).T
        color_palette = ['#FF4500', '#9400D3', '#4FD3B7', '#5DADE2', '#FF9800',
                         '#229954', '#CD6155', '#e377c2', '#5D4037', '#9467bd',
                         '#CA6F1E', '#FFEE58', '#48C9B0', '#1A5276', '#D4AC0D',
                         '#7CB342', '#CC0099', '#BB8FCE', '#8D6E63', '#FF7043',
                         '#1976D2', '#FF0000', '#666600', '#6C3483', '#FF0000',
                         '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF',
                         '#FF8000', '#8000FF', '#0080FF', '#FF0080', '#80FF00',
                         '#00FF80', '#800000', '#008000', '#000080', '#808000',
                         '#800080', '#008080', '#808080', '#FFC0CB', '#FFD700',
                         '#FFA500', '#00FF00', '#00FFFF', '#0000FF', '#800000',
                         '#008000', '#000080', '#808080', '#FF1493']

        ## Plots the data as a stacked bar chart
        ax = df.plot(kind="bar", stacked=True, color=color_palette)

        ## Designs the legend
        pos = ax.get_position()
        ax.set_position([pos.x0, pos.y0, pos.width * 0.9, pos.height])
        handles, labels = ax.get_legend_handles_labels()

        ## Displays only the first 25 COG categories in the legend
        ax.legend(reversed(handles[0:25]), reversed(labels[0:25]),
                  title='25 Largest KEGG Categories - Numbers',
                  loc='center', bbox_to_anchor=(1.86, 0.5))

        ## Sorts out the title and the x/y-axis labels
        ax.set_title('Erwinia KEGG Category Proportions')
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.xlabel('8 Erwinia Species')
        plt.ylabel('Number of Annotated Genes')
        plt.subplots_adjust(bottom=0.15, right=0.55, left = 0.05)
        plt.show()

## replace 'pass' with any of the 3 functions above
if __name__ == "__main__":
    pass