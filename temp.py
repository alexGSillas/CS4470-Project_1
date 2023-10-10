import socket
import threading
import subprocess

# Global variables to store IP address and port
server_ip = ""
server_port = 0

def run_shell_command(command):
    try:
        # Run the shell command and capture the output
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout + result.stderr
        return output
    except Exception as e:
        return str(e)

def client_thread(client_socket, client_address):
    global server_ip, server_port

    print(f"Accepted connection from {client_address}")

    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            # Handle user commands
            if data.strip() == "help":
                response = "Available commands:\n1. help\n2. myip\n3. myport\n"
            elif data.strip() == "myip":
                response = f"Server IP address: {server_ip}\n"
            elif data.strip() == "myport":
                response = f"Server is listening on port: {server_port}\n"
            else:
                # Run shell command and return the output
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
