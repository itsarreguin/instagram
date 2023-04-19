const imageUpload = document.getElementById("image_upload");

imageUpload.addEventListener("change", function() {
    const reader = new FileReader();

    reader.addEventListener("load", () => {
        let uploadedImage = reader.result;
        const imageContainer = document.getElementById("image");
        const image = document.createElement("img");
        
        if (uploadedImage) {
            image.src = uploadedImage;
            imageContainer.append(image);
        }
    });
    reader.readAsDataURL(this.files[0]);
});