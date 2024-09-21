from flask import Flask, request, render_template

app = Flask(__name__)

RED_TEAM_PLAYERS = []
GREEN_TEAM_PLAYERS = []

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
def submitRedTeams() -> None:
     for i in range(1, 21):
        player_name = request.form.get(f"player_name_{i}")
        player_id = request.form.get(f"player_id_{i}")
        if player_name and player_id:
            RED_TEAM_PLAYERS.append({f"name_{i}": player_name, f"id_{i}": player_id})
     return "", 204


@app.route("/submit-green", methods = ["POST"])
def submitGreenTeams() -> None:
     for i in range(1, 21):
        player_name = request.form.get(f"player_name_{i}")
        player_id = request.form.get(f"player_id_{i}")
        if player_name and player_id:
            GREEN_TEAM_PLAYERS.append({f"name_{i}": player_name, f"id_{i}": player_id})
     return "", 204


if __name__ == "__main__":
    app.run(debug=True)
