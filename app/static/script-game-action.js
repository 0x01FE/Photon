document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('start-button');
    const modeButton = document.getElementById('mode-button');

    startButton.addEventListener('click', () => {
        startGame();
    });
    
    modeButton.addEventListener('click', () => {
        if (modeButton.firstElementChild.innerHTML === 'Edit Teams') {
            toEditMode();
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'F5') {
            startGame();
            event.preventDefault();
        }
        if (event.key === 'F12'){
            event.preventDefault();
            if (modeButton.firstElementChild.innerHTML === 'Edit Teams') {
                toEditMode();
            }
        }
    });
});

function toEditMode() {
    document.getElementById('button1').innerHTML = 'Back to Main Screen';
    window.location.href = '/editMode';
}

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
