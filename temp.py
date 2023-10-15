import socket
import threading
import select
import sys


def help():
    print("Here is a list of commands:")
    print("myip - Returns your IP Address")
    print("myport - Returns your Port Number")
    print("connect <destination> <port> - Connect to another peer")
    print("list - List all connected peers")
    print("terminate <connection_id> - Terminate a connection")
    print("send <connection_id> <message> - Send a message to a peer")
    print("exit - Close all connections and exit")


def myip():
    try:
        return IP
    except Exception as e:
        return str(e)


def myport():
    try:
        return PORT
    except Exception as e:
        print(f"Error: {e}")


def list_peers():
    print("ID: IP address \t\tPort No.")
    for i in new_clients:
        print(f"{i[0]}: {i[1][0]} \t {i[1][1]}")


def exit_program():
    try:

        for _, _, client_socket in new_clients:
            if client_socket[0] != 1 and len(new_clients)<1:
                mes = "Closing connection"
                client_socket.send(mes.encode('utf-8'))
            client_socket.close()
        server_socket.close()
        threading.Thread(target=user_input, daemon=False)
        threading.Thread(target=server, daemon=False, args=(count,))
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        server_socket.close()
        sys.exit(1)


def terminate(connection_id):
    try:
        connection_id = int(connection_id)
        for client in new_clients:
            if client[0] == connection_id:
                _, _, client_socket = client
                client_socket.close()
                new_clients.remove(client)
                print(f"Connection ID {connection_id} terminated.")
                return
        print("Connection does not exist")
    except Exception as e:
        print(str(e))

def connect(destination, port):
    try:

        if str(destination) == str(myip())  and str(port) == str(PORT) :
            print("WARNING SELF CONNECTION")


        HEADER_LENGTH = 10
        my_username = input("Enter your name: ")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((destination, port))
        client_socket.setblocking(False)

        username = my_username.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(username_header + username)
        if client_socket in new_clients :
            print("WARRNING DUPLICATION WITH CONNECTION")
        new_clients.append((new_clients[-1][0] + 1, (destination, port), client_socket))



        print("Connection Established")
    except Exception as e:
        print("Connection Failed")
        print(f"Error connecting socket: {str(e)}")


def send(connection_id, message):
    try:
        client_socket = new_clients[0][2]

        for i in range(0, len(new_clients)):
            if int(connection_id) == new_clients[i][0]:
                print("Message sent to ID:",connection_id)
                dest_port = new_clients[i][1][1]  # int
                client_socket = new_clients[i][2]

        if message:
            # Encode message to bytes, prepare header and convert to bytes, like for username above, then send

            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)
    except Exception as e:
        print("Error:",str(e) )


def receive_message(client_socket):
    try:

        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False


def user_input():
    while True:
        user_input = input(">> ").split()
        if len(user_input) != 0:
            command = user_input[0]
            if command == "help":
                help()
            elif command == 'connect' and len(user_input) == 3:
                connect(user_input[1], int(user_input[2]))
            elif command == 'list':
                list_peers()
            elif command == 'send' and len(user_input) > 2:
                connection_id = user_input[1]
                message = " ".join(user_input[2:])
                send(connection_id, message)
            elif command == 'myip':
                print(myip())
            elif command == 'myport':
                print(myport())
            elif command == 'exit':
                exit_program()
            elif command == 'terminate' and len(user_input) == 2:
                terminate(user_input[1])
            else:
                print("Invalid command. Type 'help' for a list of commands.")


def server(count):
    try:
        while True:

            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
            for notified_socket in read_sockets:
                if notified_socket == server_socket:
                    client_socket, client_address = server_socket.accept()

                    user = receive_message(client_socket)
                    if user is False:
                        continue
                    sockets_list.append(client_socket)
                    count += 1
                    new_clients.append((count, client_address, client_socket))
                    print(
                        f'Accepted new connection from {client_address[0]}:{client_address[1]}, username: {user["data"].decode("utf-8")}')
                else:
                    message = receive_message(notified_socket)
                    if message is False:
                        print(f"Closed connection from a socket:",notified_socket[0])
                        sockets_list.remove(notified_socket)
                        new_clients.remove(next((client for client in new_clients if client[2] == notified_socket), None))
                        continue
                    user = next((client for client in new_clients if client[2] == notified_socket), None)
                    if user:
                        print(
                            f"Received message from {user[1][0]}:{user[1][1]} \nSender's port {user[2].getpeername()}\nMessage: {message['data'].decode('utf-8')}")

                        # for client_socket in sockets_list:
                        #     if client_socket != notified_socket:
                        #         m = "hi!!!"
                        #         d = m.encode('utf-8')
                        #         client_socket.send(d)
            for notified_socket in exception_sockets:
                sockets_list.remove(notified_socket)
                user = next((client for client in new_clients if client[2] == notified_socket), None)
                if user:
                    print(f"Closed connection from {user[1][0]}:{user[1][1]}")
                    new_clients.remove(user)
    except Exception as e:
        server_socket.close()
        print("")

HEADER_LENGTH = 10
IP = socket.gethostbyname(socket.gethostname())
PORT = 30001

count = 1
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT)
                   )
server_socket.listen()

sockets_list = [server_socket]
new_clients = []
new_clients.append((count, (IP, PORT), server_socket))

print(f'Listening for connections on {IP}:{PORT}...')

try:
    threading.Thread(target=user_input, daemon=False).start()
    threading.Thread(target=server, daemon=False, args=(count,)).start()
except Exception as e:
    print(str(e))
