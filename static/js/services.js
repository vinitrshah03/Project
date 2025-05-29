document.addEventListener("DOMContentLoaded", function () {
    const serviceCards = document.querySelectorAll(".service-card");

    serviceCards.forEach(card => {
        card.addEventListener("click", function () {
            window.location.href = this.getAttribute("data-url");
        });
    });
});
