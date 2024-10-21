from flask import Flask, request, render_template
import photonserver
import database
import threading
import logging

app = Flask(__name__)

s = photonserver.PhotonServer()

red_players = []
green_players = []

FORMAT = "%(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logging.getLogger('socket').setLevel(logging.ERROR)


def run_server():
    logging.info('Photon Server Task Started')
    while True:
        s.update()


t = threading.Thread(target=run_server)
t.start()


@app.route("/")
def index():
    return render_template("splash-screen.html")


@app.route("/gameAction")
def gameAction():
    redPlayers = s.red_players;
    greenPlayers = s.green_players;

    return render_template(
        "game-action.html",
        actions=[],
        redPlayers=redPlayers,
        greenPlayers=greenPlayers,
    )

    # need to return who hit who and stuff, or however we wanna do it,
    #   just need to make list for the html to loop through and display
    # actions = database.get_actions()
    # actions = [
    #     "Scooby Doo hit Opus",
    #     "Scooby Doo hit Opus",
    #     "Scooby Doo hit Opus",
    #     "Opus hit Scooby Doo",
    #     "Opus hit the Base",
    #     "Opus hit Scooby Doo",
    # ]

    # redPlayers = ["Thor", "Loki", "Odin", "Dragon"]
    # greenPlayers = ["HappyFeet", "Toothless", "Ironman", "American", "Spiderman"]


@app.route("/editMode")
def addPlayer():
    return render_template("add-player.html")

@app.route("/clearTeams", methods=["POST"])
def clearAllTeams():
    logging.info("Clearing All Teams...")
    s.clear_teams
    red_players.clear()
    green_players.clear()
    logging.info("All Teams Cleared")
    return "", 200

'''
@app.route("/submit-red", methods = ["POST"])
def submitRedTeams():
    red_players = []
    for i in range(1, 21):
        player_id = request.form.get(f"player_id_{i}")
        equipment_id = request.form.get(f"equipment_id_{i}")
        player_name = request.form.get(f"player_name_{i}")
        logging.debug(f"P_ID: {player_id}, E_ID: {equipment_id}, P_NAME: {player_name}")
        
        if player_name and player_id and equipment_id:
            logging.debug("Adding Player with s.addplayer")
            s.add_player(player_id, equipment_id, 'r', player_name)
            red_players.append({f"name_{i}": player_name, f"id_{i}": player_id})
    return "", 204

@app.route("/submit-green", methods = ["POST"])
def submitGreenTeams():
    green_players = []
    for i in range(1, 21):
        player_id = request.form.get(f"player_id_{i}")
        equipment_id = request.form.get(f"equipment_id_{i}")
        player_name = request.form.get(f"player_name_{i}")
        logging.debug(f"P_ID: {player_id}, E_ID: {equipment_id}, P_NAME: {player_name}")

        if player_name and player_id and equipment_id:
            s.add_player(player_id, equipment_id, 'g', player_name)
            green_players.append({f"name_{i}": player_name, f"id_{i}": player_id})
    return "", 204
'''

@app.route("/start-game", methods=["POST"])
def startGame():
    s.start_game()
    return "", 200

@app.route("/submit-red", methods = ["POST"])
def submitRedTeams():
    for i in range(1, 21):
        player_id = request.form.get(f"player_id_{i}")
        if(player_id == ""):
            player_id = None
        if(database.get_codename_by_id(player_id) != None):
            equipment_id = request.form.get(f"equipment_id_{i}")
            player_name = database.get_codename_by_id(player_id)

            logging.debug(f"P_ID: {player_id}, E_ID: {equipment_id}, P_NAME: {player_name}")

            if player_name and player_id and equipment_id:
                logging.debug("Adding Player with s.addplayer")
                s.add_player(player_id, equipment_id, 'r', player_name)
                red_players.append({"name": player_name, "id": player_id, "equipment_id": equipment_id})
        else:
            equipment_id = request.form.get(f"equipment_id_{i}")
            player_name = request.form.get(f"player_name_{i}")
            logging.debug(f"P_ID: {player_id}, E_ID: {equipment_id}, P_NAME: {player_name}")

            if player_name and player_id and equipment_id:
                s.add_player(player_id, equipment_id, 'r', player_name)
                red_players.append({"name": player_name, "id": player_id, "equipment_id": equipment_id})
    
    return render_template('add-player.html', green_players=green_players, red_players=red_players)



@app.route("/submit-green", methods = ["POST"])
def submitGreenTeams():
    for i in range(1, 21):
        player_id = request.form.get(f"player_id_{i}")
        if(player_id == ""):
            player_id = None
        if(database.get_codename_by_id(player_id) != None):
            equipment_id = request.form.get(f"equipment_id_{i}")
            player_name = database.get_codename_by_id(player_id)

            logging.debug(f"P_ID: {player_id}, E_ID: {equipment_id}, P_NAME: {player_name}")

            if player_name and player_id and equipment_id:
                logging.debug("Adding Player with s.addplayer")
                s.add_player(player_id, equipment_id, 'g', player_name)
                green_players.append({"name": player_name, "id": player_id, "equipment_id": equipment_id})
        else:
            equipment_id = request.form.get(f"equipment_id_{i}")
            player_name = request.form.get(f"player_name_{i}")
            logging.debug(f"P_ID: {player_id}, E_ID: {equipment_id}, P_NAME: {player_name}")

            if player_name and player_id and equipment_id:
                s.add_player(player_id, equipment_id, 'g', player_name)
                green_players.append({"name": player_name, "id": player_id, "equipment_id": equipment_id})
    
    return render_template('add-player.html', green_players=green_players, red_players=red_players)


if __name__ == "__main__":
    app.run(debug=True)
