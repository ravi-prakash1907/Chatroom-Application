from EnigmaEncryption import encoder
from EnigmaEncryption import decoder
from threading import Thread #   new

import socket
import select
import errno
import sys

HEADER_LENGTH = 10
clientSocket = None     #   new

def connect(ip, port, myUsername, error_callback):   #  new
    global clientSocket

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        clientSocket.connect((ip, port))
    except Exception as e:
        error_callback('Connection error: {}'.format(str(e)))
        return False

    username = myUsername.encode("utf-8")
    usernameHeader = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
    clientSocket.send(usernameHeader + username)

    return True

def send(message):
    message = encoder.mainFun(message) #######################################
    message = message.encode("UTF-8")
    messageHeader = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    clientSocket.send(messageHeader + message)

def start_listening(incoming_message_callback, error_callback):
    t = Thread(target=listen, args=(incoming_message_callback, error_callback,))
    t.start()

def listen(incoming_message_callback, error_callback):
    while True:
        try:
            while True:
                #receive things
                usernameHeader = clientSocket.recv(HEADER_LENGTH)
                if not len(usernameHeader):
                    error_callback("Server is down!!!")
                    #sys.exit()
                usernameLen = int(usernameHeader.decode("utf-8").strip())
                username = clientSocket.recv(usernameLen).decode("utf-8")

                messageHeader = clientSocket.recv(HEADER_LENGTH)
                messageLen = int(messageHeader.decode("utf-8").strip())
                message = clientSocket.recv(messageLen).decode("utf-8")
                message = decoder.mainFun(message)  ####################################

                #print(f"{username} > {message}")
                incoming_message_callback(username, message)
                #incoming_message_callback(f"{username} > {message}")

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                error_callback("Reading error", str(e))
                #sys.exit()
            continue

        except Exception as e:
            error_callback('General error', str(e))
            #sys.exit()





'''

IP = "127.0.0.1"
PORT = 4234

myUsername = input("Username: ")

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((IP, PORT))
clientSocket.setblocking(False) # so recieved functionality won't be blocking

username = myUsername.encode("utf-8")
usernameHeader = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
clientSocket.send(usernameHeader + username)

while True:
    message = input(f"{myUsername} > ") # DISABLE this if line below is enabled
    #message = ""                   # ENABLE to run this client just as server ie.e can only read

    if message:
        message = encoder.mainFun(message) #######################################
        message = message.encode("UTF-8")
        messageHeader = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        clientSocket.send(messageHeader + message)

    try:
        while True:
            #receive things
            usernameHeader = clientSocket.recv(HEADER_LENGTH)
            if not len(usernameHeader):
                print("Connection closed by server")
                sys.exit()
            usernameLen = int(usernameHeader.decode("utf-8").strip())
            username = clientSocket.recv(usernameLen).decode("utf-8")

            messageHeader = clientSocket.recv(HEADER_LENGTH)
            messageLen = int(messageHeader.decode("utf-8").strip())
            message = clientSocket.recv(messageLen).decode("utf-8")
            message = decoder.mainFun(message)  ####################################

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error", str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()

'''
