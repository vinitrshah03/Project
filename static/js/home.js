'use strict';

const menuToggle = document.querySelector('.menu-toggle');
const bxMenu = document.querySelector('.bx-menu');
const bxX = document.querySelector('.bx-x');
const navBar = document.querySelector('.navbar');

// --- open menu ---
bxMenu.addEventListener('click', (e) => {
    if (e.target.classList.contains('bx-menu')) {
        navBar.classList.add('show-navbar');
        bxMenu.classList.add('hide-bx');
        bxX.classList.add('show-bx');
    }
});

// --- close menu ---
bxX.addEventListener('click', (e) => {
    if (e.target.classList.contains('bx-x')) {
        navBar.classList.remove('show-navbar');
        bxMenu.classList.remove('hide-bx');
        bxX.classList.remove('show-bx');
    }
});

// --- Add click functionality for service cards ---
document.addEventListener("DOMContentLoaded", function () {
    const serviceCards = document.querySelectorAll(".service-card");

    serviceCards.forEach(card => {
        card.addEventListener("click", function () {
            window.location.href = this.getAttribute("data-url");
        });
    });
});
