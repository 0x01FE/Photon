import logging
import socket
import select

HOST = '127.0.0.1'
BROADCAST_PORT = 7500
RECIEVE_PORT = 7501

broadcasting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
broadcasting_socket.bind((HOST, BROADCAST_PORT))

recieving_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recieving_socket.bind(('', RECIEVE_PORT))

write_sockets = [ broadcasting_socket ]
read_sockets = [ recieving_socket ]

send_queue = []
end_count = 0

"""
Format of received data will be integer:integer (equipment id of player transmitting:equipment id of player hit)

After the game start count down timer finishes, the software will transmit code 202

When the game ends, the software will transmit code 221 three times

When data is received, software will transmit equipment id of player that was hit

if player tags another player on their own team, transmit their own equipment id

If code 53 is received, the red base has been scored. If the player is on the green team, they will receive 100 points and a stylized letter "B" will be added to the left of their codename.

if code 43 is received, the green base has been scored. If the player is on the red team, they will receive 100 points and a stylized letter "B" will be added to the left of their codename.
"""
def listen() -> None:

    r_sockets, w_sockets, e_sockets = select.select(read_sockets, write_sockets, [])

    # Read Recieving Sockets
    for sock in r_sockets:
        if sock == recieving_socket:
            data = sock.recv(1024)

            if not data:
                logging.warn('Disconnected from server.')
                break
            
            data = int(data)
            
            # Reset end count if _NOT_ 221
            if data != 221:
                end_count = 0

            match data:
                case 202:
                    # TODO : Signal to another part of the program that the game has started
                    pass
                case 221:
                    end_count += 1

                    if end_count >= 3:
                        # TODO : Signal that game has ended
                        pass
                case 53:
                    # TODO : Signal that the red base has been scored.
                    pass
                case 43:
                    # TODO : Signal that the green base has been socred.
                    pass
                case _:
                    # TODO : When data is received, software will transmit equipment id of player that was hit
                    pass
            
            logging.debug(f'Data Recieved: "{data}"')

    # Send any messages in queue
    for sock in w_sockets:
        if sock == broadcasting_socket:
            message: int = send_queue.pop()

            # Try to send message
            try:
                broadcasting_socket.send(bytes(message))

            # If it didn't send put it back in the queue
            except Exception as e:
                logging.error(f'{e}')
                logging.error(f'Message: "{message}"')
                send_queue.append(message)


def hit_player(id: int) -> None:
    send_queue.append(id)


while True:
    listen()