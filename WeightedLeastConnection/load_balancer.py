import requests
import time
import threading
import random
from collections import deque
import matplotlib.pyplot as plt  # Importing matplotlib for graphing

class Server:
    def __init__(self, ip, port, weight=1):
        self.ip = ip
        self.port = port
        self.weight = weight
        self.active_connections = 0  
        self.request_count = 0  
        self.active = True  

# Initialize servers with different weights
servers = [
    Server("127.0.0.1", 5001, weight=1),
    Server("127.0.0.1", 5002, weight=1),
    Server("127.0.0.1", 5003, weight=2),
    Server("127.0.0.1", 5004, weight=3)
]

# Weighted Least Connection Load Balancer
class WeightedLeastConnectionLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.request_queue = deque()  # Queue to store requests when no servers are active

    def get_next_server(self):
        active_servers = [server for server in self.servers if server.active]
        
        if not active_servers:
            print("No active servers available. Request will be queued.")
            return None
        
        # Calculate weighted least connections
        least_loaded_server = None
        least_load = float('inf')

        for server in active_servers:
            load = server.active_connections / server.weight
            if load < least_load:
                least_load = load
                least_loaded_server = server

        least_loaded_server.active_connections += 1  
        least_loaded_server.request_count += 1  

        print(f"Selected Server {least_loaded_server.port} with {least_loaded_server.active_connections - 1} connections (before increment)\n")
        return least_loaded_server

    def queue_request(self, request):
        self.request_queue.append(request)
        print(f"Request queued: {request}")

    def process_queued_requests(self):
        while self.request_queue:
            request = self.request_queue.popleft()
            server = self.get_next_server()
            if server:
                threading.Thread(target=handle_request, args=(server, request['number'], request['algorithm'])).start()

# Function to simulate requests
def simulate_requests(load_balancer, num_requests):
    for i in range(num_requests):
        request_number = i + 1  
        server = load_balancer.get_next_server()
        
        if server is None:
            request = {'number': request_number, 'algorithm': "Weighted Least Connection"}
            load_balancer.queue_request(request)
            time.sleep(15)  
            set_server_states_after_wait()
            load_balancer.process_queued_requests()
            continue
        
        thread = threading.Thread(target=handle_request, args=(server, request_number, "Weighted Least Connection"))
        thread.start()

# Function to handle individual requests
def handle_request(server, request_number, algorithm):
    try:
        response = requests.get(f'http://{server.ip}:{server.port}/?request_number={request_number}&algorithm={algorithm}')
        print(response.text)

        time.sleep(random.uniform(0.5, 2.0))  

    except Exception as e:
        print(f"Error requesting server {server.port}: {e}")
    finally:
        server.active_connections -= 1
        print(f"Server {server.port}: Active connection released. Total active: {server.active_connections}")

def set_initial_server_states():
    for server in servers:
        command = input(f"Should Server {server.port} be active? (yes/no): ").strip().lower()
        server.active = (command == 'yes')

def set_server_states_after_wait():
    for server in servers:
        command = input(f"Should Server {server.port} be active now? (yes/no): ").strip().lower()
        server.active = (command == 'yes')
        if server.active:
            print(f"Server {server.port} is now active.")

def plot_request_distribution(servers):
    server_names = [f"Server {server.port}" for server in servers]
    request_counts = [server.request_count for server in servers]

    plt.bar(server_names, request_counts, color='blue')
    plt.xlabel('Servers')
    plt.ylabel('Number of Requests Handled')
    plt.title('Request Distribution Among Servers (Weighted Least Connection)')
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust layout to prevent clipping of tick-labels
    plt.show()

if __name__ == "__main__":
    num_requests = 100 
    load_balancer = WeightedLeastConnectionLoadBalancer(servers)
    
    set_initial_server_states()
    
    simulate_requests(load_balancer, num_requests)

    # Plot the request distribution after simulation
    plot_request_distribution(servers)
