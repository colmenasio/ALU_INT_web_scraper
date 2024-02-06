from bs4 import BeautifulSoup

if __name__ == "__main__":
    with open("test_samples/web_example.html", errors="ignore") as stream:
        soup = BeautifulSoup(stream.read(), "html.parser")
    result1 = soup.select("article.page-article")
    print(len(result1))
    result2 = soup.select_one("a.next")
    print(result2["href"])

# this is 10x easier than the original
