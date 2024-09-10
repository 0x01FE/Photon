import socket

# THIS FILE IS ONLY MEANT TO TEST THE PHOTON SERVER

HOST = '127.0.0.1'
PORT = 7501 # Our recieve port in udp.py

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


print('Entering UDP tester, type int codes to send them to the server.')
print('Type "q" to exit.')
while True:
    user_input = input('$ ')

    if user_input.lower() == 'q' or user_input.lower() == 'exit':
        print('Exiting Tester')
        break

    sock.connect((HOST, PORT))
    sock.send(user_input.encode())

    print(f'Code: "{user_input}" sent.')







