import numpy as np
import matplotlib.pyplot as plt

# Define parameters
arrival_rates = np.array([10, 20, 50, 75, 100])  # requests per second
num_requests = 1000  # total requests per simulation
num_servers = 3  # number of servers

# Define server capacities for Weighted Round Robin
server_weights = [1, 2, 3]  # Server 1, 2, and 3 weights

# Functions for Load Balancing Algorithms
def calculate_response_time(arrival_rate):
    # Simulate an exponential increase in response time with arrival rate
    return np.exp(arrival_rate / 100) * 0.01  # Base response time scaled by arrival rate

def round_robin(requests):
    latencies = []
    for i in range(len(requests)):
        server = i % num_servers
        latency = requests[i] * calculate_response_time(requests[i])
        latencies.append(latency)
    return np.mean(latencies)

def weighted_round_robin(requests, weights):
    latencies = []
    server_indices = np.repeat(range(num_servers), weights)
    for i in range(len(requests)):
        server = server_indices[i % len(server_indices)]
        latency = requests[i] * calculate_response_time(requests[i])
        latencies.append(latency)
    return np.mean(latencies)

def least_connection(requests):
    latencies = []
    connections = [0] * num_servers  # Connection count for each server
    for i in range(len(requests)):
        server = np.argmin(connections)  # Select server with least connections
        connections[server] += 1
        latency = requests[i] * calculate_response_time(requests[i])
        latencies.append(latency)
        connections[server] -= 1  # Assume request is processed, reduce connection count
    return np.mean(latencies)

# Run Simulation for each arrival rate
rr_latencies, wrr_latencies, lc_latencies = [], [], []

for rate in arrival_rates:
    requests = np.random.poisson(rate, num_requests)
    
    rr_latencies.append(round_robin(requests))
    wrr_latencies.append(weighted_round_robin(requests, server_weights))
    lc_latencies.append(least_connection(requests))

# Plotting
plt.figure(figsize=(10, 6))

# Assign distinct colors and styles to each algorithm
plt.plot(arrival_rates, rr_latencies, label="Round Robin", marker='o', color='blue', markersize=8, linestyle='-')
plt.plot(arrival_rates, wrr_latencies, label="Weighted Round Robin", marker='x', color='green', markersize=8, linestyle='--')
plt.plot(arrival_rates, lc_latencies, label="Least Connection", marker='s', color='red', markersize=8, linestyle=':')

plt.xlabel("Arrival Rate (requests/sec)")
plt.ylabel("Mean Latency (s)")
plt.title("Average Latency of Different Algorithms at Different Arrival Rates")
plt.legend()
plt.grid(True)
plt.ylim(0, max(rr_latencies + wrr_latencies + lc_latencies) * 1.1)  # Adjust y-axis limit for better visibility
plt.show()
