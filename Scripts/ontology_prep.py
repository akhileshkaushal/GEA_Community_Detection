"""
Created on Thu Mar 31 21:58:59 2016

@author: LiaHarrington

ontology_prep.py

Usage:

Used to prepare data for use in enrichment_testing and community_detection

Description:

Prepares ontology data for enrichment and community detection analysis.
First, it creates the list of list of genes in ontology and then it removes
any genes in KEGG but not in IMP. Read in and parse data into dictionary of
pathways to form gene ontology. Saves path names in path names and all genes
in each pathway as a list of list in path_genes. Assumes tab delination and
that pathway name is the first string and the gene symbols start as 3rd string.
PATH_NAMES and PATH_GENES are created global variables.

"""
import pandas as pd
import pickle
import sys
import os


def prepare_ontology(ontology_filename, ontology):
    '''
    Description
    Prepares ontology pathway names and genes list and saves outputs as
    pickle files

    Arguments
    :ontology_filename: name of ontology file of interest
        options include:
            -c2.cp.kegg.v5.1.entrez.gmt.txt
            -PID.Entrez.DB.txt
    :ontology: string name of ontology of interest
        options include:
            -KEGG
            -PID

    Output
    pickle files of PATH_GENES (dictionary of genes for ontology by path
    number), ALL_GENES (list of all genes in the ontolgoy), PATH_NAMES (list of
    names of each ontology pathway), and IMP_GENES (list of all genes in IMP)
    '''

    # Initiate GLOBAL VARIABLES

    PATH_NAMES = []
    PATH_GENES = []

    # Note ALL_GENES is also a global variable
    # -------------------------------------------------------------------------

    ontology_file = os.path.join('Data', ontology_filename)
    try:
        with open(ontology_file) as FHAND:
            for line in FHAND:
                line = line.rstrip().split('\t')
                PATH_NAMES.append(line[0])
                PATH_GENES.append(line[2:len(line)])

    except:
        print 'File not found.'

    # -------------------------------------------------------------------------
    # Read in full IMP network and determine set difference between IMP and
    # KEGG and set new path_genes to exclude those genes.
    # -------------------------------------------------------------------------

    try:
        # read in all IMP genes
        edge_file = os.path.join('Data', 'global_average.filtered.dat')
        EDGE_LST = pd.read_table(edge_file, header=None)

        # set of unique IMP genes
        IMP_GENES = set(EDGE_LST[0]).union(set(EDGE_LST[1]))

        # convert IMP gene from int to string
        IMP_GENES = set([str(gene) for gene in IMP_GENES])

        # unlists genes
        ALL_GENES = set([genes for path in PATH_GENES for genes in path])

        # finds genes in ontology not in IMP
        DIFF = list(ALL_GENES.difference(IMP_GENES))

        # creates gene ontology wo/o genes in ontology but not in IMP
        PATH_GENES2 = []
        for path in PATH_GENES:
            path = [gene for gene in path if gene not in DIFF]
            PATH_GENES2.append(path)

        PATH_GENES = PATH_GENES2

        # This version removes any genes in IMP but not in ontology
        # unlists genes
        ALL_GENES = set([genes for path in PATH_GENES for genes in path])

    except:
        print 'Invalid edege-list.'

    path_genes_file = os.path.join('Data',
                                   '{}_path_genes.pkl'.format(ontology))
    pickle.dump(PATH_GENES, open(path_genes_file, 'w'))

    all_genes_file = os.path.join('Data', '{}_all_genes.pkl'.format(ontology))
    pickle.dump(ALL_GENES, open(all_genes_file, 'w'))

    path_names_file = os.path.join('Data',
                                   '{}_path_names.pkl'.format(ontology))
    pickle.dump(PATH_NAMES, open(path_names_file, 'w'))

    imp_genes_file = os.path.join('Data', 'IMP_genes.pkl')
    pickle.dump(IMP_GENES, open(imp_genes_file, 'w'))

if __name__ == '__main__':
    ontology_filename = sys.argv[1]
    ontology = sys.argv[2]
    prepare_ontology(str(ontology_filename), str(ontology))
