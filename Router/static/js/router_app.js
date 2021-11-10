
let switchMode = document.querySelector('.form-check-input');
switchMode.addEventListener('click', () => {
    if (switchMode.checked) {
        document.cookie = "mode=dark; path=/";
    }
});