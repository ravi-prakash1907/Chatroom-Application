import socket
import select
import errno
import sys

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

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

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error", str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()
