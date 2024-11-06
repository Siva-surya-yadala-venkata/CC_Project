import requests
import matplotlib.pyplot as plt

# Server class to represent a server in the load balancer
class Server:
    def __init__(self, ip, port, weight=1):
        self.ip = ip
        self.port = port
        self.weight = weight
        self.requests_log = []  # Log for incoming requests
        self.request_count = 0  # Count of requests handled by the server

# Initialize servers
servers = [
    Server("127.0.0.1", 5001, weight=1),
    Server("127.0.0.1", 5002, weight=1),
    Server("127.0.0.1", 5003, weight=2),
    Server("127.0.0.1", 5004, weight=3)
]

# Weighted Round Robin Load Balancer
class WeightedRoundRobinLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current_index = 0
        self.current_weight = 0
        self.max_weight = max(server.weight for server in servers)

    def get_next_server(self):
        while True:
            server = self.servers[self.current_index]
            # Select the server with weight
            if self.current_weight < server.weight:
                self.current_weight += 1
                return server
            
            # Reset the weight and move to the next server
            self.current_weight = 0
            self.current_index = (self.current_index + 1) % len(self.servers)

# Function to simulate requests
def simulate_requests(load_balancer, num_requests):
    for i in range(num_requests):
        server = load_balancer.get_next_server()
        algorithm = "Weighted Round Robin"
        request_number = i + 1  # Start counting from 1

        # Sending a request to the server
        response = requests.get(f'http://{server.ip}:{server.port}/?request_number={request_number}&algorithm={algorithm}')
        print(response.text)

        # Increment the request count for the server
        server.request_count += 1

# Function to plot the request distribution
def plot_request_distribution(servers):
    server_names = [f"Server {server.port}" for server in servers]
    request_counts = [server.request_count for server in servers]

    plt.bar(server_names, request_counts, color='blue')
    plt.xlabel('Servers')
    plt.ylabel('Number of Requests')
    plt.title('Request Distribution Among Servers (Weighted Round Robin)')
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust layout to prevent clipping of tick-labels
    plt.show()

# Running the simulation
if __name__ == "__main__":
    num_requests = 100  # Change this to the desired number of requests
    load_balancer = WeightedRoundRobinLoadBalancer(servers)
    simulate_requests(load_balancer, num_requests)
    
    # Plot the request distribution after simulation
    plot_request_distribution(servers)
