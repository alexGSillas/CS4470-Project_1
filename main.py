#=================TODO==========================
#need to include the arguments in the methods & get rid of LiDAR 
#delete comments about drones
#make sure it's TCP not UDP
#in the end, clean up all the files

#set time for testing
# ========================================


# Import the necessary modules
import socket
import threading
import time

print("running first line...")

# IP and port
tello1_address = ('10.85.38.178', 9000)

# IP and port of local computer
local1_address = ('', 9010)


# Create a UDP connection that we'll send the command to
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Bind to the local address and port
sock1.bind(local1_address)

dronemessage = ''

#======================================== main =================================================
if __name__ == '__main__':    
    import sys
    
    if len(sys.argv)<2:
        print ("Parameter error: Please assign the device")
        exit() 
    if sys.argv[1] == 'myip': 
        myip() 
    elif sys.argv[1] == 'myport' or sys.argv[1] == '3d': 
        myport()
    elif sys.argv[1] == 'connect' or sys.argv[1] == 'accel': 
        connect()
    elif sys.argv[1] == 'list' or sys.argv[1] == 'gyro': 
        list()
    elif sys.argv[1] == 'terminate' or sys.argv[1] == '____': 		#RPY = roll, pitch, yaw
        terminate()
    elif sys.argv[1] == 'send' or sys.argv[1] == 'LiDar' or sys.argv[1] == 'lidar': 
        send()
    elif sys.argv[1] == 'exit' or sys.argv[1] == 'LiDar' or sys.argv[1] == 'lidar': 
        exit()

#================================= 3.3 Functionality Methods ===============================================================
# help() method
def help():
    print("Here are a list of commands:")
    print(" myip \n myport \n connect \n list \n terminate \n send \n exit \n")
    

# myip() method
def myip():
    print("My IP is: " + _______ )


# connect() method
def connect():
    #** insert method here **


# list() method
def list():
    #** insert code here**


# terminate() method
def terminate():
    #** insert code here**
    

# send() method
def send():
    #** insert code here**
    
    
# exit() method
def exit():
    #** insert code here**

#=============================== Send/Receive methods below ====================================================
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


# Receive the message 
def receive():
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


receive()

receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()

send("Hello Alex, From David", 2)

print("Code completed successfully!")

# Close the socket
sock1.close()





