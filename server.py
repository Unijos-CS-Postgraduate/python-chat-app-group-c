import socket
from threading import Thread

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5002
separator_token = '<SEP>'

connected_sockets = set()

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)

print("Server Listening...")

def listen_for_client(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f'error {e}')
            connected_sockets.remove(cs)
        else:
            msg = msg.replace(separator_token, ": ")

        for client_socket in connected_sockets:
            client_socket.send(msg.encode())
while True:
    client_socket, client_address = s.accept()
    print (f"{client_address} online!")
    connected_sockets.add(client_socket)
    server_msg = "\33[33m\33[1m"+ "Welcome online!"+"\33[0m"
    client_socket.send(server_msg.encode())

    t = Thread(target=listen_for_client, args=(client_socket, ))
    t.daemon = True

    t.start()
for cs in connected_sockets:
    cs.close()



s.close()
