#==========Libraries==================
import socket
import threading
import select
import sys

#======== 3.3 Functionality Methods =========
def help():
    print("Here are a list of commands:")
    print(" connect \t connect to another peer")
    print(" list \t\t list all IP addresses")
    print(" terminate \t terminate the connection")
    print(" send \t\t send messages to peers")
    print(" exit \t\t close all connections")    

def myip():
    print(IP)
    
def myport():
    print(PORT)

def exit():
    try:
        for sock in client_sockets:
            try:
                sock.close()
            except Exception as e:
                print(f"error closing socket: {str(e)}")

        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

# list() method #TODO
def list():
    
    print("id: IP address Port No.")
       
    for i in new_clients:
        print(i[0], " ", i[1])
    
# connect() method===============
def connect(destination, port):
    
    try: 
        # This command establishes a NEW TCP connection to the specified <destination> <port no>. 
        HEADER_LENGTH = 10

        # IP = "192.168.6.133"
        # PORT = 1234
        my_username = IP + ":" + str(PORT)

        # Create a socket
        # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
        # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to a given ip and port
        client_socket.connect((destination, port))

        # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
        client_socket.setblocking(False)

        # Prepare username and header and send them
        # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
        print("MY_USERNAME: ", my_username)
        
        username = my_username.encode('utf-8')
        
        print("USERNAME ENcoded: ", username)
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        
        print("LENGTH: ", username_header)
        
        client_socket.send(username_header + username)
        
        print("sent following: ", username_header + username)
        
        clients.append(client_socket)
        new_clients.append(((new_clients[-1][0] + 1), (destination, port), client_socket))

        
        # threading.Thread(target=send_message, daemon=False, args=(client_socket,)).start()

        # On receiving any message from the peer, the receiver should display 
        # the received message along with the sender information
        # (Eg. If a process on (sender)
        # 192.168.21.20 sends a message to a process on 
        # 192.168.21.21 then the output on
        # 192.168.21.21 when receiving a message should display as shown:
    except Exception as e:
        new_clients.remove((new_clients[-1][0] - 1), (destination, port), client_socket)
        print(f"Error connecting socket: {str(e)}")


    # # a) Any attempt to connect to an invalid IP should be rejected and suitable error message should be displayed.
    # #code() #TODO
    # print("Invalid IP. Try again.")
        
    # # b.2) failure in connections between two peers should be indicated by both the peers using suitable messages.
    # #code() #TODO
    # print("Invalid IP. Try again.")
    
    # # c.1) Self-connectionsconnections should be flagged with suitable error messages.
    # #code() #TODO
    # print("Self-connections . Try again.")

    # # c.2) duplicate connections should be flagged with suitable error messages.
    # #code() #TODO
    # print("Duplicate connections . Try again.")

# send() method
def send(connection_id, message):        
    # (For example, send 3 Oh! This project is a piece of cake). 
    # This will send the message to the host on the connection that is 
    # the number 3 when command “list” is used. 
    # 
    
    dest = 0
    dest_port = 0    
    client_socket = new_clients[0][2]
    
    for i in range(0, len(new_clients)):                
        if int(connection_id) == new_clients[i][0]: 
            print("if statement HIT")  
            dest_port = new_clients[i][1][1]  # int
            client_socket = new_clients[i][2]
    
    #=================== new ==========================
        # If message is not empty - send it
    if message:
        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
    
    
        
# HELPERS ================================================
# Handles message receiving
def receive_message(client_socket):

    try:
        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False    

# def send_message(client_socket):
#     continue
        

def user_input():
    while(True):
        user_input = input(">> ").split()
            #===============================================
        if len(user_input) != 0 and user_input[0] == "help":
            help()

        elif len(user_input) == 3 and user_input[0] == 'connect': 
            connect(user_input[1], int(user_input[2]))

        elif user_input[0] == 'list': 
            list()
            
        elif user_input[0] == 'send':
            message = ""
            for i in range(2, len(user_input)):
                message += " " + user_input[i]
            send(user_input[1], message)

        else:
            print("Try again")

def server(count):
    while(True):                
    
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        
        # Iterate over notified sockets
        for notified_socket in read_sockets:

            # If notified socket is a server socket - new connection, accept it
            if notified_socket == server_socket:

                # Accept new connection
                # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                # The other returned object is ip/port set
                client_socket, client_address = server_socket.accept()

                # Client should send his name right away, receive it
                user = receive_message(client_socket)
                print("USER: ", user)

                # If False - client disconnected before he sent his name
                if user is False:
                    continue

                # Add accepted socket to select.select() list
                sockets_list.append(client_socket)

                # Also save username and username header
                client_sockets[client_socket] = user
                count += 1
                clients.append((count, client_address))
                new_clients.append((count, client_address, client_socket))


                print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
                print('\n>> ')
                
                
                client_socket.send(my_username, server_socket)
                
    #<socket.socket fd=324, family=2, type=1, proto=0, laddr=('192.168.6.133', 1234), raddr=('192.168.6.133', 52156)>: {'header': b'4         ', 'data': b'dave'

            # Else existing socket is sending a message
            else:

                # Receive message
                message = receive_message(notified_socket)

                # # If False, client disconnected, cleanup
                # if message is False:
                #     print('Closed connection from: {}'.format(client_sockets[notified_socket]['data'].decode('utf-8')))
                #     print('\n>> ')

                #     # Remove from list for socket.socket()
                #     sockets_list.remove(notified_socket)

                #     # Remove from our list of users
                #     del client_sockets[notified_socket]

                #     continue

                # Get user by notified socket, so we will know who sent the message
                user = client_sockets[notified_socket]

                # Message received from 192.168.21.20
                # Sender’s Port: <The port no. of the sender>
                # Message: “<received message>

                print(f'Received message from {user["data"].decode("utf-8")}\nMessage: {message["data"].decode("utf-8")}')
                print('\n>> ')

                # Iterate over connected clients and broadcast message
                for client_socket in client_sockets:

                    # But don't sent it to sender
                    if client_socket != notified_socket:

                        # Send user and message (both with their headers)
                        # We are reusing here message header sent by sender, and saved username header send by user when he connected
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

        # It's not really necessary to have this, but will handle some socket exceptions just in case
        for notified_socket in exception_sockets:

            # Remove from list for socket.socket()
            sockets_list.remove(notified_socket)

            # Remove from our list of users
            del client_sockets[notified_socket]


#===========MAIN========================
HEADER_LENGTH = 10

IP = "192.168.6.133"
PORT = 5554

count = 1
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]
client_sockets = {} # this holds socket objects that are difficult to access info
clients = []    # this holds tuples which is easier to access info
clients.append((count, IP, PORT))
new_clients = []
new_clients.append((count, (IP, PORT), server_socket))

print(f'Listening for connections on {IP}:{PORT}...')

threading.Thread(target=user_input, daemon=False).start()

threading.Thread(target=server, daemon=True, args=(count,)).start()
