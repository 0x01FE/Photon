from typing import Literal
import logging
import socket
import select
import time

HOST = ''
BROADCAST_PORT = 7500
RECIEVE_PORT = 7501

# Various Codes
START_CODE = '202'
END_CODE = '221'
GREEN_BASE = '43'
RED_BASE = '53'

# Times
COUNTDOWN_DURATION_SECONDS = 5
GAME_DURATION_SECONDS = 6 * 60

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


# I know someone is going to comment on the id_ variable name but i'm just following the PEP-8 style guide :)
# https://peps.python.org/pep-0008/#descriptive-naming-styles
class Player:
    score = 0
    id_: int
    equipment_id: int
    hit_enemy_base = False
    codename: str

    def __init__(self, id_: int, equipment_id: int, codename: str | None = None):
        self.id_ = id_
        self.equipment_id = equipment_id

        if codename:
            self.codename = codename

    def award_points(self, points: int | None = 10) -> None:
        self.score += points

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

    countdown_started: bool
    game_started: bool
    game_start_time: float

    send_queue: list[bytes]

    # Key is equipment id as a string
    red_players: dict[str, Player]
    green_players: dict[str, Player]

    def __init__(self):
        self.send_queue = []

        self.red_players = {}
        self.green_players = {}

        self.countdown_started = False
        self.game_started = False

    """
    To add a player you need:
        A player ID
        Equipment ID for the player
        A team (Red or Green)
        and a codename if one isn't in the database

    The method will return True if the player is successfully added.
    """
    def add_player(self, player_id: int | str, equipment_id: int | str, team: Literal['R', 'G'], codename: str | None = None) -> bool:

        if type(player_id) == int:
            player_id = str(player_id)

        if type(equipment_id) == int:
            equipment_id = str(equipment_id)

        if equipment_id == RED_BASE or equipment_id == GREEN_BASE or equipment_id in self.red_players or equipment_id in self.green_players:
            logging.error('Equipment ID is already reserved.')
            return False

        new_player = Player(player_id, equipment_id, codename=codename)

        # TODO : add code to check if player_id has a codename in the database

        if team.lower() == 'r':
            if len(self.red_players) >= 15:
                logging.error('Red team is full.')
                return False

            if equipment_id not in self.red_players:
                self.red_players[str(equipment_id)] = new_player

        elif team.lower() == 'g':
            if len(self.green_players) >= 15:
                logging.error('Green team is full.')
                return False

            if equipment_id not in self.green_players:
                self.green_players[str(equipment_id)] = new_player

        else:
            logging.error('No team, or an invalid team was selected when adding a player. Player not added.')
            return False

        # After equipment id is entered, system will broadcast the equipment id through udp port 7500
        self.send_queue.append(equipment_id.encode())

        return True

    # There will be a way to clear all entries with a single button (f12 or equivalent)
    def clear_teams(self) -> None:
        self.red_players = {}
        self.green_players = {}

    # Crazy code here I know.
    def find_player_by_equipment_id(self, equipment_id: str) -> Player | None:
        if equipment_id in self.green_players:
            return self.green_players[equipment_id]

        elif equipment_id in self.red_players:
            return self.red_players[equipment_id]

        else:
            return None

    def start_game(self) -> None:
        self.game_start_time = time.time()
        self.countdown_started = True
        logging.info('Countdown Started.')

    def end_game(self) -> None:
        self.game_started = False
        for _ in range(3):
            self.send_queue.append(END_CODE.encode())

    def check_countdown(self) -> None:
        current_time: float = time.time()

        if current_time - self.game_start_time >= COUNTDOWN_DURATION_SECONDS and not self.game_started:
            self.game_started = True
            self.send_queue.append(START_CODE.encode())
            logging.info('Game Started.')
        elif current_time - self.game_start_time >= GAME_DURATION_SECONDS and self.game_started:
            self.end_game()
            logging.info('Game Ended.')

    # This is for debugging
    def print_scores(self) -> None:
        print('Red Team:')
        for key in self.red_players:
            p = self.red_players[key]
            print(' ' * 2, end='')
            print(f'{p.codename} | {p.score} ', end='')
            if p.hit_enemy_base:
                print(' B')
            else:
                print()

        print('Green Team:')
        for key in self.green_players:
            p = self.green_players[key]
            print(' ' * 2, end='')
            print(f'{p.codename} | {p.score} ', end='')
            if p.hit_enemy_base:
                print(' B')
            else:
                print()

    def update(self) -> None:
        r_sockets, w_sockets, e_sockets = select.select(read_sockets, write_sockets, [])

        if self.countdown_started:
            self.check_countdown()

        # Read Recieving Sockets
        for sock in r_sockets:
            sock: socket.socket = sock

            if sock == recieving_socket:
                data = sock.recv(1024)

                # No need to process a message if the game hasn't started
                if not self.game_started:
                    logging.info(f'Game has not started. Not accepting message "{data}".')
                    continue

                data = data.decode()

                # Format of received data will be integer:integer (equipment id of player transmitting:equipment id of player hit)
                if ':' not in data:
                    logging.error(f'Message "{data}" could not be processed by the server.')
                    continue

                attacker_id, victim_id = data.split(':')

                attacker = self.find_player_by_equipment_id(attacker_id)

                if victim_id == GREEN_BASE and attacker_id in self.red_players:
                    attacker.hit_enemy_base = True
                    attacker.award_points(100)
                    self.send_queue.append(victim_id.encode())
                    logging.info(f'{attacker.codename} hit the enemy base! +100 points')

                elif victim_id == RED_BASE and attacker_id in self.green_players:
                    attacker.hit_enemy_base = True
                    attacker.award_points(100)
                    self.send_queue.append(victim_id.encode())
                    logging.info(f'{attacker.codename} hit the enemy base! +100 points')

                else:
                    if (victim_id in self.red_players and attacker_id in self.red_players) or (victim_id in self.green_players and attacker_id in self.green_players):
                        attacker.award_points(-10)
                        self.send_queue.append(victim_id.encode())
                        logging.info(f'{attacker.codename} hit a friendly! -10 points')
                    else:
                        attacker.award_points(10)
                        self.send_queue.append(attacker_id.encode())
                        logging.info(f'{attacker.codename} hit a hostile! +10 points')

                self.print_scores()
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
# s.add_player(1, 1, 'R', 'John Photon')
# s.add_player(2, 2, 'G', 'Jimmy Neutron')
# s.start_game()
# while True:
#     s.update()
