#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[3]:


import json
import csv
import pandas as pd


# ### Reading json file
# the file we are using is the file we obtained as a result from question 1

# In[2]:


f = open('neighbor-districts-modified.json')
data = json.load(f)
data


# ### Creating Graph

# In[4]:


class Graph:
    def __init__(self, graph_dict=None):
        if graph_dict is None:
            graph_dict = {}
        self.graph_dict = graph_dict
    
    def addNode(self, node):
        self.graph_dict[node] = []
    
    def addEdge(self, source, dest):
        self.graph_dict[source].append(dest)
    
    def getAllEdges(self):
        edges = []
        for node in self.graph_dict:
            for neighbor in self.graph_dict[node]:
                edges.append([node, neighbor])
        return edges


# ### adding node and edges to the graph

# In[5]:


graph = Graph()
for district in data:
    graph.addNode(district)

for district in data:
    for neighbor in data[district]:
        graph.addEdge(district, neighbor)


# ### writing edge list in csv file

# In[6]:


feilds = ['District1', 'District2']
rows = graph.getAllEdges()
file_name = "edge-graph.csv"
with open(file_name,'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(feilds)
    csvwriter.writerows(rows)


# In[7]:


df = pd.read_csv("edge-graph.csv")
df.head()

