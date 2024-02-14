from source.Disaster import Categories
# IGNORE THIS, THIS IS JUST FOR TEMPORAL TEST (i should add this to the gitignore)


def abstract_nonsense_1():
    a = Categories.build_from_json()
    print(a._questions)


if __name__ == "__main__":
    abstract_nonsense_1()
    print("done")
