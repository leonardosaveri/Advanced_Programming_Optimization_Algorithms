import os
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import numpy as np
import math
import re
from sklearn import preprocessing


'''
This is the code for the second homework. As I have specified in the "normalize_data" function, I did not succeed to
normalize correctly the data. I always had some kind of problem with the approximations.
Because I wanted to submit something, I gave all the "pixels" of the jellyfish the same brightness.

I believe that except for what in the "normalize_data" the code works, and that someone could simply implement such
function and add at line 91 "demand=p1[j, i]*sign" as commented to use this code correctly. 
'''


def how_many_files(directory):
    count = 0
    for path in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, path)):
            count += 1
    return count


def normalize_data(values):

    '''
    I have tried different normalization, but unfortunately I was not able to find a way to get the total demand == 0
    The problem that I found the most was that the sum of demands were equal to something to the order or 10^-17
    This is almost 0, so I tried different ways to return an approximated result.
    Here are some normalization that I tried:

    return (values - values.min()) / (values - values.min()).sum()*100000000000000000
    return ((values - values.min()) / (values.max() - values.min()))*100000000000000000
    return (values/values.sum())*80 if values.sum() == 80 else (values/values.sum())*39
    return preprocessing.normalize(values, norm='l1')
    return preprocessing.normalize(values, norm='l2')
    return preprocessing.normalize(values, norm='max')

    Because none of this worked, but I wanted to submit a solution anyway, I just returned here the normal pictures,
    not the normalized one.
    Because I could not use the original brightness (total demand != 0) I assigned some default values such that the
    total demand would be 0 (in line 91, to change we could put "demand=p1[j, i]*sign" as commented)
    '''

    return values


def column_distance(a, b):
    n = 0
    for i in range(80):
        if not np.all(a[:, i] == 0) and n == 0:
            n = i
            continue
        if not np.all(b[:, i] == 0) and n != 0:
            return i-n
    for i in range(n):
        if not np.all(b[:, i] == 0):
            return 80-n+i


def d(a, b):
    return distances[a + b] if a + b in distances.keys() else distances[b + a]


def print_graph(G):
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, font_color='white', node_color='blue', node_size=500, width=0.5)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    # plt.savefig("Graph.svg", format="SVG")
    plt.show()


def distances_nodes(a, b):
    if b['column'] < a['column']:
        return math.sqrt((a['row'] - b['row']) ** 2 + (a['column'] - b['column'] + 80) ** 2)
    else:
        return math.sqrt((a['row'] - b['row']) ** 2 + (a['column'] - b['column']) ** 2)


def create_graph(p1, c, sign):
    G = nx.DiGraph()
    for i in range(80):
        if not np.all(p1[:, i] == 0):
            for j in range(10):
                if p1[j, i] != 0:
                    G.add_node(c, column=i + 1, row=j + 1, demand=sign)  # demand=p1[j, i]*sign)
                    c += 1
    for i, j in combinations(G.nodes(data=True), 2):
        d = distances_nodes(i[1], j[1])
        G.add_edge(i[0], j[0], weight=d)
        G.add_edge(j[0], i[0], weight=d)
    return G, c


def get_single_graph(pic1, pic2, p1, p2):
    G1, c = create_graph(pic1, 1, -1)
    G2, c = create_graph(pic2, c, 1)
    G = nx.compose(G1, G2)
    '''
    # This is an alternative test but I think it's right the one I used
    
    for i in G1.nodes(data=True):
        for j in G2.nodes(data=True):
            G.add_edge(i[0], j[0], weight=distances_nodes(i[1], j[1]))
            G.add_edge(j[0], i[0], weight=distances_nodes(i[1], j[1]))
    '''
    for i in range(G.number_of_nodes() // 2):
        G.add_edge(i + 1, i + G.number_of_nodes() // 2, weight=d(p1, p2))
        G.add_edge(i + G.number_of_nodes() // 2, i + 1, weight=d(p1, p2))
    # print_graph(G)

    return G


def compute_emd(graph):
    return nx.min_cost_flow_cost(graph)


def get_shortest_each_time(graph, s, exclude, path=None):
    if len(exclude) == 12:
        return path
    if len(exclude) == 1:
        path = [s]
    t = ""
    shortest = float("inf")
    for e in graph.edges(s, data=True):
        if e[2]['weight'] < shortest and e[1] not in exclude:
            t = e[1]
            shortest = e[2]['weight']
    path.append(t)
    exclude.append(t)
    return get_shortest_each_time(graph, t, exclude, path)


directory = "hw2"
number_of_files = how_many_files(directory)
import_pics = []
for x in range(number_of_files):
    with open('hw2/P{0}.txt'.format(x+1), 'r') as f:
        import_pics.append([list(line.strip()) for line in f])

pics = {}
for i in range(len(import_pics)):
    pics["P{0}".format(i+1)] = normalize_data(np.array(import_pics[i], dtype='int'))

distances = {}
for i, j in combinations(range(len(pics)), 2):
    distances["P{0}".format(i+1)+"P{0}".format(j+1)] = column_distance(pics["P{0}".format(i+1)],
                                                                       pics["P{0}".format(j+1)])

graphs = {}
for i, j in combinations(pics, 2):
    graphs[(i, j)] = get_single_graph(pics[i], pics[j], i, j)

G = nx.Graph()
for i in range(12):
    G.add_node("P{0}".format(i+1))

for key in graphs:
    G.add_edge(key[0], key[1], weight=compute_emd(graphs[key]))

starting = 'P1'
ans = get_shortest_each_time(G, starting, [starting])
print_graph(G)
for i in ans:
    print(int(re.sub('[^0-9]', "", i)), end=' ')

