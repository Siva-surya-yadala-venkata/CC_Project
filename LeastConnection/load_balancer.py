import requests
import time
import threading
import random
import matplotlib.pyplot as plt
from collections import deque

class Server:
    def __init__(self, ip, port, weight=1):
        self.ip = ip
        self.port = port
        self.weight = weight
        self.active_connections = 0  
        self.request_count = 0  
        self.active = True  

# Initialize servers
servers = [
    Server("127.0.0.1", 5001, weight=1),
    Server("127.0.0.1", 5002, weight=1),
    Server("127.0.0.1", 5003, weight=1),
    Server("127.0.0.1", 5004, weight=1)
]

# Least Connection Load Balancer
class LeastConnectionLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.request_queue = deque()  # Queue to store requests when no servers are active

    def get_next_server(self):
        active_servers = [server for server in self.servers if server.active]
        
        if not active_servers:
            print("No active servers available. Request will be queued.")
            return None
        
        least_loaded_server = min(active_servers, key=lambda server: server.active_connections)
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
            request = {'number': request_number, 'algorithm': "Least Connection"}
            load_balancer.queue_request(request)
            time.sleep(15)  
            set_server_states_after_wait()
            load_balancer.process_queued_requests()
            continue
        
        thread = threading.Thread(target=handle_request, args=(server, request_number, "Least Connection"))
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

def plot_request_distribution(servers):
    server_names = [f"Server {server.port}" for server in servers]
    request_counts = [server.request_count for server in servers]

    plt.bar(server_names, request_counts, color='blue')
    plt.xlabel('Servers')
    plt.ylabel('Number of Requests Handled')
    plt.title('Request Distribution Among Servers (Least Connection)')
    plt.xticks(rotation=45)
    plt.tight_layout()  
    plt.show()

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

if __name__ == "__main__":
    num_requests = 100 
    load_balancer = LeastConnectionLoadBalancer(servers)
    
    set_initial_server_states()
    
    simulate_requests(load_balancer, num_requests)

    plot_request_distribution(servers)
