import hashlib
import bisect
import matplotlib.pyplot as plt

class ConsistentHashRing:
    def __init__(self, num_replicas=3):
        self.ring = dict()  # Maps hash values to virtual nodes (server replicas)
        self.sorted_keys = []  # Keeps track of the sorted hash keys
        self.num_replicas = num_replicas
        self.servers = []  # To keep track of added servers

    def _hash(self, key):
        """Generate an MD5 hash and convert it to an integer."""
        hash_value = int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)
        return hash_value

    def add_server(self, server):
        """Add a server to the hash ring with replicas."""
        self.servers.append(server)  # Keep track of added servers
        for i in range(self.num_replicas):
            replica_key = f"{server}-{i}"  # Create unique key for each replica
            hashed_key = self._hash(replica_key)
            self.ring[hashed_key] = replica_key  # Store replica in the ring
            bisect.insort(self.sorted_keys, hashed_key)  # Keep keys sorted
        print(f"Added server {server} with {self.num_replicas} replicas.")

    def remove_server(self, server):
        """Remove a server and its replicas from the hash ring."""
        if server in self.servers:
            self.servers.remove(server)  # Remove from servers list
            for i in range(self.num_replicas):
                replica_key = f"{server}-{i}"
                hashed_key = self._hash(replica_key)
                if hashed_key in self.ring:
                    del self.ring[hashed_key]
                    self.sorted_keys.remove(hashed_key)
            print(f"Removed server {server}.")
        else:
            print(f"Server {server} not found.")

    def get_server(self, request_key):
        """Get the virtual node responsible for handling the request."""
        if not self.ring:
            return None

        hashed_key = self._hash(request_key)
        idx = bisect.bisect(self.sorted_keys, hashed_key) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]  # Return the virtual node (replica)

    def distribute_requests(self, requests):
        """Distribute the requests among the virtual nodes (servers)."""
        distribution = {}
        hash_mapping = {}  # Store the hashes of requests for visualization
        for request in requests:
            hashed_key = self._hash(request)
            server = self.get_server(request)  # Get the specific virtual node (replica)
            hash_mapping[request] = hashed_key  # Save the hash value

            if server not in distribution:
                distribution[server] = []
            distribution[server].append(request)  # Assign request to the virtual node

        return distribution, hash_mapping  # Returning the hash values along with distribution

    def count_requests_per_server(self, distribution):
        """Count total requests handled by each main server."""
        server_counts = {server: 0 for server in self.servers}
        for virtual_node in distribution.keys():
            server_name = virtual_node.split('-')[0]  # Extract server name from virtual node
            if server_name in server_counts:
                server_counts[server_name] += len(distribution[virtual_node])
        return server_counts

# Function to plot request distribution and load balancing
def plot_distribution(distribution, hash_mapping, server_counts):
    # Plotting request distribution across virtual nodes (server replicas)
    plt.figure(figsize=(12, 6))
    servers = list(distribution.keys())
    num_requests = [len(distribution[server]) for server in servers]
    bars = plt.bar(servers, num_requests, color='skyblue', alpha=0.7)
    plt.xlabel('Virtual Nodes (Server Replicas)')
    plt.ylabel('Number of Requests')
    plt.title('Virtual Consistent Hashing Distribution Across Server Replicas')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--')

    # Add labels to each bar (number of requests handled)
    for bar, count in zip(bars, num_requests):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{count}', ha='center', va='bottom')

    plt.show()

    # Plotting the total requests handled by each main server
    plt.figure(figsize=(12, 6))
    servers = list(server_counts.keys())
    total_requests = list(server_counts.values())
    bars = plt.bar(servers, total_requests, color='orange', alpha=0.7)
    plt.xlabel('Main Servers')
    plt.ylabel('Total Number of Requests')
    plt.title('Total Request Distribution Across Main Servers')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--')

    # Add labels to each bar (total requests handled)
    for bar, count in zip(bars, total_requests):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{count}', ha='center', va='bottom')

    plt.show()

# Command-line interaction
if __name__ == "__main__":
    consistent_hash = ConsistentHashRing(num_replicas=3)
    requests = [f"Request_{i}" for i in range(10000)]  # Simulating 100 unique requests

    while True:
        print("\n1. Add Server")
        print("2. Remove Server")
        print("3. View Distribution")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            server_name = input("Enter server name to add (e.g., Server1, Server2): ")
            consistent_hash.add_server(server_name)

            # Show new distribution of requests after adding a server
            print("\nDistribution after adding server:")
            distribution, hash_mapping = consistent_hash.distribute_requests(requests)
            server_counts = consistent_hash.count_requests_per_server(distribution)
            plot_distribution(distribution, hash_mapping, server_counts)

        elif choice == '2':
            server_name = input("Enter server name to remove (e.g., Server1, Server2): ")
            consistent_hash.remove_server(server_name)

            # Show new distribution of requests after removing a server
            print("\nDistribution after removing server:")
            distribution, hash_mapping = consistent_hash.distribute_requests(requests)
            server_counts = consistent_hash.count_requests_per_server(distribution)
            plot_distribution(distribution, hash_mapping, server_counts)

        elif choice == '3':
            # Show current request distribution across virtual nodes (server replicas)
            print("\nCurrent distribution of requests:")
            distribution, hash_mapping = consistent_hash.distribute_requests(requests)
            server_counts = consistent_hash.count_requests_per_server(distribution)
            plot_distribution(distribution, hash_mapping, server_counts)

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
