from turtle import title
from django.shortcuts import redirect, render
from django.http import HttpResponse
import random

complete_content_list = [
    "Obi-Wan Kenobi",
    "Qui-Gon Jinn",
    "Padme",
    "Anakin",
    "Yoda",
    "Mace Windu",
    "Ki-Adi Mundi",
    "Kit Fisto",
    "Plo Koon",
    "Aayla Secura",
    "Shaak Ti",
    "Darth Maul",
    "Emporer Palpatine",
    "R2-D2",
    "C-3PO",
    "Watto",
    "Shmi Skywalker",
    "Nute Gunray",
    "Batlle Droid",
    "Super Battle Droid",
    "Droideka",
    "Jar Jar Binks",
    "Boss Nass",
    "Zam Wessel",
    "Jango Fett",
    "Dexter Jester",
    "Count Dooku",
    "Poggle the Lesser",
    "Clone Trooper",
    "Commander Cody",
    "Captain Rex",
    "The Younglings",
    "Darth Vader",
    "Tusken Raiders",
    "General Grievous",
    "Luke Skywalker",
    "Leia Organa",
    "Han Solo",
    "Chewbacca",
    "Greedo",
    "Boba Fett",
    "Stormtrooper",
    "Death Trooper",
    "Grand Moff Tarkin",
    "Jabba the Hutt",
    "Aunt Beru",
    "Uncle Owen",
    "Jawa",
    "Lando Calrissian",
    "Wampa",
    "Bantha",
    "Womp Rat",
    "Admiral Akbar",
    "Rey",
    "Finn",
    "Poe",
    "Kylo Ren",
    "BB-8",
    "Snoke",
    "Rose Tico",
    "General Hux",
    "D-O",
    "Maz Kanata",
    "Babu Frik",
    "Admiral Holdo",
    "Ahsoka",
    "Fives",
    "Savage Oppress",
    "Asajj Ventress",
    "Gregor",
    "Wolfe",
    "Mother Talzin",
    "Nightbrothers",
    "Nightsisters",
    "Cad Bane",
    "Fennec Shand",
    "Echo",
    "Hunter",
    "Wrecker",
    "Tech",
    "Crosshair",
    "Omega",
    "Cal Kestis",
    "BD-1",
    "Cere",
    "Trilla",
    "Merrin",
    "Greeze",
    "Reva",
    "Kanan Jarrus",
    "Ezra Bridger",
    "Hera Syndulla",
    "Chopper",
    "Sabine",
    "Zeb",
    "Grand Admiral Thrawn",
    "The Mandalorian",
    "Grogu",
    "Kuill",
    "Cara Dune",
    "Greef Carga",
    "Moff Gideon",
    "Bo Katan",
    "Pre Vizla",
    "The Armorer",
    "Gonk Droid",
    "Darth Jar Jar",
    "Tatooine",
    "Naboo",
    "Coruscant",
    "Geonosis",
    "Mustafar",
    "Utapau",
    "Kamino",
    "Alderaan",
    "Hoth",
    "Bespin (Cloud City)",
    "Endor",
    "Jakku",
    "Exegol",
    "Mortis",
    "Illum",
    "Lothal",
    "Lightsaber",
    "Blaster",
    "The Force",
    "The Dark Side",
    "Beskar",
    "Wrist Rocket",
    "Flamethrower",
    "The Dark Saber",
    "Kaiber Crystal",
    "Slingshot",
    "Rocket",
    "Jetpack",
    "Ray Shield",
    "Sand",
    "The High Ground",
    "Millenium Falcon",
    "Death Star",
    "The Ghost",
    "Starkiller Base",
]

#Class which contains a title of card and a type of card which includes a red, blue, nuetral, or death card
class Card:
    def __init__(self, title, type):
        self.title = title
        if type in ["red", "blue", "nuetral", "death"]:
            self.type = type
    
    def __str__(self):
        return f"{self.title}, {self.type}"

#Returns a list of cards with titles in list_of_content with types defined by the parameters
def generate_cards(list_of_content, num_red = 8, num_blue = 8, num_nuetral = 8, num_death = 1):
    
    #Creates a list of card types containing the parameter values
    type_list = []
    for i in range(num_red):
        type_list.append("red")
    for i in range(num_blue):
        type_list.append("blue")
    for i in range(num_nuetral):
        type_list.append("nuetral")
    for i in range(num_death):
        type_list.append("death")

    #Shuffles the list of card types
    random.shuffle(type_list)

    #Creates Cards with tiles from list_of_content and types from type_list
    card_list = []
    for i in range(len(list_of_content)):
        card_list.append(Card(list_of_content[i], type_list[i]))

    #Returns list of cards
    return card_list

def select_random():
    pass

#Index Route
def index(request):
    #If there is no seed specified in the URL then generate a random one each time the page loads
    seed = request.GET.get("seed")
    if seed is None:
        seed = random.randint(0, 999999999)

    context = {
        "seed" : seed,
    }
    return render(request, 'main/index.html', context)

#Gameplay page for Codenames
def gameboard(request):
    #If there is no seed, then return the index.html page to generate one
    seed = request.GET.get("seed")
    if seed is None:
        return index(request)

    #Set the random module's seed to the generated seed
    random.seed(seed)

    #If solution is true in the URL params then set mark all cards as clicked and viewing_solution to true. 
    #Otherwise, mark cards as unclicked and viewing_solution to false
    if request.GET.get("solution") == "true":
        click_option = "clicked-card"
        viewing_solution = "true"
    else:
        click_option = "unclicked-card"
        viewing_solution = "false"

    #Select 25 random cards from the list of available card choices
    this_content_list = random.sample(complete_content_list, 25)

    #Generate cards from this games card content titles
    card_list = generate_cards(this_content_list)

    #Shuffle the cards
    random.shuffle(card_list)

    context = {
        "seed" : seed,
        "card_list" : card_list,
        "click_option" : click_option,
        "viewing_solution" : viewing_solution
    }
    return render(request, 'main/codenames.html', context)