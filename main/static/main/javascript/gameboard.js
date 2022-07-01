revealedSolution = false;

//When the DOM tree is loaded
document.addEventListener('DOMContentLoaded', function() {
    //The button that says 'View solution/gameboard'
    solutionButton = document.querySelector("#solution-button");

    //A list of all cards on the gameboard
    codenameCards = document.querySelectorAll(".codename-card");

    //Makes the solution button toggle whether or not you are viewing the solution or not
    solutionButton.onclick = toggleSolution;

    //Set the default onclick function for every card to reveal the card
    codenameCards.forEach(function(card) {
        card.onclick = function() { revealCard(card); }
    })

    //Get the url parameters for deck and seed
    const querystring = window.location.search;
    const urlParams = new URLSearchParams(querystring);
    let decks = urlParams.getAll('deck');
    let seed = urlParams.get('seed');

    setCardTexts(decks, seed)

})

//Replaces all the card text boxes with new card titles generated from the given decks and seed parameters
function setCardTexts(decks, seed) {
    //Create a url parameter string with each deck form the current url parameters
    deckParamString = ""
    decks.forEach(deck => {
        deckParamString += `deck=${deck}&`
    })

    //Initializes the card number counter (which will be used to select the next card in the sequence) to 0
    let cardNumCounter = 0;

    //Replace all card text boxes with a new set of card titles using the selected parameters
    fetch(`/codenames/getcardtitles/?${deckParamString}seed=${seed}&limit=25`)
    .then(response => response.json())
    .then(jsonCards => {
        //After the selected cards titles have loaded, set the innerHTML of the card's text boxes to contain the card titles
        document.querySelectorAll('.codename-card').forEach(codenameCard => {
            codenameCard.querySelectorAll('.card-text').forEach(cardText => {
                console.log("Written");
                cardText.innerHTML = jsonCards.cards[cardNumCounter];
            })
            cardNumCounter++;
        })
        console.log(jsonCards)
    })
}

//Covers the inputed in a screen colored based on the cards datatype
function revealCard(e) {
    cardScreen = e.querySelector(".card-screen");
    cardScreen.style.backgroundColor = e.dataset.color;
    cardScreen.style.opacity = 0.7;
    cardScreen.style.display = "block";
}

//Removes the colored screen from the inputed card
function unrevealCard(e) {
    cardScreen = e.querySelector(".card-screen");
    cardScreen.removeAttribute('style');
}

//Displays a cross on the inputed card
function crossCard(e) {
    cardCross = e.querySelector(".card-cross");
    cardCross.style.display = "block";
}

//Removes the cross on the inputed card
function uncrossCard(e) {
    cardCross = e.querySelector(".card-cross");
    cardCross.removeAttribute('style');
}

//Toggles whether viewing the solution board or playable board
function toggleSolution() {
    //When viewing playable gameboard
        //Solution button's text reads 'View Solution'
        //Clicking a card reveals the card
        //Crosses are not placed

    //When viewing solution gameboard
        //Solution button's text reads 'View Gameboard'
        //Clicking a card places a cross
        //All cards are already revealed

    //When the view gameboard button is clicked
    if (revealedSolution) {
        revealedSolution = false;
        solutionButton.innerHTML = "View Solution";
        codenameCards.forEach(function(card) {
            card.onclick = function() { revealCard(card); }
            unrevealCard(card);
            uncrossCard(card);
        })

    }
    //When the view solution button is clicked
    else {
        revealedSolution = true;
        solutionButton.innerHTML = "View Gameboard";
        codenameCards.forEach(function(card) {
            card.onclick = function() { crossCard(card); }
            revealCard(card);
        })
    }
}