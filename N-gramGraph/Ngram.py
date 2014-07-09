__author__ = 'andocavallari'
import math
import networkx as nx
from collections import Counter
from operator import add
#define the rank of the gram
rank = 3
#define the windowsDistance
windowsDistance = 6

class Ngram:
    def __init__(self,ngram):
        self.n = ngram
        self.e = {}
    def addNeighbour(self, neighbour):
        try: self.e[neighbour] += 1
        except KeyError: self.e[neighbour] = 1

#produce N-Gram of the text
def getGram(n):
    listGram = []
    for i in range(0,(len(n) - rank + 1)):
        gram = n[i : i + rank]
        listGram.append(gram)
    return listGram


def graph_node_computation(listGram):
    #Genera un dictionary
    Graph = nx.Graph()
    Graph.add_nodes_from(listGram)

    first = True

    nodeDic = []
    for i in range(0, len(listGram)):
        gram = Ngram(listGram[i])
        #compute neighbour
        for j in range(1,windowsDistance):
            if (i-j) >= 0 :
                gram.addNeighbour(listGram[i-j])
            if (i+j) < len(listGram) :
                gram.addNeighbour(listGram[i+j])
            elif (i-j) <= 0 and (i+j) >= len(listGram):
                break

        #primo nodo computato
        if first:
            for neighbour, w in gram.e.items():
                Graph.add_edge(gram.n, neighbour , weight = w )
            first = False
            #print(Graph.edges())
        else:
            edgeDic = gram.e
            allEdge = [gram.e]
            for node in nodeDic:
                if node.n == gram.n:
                    allEdge.append(node.e)
                    #calcolo il totale peso dei archi
                    edgeDic = dict(reduce(add, (Counter(dict(x)) for x in allEdge)))
                    #aggiorno i archi
            for neighbour, w in edgeDic.items():
                Graph.add_edge( gram.n, neighbour , weight = w )



        nodeDic.append(gram)

    return Graph

def ngrams_similarity(listGram):
    #Genera un dictionary
    d = {}
    for ngram in listGram :
        try: d[ngram] += 1
        except KeyError: d[ngram] = 1

    norm = math.sqrt(sum(x**2 for x in d.values()))
    for k, v in d.iteritems():
        #cicla per ogni chiave k nel dizionario prende il suo valore v
        d[k] = v/norm
    return d