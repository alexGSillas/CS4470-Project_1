import select
import socket
import threading
import subprocess

# Global variables to store IP address and port
server_ip = ""
server_port = 0

# Dictionary to store active connections
connections = {}
connection_id = 1

def run_shell_command(command):
    try:
        # Run the shell command and capture the output
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout + result.stderr
        return output
    except Exception as e:
        return str(e)

def client_thread(client_socket, client_address):
    global server_ip, server_port, connections, connection_id

    print(f"Accepted connection from {client_address}")

    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            # Handle user commands
            command_parts = data.strip().split()
            if not command_parts:
                continue

            command = command_parts[0]

            if command == "help":
                response = "Available commands:\n1. help\n2. myip\n3. myport\n4. connect <destination> <port>\n5. list\n6. terminate <connection_id>\n7. send <connection_id> <message>\n8. exit\n"
            elif command == "myip":
                response = f"Server IP address: {server_ip}\n"
            elif command == "myport":
                response = f"Server is listening on port: {server_port}\n"
            elif command == "connect":
                if len(command_parts) != 3:
                    response = "Usage: connect <destination> <port>\n"
                else:
                    destination = command_parts[1]
                    port = int(command_parts[2])

                    # Check for self-connection and duplicate connections
                    if destination == server_ip and port == server_port:
                        response = "Error: Self-connection is not allowed.\n"
                    elif (destination, port) in connections.values():
                        response = "Error: Duplicate connection.\n"
                    else:
                        try:
                            # Try to establish a new connection
                            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            new_socket.connect((destination, port))

                            # Add the new connection to the dictionary
                            connections[connection_id] = (destination, port, new_socket)

                            response = f"Connected to {destination}:{port} (Connection ID: {connection_id})\n"
                            connection_id += 1
                        except Exception as e:
                            response = f"Error: {e}\n"
            elif command == "list":
                response = "Active connections:\n"
                for conn_id, (dest, port, _) in connections.items():
                    response += f"{conn_id}: {dest} {port}\n"
            elif command == "terminate":
                if len(command_parts) != 2:
                    response = "Usage: terminate <connection_id>\n"
                else:
                    try:
                        conn_id = int(command_parts[1])
                        if conn_id in connections:
                            connections[conn_id][2].close()
                            del connections[conn_id]
                            response = f"Connection {conn_id} terminated\n"
                        else:
                            response = f"Error: Invalid connection ID {conn_id}\n"
                    except ValueError:
                        response = "Error: Invalid connection ID\n"
            elif command == "send":
                if len(command_parts) < 3:
                    response = "Usage: send <connection_id> <message>\n"
                else:
                    try:
                        conn_id = int(command_parts[1])
                        if conn_id in connections:
                            message = " ".join(command_parts[2:])
                            dest, _, sock = connections[conn_id]
                            sock.send(message.encode('utf-8'))
                            response = f"Message sent to {conn_id}\n"
                        else:
                            response = f"Error: Invalid connection ID {conn_id}\n"
                    except ValueError:
                        response = "Error: Invalid connection ID\n"
            elif command == "exit":
                # Close all connections and terminate the server
                for _, (_, _, sock) in connections.items():
                    sock.close()
                server_socket.close()
                print("Server closed.")
                return
            else:
                response = run_shell_command(data)

            # Send the response back to the client
            client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            break

    print(f"Connection closed for {client_address}")
    client_socket.close()

def main():
    global server_ip, server_port

    # Get the server's IP address
    server_ip = socket.gethostbyname(socket.gethostname())

    # Define the server port
    server_port = 12345

    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server address and port
    server_socket.bind((server_ip, server_port))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server is listening on {server_ip}:{server_port}...")

    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()

        # Start a new thread to handle the client
        client_handler = threading.Thread(target=client_thread, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    main()
