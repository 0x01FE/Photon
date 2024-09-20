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
