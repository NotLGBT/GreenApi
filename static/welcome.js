document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("container");
    const text = document.getElementById("text");

    setTimeout(() => {
        container.classList.add("centered");

        setTimeout(() => {
            text.classList.add("visible");
        }, 1000); 
    }, 3000); 
});
