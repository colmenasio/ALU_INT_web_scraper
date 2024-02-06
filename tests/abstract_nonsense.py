from bs4 import BeautifulSoup
# IGNORE THIS, THIS IS JUST FOR TEMPORAL TEST (i should add this to the gitignore)


def abstract_nonsense_1():
    with open("test_samples/web_example.html", errors="ignore") as stream:
        soup = BeautifulSoup(stream.read(), "html.parser")
    result1 = soup.select("article.page-article > h2 > a")
    print(len(result1))
    result2 = soup.select_one("a.next")
    print(result2["href"])
    result3 = soup.select_one("main.site-main")
    result4 = result3.select("article.page-article > h2 > a")
    [print(x["href"]) for x in result4]


def abstract_nonsense_2():
    with open("test_samples/new_example.html", errors="ignore") as stream:
        soup = BeautifulSoup(stream.read(), "html.parser")
    result1 = soup.select_one("h1.entry-title")
    print(result1)
    result2 = soup.select("div.entry-content > p")
    [print(x.text) for x in result2]


if __name__ == "__main__":
    # abstract_nonsense_1()
    abstract_nonsense_2()
