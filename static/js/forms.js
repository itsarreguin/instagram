const newCollectionBtn = document.getElementById("collection-btn");
const newCollModal = document.getElementById("collection-modal");
const closeCollectionBtn = document.getElementById("close-collection");

newCollectionBtn.addEventListener("click", function(event) {
    if (!newCollModal.classList.contains("container-modal-show")) {
        newCollModal.classList.add("container-modal-show");
    }
});

closeCollectionBtn.addEventListener("click", function(evnet) {
    if (newCollModal.classList.contains("container-modal-show")) {
        newCollModal.classList.remove("container-modal-show");
    }
});