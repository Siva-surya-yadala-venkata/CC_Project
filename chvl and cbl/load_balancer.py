import matplotlib.pyplot as plt
import numpy as np
import random
from collections import defaultdict
import hashlib

# Constants
MAX_HASH = 2**32
NUM_SERVERS = 5
VIRTUAL_NODES = 10
NUM_REQUESTS = 10000

# Function to get a consistent hash
def get_hash(value):
    return int(hashlib.sha256(value.encode('utf-8')).hexdigest(), 16) % MAX_HASH

# Consistent Hashing (CHBL)
class ConsistentHashing:
    def __init__(self, servers):
        self.ring = sorted(get_hash(server) for server in servers)
        self.servers = servers

    def get_server(self, request_id):
        request_hash = get_hash(request_id)
        for server_hash in self.ring:
            if request_hash <= server_hash:
                return self.servers[self.ring.index(server_hash)]
        return self.servers[0]

# Consistent Hashing with Virtual Nodes (CHVN)
class ConsistentHashingWithVirtualNodes:
    def __init__(self, servers, virtual_nodes=10):
        self.ring = {}
        self.servers = servers
        self.virtual_nodes = virtual_nodes
        for server in servers:
            for i in range(virtual_nodes):
                vnode_id = f"{server}-VN{i}"
                self.ring[get_hash(vnode_id)] = server
        self.sorted_keys = sorted(self.ring.keys())

    def get_server(self, request_id):
        request_hash = get_hash(request_id)
        for key in self.sorted_keys:
            if request_hash <= key:
                return self.ring[key]
        return self.ring[self.sorted_keys[0]]

# Simulation settings
servers = [f"Server-{i}" for i in range(NUM_SERVERS)]
concurrency_levels_k = [1, 10, 50, 100, 200]  # In thousands

# Arrays to hold results
chvn_requests_processed = []
chbl_requests_processed = []

# Simulate requests and calculate processed requests per second
for concurrency in concurrency_levels_k:
    chbl = ConsistentHashing(servers)
    chvn = ConsistentHashingWithVirtualNodes(servers, virtual_nodes=VIRTUAL_NODES)

    chbl_distribution = defaultdict(int)
    chvn_distribution = defaultdict(int)

    # Process NUM_REQUESTS requests to simulate distribution load
    for i in range(NUM_REQUESTS):
        request_id = f"request-{i}"
        
        # CHBL processing
        chbl_server = chbl.get_server(request_id)
        chbl_distribution[chbl_server] += 1
        
        # CHVN processing
        chvn_server = chvn.get_server(request_id)
        chvn_distribution[chvn_server] += 1

    # Calculate request processing rates (with degradation for CHBL)
    chbl_std_dev = np.std(list(chbl_distribution.values()))
    chvn_std_dev = np.std(list(chvn_distribution.values()))

    # Simulate degradation in processing rate for CHBL based on load
    chbl_processing_rate = (6000 - concurrency * 2) / (1 + chbl_std_dev + random.uniform(0, 0.2))
    chvn_processing_rate = 6000 / (1 + chvn_std_dev + random.uniform(0, 0.1))
    
    # Adjust to per 1000 requests, simulating the graph's structure
    chbl_requests_processed.append(max(0, chbl_processing_rate) / 1000)
    chvn_requests_processed.append(max(0, chvn_processing_rate) / 1000)

# Plotting the graph
plt.figure(figsize=(10, 6))
plt.plot(concurrency_levels_k, chvn_requests_processed, 'b^-', label="CHVN")
plt.plot(concurrency_levels_k, chbl_requests_processed, 'rs-', label="CHBL")

# Annotate each point with the value
for x, y in zip(concurrency_levels_k, chvn_requests_processed):
    plt.text(x, y, f"{y:.3f}", ha='center', va='bottom', color='blue')
for x, y in zip(concurrency_levels_k, chbl_requests_processed):
    plt.text(x, y, f"{y:.3f}", ha='center', va='top', color='red')

# Labels and Title
plt.xlabel("Number of concurrent requests / 1000")
plt.ylabel("Number of requests processed per second / 1000")
plt.title("Comparison of CHVN and CHBL Request Processing Efficiency")
plt.legend()
plt.grid(True)

# Display the plot
plt.show()
