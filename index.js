const settings = document.getElementById("settings");

const solutionColors = {
    "team1": settings.team1Color.value,
    "team2": settings.team2Color.value,
    "team3": settings.team3Color.value,
    "team4": settings.team4Color.value,
    "neutral": settings.neutralColor.value,
    "death": settings.deathColor.value
}



settings.seed.value = Math.round(Math.random() * 1000000000);
const menu = new Menu();
const menuButton = document.getElementById("menu-button");
menuButton.onclick = () => menu.show();



let gameboard = new Gameboard(settings);

settings.onchange = () => gameboard = new Gameboard(settings);



settings.team1Color.onchange = () => solutionColors["team1"] = settings.team1Color.value;
settings.team2Color.onchange = () => solutionColors["team2"] = settings.team2Color.value;
settings.team3Color.onchange = () => solutionColors["team3"] = settings.team3Color.value;
settings.team4Color.onchange = () => solutionColors["team4"] = settings.team4Color.value;
settings.neutralColor.onchange = () => solutionColors["neutral"] = settings.neutralColor.value;
settings.deathColor.onchange = () => solutionColors["death"] = settings.deathColor.value;



function stringToHtml(str) {
    const e = document.createElement("div");
    e.innerHTML = str;
    return e.firstChild;
}
