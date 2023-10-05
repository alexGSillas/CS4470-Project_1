# =================TODO==========================
# need to include the arguments in the methods & get rid of LiDAR
# delete comments about drones
# make sure it's TCP not UDP
# in the end, clean up all the files

# set time for testing
# ========================================


# ==========Libraries==================
import socket
import threading
import time


# ======== 3.3 Functionality Methods =========
# Done!
# help() method
def help():
    print("Here are a list of commands:")
    # print(" myip \n myport \n connect \n list \n terminate \n send \n exit \n")
    print(" myip \t\t display IP address")
    print(" myport \t display port number")
    print(" connect \t connect to another peer")
    print(" list \t\t list all IP addresses")
    print(" terminate \t terminate the connection")
    print(" send \t\t send messages to peers")
    print(" exit \t\t close all connections")

# Done!
# myip() method
def myip():
    try:
        # Create a socket to get the local IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(0.1)  # Set a timeout to avoid blocking
            s.connect(("8.8.8.8", 80))  # Connect to a public IP address
            local_ip = s.getsockname()[0]
            print("My IP is: " + local_ip)
    except Exception as e:
        print(f"Error: {e}")

    # myport() method

# Done!
def myport():
    try:
        # Create a socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Bind the socket to a specific address and port
            s.bind(("localhost", 0))  # Use port 0 to let the OS assign an available port
            # Get the socket's port number
            local_port = s.getsockname()[1]
            print("The program runs on port number :", str(local_port))
    except Exception as e:
        print(f"Error: {e}")


# broken connect() method
#Self-connections and duplicate connections should be flagged with suitable error messages
def connect(destination, port):

    my_address = ('', 9010)

    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the specified IP address and port
        client_socket.connect((destination, port))
        client_socket.bind(myip().local_ip,myport().local_port)
        # Return the connected socket
        print("The connection to peer "+str(destination)+"is successfully established")
    except Exception as e:
        print(f"Error: {e}")
        return None



# Receive the message
def receive(sock1):
    # Continuously loop and listen for incoming messages
    while True:
        # Try to receive the message otherwise print the exception
        try:
            print("listening now...")
            response1, ip_address = sock1.recvfrom(2048)

            print("Received message: from David EDU #1: " + response1.decode(encoding='utf-8'))

        except Exception as e:
            # If there's an error close the socket and break out of the loop
            sock1.close()

            print("Error receiving: 2" + str(e))
            break


# list() method
def list():
    # ** insert code here**
    print("id: IP address \t Port No.")


# terminate() method
def terminate(connection_id):
    # ** insert code here**
    print()


# send() method
def send(connection_id, message, sock1):
    # Try to send the message otherwise print the exception
    try:
        sock1.sendto(message.encode(), connection_id)

        print("Sending message: " + message)
    except Exception as e:
        print("Error sending: 1" + str(e))

    # ============ SETUP ============


# # IP and port
# first_address = ('10.85.38.178', 9000)

# # IP and port of local computer
# local1_address = ('', 9010)

# # Create a UDP connection that we'll send the command to
# sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # Bind to the local address and port
# sock1.bind(local1_address)

message = ''

while (True):
    print()
    print("==================================================================")
    print("Setting up...")
    print()

    # print("==================================================================")

    user_input = input("input your command: ").split()

    if len(user_input) != 0 and user_input[0] == "exit":
        print('exit')
        print("Closing program...")
        exit()

    elif user_input[0] == "help":
        help()

    elif user_input[0] == 'myip':
        myip()

    elif user_input[0] == 'myport':
        myport()

    elif len(user_input) == 3 and user_input[0] == 'connect':
        # connect(destination, port)
        connect(user_input[1], user_input[2])

    elif user_input[0] == 'list':
        list()

    elif len(user_input) == 2 and user_input[0] == 'terminate':
        # terminate(connection_id)
        terminate(user_input[1])

    elif len(user_input) == 3 and user_input[0] == 'send':
        # send(connection_id, msg)
        send(user_input[1], user_input[2])

    else:
        print("Try again")

# =============================== Send/Receive methods below ====================================================

# receive()

# receiveThread = threading.Thread(target=receive)
# receiveThread.daemon = True
# receiveThread.start()

# send("Hello Alex, From David", 2)

# print("Code completed successfully!")

# # Close the socket
# sock1.close()





