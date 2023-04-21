import threading
import socket

host = "127.0.0.1" # localhost
port = 8000

#starting service
server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
# bind the server to host and ip adress
server.bind((host,port))
server.listen() # listening mode

# client and nickname lists
clients =[]
nicknames =[]

# defining some methods
# 1 - broadcast - send a message to all the clients currently connected to the server
def broadcast(message):
    for client in clients:
        client.send(message)

# 2 - handling client connections - recieving message from client - send that back to all other clients

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            # if error - cut connection to the client
            index = clients.index(client) # getting list index of the client
            clients.remove(client)
            nickname = nicknames[index] # nickname of the client- which we would take from client while joining the chat room
            nicknames.remove(nickname)
            print(f"{nickname} left the chat room".encode("ascii"))

            break 

# 3 - recieve method - combine everythin

def recieve():
    while True:
        client, address = server.accept() # basically accepting all connections
        print(f"Connected with {str(address)}")

        #asking client for nickname- the first message that the client send to us should be the nickname - so thats what we're asking

        # this is a code we're sending to the client - the user doesnt see it  - if the client side recieves this - this should inform the client that it should ask for the nickname
        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        # adding to list
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat".encode("ascii"))
        client.send("Connected to the server !".encode("ascii"))

        # multi threading thing - define and running a thread
        #PS  - LEARN MORE 'BOUT THREADING MODULE
        thread = threading.Thread(target=handle, args=(client,))
        thread.start() # you need start() instead of run()

# calling recieve - starting the server when file is run
print("Sever is listening...")
recieve()
