import openai

with open("gpt_key.txt") as stream:
    keys = list(map(lambda x: x.rstrip("\n", ), stream.readlines()))
    chat = openai.OpenAI(api_key=keys[0], organization=keys[1]).chat.completions


def test_1():
    messages = [{"role": "system",
                 "content": "You are a scraping tool. The following messages will containt text from news parsed as a "
                            "python dictionary, as well as a list of parameters. Parse the new, obtaining the "
                            "data corresponding to each parameter, and return the answers in json format."},
                {"role": "user",
                 "content": "New: {'link': 'https://floodlist.com/america/usa/storm-floods-north-east-december-2023', 'title': 'USA – Fatalities and Evacuations After Powerful Storm Triggers Flooding in Eastern States', 'body': 'A powerful storm hit the East Coast of the United States over the last few days, causing widespread devastation and damages as it moved north and into Atlantic Canada on 19 December 2023.Heavy rain from the storm caused rivers to break their banks in multiple states from South Carolina to Maine, flooding roads, damaging homes and prompting rescues and evacuations. River levels remain high in many areas.The severe weather caused several fatalities, including 3 people who died in separate incidents in flood waters in South Carolina, New York and Pennsylvania. As of 19 December, 2 people were reported missing in floods in Maine.Strong winds also caused major damages, including at least 2 fatalities in Massachusetts and Maine. At one point more than 800,000 were left without power across the region.Heavy rain combined with high tides and storm surge flooded areas along the South Carolina from Charleston to Myrtle Beach on 16 to 17 December 2023. A daily record high of 3.89 inches (98.81 mm) of rain was recorded in Downtown Charleston.Streets of Charleston were under 2 feet (60 cm) of water in some areas following the rain and a historic high tide of 9.86 feet on 17 December 2023. Charleston Fire Department rescued at least 40 people from flood waters. Emergency crews were also called on to rescue dozens of motorists stranded by flooding in Georgetown. One person died when a vehicle was trapped in flood waters Mount Pleasant.Heavy rain from the storm caused severe problems in parts of New York state. One person died in flood waters in New York State after a vehicle was swept into the Catskill Creek near Leeds, authorities reported.Elsewhere in the state, flooding prompted evacuations in New Windsor and Highland Falls. Areas of Congers, Clarkstown and Orangetown areas are flooded, Rockland County officials said. The NWS reported 4.85 inches (123.19 mm) of rain in 24 hours to 18 December in Spring Valley, Rockland County.Washed out roads left communities in the Adirondacks mountain range isolated, including Keene town in central Essex County. The Ausable River at Au Sable Forks, around 14 miles (23 km) north of Keene exceeded Major Flood Stage on 18 December.Storm surge caused flooding along the New Jersey coastline, in particular in Bay Head and Mantoloking.Meanwhile, heavy rain triggered flash flooding and caused river to break their banks in multiple locations of the state. The swollen Passaic and Pompton rivers prompted evacuations in Lincoln Park where 5.18 inches (131.57 mm) of rain fell in 24 hours to 18 December.Flooding from the Passaic also prompted evacuations in Little Falls and caused severe damage in the nearby city of Paterson, where officials declared a state of emergency on 18 December.The Passaic River at Little Falls exceeded Major Flood stage on 19 December and has continued to rise since then.The flooding Rockway River damaged homes in Dover and Denville, while the Pompton River flooded areas of Pequannock. Flooding was also reported in Highland Park where the Raritan River broke its banks.Local media reported the swollen Perkiomen Creek flooded areas of Montgomery County including Lower Providence Township. Further west, one person died after in hospital after being rescued from floods near Ephrata in Lancaster County.Dozens of homes were evacuated in the village of Moretown, Vermont, after the nearby Mad River flooded.Residents of the state capital Montpelier feared a repeat of the catastrophic flooding of July 2023 after levels of the Winooski River started to rise. Fortunately the river crested at Moderate Flood stage on 18 December.Around 17 people had to be rescued from flooding in Conway, New Hampshire, after the Saco River broke it banks. Flood was so severe local fire crews were unable to reach all the victim and 4 people had to be rescued by New Hampshire Army National Guard Black Hawk helicopter.Levels of the Saco River jumped more than 13 feet in the space of a few hours on 18 December.In Maine, the the Kennebec River has continued to rise since heavy rain from 17 December. As of 18 December, officials called for residents near the river in Fairfield to evacuate their home. Flooding has also affected the city of Augusta where some roads were closed.The Kennebec River at North Sidney, south of Fairfield, was above Major Flood stage as of 19 December 2023.Further south, the flooding Androscoggin River prompted evacuations in the city of Lewiston and neighbouring Auburn.In western Maine, the flooding Swift River, a tributary of the Androscoggin, swept away a vehicle trying to cross a bridge from Mexico to Rumford on 18 December 2023. Two people were rescued and were treated for hypothermia but 2 other occupants of the vehicle were not found at the time and have been reported missing.MaineMassachusettsNew HampshireNew JerseyNew YorkPennsylvaniaSouth CarolinaVermont'}"
                            "Parameters: ['Number of lethal victims', 'Date of the event', 'Country the event took place in']"}
                ]
    response_0 = chat.create(
        model="gpt-3.5-turbo",
        messages=[messages[0]]
    )
    # print(response_0.choices[0].message.content)
    response = chat.create(
        model="gpt-3.5-turbo",
        messages=[messages[1]]
    )
    print(response.choices[0].message.content)


def consumer_test():
    while True:
        print("ready for next!")
        new_text = (yield)
        print(type(new_text))
        print(new_text)


consum = consumer_test()
print("haciendo el next")
next(consum)
print("SENDING 1")
consum.send("1: lolololo")
print("SENDING 2")
consum.send(2)
