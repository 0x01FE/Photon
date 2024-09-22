from flask import Flask, request, render_template
from celery import Celery
import photonserver
import database
import threading
import logging

app = Flask(__name__)

#app.config['CELERY_BROKER_URL'] = "sqla+postgresql://student:student@localhost:5432/photon"
#app.config['CELERY_RESULT_BACKEND'] = "sqla+postgresql://student:student@localhost:5432/photon"

def make_celery(app):
    celery = Celery(app.import_name, broker="sqla+postgresql://student:student@localhost:5432/photon")
    celery.conf.update(app.config)
    return celery
celery = make_celery(app)
s = photonserver.PhotonServer()

FORMAT = "%(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logging.getLogger('socket').setLevel(logging.ERROR)

@celery.task
def run_server():
    print('Celery Photon Server Task Started')
    while True:
        s.update()

@app.route("/")
def index():
    return render_template("splash-screen/splash-screen.html")

@app.route("/gameAction")
def gameAction():
    return render_template("game-action/game-action.html")

@app.route("/editMode")
def addPlayer():
    return render_template("add-player/add-player.html")

@app.route("/submit-red", methods = ["POST"])
def submitRedTeams():
    red_players = []
    for i in range(1, 21):
        player_id = request.form.get(f"player_id_{i}")
        equipment_id = request.form.get(f"equipment_id{i}")
        player_name = request.form.get(f"player_name_{i}")
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
        equipment_id = request.form.get(f"equipment_id{i}")
        player_name = request.form.get(f"player_name_{i}")
        if player_name and player_id and equipment_id:
            s.add_player(player_id, equipment_id, 'g', player_name)
            green_players.append({f"name_{i}": player_name, f"id_{i}": player_id})
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)

