let navBtn = document.getElementById("nav-menu-btn");
let navMenu = document.getElementById("nav-menu");

const openNavMenu = (event) => {
    if (!navMenu.classList.contains("nav-dropdown-show")) {
        navMenu.classList.add("nav-dropdown-show");
    } else {
        navMenu.classList.remove("nav-dropdown-show");
    }
}

navBtn.addEventListener("click", openNavMenu);