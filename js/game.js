function shuffle(seed, list) {
    Math.seedrandom(seed)

    list = [...list]

    let currentIndex = list.length,  randomIndex;
    while (currentIndex != 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;

        [list[currentIndex], list[randomIndex]] = [
        list[randomIndex], list[currentIndex]];
    }

    return list; 
}

function combineDecks(list) {
    combinedDeck = []
    for (const deckName of list) {
        combinedDeck.push(...decks[deckName]);
    }
    return combinedDeck;
}

class Card {
    constructor(title, color) {
        this.color = color;
        this.cardElement = new CardElement(title);
    }

    colorCard(bool) {
        if (bool) {this.cardElement.screen.style.backgroundColor = this.color;}
        else {this.cardElement.screen.style.backgroundColor = null;}
    }

    crossCard(bool) {
        if (bool) {
            this.cross = stringToHtml('<div class="card__cross"></div>');
            this.cardElement.element.appendChild(this.cross);
            this.cardElement.element.onclick = () => {
                this.crossCard(false);
                this.cardElement.element.onclick = () => this.crossCard(true);
            }
        }
        else {
            if (this.cross) {this.cross.remove();}
        }
    }

    reveal(bool) {
        if (bool) {
            this.colorCard(true);
            this.cardElement.element.classList.remove("card--unrevealed");
            this.cardElement.element.classList.remove("card--interactable");
        }
        else {
            this.colorCard(false);
            this.crossCard(false);
            this.cardElement.element.classList.add("card--unrevealed");
            this.cardElement.element.classList.add("card--interactable");
            this.cardElement.element.onclick = () => this.reveal(true);
        }
    }

    viewSolution(bool) {
        if (bool) {
            this.colorCard(true);
            this.cardElement.element.classList.add("card--interactable");
            this.cardElement.element.onclick = () => this.crossCard(true)
        }
        else {
            this.reveal(false);
        }
    }
}

class CardElement {
    constructor(title) {
        this.element = stringToHtml('<div class="card"></div>');
        this.texture = stringToHtml('<div class="card__texture"></div>'); 
        this.title = stringToHtml(`<div class="card__title">${title}</div>`);
        this.titleFlipped = stringToHtml(`<div class="card__title card__title--flipped">${title}</div>`); 
        this.screen = stringToHtml('<div class="card__screen"></div>');

        this.element.appendChild(this.title);
        this.element.appendChild(this.titleFlipped);
        this.element.appendChild(this.texture);
        this.element.appendChild(this.screen); 
    }
}

class Gameboard {
    constructor(settings) {
        const size = settings.size.value;
        const selectedDecks = settings.selectedDecks.selectedOptions;
        const seed = settings.seed.value;
        const viewSolution = settings.viewSolution.checked;
        const viewBidirectional = settings.viewBidirectional.checked;
        const teamCount = settings.teamCount.value;

        const colorDict = {
            "team1": settings.team1Color.value,
            "team2": settings.team2Color.value,
            "team3": settings.team3Color.value,
            "team4": settings.team4Color.value,
            "neutral": settings.neutralColor.value,
            "death": settings.deathColor.value
        }

        let combinedDeck = [];
        if (settings.showTitles.checked) {
            let selectedDeckValues = []
            for (const selectedDeck of selectedDecks) {
                selectedDeckValues.push(selectedDeck.value)
            }
            combinedDeck = combineDecks(selectedDeckValues);
        }
        else {
            combinedDeck = [];
        }

        this.element = document.getElementById("gameboard");
        this.deck = new Deck(
            size,
            shuffle(seed, combinedDeck),
            Gameboard.createSolution(seed, size, teamCount, colorDict)
        );
        this.deck.viewSolution(viewSolution);
        this.viewBidirectional(viewBidirectional);
        this.setBorderColor(Gameboard.generateStartingColor(seed, teamCount, colorDict));
        this.displayElement();
    }

    static createSolution(seed, deckSize, teamCount, colorDict) {
        let colorList = [];
        let cardsRemaining = deckSize * deckSize;
        const cardsPerTeam = Math.floor(cardsRemaining / (parseInt(teamCount) + 1));

        colorList.push(colorDict["death"]);
        cardsRemaining--;

        for (let i = 0; i < cardsPerTeam; i++) {
            if (teamCount >= 1) {colorList.push(colorDict["team1"]); cardsRemaining--;}
            if (teamCount >= 2) {colorList.push(colorDict["team2"]); cardsRemaining--;}
            if (teamCount >= 3) {colorList.push(colorDict["team3"]); cardsRemaining--;}
            if (teamCount >= 4) {colorList.push(colorDict["team4"]); cardsRemaining--;}
        }

        for (let i = 0; i < cardsRemaining; i++) {
            colorList.push(colorDict["neutral"]);
        }

        const shuffledColors = shuffle(seed, colorList);
        return shuffledColors;
    }

    static generateStartingColor(seed, teamCount, colorDict) {
        let colorList = [];
        if (teamCount >= 1) {colorList.push(colorDict["team1"]);}
        if (teamCount >= 2) {colorList.push(colorDict["team2"]);}
        if (teamCount >= 3) {colorList.push(colorDict["team3"]);}
        if (teamCount >= 4) {colorList.push(colorDict["team4"]);}
        return shuffle(seed, colorList)[0];
    }

    setBorderColor(color) {
        this.element.style.borderColor = color;
    }

    viewBidirectional(bool) {
        if (bool) {this.element.classList.add("gameboard--bidirectional");}
        else {this.element.classList.remove("gameboard--bidirectional");}
    }

    displayElement() {
        this.element.innerHTML = "";
        this.element.style.gridTemplateColumns = `repeat(${this.deck.size}, 1fr)`;
        this.element.style.gridTemplateRows = `repeat(${this.deck.size}, 1fr)`;
        for (const card of this.deck.cards) {
            this.element.appendChild(card.cardElement.element);
        }
    }
}

class Deck {
    constructor(size, titles, solutions) {
        this.size = size;
        this.titles = titles;
        this.cards = Deck.constructCards(size, titles, solutions);
    }

    static constructCards(size, titles, solutions) {
        const cards = [];
        for (let i = titles.length; i < size * size; i++) {
            titles.push("");
        }
        for (let i = 0; i < size * size; i++) {
            cards.push(new Card(titles[i], solutions[i]));
        }
        return cards;
    }

    viewSolution(bool) {
        if (bool) {
            for (const card of this.cards) {
                card.viewSolution(true);
            }
        }
        else {
            for (const card of this.cards) {
                card.viewSolution(false);
            }
        }
    }
}

