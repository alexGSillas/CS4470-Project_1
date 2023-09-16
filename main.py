
# might need to change the delays wi
# ========================================


# Import the necessary modules
import socket
import threading
import time


# IP and port of Tello
tello1_address = ('10.85.38.178', 9010)

# IP and port of local computer
local1_address = ('10.85.39.138', 9010)


# Create a UDP connection that we'll send the command to
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Bind to the local address and port
sock1.bind(local1_address)

dronemessage = ''


# Send the message to Tello and allow for a delay in seconds
def send(message, delay):
    # Try to send the message otherwise print the exception
    try:
        sock1.sendto(message.encode(), tello1_address)

        print("Sending message: " + message)
    except Exception as e:
        print("Error sending: 1" + str(e))

    # Delay for a user-defined period of time
    time.sleep(delay)


# Receive the message from Tello and hexapod

def receive():
    # Continuously loop and listen for incoming messages
    while True:
        # Try to receive the message otherwise print the exception
        try:
            response1, ip_address = sock1.recvfrom(2048)

            print("Received message: from David EDU #1: " + response1.decode(encoding='utf-8'))

        except Exception as e:
            # If there's an error close the socket and break out of the loop
            sock1.close()

            print("Error receiving: 2" + str(e))
            break


receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()



# Put Tello into command mode
send("Hello David", 3)



print("Mission completed successfully!")

# Close the socket
sock1.close()



