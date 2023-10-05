import select
import socket
import threading

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

def client_thread(client_socket, address):
    print(f"Accepted connection from {address}")
    while True:
        received_message = receive_data(client_socket)
        if received_message is None:
            # Client has disconnected
            print(f"Connection closed for {address}")
            client_socket.close()
            break

        print(f"Received data from {address}: {received_message}")

        # Process the received data (you can replace this with your logic)
        response = input(">>")

        # Send a response back to the sender
        send_data(client_socket, response)

def main():
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", 12345))
    server_socket.listen(5)

    print("Server is listening on port 12345...")

    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()

        # Start a new thread to handle the client
        client_handler = threading.Thread(target=client_thread, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    main()
