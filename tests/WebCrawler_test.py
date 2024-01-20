from bs4 import BeautifulSoup
from source.WebCrawler import WebCrawler


def run_tests():
    test_get_hrefs()
    test_filters()


def test_get_hrefs():
    flood_list = WebCrawler(news_tag_type_arg="main",
                            news_tag_attr_arg={"id": "more-content", "class": "site-main", "role": "main"},
                            new_link_tag_type_arg="h2",
                            new_link_tag_attr_arg={"class": "entry-title", "itemprop": "headline"},
                            news_links_blacklist_arg=["https://floodlist.com/news/.+"]
                            )
    with open("test_samples/floodlist_example.html", errors="ignore") as stream:
        soup = BeautifulSoup(stream.read(), "html.parser")
    result = flood_list._get_hrefs(soup)
    assert len(result) == 16
    assert all([x is not None for x in result])


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
    assert [no_filters._filter_link(x) for x in links] == [True, True, True, True]
    assert [only_whitelists._filter_link(x) for x in links] == [True, False, False, True]
    assert [only_blacklists._filter_link(x) for x in links] == [True, True, False, False]
    assert [both_filters._filter_link(x) for x in links] == [True, False, False, False]


if __name__ == "__main__":
    run_tests()
