import socket

# THIS FILE IS ONLY MEANT TO TEST THE PHOTON SERVER

HOST = '127.0.0.1'
PORT = 7501 # Our recieve port in udp.py
RECV_PORT = 7500

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

recv_sock.bind(('', RECV_PORT))

def listen() -> str:
    data, addr = recv_sock.recvfrom(1024)

    return data.decode()

print('Entering UDP tester, type int codes to send them to the server.')
print('Type "q" to exit.')
print(f'Type "l" to listen for incoming messages on port {RECV_PORT}.')
print('Otherwise type what code you want to send to the photon server.')
while True:
    user_input = input('$ ')

    if user_input.lower() == 'q' or user_input.lower() == 'exit':
        print('Exiting Tester')
        break
    elif user_input.lower() == 'l':
        data = listen()

        print(f'Recevied Data: "{data}"')
    else:

        sock.connect((HOST, PORT))
        sock.send(user_input.encode())

        print(f'Code: "{user_input}" sent.')

        data = listen()

        print(f'Recevied Data: "{data}"')

