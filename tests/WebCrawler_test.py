from bs4 import BeautifulSoup
from source.WebCrawler import WebCrawler


def run_tests():
    test_get_hrefs()


def test_get_hrefs():
    example_web = WebCrawler(news_wapper_selector_arg="main.site-main",
                             new_link_selector_arg="article.page-article > h2 > a",
                             news_links_blacklist_arg=["https://floodlist.com/news/.+"]
                             )
    with open("test_samples/web_example.html", errors="ignore") as stream:
        soup = BeautifulSoup(stream.read(), "html.parser")
    result = example_web._get_hrefs(soup)
    assert len(result) == 16
    assert all([x is not None for x in result])


def test_get_next_page_link():
    example_web1 = WebCrawler(next_page_link_selector_arg="a.next")
    with open("test_samples/web_example.html", errors="ignore") as stream:
        soup = BeautifulSoup(stream.read(), "html.parser")
        result = example_web1._get_next_page_link(soup)
    assert result == "https://next_page"
    example_web2 = "<html></html>"


def test_build_unparsed_disaster():
    example_web = WebCrawler(title_selector_arg="h1.entry-title", body_selector_arg="div.entry-content > p")
    with open("test_samples/new_example.html", errors="ignore") as stream:
        soup = BeautifulSoup(stream.read(), "html.parser")
    result = example_web._build_unparsed_disaster(soup, "xdddd")
    print(result)


def test_filters():
    no_filters = WebCrawler()
    only_whitelists = WebCrawler(
        news_links_whitelist_arg=[".+accept_this.*"]
    )
    only_blacklists = WebCrawler(
        news_links_blacklist_arg=[".*SIKE.*"]
    )
    both_filters = WebCrawler(
        news_links_whitelist_arg=[".*accept_this.*"],
        news_links_blacklist_arg=[".*SIKE.*"]
    )
    links = ["wfnodaoaccept_thisaefnsepoid", "efnfsofnsofnpa", "sofnisfonSIKEdobad", "dspenfeoinfaccept_thisdaoiSIKE"]
    assert [no_filters._matches_filters(x) for x in links] == [True, True, True, True]
    assert [only_whitelists._matches_filters(x) for x in links] == [True, False, False, True]
    assert [only_blacklists._matches_filters(x) for x in links] == [True, True, False, False]
    assert [both_filters._matches_filters(x) for x in links] == [True, False, False, False]


if __name__ == "__main__":
    run_tests()
