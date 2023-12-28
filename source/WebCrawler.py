import queue
import warnings
from bs4 import BeautifulSoup
from Disaster_Subclasses import *
import re
import requests
from selenium import webdriver
import threading
from queue import Queue

if __name__ == "__main__":
    print("lololololol")


class Website:
    """Class to wrap the information needed to crawl through a web and the methods to scrape it"""
    sel_options = webdriver.ChromeOptions()
    sel_options.add_argument("--headless")
    sel_driver = webdriver.Chrome(options=sel_options)
    sel_driver.implicitly_wait(time_to_wait=3)
    sel_session_lock = threading.Lock()

    def __init__(self, web_name_arg: str, main_page_link_arg: str,
                 news_tag_type_arg: str, news_tag_attr_arg: dict,
                 new_link_tag_type_arg: str, new_link_tag_attr_arg: dict,
                 title_tag_type_arg: str, title_tag_attr_arg: dict,
                 body_tag_type_arg: str, body_tag_attr_arg: dict,
                 next_page_tag_attr_arg: dict = None,
                 news_links_blacklist_arg: [str] = None, news_links_whitelist_arg: [str] = None,
                 base_next_page_link_arg: str = "", base_news_link_arg: str = "",
                 scraping_method_arg: str = "generic",
                 main_needs_selenium_arg: bool = False, news_needs_selenium_arg: bool = False,
                 encoding_arg: str = "UTF-8"):
        # TODO make more default arguments: news_tag_type_arg = "section", title_tag_type = "h1", ect...
        self.web_name = web_name_arg
        self.main_link = main_page_link_arg
        self.news_tag_type = news_tag_type_arg
        self.news_tag_attr = news_tag_attr_arg
        self.new_link_tag_type = new_link_tag_type_arg
        self.new_link_tag_attr = new_link_tag_attr_arg
        self.next_page_tag_attr = next_page_tag_attr_arg
        self.title_tag_type = title_tag_type_arg
        self.title_tag_attr = title_tag_attr_arg
        self.body_tag_type = body_tag_type_arg
        self.body_tag_attr = body_tag_attr_arg
        self.link_whitelist = news_links_whitelist_arg if news_links_whitelist_arg is not None else []
        self.link_blacklist = news_links_blacklist_arg if news_links_blacklist_arg is not None else []
        self.main_needs_sel = main_needs_selenium_arg
        self.news_needs_sel = news_needs_selenium_arg
        self.next_page_base_link = base_next_page_link_arg
        self.news_base_link = base_news_link_arg
        self.scraping_method = scraping_method_arg
        self.encoding = encoding_arg

        self.link_pipeline = Queue()  # Queue of dictionaries in the form of: {Link: "", Status: ""}

    def filter_link(self, link_arg: str, debug_arg: bool = False) -> bool:
        """Filters links. Yeah, that's it"""
        warnings.warn("Warning: I haven´t tested the filter method thoroughly, although think it works just fine")
        in_whitelist = any(map(lambda x: re.match(x, link_arg), self.link_whitelist)) or len(self.link_whitelist) == 0
        # True if present in whitelist (or there are no whitelists)
        not_in_blacklists = not any(map(lambda x: re.match(x, link_arg), self.link_blacklist))
        # False if present in blacklist
        if debug_arg:
            print(f"{link_arg} has {'passed' if in_whitelist and not_in_blacklists else 'failed'}")
        return in_whitelist and not_in_blacklists

    def parse_link(self, scraped_tag_arg, parse_next_page_link_arg: bool = 0, debug_bool=False) -> str:
        """Adds the base address to the relative address."""
        base_link = self.next_page_base_link if parse_next_page_link_arg is True else self.news_base_link
        return base_link + scraped_tag_arg["href"]

    def add_to_links_pipeline(self, links_arg: [str], status_arg="Not_Yet_Executed"):
        """kinda irrelevant, only used in get_links. TO BE REMOVED"""
        [self.link_pipeline.put({"link": x, "status": status_arg}) for x in links_arg]

    def get_soup_from_link(self, link_arg: str, use_selenium_arg: bool = False) -> BeautifulSoup:
        if use_selenium_arg:
            Website.sel_session_lock.acquire()
            Website.sel_driver.get(link_arg)
            raw_html = Website.sel_driver.page_source
            Website.sel_session_lock.release()
        else:
            with requests.get(link_arg) as stream:
                raw_html = stream.content.decode(self.encoding, errors="replace")
        return BeautifulSoup(raw_html, "html.parser")

    def get_hrefs_from_soup(self, soup_arg: BeautifulSoup) -> list[str]:
        main_section = soup_arg.find(name=self.news_tag_type, attrs=self.news_tag_attr)
        relevant_a_tags = map(lambda x: x.find(name="a"),
                              main_section.find_all(name=self.new_link_tag_type, attrs=self.new_link_tag_attr))
        hrefs = [self.parse_link(x) for x in relevant_a_tags if self.filter_link(x["href"])]
        return hrefs if len(hrefs) > 0 else None

    def get_next_page_from_soup(self, soup_arg: BeautifulSoup) -> str:
        next_page_tag = soup_arg.find(name="a", attrs=self.next_page_tag_attr)
        return self.parse_link(next_page_tag, parse_next_page_link_arg=True) if next_page_tag is not None else None

    def get_links(self, overwrite_link_arg=None, max_links=100) -> None:
        """Crawls through the main page and get links of relevant instances"""
        # ideas: just rework the recursive part of the function to take advantage of mutability.
        # TODO: this code may cause the same link to be analyzed twice if the script is run twice in a short time or if
        #  max_links is too high. Implement a "last link" check so that if the collection of links reaches
        #  the first link of the last search, it stops
        if max_links <= 0:
            return

        link = self.main_link if overwrite_link_arg is None else overwrite_link_arg
        soup = self.get_soup_from_link(link, use_selenium_arg=self.main_needs_sel)
        hrefs = self.get_hrefs_from_soup(soup)
        if hrefs is None:
            return
        self.add_to_links_pipeline(hrefs)

        next_page_link = self.get_next_page_from_soup(soup)
        if next_page_link is None:
            return

        # print(f"Length of the page in links: {len(hrefs)}\n next page link: {next_page_link}")
        self.get_links(overwrite_link_arg=next_page_link, max_links=max_links - len(hrefs))

    def dispatch_links(self, extracting_method_arg: str = "generic", n_of_threads: int = 10,
                       status_filter_arg: str = None) -> None:
        """Visits links in the pipeline and initialize the consumer threads.
        -> extracting_method_arg is a string indicating the parsing method"""
        methods = {"generic": lambda x, link: Website.generic_new_scraping(x, link),
                   "gdacs": lambda x, link: Website.gdacs_new_scraping(x, link),
                   "just print": lambda _, link: print(link)}
        parse_method = methods[extracting_method_arg]
        failed_links = Queue()
        threads = [threading.Thread(target=lambda: self.thread_function(parse_method, failed_links, status_filter_arg))
                   for _ in range(n_of_threads)]
        [x.start() for x in threads]
        self.link_pipeline.join()
        self.link_pipeline = failed_links

    def thread_function(self, apply_method_arg, failed_links_queue_arg: Queue, filter_arg: str) -> None:
        """Consumer thread main function. Will continuously consume elements from the pipeline.
        -> apply_method_arg is a website method that parses and sends the info the database
        -> failed_links_queue_arg is a queue object where links will be added in case of exception
        -> filter_arg is a string filtering links to analyze by status. None will match all. Rejected links will be
            sent to failed_links_queue_arg"""
        curr_link_dict = None
        while True:
            try:
                curr_link_dict = self.link_pipeline.get(block=False)
                if filter_arg is not None and curr_link_dict["status"] != filter_arg:
                    failed_links_queue_arg.put(curr_link_dict)
                    continue
                apply_method_arg(self, curr_link_dict["link"])
                self.link_pipeline.task_done()
            except Exception as e:
                if isinstance(e, queue.Empty):
                    return
                elif isinstance(e, ConnectionError):
                    curr_link_dict["status"] = "Connection_Error"
                elif isinstance(e, TypeError) or isinstance(e, AttributeError):
                    curr_link_dict["status"] = "Parsing_Error"
                elif isinstance(e, UnableToDetectDisasterType):
                    curr_link_dict["status"] = "Disaster_Type_Not_Found"
                print(curr_link_dict)
                failed_links_queue_arg.put(curr_link_dict)
                self.link_pipeline.task_done()

    def generic_new_scraping(self, link_to_new_arg: str) -> None:  # return a Disaster instance
        """Generic method to scrape text out of a new consisting of a title and main body"""
        curr_disaster = Disaster(self.dict_from_new_link(link_to_new_arg))
        curr_disaster.classify()
        curr_disaster.extract_json()
        curr_disaster.save_to_database()  # TODO Rn it just prints the data. Add code in each subclass

    def dict_from_new_link(self, link_to_new_arg: str) -> dict:
        soup = self.get_soup_from_link(link_to_new_arg, use_selenium_arg=self.news_needs_sel)
        title = soup.find(self.title_tag_type, attrs=self.title_tag_attr)
        body = soup.find(self.body_tag_type, attrs=self.body_tag_attr).find_all("p")
        parsed_title = re.sub(r'\s+', ' ', title.text)
        parsed_body = re.sub(r'\s+', ' ', "".join([x.text for x in body]))
        return {"link": link_to_new_arg, "title": parsed_title, "body": parsed_body}

    def gdacs_new_scraping(self, link_to_new_arg: str) -> Disaster:
        """call the api i guess"""
        raise NotImplementedError
