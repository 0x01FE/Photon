document.addEventListener('DOMContentLoaded', () => {
    const actionButton = document.getElementById('action-button');
    const editButton = document.getElementById('clear-button');

    actionButton.addEventListener('click', () => {
        toGameAction();
    });

    editButton.addEventListener('click', () => {
        toEditMode();
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'F5') {
            event.preventDefault();
            toGameAction();
        }
        if (event.key === 'F12') {
            event.preventDefault();
            toEditMode();
        }
    });
});

function toGameAction() {
    window.location.href = "/gameAction";
}

function toEditMode() {
    window.location.href = "/editMode";
}