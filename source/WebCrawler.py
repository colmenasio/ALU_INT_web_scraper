from __future__ import annotations
from bs4 import BeautifulSoup
from os import listdir
from selenium import webdriver
from queue import Queue, Empty

import json
import re
import requests
import threading
import warnings

from source.CustomExceptions import InvalidCategoryErr
from source.Disaster import Disaster

if __name__ == "__main__":
    print("lololololol wrong file. dont delete this its useful for testing xd")


class WebCrawler:
    """API interface.
    Meant to be instanced once per website.
    Wraps the methods for crawling a website and processing news in a convenient way
    Can be initialized with either arguments or a dictionary of arguments"""
    sel_options = webdriver.ChromeOptions()
    sel_options.add_argument("--headless")
    sel_driver = webdriver.Chrome(options=sel_options)
    sel_driver.implicitly_wait(time_to_wait=3)
    sel_session_lock = threading.Lock()

    DEFINITIONS_PATH = "../configs/website_definitions/definitions"
    SHOW_EXCEPTIONS = False

    def __init__(self,
                 web_name: str = None,
                 main_page_link: str = None,

                 news_wapper_selector: str = None,
                 new_link_selector: str = None,
                 next_page_link_selector: str = None,
                 title_selector: str = None,
                 body_selector: str = None,

                 news_links_blacklist: [str] = None,
                 news_links_whitelist: [str] = None,

                 next_page_root_link: str = "",
                 news_root_link: str = "",
                 main_needs_selenium: bool = False,
                 news_needs_selenium: bool = False,

                 encoding: str = "UTF-8",
                 language: str = "en",

                 **kwargs
                 ):
        """
        :param web_name: Website name. Purely aesthetic. Currently useless
        :param main_page_link: Link to the first page to extract links from
        :param news_wapper_selector: Selector to the tag that wraps relevant news articles
        :param new_link_selector: Selector to the 'a' tag containing the link to a new
            (relative to the news_wrapper_selector)
        :param next_page_link_selector: Selector to the 'a' tag containing the href of the next page to crawl
        :param title_selector: Selector to the title of the new
        :param body_selector: Seletor to the different paragrafs of text in the new
        :param news_links_blacklist: re Regex that news links must match to be processed.
            If None, matches all links. Defaults to None
        :param news_links_whitelist: re Regex that news links must not match to be processed.
            Defaults to None
        :param next_page_root_link: Prefix to be added to the relative address of the next page link
        :param news_root_link: Prefix to be added to the relative addresses of the individual news links
        :param main_needs_selenium: Bool indicating if selenium is needed in the main pages
            (if server response is required)
        :param news_needs_selenium: Bool indicating if selenium is needed in the main pages
            (if server response is required)
        :param language: Language of the website. Uses ISO 639-1 Code. Defaults to en (english).
        :param encoding: Defaults to UTF-8.
        """
        # TODO: some crawling/scraping methods will require different fields than others. Write
        #   functions that ensure the method called can be run with the current parameters Man i wish you could
        #   do like rust and just write each field once
        #  TODO Also this is a mess
        self._web_name = web_name
        self._main_page_link = main_page_link

        self._news_wapper_selector = news_wapper_selector
        self._new_link_selector = new_link_selector
        self._next_page_link_selector = next_page_link_selector
        self._title_selector = title_selector
        self._body_selector = body_selector

        self._link_whitelist = news_links_whitelist
        self._link_blacklist = news_links_blacklist
        self._main_needs_sel = main_needs_selenium
        self._news_needs_sel = news_needs_selenium
        self._next_page_root_link = next_page_root_link
        self._news_root_link = news_root_link

        self._encoding = encoding
        self._language = language

        self._link_pipeline = Queue()  # Queue of dictionaries in the form of: {Link: "", Status: ""}

    @staticmethod
    def build_from_dict(arguments: dict) -> WebCrawler:
        """Factory method initializing a crawler from a dictionary"""
        warnings.warn(
            "The method (build_from_dict) isnt fully implemented and, even tho it does instanciate "
            "as it should, it does not check if the parameters given are correct or not\n"
            "(check source for more info)")
        # TODO: IMPORTANT!!
        #   Since the kwargs just overwrite the default values, and "not-expected" values just arent used, its kinda
        #   difficult to know wether the instance was initialized correctly or not
        #   (eg: one could supply webname instead of web_name,
        #   then self.web_name would be None and there would be no easy way of checking)
        return WebCrawler(**arguments)

    @staticmethod
    def build_from_json(file_name_arg: str) -> WebCrawler:
        """Factory method initializing a crawler from a single file in the 'definitions' folder
        :param file_name_arg: eg: 'web1.json'
        """
        # TODO add error handling
        path = WebCrawler.DEFINITIONS_PATH+"/"+file_name_arg
        try:
            with open(path) as fstream:
                parsed_json = json.load(fstream)
            return WebCrawler.build_from_dict(parsed_json)
        except FileNotFoundError:
            raise FileNotFoundError(f"Tried opening {path}, file not found\n")

    @staticmethod
    def build_all_from_json() -> [WebCrawler]:
        """Factory method initializing a crawler from each file in the definitions folder"""
        definitions = listdir(WebCrawler.DEFINITIONS_PATH)
        return [WebCrawler.build_from_json(file_name) for file_name in definitions if file_name.endswith(".json")]

    def auto_fill_pipeline(self, link: str = None, min_links_arg=100) -> None:
        """Recursive crawler function. Extracts individual news links from the main page specified by main_page_link.

        Calls itself on the next page until the max_links have been reached. The links obtained will be added to the
        pipeline with status: "Not_Yet_Dispatched"

        :param link: Recursion parameter indicating the page to crawl. Defaults to None, in which case crawls the
            page specified by self->main_page_link
        :param min_links_arg: Lower bound on the number of links added to the pipeline until recursion ends
        """
        # TODO: implement a check so that if the collection of links reaches the first link of the last search, it stops
        if link is None:
            link = self._main_page_link
        soup = self._get_soup_from_link(link, use_selenium_arg=self._main_needs_sel)
        hrefs = self._get_hrefs(soup)
        if hrefs is None:
            print("auto_fill_pipeline stopped prematurely. "
                  "Either there are not enough link in the page or a selector didnt work")
            return
        self._add_to_pipeline(hrefs)

        # go to the next page if necessary
        if min_links_arg - len(hrefs) <= 0:
            return
        next_page_link = self._get_next_page_link(soup)
        if next_page_link is None:
            return
        self.auto_fill_pipeline(next_page_link, min_links_arg=min_links_arg - len(hrefs))

    def push_to_pipeline(self, links_arg: [str]) -> None:
        if isinstance(links_arg, list):
            self._add_to_pipeline(links_arg)
        else:
            raise ValueError(f"push_to_pipeline expected a list, got {type(links_arg)}\n")

    def dispatch_links(self, extracting_method_arg: str = "generic", n_of_threads_arg: int = 1,
                       status_filter_arg: str = None) -> None:
        """Processes links from the pipeline and sends extracted information to the database.

        This function will consume the entire pipeline unless a specific status to consume is provided

        :param extracting_method_arg: string indicating the desired parsing method. Currently implemented:
            ["generic", "only print"]. Refer the documentation for more information
        :param n_of_threads_arg: integer indicated the number of consumer threads to be initialized
        :param status_filter_arg: String indicating a status.
            Only links that match the indicated status will be dispatched"""
        methods = {"generic": lambda x, link: WebCrawler._generic_new_scraping(x, link),
                   "gdacs": lambda x, link: WebCrawler._gdacs_new_scraping(x, link),
                   "only print": lambda _, link: print(link)}
        parse_method = methods[extracting_method_arg]
        failed_links = Queue()
        threads = [threading.Thread(target=lambda: self._consumer_thread(parse_method, failed_links, status_filter_arg))
                   for _ in range(n_of_threads_arg)]
        for thread in threads:
            thread.start()
        self._link_pipeline.join()
        self._link_pipeline = failed_links

    def _matches_filters(self, link_arg: str) -> bool:
        """Filters a link based on self's whitelists/blacklists. Yeah, that's it.

        :param link_arg: A string containing the link to be filtered
        :returns: True if the link matches the filters, false if it doesn't. Note that to pass the filters, the link
            must simultaneously be in the whitelists and not be in the whitelists
        """
        if self._link_whitelist is None:
            matches_whitelist = True
        else:
            matches_whitelist = any(map(lambda x: re.match(x, link_arg), self._link_whitelist))
        # True if present in whitelist (or there are no whitelists)
        if self._link_blacklist is None:
            matches_blacklist = False
        else:
            matches_blacklist = any(map(lambda x: re.match(x, link_arg), self._link_blacklist))
        # False if present in blacklist
        return matches_whitelist and not matches_blacklist

    def _format_link(self, relative_link: str, is_next_page_link_arg: bool = False) -> str:
        """Adds the base address to the relative address to get a valis address"""
        # TODO move the ["href"] out of this function
        base_link = self._next_page_root_link if is_next_page_link_arg is True else self._news_root_link
        return base_link + relative_link

    def _add_to_pipeline(self, links_arg: [str], status_arg="Not_Yet_Dispatched"):
        """kinda irrelevant, only used in auto_fill_pipeline. TO BE REMOVED"""
        # TODO refactor this xd
        for x in links_arg:
            self._link_pipeline.put({"link": x, "status": status_arg})
        # Alt way: [self.link_pipeline.put({"link": x, "status": status_arg}) for x in links_arg]

    def _get_soup_from_link(self, link_arg: str, use_selenium_arg: bool = False) -> BeautifulSoup:
        """Fetches the html of the given link and instantiates a BeautifulSoup with it

        If the raw source is not enough and the link in question needs waiting for a server response,
        selenium must be used

        :param link_arg: source of the html
        :param use_selenium_arg: bool indicating if selenium must be used. Defaults to False"""
        if use_selenium_arg:
            WebCrawler.sel_session_lock.acquire()
            WebCrawler.sel_driver.get(link_arg)
            raw_html = WebCrawler.sel_driver.page_source
            WebCrawler.sel_session_lock.release()
        else:
            with requests.get(link_arg) as stream:
                raw_html = stream.content.decode(self._encoding, errors="replace")
        return BeautifulSoup(raw_html, "html.parser")

    def _get_hrefs(self, soup_arg: BeautifulSoup) -> list[str]:
        """Given a soup, find all links in the tags that match the ones in self

        First, the tag in which the links are grouped is fetched.
        Then, the individual links are collected"""
        # print(soup_arg.prettify())
        main_section = soup_arg.select_one(self._news_wapper_selector)
        if main_section is None:
            raise ValueError("Invalid news_wapper_selector")
        relevant_a_tags = main_section.select(self._new_link_selector)

        hrefs = []  # The next chunk of code looks horribke but it will make error handling eaiser in the long run
        for tag in relevant_a_tags:
            href = tag["href"]
            if not self._matches_filters(href):
                continue
            hrefs.append(self._format_link(href))
        return hrefs if len(hrefs) > 0 else None

    def _get_next_page_link(self, soup_arg: BeautifulSoup) -> str | None:
        """Given a soup, find the link to the next page to be crawled.
        Returns None if no tag attributes were specified
        """
        if self._next_page_link_selector is None:
            return None
        next_page_tag = soup_arg.select_one(self._next_page_link_selector)
        if next_page_tag is None:
            raise ValueError("Invalid next_page_link_selector")
        return self._format_link(next_page_tag["href"], is_next_page_link_arg=True)

    def _consumer_thread(self, parsing_method_arg, failed_links_queue_arg: Queue, status_filter_arg: str) -> None:
        """Consumer thread wrapper. Will consume elements from self->link_pipeline until its empty, then dies.

        :param parsing_method_arg: A method with the following signature: method(self, link)->None. This is the method
            that the thread will call on each link in th pipeline. It's expected to both
            extract information and send it to the database
        :param failed_links_queue_arg: A queue that will be modified in place, where the links that produce an exception
            or don't match the status filter will go
        :param status_filter_arg: A string indicating which links of the pipeline will be processed. The rejected links
            will be added to failed_link_queue
        """
        while True:
            try:
                self._thread_main(parsing_method_arg, failed_links_queue_arg, status_filter_arg)
                self._link_pipeline.task_done()
            except Empty:
                return

    def _thread_main(self, parsing_method_arg, failed_links_queue_arg: Queue, status_filter_arg: str) -> None:
        """Consumer thread main function. Processes a link and mutates both the
        link_pipeline and the failed_link queue in-place.

        :except queue.Empty: When self->link_pipeline is finally empty
        """
        global e
        curr_link = self._link_pipeline.get(block=False)
        if status_filter_arg is not None and curr_link["status"] != status_filter_arg:
            failed_links_queue_arg.put(curr_link)
            return
        try:
            parsing_method_arg(self, curr_link["link"])
            return
        except ConnectionError as e:
            curr_link["status"] = "Connection_Error"
            if self.SHOW_EXCEPTIONS:
                print(e)
        except (TypeError, AttributeError) as e:
            curr_link["status"] = "General_Parsing_Error"
            if self.SHOW_EXCEPTIONS:
                print(e)
        except InvalidCategoryErr as e:
            curr_link["status"] = "Could_not_Classify_New"
            if self.SHOW_EXCEPTIONS:
                print(e)
        failed_links_queue_arg.put(curr_link)
        print(f"An error occurred when trying to process a link: \n{curr_link['link']}\n Error: {curr_link['status']}")
        return

    def _generic_new_scraping(self, link_arg: str) -> None:
        """Generic extracting method used on news consisting of a title and main body"""
        soup = self._get_soup_from_link(link_arg)
        curr_disaster = self._build_unparsed_disaster(soup, link_arg)
        curr_disaster.classify()
        curr_disaster.extract_data()
        # TODO modify the way the db connection is handled to add propper context management
        curr_disaster.save_to_database()

    def _gdacs_new_scraping(self, link_to_new_arg: str) -> Disaster:
        """call the api I guess"""
        raise NotImplementedError

    def _build_unparsed_disaster(self, soup_arg: BeautifulSoup, link_arg: str) -> Disaster:
        """Disaster instance builder. The returned Disaster type will only have
        the raw_data and link attributes initialized"""
        # TODO add debug info to execptions
        title = soup_arg.select_one(self._title_selector)
        body = soup_arg.select(self._body_selector)
        parsed_title = re.sub(r'\s+', ' ', title.text)
        parsed_body = re.sub(r'\s+', ' ', "".join([x.text for x in body]))
        return Disaster(raw_data_arg={"title": parsed_title, "body": parsed_body},
                        news_portal_arg=self._web_name,
                        link_arg=link_arg,
                        language_arg=self._language)
