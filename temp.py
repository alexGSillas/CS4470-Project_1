import select
import socket

def receive_data(sock):
    try:
        data = sock.recv(1024)
        if not data:
            return None  # No data received, client has disconnected
        return data.decode('utf-8')
    except Exception as e:
        print(f"Error while receiving data: {e}")
        return None

def send_data(sock, message):
    try:
        sock.send(message.encode('utf-8'))
    except Exception as e:
        print(f"Error while sending data: {e}")

def main():
    # Create a list of sockets to monitor for readability
    sockets_to_monitor = []

    # Create a server socket and add it to the list
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(5)
    sockets_to_monitor.append(server_socket)

    print("Server is listening on port 12345...")

    while True:
        # Use select to monitor sockets for readability
        readable, _, _ = select.select(sockets_to_monitor, [], [])

        for sock in readable:
            if sock is server_socket:
                # If the server socket is readable, accept a new connection
                client_socket, client_address = server_socket.accept()
                sockets_to_monitor.append(client_socket)
                print(f"Accepted connection from {client_address}")
            else:
                # If a client socket is readable, receive and process data
                received_message = receive_data(sock)
                if received_message is None:
                    # Client has disconnected
                    print(f"Connection closed for {sock.getpeername()}")
                    sockets_to_monitor.remove(sock)
                    sock.close()
                else:
                    print(f"Received data from {sock.getpeername()}: {received_message}")
                    
                    # Process the received data (you can replace this with your logic)
                    response = "Server received your message: " + received_message

                    # Send a response back to the sender
                    send_data(sock, response)

    # Close all sockets
    for sock in sockets_to_monitor:
        sock.close()

if __name__ == "__main__":
    main()
