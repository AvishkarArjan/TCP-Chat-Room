import socket
import threading

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1",8000)) # host,port

# we need 2 threads simultaneously running - to recieve and send message continously

def recieve():
    while True:
        try:
            message = client.recv(1024).decode("ascii") # we're still recieving messages from the client - dont get confused ?

            # if we get key 
            if (message== "NICK"):
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        
        except:
            print("An error occured !!!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

# multi threading
recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
