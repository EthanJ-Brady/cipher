const settings = document.getElementById("settings");

settings.seed.value = Math.round(Math.random() * 1000000000);
const menu = new Menu();
const menuButton = document.getElementById("menu-button");
menuButton.onclick = () => menu.show();

const selectedDecks = settings.selectedDecks;
var deckKeys = Object.keys(decks);
deckKeys.sort();
for (deckKey of deckKeys) {
    option = stringToHtml(`<option value="${deckKey}">${deckKey}</option>`);
    selectedDecks.add(option);
}

let gameboard = new Gameboard(settings);
settings.onchange = () => {
    gameboard = new Gameboard(settings);
}

function stringToHtml(str) {
    const e = document.createElement("div");
    e.innerHTML = str;
    return e.firstChild;
}
