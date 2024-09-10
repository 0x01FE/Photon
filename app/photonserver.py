import logging
import socket
import select

HOST = ''
BROADCAST_PORT = 7500
RECIEVE_PORT = 7501

broadcasting_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcasting_socket.bind((HOST, BROADCAST_PORT))

recieving_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recieving_socket.bind((HOST, RECIEVE_PORT))

write_sockets = [ broadcasting_socket ]
read_sockets = [ recieving_socket ]

send_queue = []
end_count = 0

FORMAT = "%(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logging.getLogger('socket').setLevel(logging.ERROR)


"""
Format of received data will be integer:integer (equipment id of player transmitting:equipment id of player hit)

After the game start count down timer finishes, the software will transmit code 202

When the game ends, the software will transmit code 221 three times

When data is received, software will transmit equipment id of player that was hit

if player tags another player on their own team, transmit their own equipment id

If code 53 is received, the red base has been scored. If the player is on the green team, they will receive 100 points and a stylized letter "B" will be added to the left of their codename.

if code 43 is received, the green base has been scored. If the player is on the red team, they will receive 100 points and a stylized letter "B" will be added to the left of their codename.
"""
class PhotonServer:

    send_queue: list[bytes]

    # looks something like {equipment_id : score}
    player_scores: dict[int, int]

    def __init__(self):
        self.send_queue = []
        self.player_scores = {}

    def add_player(self, id: int | str) -> None:
        if id not in self.player_scores:
            self.player_scores[str(id)] = 0

    def award_points(self, id: str, score: int | None = 10) -> None:
        self.send_queue.append(id.encode())
        self.player_scores[id] += score

    def end_game(self) -> None:
        for _ in range(3):
            self.send_queue.append('221'.encode())

    def listen(self) -> None:
        r_sockets, w_sockets, e_sockets = select.select(read_sockets, write_sockets, [])

        # Read Recieving Sockets
        for sock in r_sockets:
            sock: socket.socket = sock

            if sock == recieving_socket:
                data = sock.recv(1024)

                if not data:
                    logging.warning('Disconnected from server.')
                    break

                data = data.decode()

                # Format of received data will be integer:integer (equipment id of player transmitting:equipment id of player hit)
                attacker, victim = data.split(':')

                # Green Base was hit
                if victim == 43:
                    # TODO : hit green base
                    pass
                # Red Base was hit
                elif victim == 53:
                    # TODO : hit red base
                    pass
                elif attacker == victim:
                    self.award_points(attacker, -10)
                else:
                    self.award_points(attacker)

                logging.debug(f'Data Recieved: "{data}"')

        # Send any messages in queue
        for sock in w_sockets:
            if sock == broadcasting_socket and send_queue:
                message: bytes = send_queue.pop()

                # Try to send message
                try:
                    broadcasting_socket.send(message)

                # If it didn't send put it back in the queue
                except Exception as e:
                    logging.error(f'{e}')
                    logging.error(f'Message: "{message}"')
                    send_queue.append(message)

# Code for Debugging

# s = PhotonServer()
# s.add_player(1)
# while True:
#     s.listen()

