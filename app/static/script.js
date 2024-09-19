document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('button').addEventListener('click', updateMessage);
});

function updateMessage() {
    document.getElementById('message').innerHTML = 'Save and Exit to Main Screen';
    document.getElementById('title').innerHTML = 'Edit Teams Mode';
}
