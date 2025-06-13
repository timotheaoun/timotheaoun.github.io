// Sélection du menu contextuel
const contextMenu = document.getElementById("contextMenu");

// Fonction pour afficher le menu
document.addEventListener("contextmenu", (event) => {
    event.preventDefault(); // Empêche le menu contextuel par défaut
    contextMenu.style.display = "block";
    contextMenu.style.top = `${event.clientY}px`;
    contextMenu.style.left = `${event.clientX}px`;
});

// Fonction pour cacher le menu lorsqu'on clique ailleurs
document.addEventListener("click", () => {
    contextMenu.style.display = "none";
});
