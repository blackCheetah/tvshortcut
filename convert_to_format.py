import json
import os

def create_a_json_file(location, file_name, json_data):
    try:
        with open(os.path.join(location + "/", file_name), "w", encoding='utf-8', errors='ignore') as output_file:
            output_file.write(json_data)
             #json.dump(json_data, output_file, indent=4, sort_keys=True,  ensure_ascii=False)

    except FileNotFoundError as fNot:
    #except IOError as e:
        print("Jezuz christ!!! File not found!! \n{0}".format(fNot))

tv_shows = {
    "Arrow":
    "arrow",

    "Agents of S.H.I.E.L.D.":
    "agents-of-shield",

    "Better Call Saul":
    "better-call-saul",

    "Daredevil":
    "daredevil",

    "Fear the Walking Dead":
    "fear-the-walking-dead",

    "Game of Thrones":
    "game-of-thrones",

    "Gotham":
    "gotham",

    "Iron Fist":
    "iron-fist",

    "Jessica Jones":
    "jessica-jones",

    "Legends of Tomorrow":
    "legends-of-tomorrow",

    "Luke Cage":
    "luke-cage",

    "Marco Polo":
    "marco-polo",

    "Mr. Robot":
    "mr-robot",

    "Supergirl":
    "supergirl",

    "Vikings":
    "vikings",

    "The Flash":
    "the-flash",

    "The Walking Dead":
    "walking-dead",

    "Prison break":
    "prison-break",

    "American Gods":
    "american-gods",

    "Narcos":
    "narcos",

    "House of Cards":
    "house-of-cards",

    "Peaky Blinders":
    "peaky-blinders",

    "West World":
    "westworld",

    "Homeland":
    "homeland",

    "The 100":
    "the-hundred",

    "SouthPark":
    "south-park",

    "Defenders":
    "defenders"
}

new_tv_shows = {'tvShows' : []}
default = {"name": "", "shortcut": "", "new" : ""}

for iterator in range(0, len(tv_shows.items())):
    new_tv_shows.get('tvShows').append(default)

json_string = json.dumps(new_tv_shows)
jdict = json.loads(json_string)
    
iterator = 0
for key, value in tv_shows.items():
    jdict["tvShows"][iterator]["name"] = key
    jdict["tvShows"][iterator]["shortcut"] = value
    jdict["tvShows"][iterator]["new"] = ""
    iterator += 1

new_json_string = json.dumps(jdict, indent=4, sort_keys=True,  ensure_ascii=False)
#print(new_json_string)

create_a_json_file("data", "/tvshows.json", new_json_string)

"""
# Structure
{
    "tvShows": [
        {
            "name": "Arrow",
            "shorctut": "arrow",
            "new": ""
        },
        {
            "name": "something",
            "shorctut": "something",
            "new": ""
        }
    ]
    
}
"""
