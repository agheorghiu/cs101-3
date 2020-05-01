import networkx as nx
import matplotlib.pyplot as plt
import time

times = []

for t in range(20, 210, 10):
    print(t)
    tin = time.perf_counter()
    G = nx.to_undirected(nx.generators.community.gaussian_random_partition_graph(t, 20, 10, 0.5, 0.5, directed=False))
    print(nx.algorithms.clique.graph_clique_number(G))
    tout = time.perf_counter()
    print(tout - tin)
    times += [(t, tout - tin)]

plt.scatter(*zip(*times))
plt.xlabel('Number of vertices')
plt.ylabel('Time (seconds)')
plt.title('Finding the largest clique')
plt.show()


