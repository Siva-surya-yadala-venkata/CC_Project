import numpy as np
import matplotlib.pyplot as plt

# Define parameters
server_counts = [2, 4, 7, 10, 15, 20]
num_requests = 1000  # Total requests per simulation
request_sizes = np.random.randint(1, 10, num_requests)  # Simulated request sizes
algorithms = ['Round Robin', 'Weighted Round Robin', 'Least Connection']
mean_latency_results = {alg: [] for alg in algorithms}

# Simulation functions
def round_robin(num_servers, requests):
    server_loads = [0] * num_servers
    total_latency = 0
    for i, req_size in enumerate(requests):
        server_index = i % num_servers
        server_loads[server_index] += req_size
        total_latency += server_loads[server_index]
    return total_latency / len(requests)

def weighted_round_robin(num_servers, requests, weights=None):
    weights = weights or [1] * num_servers
    server_loads = [0] * num_servers
    total_latency = 0
    index = 0
    for req_size in requests:
        server_index = index % num_servers
        if weights[server_index] == 0:
            index += 1
            continue
        server_loads[server_index] += req_size
        total_latency += server_loads[server_index]
        weights[server_index] -= 1
        if weights[server_index] == 0:
            index += 1
    return total_latency / len(requests)

def least_connection(num_servers, requests):
    server_loads = [0] * num_servers
    total_latency = 0
    for req_size in requests:
        server_index = server_loads.index(min(server_loads))  # Select least loaded server
        server_loads[server_index] += req_size
        total_latency += server_loads[server_index]
    return total_latency / len(requests)

# Running the simulation
for server_count in server_counts:
    for alg in algorithms:
        if alg == 'Round Robin':
            mean_latency_results[alg].append(round_robin(server_count, request_sizes))
        elif alg == 'Weighted Round Robin':
            weights = [np.random.randint(1, 3) for _ in range(server_count)]
            mean_latency_results[alg].append(weighted_round_robin(server_count, request_sizes, weights))
        elif alg == 'Least Connection':
            mean_latency_results[alg].append(least_connection(server_count, request_sizes))

# Ensure that the results for each algorithm were collected properly
print("Mean Latency Results:")
for alg in algorithms:
    print(f"{alg}: {mean_latency_results[alg]}")

# Plotting the results with distinct colors and line styles
plt.figure(figsize=(10, 6))
plt.plot(server_counts, mean_latency_results['Round Robin'], color='blue', marker='o', linestyle='-', label='Round Robin')
plt.plot(server_counts, mean_latency_results['Weighted Round Robin'], color='green', marker='s', linestyle='--', label='Weighted Round Robin')
plt.plot(server_counts, mean_latency_results['Least Connection'], color='red', marker='^', linestyle='-.', label='Least Connection')

plt.xlabel('Number of Servers')
plt.ylabel('Mean Latency')
plt.title('Effect of Number of Servers on Average Latency for Different Algorithms')
plt.legend()
plt.grid(True)
plt.show()
