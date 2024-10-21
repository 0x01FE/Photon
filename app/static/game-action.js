document.addEventListener('DOMContentLoaded', () => {
    const modeButton = document.getElementById('mode-button');

    modeButton.addEventListener('click', () => {
        window.location.href = '/editMode';
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'F5') {
            startGame();
            event.preventDefault();
        }
    });
});

// I do _not_ like Javascript. - Jackson
async function startGame() {
    let response = await fetch("/start-game", {
        method: "POST"
    });
    console.log("Starting game with response: " + response);
    
    const timerEl = document.getElementById('timer');
    let countdownTime = 30;

    let countdownTimer = setInterval(function() {
        timerEl.innerHTML = "GAME START - 00:" + (countdownTime < 10 ? '0' : '') + countdownTime;
        countdownTime--;
        if (countdownTime < 0) {
            stopTimer();
        }
    }, 1000);

    function stopTimer() {
        clearInterval(countdownTimer);
        realStartGame();
    }
}

async function realStartGame() {
    const timerEl = document.getElementById('timer');
    let countdownTime = 6 * 60;

    let countdownTimer = setInterval(function() {
        timerEl.innerHTML = "GAME END - 0" + Math.floor(countdownTime/60) + ":" + (countdownTime % 60 < 10 ? '0' : '') + (countdownTime % 60);
        countdownTime--;

        if (countdownTime < 0) {
            stopTimer();
        }
    }, 1000);

    function stopTimer() {
        clearInterval(countdownTimer);
    }
}

