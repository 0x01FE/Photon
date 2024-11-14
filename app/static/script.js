document.addEventListener('DOMContentLoaded', () => {
    // Get all player-name and player-id inputs
    const playerInputs = document.querySelectorAll('.player-name');
    const idInputs = document.querySelectorAll('.player-id');
    const equipIdInputs = document.querySelectorAll('.equipment-id');

    idInputs.forEach((input) => {
        const icon = input.previousElementSibling;

        if (icon && icon.classList.contains('icon')) {
            input.addEventListener('focus', () => {
                icon.style.opacity = '1';
            });

            input.addEventListener('blur', () => {
                if (input.value === '') {
                    icon.style.opacity = '0';
                }
            });
        }
    });

    playerInputs.forEach((input) => {
        const icon = input.previousElementSibling.previousElementSibling;
        if (icon && icon.classList.contains('icon')) {
            input.addEventListener('focus', () => {
                icon.style.opacity = '1';
            });
            input.addEventListener('blur', () => {
                if (input.value === '') {
                    icon.style.opacity = '0';
                }
            });
        }
    });

    equipIdInputs.forEach((input) => {
        const icon = input.previousElementSibling.previousElementSibling.previousElementSibling;
        if (icon && icon.classList.contains('icon')) {
            input.addEventListener('focus', () => {
                icon.style.opacity = '1';
            });
            input.addEventListener('blur', () => {
                if (input.value === '') {
                    icon.style.opacity = '0';
                }
            });
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const splashScreen = document.getElementById('splash-screen');
        splashScreen.style.opacity = '0';

        splashScreen.addEventListener('transitionend', () => {
            splashScreen.style.display = "none";
            window.location.href = '/editMode';
        });
    }, 3000);
});

document.addEventListener('DOMContentLoaded', () => {
    const modeButton = document.getElementById('mode-button');
    const clearButton = document.getElementById('clear-button');

    modeButton.addEventListener('click', () => {
        if (modeButton.firstElementChild.innerHTML === 'Edit Teams') {
            this.toEditMode();
        } else {
            this.toGameAction();
        }
    });

    clearButton.addEventListener('click', () => {
        clearInputs();
        clearTeams();
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'F5') {
            event.preventDefault();
            if (modeButton.firstElementChild.innerHTML === 'Edit Teams') {
                toEditMode();
            } else {
                toGameAction();
            }
        }
        if (event.key === 'F12') {
            event.preventDefault();
            clearInputs();
            clearTeams();
        }
    });
});

function checkEditScreenInputs(event) {
    const form = event.target;
    let equipment_id;

    for (let i = 1; i <= 20; i++) {
        equipment_id = form.querySelector(`#equipment_id_${i}`).value.trim();

        if (equipment_id !== '') {
            return;
        } else if (equipment_id === '') {
            alert('Please fill out all fields');
            event.preventDefault();
            return;
        }
    }
}


function toEditMode() {
    document.getElementById('button1').innerHTML = 'Back to Main Screen';
    window.location.href = '/editMode';
}

function toGameAction() {
    document.getElementById('button1').innerHTML = 'Edit Teams';
    window.location.href = '/gameAction';
}

async function clearTeams(){
    let response = await fetch("/clearTeams", {
        method: "POST"
    });
    console.log("Starting game with response: " + response);

}

function clearInputs() {
    const playerInputs = document.querySelectorAll('.player-name');
    const idInputs = document.querySelectorAll('.player-id');
    const equipIdInputs = document.querySelectorAll('.equipment-id');

    alert('Clearing all Player Entries');

    playerInputs.forEach((input) => {
        input.value = '';
    });

    idInputs.forEach((input) => {
        input.value = '';
    });

    equipIdInputs.forEach((input) => {
        input.value = '';
    });
}
