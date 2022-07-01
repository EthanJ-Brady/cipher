from ast import Return
from email.policy import HTTP
from select import select
from django.shortcuts import redirect, render
from django.http import HttpResponse
from main.models import CodenameCard, Deck
import random

#The number of cards on the gameboard is 25
numCards = 25

#Retrives entries from the CodenameCard model
all_codename_cards = CodenameCard.objects.all()

#Creates a set of unique card decks available into available_decks
available_decks = set()
for card in all_codename_cards:
    available_decks.add(card.deck)

#Class which contains a title of card and a type of card which includes a red, blue, nuetral, or death card
class ColoredCard:
    def __init__(self, title, type):
        self.title = title
        if type in ["red", "blue", "gray", "black"]:
            self.type = type
    
    def __str__(self):
        return f"{self.title}, {self.type}"

    #Returns a list of cards with titles in list_of_content with types defined by the parameters
    @staticmethod
    def generate_colored_cards(card_titles, red_cnt, blue_cnt, nuetral_cnt, death_cnt):
        
        #Creates a list of card colors
        colors = []
        for i in range(red_cnt):
            colors.append("red")
        for i in range(blue_cnt):
            colors.append("blue")
        for i in range(nuetral_cnt):
            colors.append("gray")
        for i in range(death_cnt):
            colors.append("black")

        #Shuffles the list of card colors
        random.shuffle(colors)

        #Creates Cards with tiles from list_of_content and types from type_list
        cards = []
        for i in range(len(card_titles)):
            cards.append(ColoredCard(str(card_titles[i]), colors[i]))

        #Returns list of cards
        return cards


#Index Route
def index(request):
    #If there is no seed specified in the URL then generate a random one each time the page loads
    seed = request.GET.get("seed")
    if seed is None:
        seed = random.randint(0, 999999999)

    context = {
        "seed" : seed,
        "available_decks": available_decks
    }
    return render(request, 'main/index.html', context)


#Gameplay page for Codenames
def gameboard(request):
    seed = request.GET.get("seed")
    selected_deck = request.GET.getlist("deck")

    #If seed or selected_deck is empty then return to index for selection
    if seed is None:
        return index(request)

    if selected_deck == []:
        return index(request)

    #Set the random module's seed to the generated seed
    random.seed(seed)
    
    #Determine first player and determines card amounts
    if random.randint(0, 1):
        first_player = "red"
        red_cnt = 9
        blue_cnt = 8
    else:
        first_player = "blue"
        red_cnt = 8
        blue_cnt = 9

    #Filter all available cards down to the cards from the selected deck
    available_card_titles = CodenameCard.objects.all()
    card_titles = []
    for card in available_card_titles:
        if str(card.deck.id) in selected_deck:
            card_titles.append(card.card_title)

    #Select 25 random cards from the selected decks
    card_titles = random.sample(card_titles, 25)

    #Create shuffled colored cards from the 25 selected cards
    cards = ColoredCard.generate_colored_cards(card_titles, red_cnt=red_cnt, blue_cnt=blue_cnt, nuetral_cnt=7, death_cnt=1)
    random.shuffle(cards)

    context = {
        "seed" : seed,
        "cards" : cards,
        "selected_deck" : selected_deck,
        "first_player" : first_player
    }
    return render(request, 'main/gameboard.html', context)