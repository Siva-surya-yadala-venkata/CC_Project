from flask import Flask, request, jsonify
import sys

app = Flask(__name__)
requests_log = []

@app.route('/')
def index():
    # Get request number and algorithm from query parameters
    request_number = request.args.get('request_number', 'unknown')
    algorithm = request.args.get('algorithm', 'unknown')

    # Log the request
    log_entry = f"{request_number}th request arrived from {algorithm}"
    requests_log.append(log_entry)

    return f"Response from Server (Port {port}) - {log_entry}"

@app.route('/status')
def status():
    return jsonify({
        "server": f"Server (Port {port})",
        "port": port,
        "total_requests": len(requests_log),
        "requests_log": requests_log
    })

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])  # Get port from command line
    app.run(port=port)

