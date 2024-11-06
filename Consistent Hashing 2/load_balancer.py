import hashlib
import bisect
import matplotlib.pyplot as plt

class ConsistentHashRing:
    def __init__(self):
        self.ring = dict()          # {Server : Hashed Key }A dictionary to store the server for each position on the ring
        self.sorted_keys = []       # {Sorted Hash Values in the Ring}Sorted list of hash values to efficiently find the next server
    
    def _hash(self, key):
        """Generate an MD5 hash and convert it to an integer."""
        hash_value = int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)
        return hash_value

    def add_server(self, server):
        """Add a server to the hash ring."""
        hashed_key = self._hash(server)   # Hash the server to find its position on the ring
        if hashed_key not in self.ring:
            self.ring[hashed_key] = server
            bisect.insort(self.sorted_keys, hashed_key)  # Helps to maintain the sorted keys after the adding the keys in the list
            print(f"Added server {server} at position {hashed_key}.")
        else:
            print(f"Server {server} is already present on the ring.")
    
    def remove_server(self, server):
        """Remove a server from the hash ring."""
        hashed_key = self._hash(server)
        if hashed_key in self.ring:
            del self.ring[hashed_key]
            self.sorted_keys.remove(hashed_key)
            print(f"Removed server {server} from position {hashed_key}.")
        else:
            print(f"Server {server} not found in the ring.")

    def get_server(self, request_key):
        """Find the server responsible for handling the given request."""
        if not self.ring:
            return None

        hashed_key = self._hash(request_key)
        idx = bisect.bisect(self.sorted_keys, hashed_key) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]

    def distribute_requests(self, requests):
        """Distribute the requests among the servers and return the distribution."""
        distribution = {}
        hash_mapping = {}

        for request in requests:
            hashed_key = self._hash(request)
            server = self.get_server(request)
            hash_mapping[request] = hashed_key

            if server not in distribution:
                distribution[server] = []
            distribution[server].append(request)

        return distribution, hash_mapping

# Function to plot request distribution and hash values
def plot_distribution(distribution, hash_mapping):
    servers = list(distribution.keys())
    num_requests = [len(distribution[server]) for server in servers]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(servers, num_requests, color='skyblue', alpha=0.7)
    plt.xlabel('Servers')
    plt.ylabel('Number of Requests')
    plt.title('Consistent Hashing Distribution Across Servers')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--')

    # Add labels to each bar (number of requests handled)
    for bar, count in zip(bars, num_requests):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{count}', ha='center', va='bottom')

    # Print hash values and corresponding server distribution
    print("\nHash Value Distribution:")
    for request, hash_value in hash_mapping.items():
        server = consistent_hash.get_server(request)
        print(f"Request: {request}, Hash Value: {hash_value}, Server: {server}")

    plt.show()

# Command-line interaction
if __name__ == "__main__":
    consistent_hash = ConsistentHashRing()
    requests = [f"Request_{i}" for i in range(10000)]

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
            plot_distribution(distribution, hash_mapping)

        elif choice == '2':
            server_name = input("Enter server name to remove (e.g., Server1, Server2): ")
            consistent_hash.remove_server(server_name)

            # Show new distribution of requests after removing a server
            print("\nDistribution after removing server:")
            distribution, hash_mapping = consistent_hash.distribute_requests(requests)
            plot_distribution(distribution, hash_mapping)

        elif choice == '3':
            # Show current request distribution
            print("\nCurrent distribution of requests:")
            distribution, hash_mapping = consistent_hash.distribute_requests(requests)
            plot_distribution(distribution, hash_mapping)

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
