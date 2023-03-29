const settings = document.getElementById("settings");

settings.seed.value = Math.round(Math.random() * 1000000000);
const menu = new Menu();
const menuButton = document.getElementById("menu-button");
menuButton.onclick = () => menu.show();

const selectedDecks = settings.selectedDecks;
for (deck in decks) {
    option = stringToHtml(`<option value=${deck}>${deck.replace("-", " ")}</option>`);
    selectedDecks.add(option);
}

let gameboard = new Gameboard(settings);
settings.onchange = () => gameboard = new Gameboard(settings);

function stringToHtml(str) {
    const e = document.createElement("div");
    e.innerHTML = str;
    return e.firstChild;
}
