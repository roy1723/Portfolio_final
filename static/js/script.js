const menuIcon = document.querySelector('#menu-icon');
const navbar = document.querySelector('.navbar');
menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x')
    navbar.classList.toggle('active');
}
const spinnerWrapperEl = document.querySelector('.loader')
window.addEventListener('load', () => {
    spinnerWrapperEl.style.opacity = '0';
    setTimeout(() => {
        spinnerWrapperEl.style.display = 'none';

    },  1200);
})

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("contactForm");

    // Replace this with your environment variable
    const formspreeUrl = process.env.FORMSPREE_URL;

    form.action = formspreeUrl;
});
