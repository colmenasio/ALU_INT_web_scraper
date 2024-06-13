# IGNORE THIS, THIS IS JUST FOR TEMPORAL TEST (i should add this to the gitignore)
import json

def abstract_nonsense_1():
    with open("../configs/categories/categories.json") as fstream:
        disaster_types = json.load(fstream)
    for key in list(disaster_types.keys()):
        for shit in disaster_types[key]:
         print(shit)


if __name__ == "__main__":
    abstract_nonsense_1()
    print("done")
