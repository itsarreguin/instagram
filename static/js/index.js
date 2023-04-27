// User dropdown ment consts
const navBtn = document.getElementById("nav-menu-btn");
const navMenu = document.getElementById("nav-menu");
// Post modal consts
const openModalBtn = document.getElementById("open-popup");
const closeModalBtn = document.getElementById("close-popup");
const popup = document.getElementById("post-modal");

const openNavMenu = (event) => {
    if (!navMenu.classList.contains("nav-dropdown-show")) {
        navMenu.classList.add("nav-dropdown-show");
    } else {
        navMenu.classList.remove("nav-dropdown-show");
    }
}

navBtn.addEventListener("click", openNavMenu);

const openModal = (event) => {
    if (!popup.classList.contains("container-modal-show")) {
        popup.classList.add("container-modal-show");
    }
}

const closeModal = (event) => {
    if (popup.classList.contains("container-modal-show")) {
        popup.classList.remove("container-modal-show");
    }
}

openModalBtn.addEventListener("click", openModal);
closeModalBtn.addEventListener("click", closeModal);