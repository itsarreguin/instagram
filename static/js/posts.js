const imageUpload = document.getElementById("image_upload");
const clearButton = document.getElementById("image-clear");

imageUpload.addEventListener("change", function() {
    const reader = new FileReader();

    reader.addEventListener("load", () => {
        let uploadedImage = reader.result;
        const imageContainer = document.getElementById("image");
        const image = document.createElement("img");
        image.setAttribute("id", "displayed-image");
        
        if (uploadedImage) {
            image.src = uploadedImage;
            imageContainer.style.display = "flex";
            imageContainer.appendChild(image);
            clearButton.style.display = "flex";

            clearButton.addEventListener("click", () => {
                imageContainer.style.display = "none";
                imageContainer.replaceChildren("");
                imageUpload.value = "";
            });

            new Cropper(image, {
                aspectRatio: 1 / 1,
                crop(event) {
                    console.log(event.detail.x);
                    console.log(event.detail.y);
                    console.log(event.detail.width);
                    console.log(event.detail.height);
                },
            });
        }
    });
    reader.readAsDataURL(this.files[0]);
});