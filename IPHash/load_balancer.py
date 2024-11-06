import requests
import hashlib
import matplotlib.pyplot as plt

# Server class to represent a server in the load balancer
class Server:
    def __init__(self, ip, port, weight=1):
        self.ip = ip
        self.port = port
        self.weight = weight
        self.request_count = 0  # Track the number of requests for this server

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
        algorithm = "IP Hash"
        request_number = i + 1  # Start counting from 1

        print(f"Selected Server {server.port} for request {request_number}")

        # Increment the request count for the selected server
        server.request_count += 1

        # Sending a request to the server
        try:
            response = requests.get(f'http://{server.ip}:{server.port}/?request_number={request_number}&algorithm={algorithm}')
            print(response.text)
        except Exception as e:
            print(f"Error requesting server {server.port}: {e}")

# Function to plot request distribution
def plot_request_distribution(servers):
    ports = [server.port for server in servers]
    request_counts = [server.request_count for server in servers]

    plt.figure(figsize=(10, 6))
    plt.bar(ports, request_counts, color='blue', alpha=0.7)
    plt.xlabel('Server Ports')
    plt.ylabel('Number of Requests')
    plt.title('IP HASH Request Distribution Across Servers')
    plt.xticks(ports)
    plt.grid(axis='y')
    plt.show()

# Running the simulation
if __name__ == "__main__":
    num_requests = 100  # Change this to the desired number of requests
    load_balancer = IPHashLoadBalancer(servers)
    simulate_requests(load_balancer, num_requests)

    # Plot the request distribution after simulation
    plot_request_distribution(servers)
