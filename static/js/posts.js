function imageCropper(image) {
    const confirmButton = document.getElementById("publish");
    const csrf = document.getElementsByName("csrfmiddlewaretoken");

    const cropper = new Cropper(image, {
        aspectRatio: 1 / 1,
        scalable: false,
        minCropBoxWidth: 320,
	    minCropBoxHeight: 320,
    });
    confirmButton.addEventListener("click", (event) => {
        cropper.getCroppedCanvas().toBlob((blob) => {
            const formData = new FormData();
            formData.append("csrfmiddlewaretoken", csrf[0].value);
            formData.append("thumbnail", blob);

            fetch(postForm.action, {
                method: "POST",
                body: formData,
            })
            .then((response) => {
                return response.text();
            })
            .catch((err) => console.error(err));
        });
    });
}

function uploadImage() {
    const postForm = document.getElementById("create-post-form");
    const imageUpload = document.getElementById("post-image");
    const clearButton = document.getElementById("image-clear");
    
    imageUpload.addEventListener("change", function() {
        const reader = new FileReader();
        
        reader.addEventListener("load", () => {
            let uploadedImage = reader.result;
            const imageContainer = document.getElementById("image-container");
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
                imageCropper(image);
            }
        });
        reader.readAsDataURL(this.files[0]);
    });
}

uploadImage();