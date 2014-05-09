from networkx.classes.graph import Graph

__author__ = 'andocavallari'
import networkx as nx
import Ngram as gr
import matplotlib.pyplot as plt


#text
n = "aaabbbrraaa"
grams = gr.getGram(n)
Graph = gr.graph_node_computation(grams)



#Drawing graph
pos = nx.spring_layout(Graph)
nx.draw_circular(Graph)
#Drawing graph weight, specifiy edge labels explicitly

# edge_labels = dict([((u,v,),d['weight'])
#                   for u,v,d in Graph.edges(data=True)])
# nx.draw_networkx_edge_labels(Graph,pos,edge_labels=edge_labels)

plt.show()

#print(Graph.nodes())
#print(Graph.edges())

#for i,j in Graph.edges():
#    print(i + ' - '+ j +' , ' + str(Graph[i][j]['weight']))



