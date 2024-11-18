document.addEventListener("DOMContentLoaded", () => {
    const startButton = document.getElementById("start-button");
    const modeButton = document.getElementById("mode-button");

    startButton.addEventListener("click", () => {
        playMusic();
        startGame();
    });

    modeButton.addEventListener("click", () => {
        if (modeButton.firstElementChild.innerHTML === "Edit Teams") {
            toEditMode();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "F5") {
            startGame();
            startMsic();
            event.preventDefault();
        }
        if (event.key === "F12") {
            event.preventDefault();
            if (modeButton.firstElementChild.innerHTML === "Edit Teams") {
                toEditMode();
            }
        }
    });
});

function toEditMode() {
    document.getElementById("button1").innerHTML = "Back to Main Screen";
    window.location.href = "/editMode";
}

// I do _not_ like Javascript. - Jackson
async function startGame() {
    let response = await fetch("/start-game", {
        method: "POST",
    });
    console.log("Starting game with response: " + response);

    const popUpEl = document.getElementById("pop-up");
    popUpEl.style.visibility = "visible";
    popUpEl.style.display = "inline-block";

    const shortTimerEl = document.getElementById("short-timer");
    let countdownTime = 15;
    document.getElementById("timer").innerHTML = "STARTING GAME...";

    let countdownTimer = setInterval(function() {

        console.log("Countdown time: " + countdownTime);

        if (countdownTime > 0) {
            shortTimerEl.innerHTML = (countdownTime < 10 ? '0' : '') + countdownTime;
        }else if (countdownTime <= 0 && countdownTime > -1) {
            shortTimerEl.innerHTML = "STARTING GAME...";
        } else {
            shortTimerEl.innerHTML = "BEGIN!";
        }
        countdownTime--;

        if (countdownTime < -2) {
            stopTimer();
        }
    }, 1000);

    function stopTimer() {
        clearInterval(countdownTimer);
        document.getElementById("pop-up").style.visibility = "hidden";
        document.getElementById("pop-up").style.display = "none";

        realStartGame();
    }
}

async function realStartGame() {
    const timerEl = document.getElementById("timer");
    let countdownTime = 6 * 60;

    let countdownTimer = setInterval(function () {
        timerEl.innerHTML = "TIME LEFT: 0" + Math.floor(countdownTime / 60) + ":" + (countdownTime % 60 < 10 ? "0" : "") + (countdownTime % 60);
        countdownTime--;

        if (countdownTime < -2) {
            stopTimer();
        }
        else if (countdownTime < 0) {
            timerEl.innerHTML = "GAME OVER";
        }
        
    }, 1000);

    function stopTimer() {
        clearInterval(countdownTimer);
        window.location.href = "/gameOver";
    }
}

function playMusic() {
    const num = Math.floor(Math.random() * 8) + 1;
    const audio = new Audio("/static/photon_tracks/Track0"+ num + ".mp3");

    console.log("Playing music: Track0" + num);
    audio.play();
}

const socket = io();
socket.on("new_action", (data) => {
    const currentActionContainer = document.querySelector(".current-action");
    const newAction = document.createElement("div");
    newAction.classList.add("action-alert");
    newAction.textContent = data.action;

    if (currentActionContainer.children.length > 5) {
        currentActionContainer.removeChild(currentActionContainer.firstChild);
    }

    currentActionContainer.appendChild(newAction);
    currentActionContainer.scrollTop = currentActionContainer.scrollHeight;
});

socket.on("new_red_score", (data) => {
    // Expecting `data` to be an object with keys `player_id` and `score`
    const { player_name, score } = data;
    console.log(score);

    // Find the element corresponding to the player's score
    const scoreElement = document.getElementById(`score_${player_name}`);
    console.log(scoreElement);

    if (scoreElement) {
        // Update the score
        scoreElement.textContent = score;
    } else {
        console.error(`No score element found for player ID: ${player_name}`);
    }
});


socket.on("new_green_score", (data) => {
    // Expecting `data` to be an object with keys `player_id` and `score`
    const { player_name, score } = data;

    // Find the element corresponding to the player's score
    const scoreElement = document.getElementById(`score_${player_name}`);
    
    if (scoreElement) {
        // Update the score
        scoreElement.textContent = score;
    } else {
        console.error(`No score element found for player ID: ${player_name}`);
    }
});