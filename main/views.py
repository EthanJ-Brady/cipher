from ast import Return
from email.policy import HTTP
from http.client import HTTPResponse
from select import select
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from main.models import CodenameCard, Deck
import random

#Retrives entries from the CodenameCard model
all_codename_cards = CodenameCard.objects.all()

#Creates a set of unique card decks available into available_decks
available_decks = set()
for card in all_codename_cards:
    available_decks.add(card.deck)

def generate_card_colors(red=0, blue=0, gray=0, black=0):

    #Creates a list of card colors
    colors = []
    for i in range(red):
        colors.append("red")
    for i in range(blue):
        colors.append("blue")
    for i in range(gray):
        colors.append("gray")
    for i in range(black):
        colors.append("black")

    random.shuffle(colors)
    return colors

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

    #If seed or selected_deck is empty then return to index for selection
    if seed is None:
        return index(request)

    #Set the random module's seed to the generated seed
    random.seed(seed)
    
    #Determine first player and determines card amounts
    if random.randint(0, 1):
        first_player = "red"
        colors = generate_card_colors(red=9, blue=8, gray=7, black=1)
    else:
        first_player = "blue"
        colors = generate_card_colors(red=8, blue=9, gray=7, black=1)

    context = {
        "seed" : seed,
        "colors" : colors,
        "first_player" : first_player
    }
    return render(request, 'main/gameboard.html', context)

#JsonResponse page for card_titles
def get_card_titles(request):
    seed = request.GET.get("seed")
    selected_decks = request.GET.getlist("deck")
    limit = request.GET.get("limit")

    if seed is None:
        random.seed(random.randint(0,999999999))
    else:
        random.seed(seed)

    if selected_decks == []:
        return JsonResponse({"cards:": []})

    selected_card_titles = []
    available_card_titles = CodenameCard.objects.all()
    for card in available_card_titles:
        if str(card.deck.id) in selected_decks:
            selected_card_titles.append(card.card_title)

    if limit is None:
        random.shuffle(selected_card_titles)
        return JsonResponse({"cards": selected_card_titles})
    elif len(selected_card_titles) < int(limit):
        random.shuffle(selected_card_titles)
        return JsonResponse({"cards": selected_card_titles})
    else:
        selected_card_titles = random.sample(selected_card_titles, int(limit))
        return JsonResponse({"cards": selected_card_titles})
    