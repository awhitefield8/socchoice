import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


def plot_condorcet_graph(DF,title):
    ''' taking in df, and plots a condorcet graph
    the df contains rankings where lower ranking mean high preference. column names are alturnatives
    Args,
        df: data frame where columns are alturnatives with rankings as values 
    Returns:
        plots a networks object
    '''
    ###setup
    options = list(DF.columns)
    combs = list(combinations(options,2))
    
    ###compute orderings
    edge_list = []
    for pair in combs:
        if np.mean(DF[pair[0]] < DF[pair[1]]) > 0.5:
            res = (pair[0],pair[1])
        else:
            res = (pair[1],pair[0])
        edge_list.append(res)
    
    ###learn about graph

    #setup graph object
    G = nx.DiGraph()
    G.add_edges_from(edge_list)
    pos = nx.circular_layout(G)

    topological_sort = list(nx.topological_sort(G)) #returns nodes in order
    condorcet_winner = topological_sort[0]
    topological_ordering = [(topological_sort[i],topological_sort[i+1]) for i in range(len(topological_sort)-1)]

    ### plot graph
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set_title(title,fontsize = 20)

    #draw graph base
    nx.draw_circular(G, 
                     width=1.0, 
                     alpha=0.3,
                     nodelist=topological_sort[1:len(topological_sort)],
                     edge_color="tab:grey",
                     node_color="tab:grey",
                     node_size=1000)

    #draw topoligcal ordering
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=topological_ordering,
        width=6,
        alpha=0.3,
        edge_color="tab:red",
    )

    #add lables
    nx.draw_networkx_labels(G, pos, font_size=14, font_color="black")

    #draw winner
    nx.draw_networkx_nodes(G,
                           pos,
                           nodelist=[condorcet_winner],
                           alpha=0.3,
                           node_color="tab:blue",
                           node_size=1000)