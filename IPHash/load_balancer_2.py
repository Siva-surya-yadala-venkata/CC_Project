import hashlib
import requests
import matplotlib.pyplot as plt
import time

# Server class to represent a server in the load balancer
class Server:
    def __init__(self, ip, port, weight=1):
        self.ip = ip
        self.port = port
        self.weight = weight
        self.request_count = 0  # Track the number of requests for this server
        self.response_times = []  # Store response times for each request

# Initialize servers (all are included in the pool)
servers = [
    Server("127.0.0.1", 5001, weight=1),
    Server("127.0.0.1", 5002, weight=1),
    Server("127.0.0.1", 5003, weight=1),
    Server("127.0.0.1", 5004, weight=1)
]

# IP Hash Load Balancer
class IPHashLoadBalancer:
    def __init__(self, servers):
        self.servers = servers

    def get_next_server(self, client_ip):
        # Generate a hash of the client IP and determine the server index
        hashed_ip = hashlib.md5(client_ip.encode()).hexdigest()
        server_index = int(hashed_ip, 16) % len(self.servers)
        
        # Debug output to understand hash distribution
        print(f"Client IP: {client_ip}, Hashed IP: {hashed_ip}, Server Index: {server_index}")

        return self.servers[server_index]

# Function to simulate requests
def simulate_requests(load_balancer, num_requests):
    for i in range(num_requests):
        # Generate unique client IP addresses to improve distribution
        client_ip = f"192.168.1.{i % 20}"  # Simulate IPs from 192.168.1.0 to 192.168.1.19

        server = load_balancer.get_next_server(client_ip)
        request_number = i + 1  # Start counting from 1

        print(f"Selected Server {server.port} for request {request_number}")

        # Increment the request count for the selected server
        server.request_count += 1

        # Send a request to the server and measure response time
        start_time = time.time()  # Start time before the request
        try:
            # Make a GET request to the server
            response = requests.get(f'http://{server.ip}:{server.port}/?request_number={request_number}')
            response_time = time.time() - start_time  # Calculate response time

            print(f"Response from server {server.port}: {response.text} (Response Time: {response_time:.2f} seconds)")

            # Store the response time for averaging later
            server.response_times.append(response_time)

        except requests.exceptions.RequestException as e:
            print(f"Error requesting server {server.port}: {e}")

# Function to plot request distribution and average response times
def plot_metrics(servers):
    ports = [server.port for server in servers]
    request_counts = [server.request_count for server in servers]
    
    # Calculate average response times for each server
    average_response_times = [
        sum(server.response_times) / len(server.response_times) if server.response_times else 0
        for server in servers
    ]
    
    # Display average response times in the console
    print("\nAverage Response Times:")
    for server, avg_time in zip(servers, average_response_times):
        print(f"Server {server.port} -> Average Response Time: {avg_time:.2f} seconds")
    
    # Plot request distribution across servers
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    plt.bar(ports, request_counts, color='blue', alpha=0.7)
    plt.xlabel('Server Ports')
    plt.ylabel('Number of Requests')
    plt.title('IP HASH Request Distribution Across Servers')
    plt.xticks(ports)
    plt.grid(axis='y')

    # Plot average response times for each server
    plt.subplot(1, 2, 2)
    plt.bar(ports, average_response_times, color='green', alpha=0.7)
    plt.xlabel('Server Ports')
    plt.ylabel('Average Response Time (s)')
    plt.title('Average Response Time per Server')
    plt.xticks(ports)
    plt.grid(axis='y')

    # Show both plots
    plt.tight_layout()
    plt.show()

# Running the simulation
if __name__ == "__main__":
    num_requests = 100  # Change this to the desired number of requests
    load_balancer = IPHashLoadBalancer(servers)
    simulate_requests(load_balancer, num_requests)

    # Plot request distribution and average response times after simulation
    plot_metrics(servers)
