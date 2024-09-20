from flask import Flask, render_template

app = Flask(__name__)


@app.route("/editMode")
def addPlayer():
    return render_template("add-player/add-player.html")


@app.route("/")
def index():
    return render_template("splash-screen/splash-screen.html")


@app.route("/gameAction")
def gameAction():
    return render_template("game-action/game-action.html")


if __name__ == "__main__":
    app.run(debug=True)
