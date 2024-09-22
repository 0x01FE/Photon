document.addEventListener('DOMContentLoaded', () => {
    // Get all player-name and player-id inputs
    const inputs = document.querySelectorAll('.player-name');

    inputs.forEach((input) => {
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
});

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const splashScreen = document.getElementById('splash-screen');
        splashScreen.style.opacity = '0';

        splashScreen.addEventListener('transitionend', () => {
            splashScreen.style.display = 'none';

            window.location.href = '/gameAction';
        });
    }, 3000);
});

function checkEditScreenInputs(event) { 
    const form = event.target;
    let player_name, player_id, equipment_id;

    for(let i = 1; i<= 20; i++){
        player_name = form.querySelector(`#player_name_${i}`).value.trim();
        player_id = form.querySelector(`#player_id_${i}`).value.trim();

        if((player_name === "" && player_id === "" && equipment_id === "") || (player_name !== "" && player_id !== "" && equipment_id !== "")){
            return;
        }
         else if (player_name == "" || player_id === "" || equipment_id === "") {
            alert('Please fill out all fields');
            event.preventDefault();
            return;
        }
    }
};


// document.addEventListener('DOMContentLoaded', () => {
//     document.querySelector('button').addEventListener('click', () => {
//         window.location.href = '/editMode';
//     });
// });

// function toEditMode() {
//     window.location.href = '/editMode';
//     // document.getElementById('message').innerHTML = 'Save and Exit to Main Screen';
// }

// function toMainScreen() {
//     window.location.href = '/gameAction';
//     document.getElementById('message').innerHTML = 'Edit Teams';
//     // document.getElementById('title').innerHTML = 'Main';
// }
