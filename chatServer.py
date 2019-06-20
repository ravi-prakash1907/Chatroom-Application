import socket
import select       # to manage many connection i.e. diferent Operation

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # cleare why we used setsockopt()

serverSocket.bind((IP, PORT))
serverSocket.listen()





def receiveMsg(clientSocket):
    try:
        msgHeader = clientSocket.recv(HEADER_LENGTH)
        if not len(msgHeader):
            return False

        msgLen = int(msgHeader.decode("utf-8").strip())
        return {"header": msgHeader, "data": clientSocket.recv(msgLen)}

    except:
        return False





# actual server stuff
socketList = [serverSocket]   #list of clients as soon as they connection

clients = {}

while True:
    readSockets, _, exceptionSocket = select.select(socketList, [], socketList)
    for notifiedSoc in readSockets:
        if notifiedSoc == serverSocket:     # someone has requested to connect
            clientSocket, clientAddr = serverSocket.accept()

            user = receiveMsg(clientSocket)
            if user is False:  # someone Disconnected
                continue

            socketList.append(clientSocket)
            clients[clientSocket] = user

            print(f"Accepted new connection from {clientAddr[0]}:{clientAddr[1]} username:{user['data'].decode('utf-8')}")

        else:
            message = receiveMsg(notifiedSoc)

            if message is False:
                print(f"Closed conn. from {clients[notifiedSoc]['data'].decode('utf-8')}")
                socketList.remove(notifiedSoc)
                del clients[notifiedSoc]
                continue

            user = clients[notifiedSoc]
            print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for clientSocket in clients:
                if clientSocket != notifiedSoc:
                    clientSocket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notifiedSoc in exceptionSocket:
        socketList.remove(notifiedSoc)
        del clients[notifiedSoc]

















#
