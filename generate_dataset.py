import pandas as pd
import random


destinations = {
    "Agra":       {"Type":"Historical","Season":"Winter","Activities":["TajMahal","Culture"],"Region":"India"},
    "Andaman":    {"Type":"Beach","Season":"Winter","Activities":["Scuba","Beach"],"Region":"India"},
    "Bali":       {"Type":"Beach","Season":"Summer","Activities":["Beach","Culture"],"Region":"Other"},
    "Delhi":      {"Type":"City","Season":"Winter","Activities":["Sightseeing","Culture"],"Region":"India"},
    "Dubai":      {"Type":"City","Season":"Winter","Activities":["Shopping","Adventure"],"Region":"Other"},
    "Goa":        {"Type":"Beach","Season":"Summer","Activities":["Beach","Party","Relaxation"],"Region":"India"},
    "Hampi":      {"Type":"Historical","Season":"Winter","Activities":["Sightseeing","Photography"],"Region":"India"},
    "Interlaken": {"Type":"Mountain","Season":"Summer","Activities":["Adventure","Paragliding"],"Region":"Other"},
    "Jaipur":     {"Type":"Historical","Season":"Winter","Activities":["Fort","Culture"],"Region":"India"},
    "Kerala":     {"Type":"Hill/Beach","Season":"Monsoon","Activities":["Houseboat","Relaxation"],"Region":"India"},
    "Leh":        {"Type":"Mountain","Season":"Summer","Activities":["Trekking","Adventure"],"Region":"India"},
    "London":     {"Type":"City","Season":"Winter","Activities":["Culture","Sightseeing"],"Region":"Other"},
    "Manali":     {"Type":"Mountain","Season":"Winter","Activities":["Trekking","Adventure"],"Region":"India"},
    "Ooty":       {"Type":"Hill/Beach","Season":"Winter","Activities":["Relaxation","Trekking"],"Region":"India"},
    "Paris":      {"Type":"City","Season":"Summer","Activities":["Sightseeing","Culture"],"Region":"Other"},
    "Phuket":     {"Type":"Beach","Season":"Winter","Activities":["Beach","IslandHopping"],"Region":"Other"},
    "Queenstown": {"Type":"Adventure","Season":"Summer","Activities":["Bungee","Adventure"],"Region":"Other"},
    "Rishikesh":  {"Type":"Adventure","Season":"Summer","Activities":["Rafting","Yoga"],"Region":"India"},
    "Shimla":     {"Type":"Hill/Beach","Season":"Winter","Activities":["Snow","Relaxation"],"Region":"India"},
    "Zermatt":    {"Type":"Mountain","Season":"Winter","Activities":["Skiing","Mountain"],"Region":"Other"},
    "Zurish":     {"Type":"City","Season":"Summer","Activities":["Culture","Shopping"],"Region":"Other"},
    "Munnar":     {"Type":"Hill/Beach","Season":"Winter","Activities":["TeaPlantations","Relaxation"],"Region":"India"}
}


travel_groups = ["Family","Friends","Solo","Couple"]
durations = ["Short","Long"]
health_conditions = ["None","Heart Issues","Asthma"]


rows = []


for _ in range(1000):
    place = random.choice(list(destinations.keys()))
    info = destinations[place]


    rows.append([
        place,
        info["Type"],
        info["Season"],
        random.choice(travel_groups),
        ",".join(info["Activities"]),
        random.randint(3000,25000),
        random.choice(durations),
        random.choice(health_conditions),
        random.randint(1,6),
        info["Region"]
    ])


df = pd.DataFrame(rows, columns=[
    "Destination","Type","Season","TravelGroup","Activities",
    "BudgetPerPerson","Duration","HealthCondition","NumPeople","Region"
])


df.to_csv("travel_dataset1.csv",index=False)
print("Dataset Generated:",len(df))
