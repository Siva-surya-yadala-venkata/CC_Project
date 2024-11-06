# import matplotlib.pyplot as plt
# import numpy as np
# import hashlib
# from collections import defaultdict

# class ConsistentHashing:
#     def __init__(self, nodes):
#         self.nodes = nodes
#         self.ring = []
#         self.node_map = {}
#         for node in nodes:
#             hash_val = self._hash(node)
#             self.ring.append(hash_val)
#             self.node_map[hash_val] = node
#         self.ring.sort()

#     def _hash(self, key):
#         return int(hashlib.md5(key.encode()).hexdigest(), 16)

#     def get_node(self, key):
#         hash_val = self._hash(key)
#         for node_hash in self.ring:
#             if hash_val <= node_hash:
#                 return self.node_map[node_hash]
#         return self.node_map[self.ring[0]]


# class VirtualNodeConsistentHashing:
#     def __init__(self, nodes, virtual_nodes=3):
#         self.nodes = nodes
#         self.virtual_nodes = virtual_nodes
#         self.ring = []
#         self.node_map = {}
#         for node in nodes:
#             for i in range(virtual_nodes):
#                 virtual_node_id = f"{node}-{i}"
#                 hash_val = self._hash(virtual_node_id)
#                 self.ring.append(hash_val)
#                 self.node_map[hash_val] = node
#         self.ring.sort()

#     def _hash(self, key):
#         return int(hashlib.md5(key.encode()).hexdigest(), 16)

#     def get_node(self, key):
#         hash_val = self._hash(key)
#         for node_hash in self.ring:
#             if hash_val <= node_hash:
#                 return self.node_map[node_hash]
#         return self.node_map[self.ring[0]]


# # Simulation parameters
# nodes = ["A", "B", "C"]
# concurrency_levels = [1000, 10000, 50000, 100000, 200000]
# num_requests_per_level = 10000

# # Initialize both hashing algorithms
# chbl = ConsistentHashing(nodes)
# chvn = VirtualNodeConsistentHashing(nodes, virtual_nodes=5)

# # Data to store results
# chbl_results = defaultdict(list)
# chvn_results = defaultdict(list)

# # Simulate for each concurrency level
# for concurrency in concurrency_levels:
#     chbl_load = defaultdict(int)
#     chvn_load = defaultdict(int)
#     for i in range(num_requests_per_level):
#         key = f"request-{i + concurrency}"  # Create a unique key for each request

#         # CHBL
#         chbl_node = chbl.get_node(key)
#         chbl_load[chbl_node] += 1

#         # CHVN
#         chvn_node = chvn.get_node(key)
#         chvn_load[chvn_node] += 1

#     # Record results for each node load distribution
#     chbl_results['nodes'].append(list(chbl_load.values()))
#     chvn_results['nodes'].append(list(chvn_load.values()))

# # Calculate standard deviation of loads for each method at each concurrency level
# concurrency_levels_k = [x / 1000 for x in concurrency_levels]
# chbl_stddev = [np.std(loads) for loads in chbl_results['nodes']]
# chvn_stddev = [np.std(loads) for loads in chvn_results['nodes']]

# # Plotting Fig. 6 - Allocation Efficiency (Standard Deviation of Loads)
# plt.figure(figsize=(10, 5))
# plt.plot(concurrency_levels_k, chbl_stddev, 'r--', label="Consistent Hashing (CHBL) Std Dev")
# plt.plot(concurrency_levels_k, chvn_stddev, 'b-', label="Virtual Consistent Hashing (CHVN) Std Dev")
# plt.xlabel("Number of concurrent requests (x1000)")
# plt.ylabel("Standard Deviation of Requests per Node")
# plt.title("Comparison of Allocation Efficiency of Two Hash Algorithms (Load Variability)")
# plt.legend()
# plt.grid(True)
# plt.show()

# # Plotting Fig. 7 - Load of Each Node for CHBL and CHVN
# fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# # Subplot (a) - CHBL Load Distribution
# for i, loads in enumerate(chbl_results['nodes']):
#     axs[0].bar(np.arange(len(nodes)) + i * 0.2, loads, width=0.2, label=f"{concurrency_levels_k[i]}K")

# axs[0].set_xlabel("Nodes")
# axs[0].set_ylabel("Request allocation per node")
# axs[0].set_title("Consistent Hashing (CHBL) Node Load Distribution")
# axs[0].set_xticks(np.arange(len(nodes)) + 0.2 * (len(concurrency_levels) - 1) / 2)
# axs[0].set_xticklabels(nodes)
# axs[0].legend(title="Concurrency level (x1000)")

# # Subplot (b) - CHVN Load Distribution
# for i, loads in enumerate(chvn_results['nodes']):
#     axs[1].bar(np.arange(len(nodes)) + i * 0.2, loads, width=0.2, label=f"{concurrency_levels_k[i]}K")

# axs[1].set_xlabel("Nodes")
# axs[1].set_ylabel("Request allocation per node")
# axs[1].set_title("Virtual Consistent Hashing (CHVN) Node Load Distribution")
# axs[1].set_xticks(np.arange(len(nodes)) + 0.2 * (len(concurrency_levels) - 1) / 2)
# axs[1].set_xticklabels(nodes)
# axs[1].legend(title="Concurrency level (x1000)")

# plt.tight_layout()
# plt.show()


import matplotlib.pyplot as plt
import numpy as np
import hashlib
from collections import defaultdict

class ConsistentHashing:
    def __init__(self, nodes):
        self.nodes = nodes
        self.ring = []
        self.node_map = {}
        for node in nodes:
            hash_val = self._hash(node)
            self.ring.append(hash_val)
            self.node_map[hash_val] = node
        self.ring.sort()

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def get_node(self, key):
        hash_val = self._hash(key)
        for node_hash in self.ring:
            if hash_val <= node_hash:
                return self.node_map[node_hash]
        return self.node_map[self.ring[0]]


class VirtualNodeConsistentHashing:
    def __init__(self, nodes, virtual_nodes=3):
        self.nodes = nodes
        self.virtual_nodes = virtual_nodes
        self.ring = []
        self.node_map = {}
        for node in nodes:
            for i in range(virtual_nodes):
                virtual_node_id = f"{node}-{i}"
                hash_val = self._hash(virtual_node_id)
                self.ring.append(hash_val)
                self.node_map[hash_val] = node
        self.ring.sort()

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def get_node(self, key):
        hash_val = self._hash(key)
        for node_hash in self.ring:
            if hash_val <= node_hash:
                return self.node_map[node_hash]
        return self.node_map[self.ring[0]]


# Simulation parameters
nodes = ["A", "B", "C"]
concurrency_levels = [1000, 10000, 50000, 100000, 200000]
num_requests_per_level = 10000

# Initialize both hashing algorithms
chbl = ConsistentHashing(nodes)
chvn = VirtualNodeConsistentHashing(nodes, virtual_nodes=5)

# Data to store results
chbl_results = defaultdict(list)
chvn_results = defaultdict(list)

# Simulate for each concurrency level
for concurrency in concurrency_levels:
    chbl_load = defaultdict(int)
    chvn_load = defaultdict(int)
    for i in range(num_requests_per_level):
        key = f"request-{i + concurrency}"  # Create a unique key for each request

        # CHBL
        chbl_node = chbl.get_node(key)
        chbl_load[chbl_node] += 1

        # CHVN
        chvn_node = chvn.get_node(key)
        chvn_load[chvn_node] += 1

    # Record results for each node load distribution
    chbl_results['nodes'].append(list(chbl_load.values()))
    chvn_results['nodes'].append(list(chvn_load.values()))

# Plotting Fig. 7 - Load of Each Node for CHBL and CHVN
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Subplot (a) - CHBL Load Distribution
for i, loads in enumerate(chbl_results['nodes']):
    axs[0].bar(np.arange(len(nodes)) + i * 0.2, loads, width=0.2, label=f"{concurrency_levels[i] // 1000}K")

axs[0].set_xlabel("Nodes")
axs[0].set_ylabel("Request allocation per node")
axs[0].set_title("Consistent Hashing (CHBL) Node Load Distribution")
axs[0].set_xticks(np.arange(len(nodes)) + 0.2 * (len(concurrency_levels) - 1) / 2)
axs[0].set_xticklabels(nodes)
axs[0].legend(title="Concurrency level (x1000)")

# Subplot (b) - CHVN Load Distribution
for i, loads in enumerate(chvn_results['nodes']):
    axs[1].bar(np.arange(len(nodes)) + i * 0.2, loads, width=0.2, label=f"{concurrency_levels[i] // 1000}K")

axs[1].set_xlabel("Nodes")
axs[1].set_ylabel("Request allocation per node")
axs[1].set_title("Virtual Consistent Hashing (CHVN) Node Load Distribution")
axs[1].set_xticks(np.arange(len(nodes)) + 0.2 * (len(concurrency_levels) - 1) / 2)
axs[1].set_xticklabels(nodes)
axs[1].legend(title="Concurrency level (x1000)")

plt.tight_layout()
plt.show()
