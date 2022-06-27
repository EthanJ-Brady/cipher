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
        if type in ["red", "blue", "nuetral", "death"]:
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
            colors.append("nuetral")
        for i in range(death_cnt):
            colors.append("death")

        #Shuffles the list of card colors
        random.shuffle(colors)

        #Creates Cards with tiles from list_of_content and types from type_list
        cards = []
        for i in range(len(card_titles)):
            cards.append(ColoredCard(card_titles[i], colors[i]))

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
    selected_deck = request.GET.get("deck")

    #If seed or selected_deck is empty then return to index for selection
    if seed is None or selected_deck is None:
        return index(request)

    #Set the random module's seed to the generated seed
    random.seed(seed)

    #If solution is true in the URL params then set mark all cards as clicked and viewing_solution to true. 
    #Otherwise, mark cards as unclicked and viewing_solution to false
    if request.GET.get("solution") == "true":
        click_option = "clicked-card"
        viewing_solution = True
    else:
        click_option = "unclicked-card"
        viewing_solution = False
    

    #Determine first player and determines card amounts
    if random.randint(0, 1):
        first_player = "red"
        red_cnt = 9
        blue_cnt = 8
    else:
        first_player = "blue"
        red_cnt = 8
        blue_cnt = 9

    #Generate 25 randomly shuffled colored cards from the selected card titles
    card_titles = random.sample(list(CodenameCard.objects.all().filter(deck=selected_deck)), 25)
    cards = ColoredCard.generate_colored_cards(card_titles, red_cnt=red_cnt, blue_cnt=blue_cnt, nuetral_cnt=7, death_cnt=1)
    random.shuffle(cards)

    context = {
        "seed" : seed,
        "cards" : cards,
        "selected_deck" : selected_deck,
        "click_option" : click_option,
        "viewing_solution" : viewing_solution,
        "first_player" : first_player
    }
    return render(request, 'main/gameboard.html', context)