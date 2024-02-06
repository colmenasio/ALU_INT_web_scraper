from __future__ import annotations

from bs4 import BeautifulSoup
import re
import requests
from selenium import webdriver
from source.CustomExceptions import InvalidCategoryErr
from source.Disaster import Disaster
import threading
from queue import Queue, Empty
import warnings

if __name__ == "__main__":
    print("lololololol wrong file. dont delete this its useful for testing xd")


class WebCrawler:
    """API interface.
    Meant to be instanced once per website.
    Wraps the methods for crawling a website and processing news in a convenient way"""
    sel_options = webdriver.ChromeOptions()
    sel_options.add_argument("--headless")
    sel_driver = webdriver.Chrome(options=sel_options)
    sel_driver.implicitly_wait(time_to_wait=3)
    sel_session_lock = threading.Lock()

    def __init__(self,
                 web_name_arg: str = None,
                 main_page_link_arg: str = None,

                 news_wapper_selector_arg: str = None,
                 new_link_selector_arg: str = None,
                 next_page_link_selector_arg: str = None,
                 title_selector_arg: str = None,
                 body_selector_arg: str = None,

                 news_links_blacklist_arg: [str] = None,
                 news_links_whitelist_arg: [str] = None,

                 base_next_page_link_arg: str = "",
                 base_news_link_arg: str = "",
                 does_main_needs_selenium_arg: bool = False,
                 do_news_needs_selenium_arg: bool = False,
                 encoding_arg: str = "UTF-8"):
        """
        :param web_name_arg: Website name. Purely aesthetic. Currently useless
        :param main_page_link_arg: Link to the first page to extract links from
        :param news_wapper_selector_arg: Selector to the tag that wraps relevant news articles
        :param new_link_selector_arg: Selector to the 'a' tag containing the link to a new
            (relative to the news_wrapper_selector)
        :param next_page_link_selector_arg: Selector to the 'a' tag containing the href of the next page to crawl
        :param title_selector_arg: Selector to the title of the new
        :param body_selector_arg: Seletor to the different paragrafs of text in the new
        :param news_links_blacklist_arg: re Regex that news links must match to be processed.
            If None, matches all links. Defaults to None
        :param news_links_whitelist_arg: re Regex that news links must not match to be processed.
            Defaults to None
        :param base_next_page_link_arg: Prefix to be added to the relative address of the next page link
        :param base_news_link_arg: Prefix to be added to the relative addresses of the individual news links
        :param does_main_needs_selenium_arg: Bool indicating if selenium is needed in the main pages
            (if server response is required)
        :param do_news_needs_selenium_arg: Bool indicating if selenium is needed in the main pages
            (if server response is required)
        :param encoding_arg: Defaults to UTF-8.
        """
        # TODO: this is absolutely horrible remember to eventually change this to use css selectors instead
        # TODO: documentation :pain:
        # TODO: some crawling/scraping methods will require different fields than others. Write
        #   functions that ensure the method called can be run with the current parameters Man i wish you could do
        #   like rust and just write each field once Also this is a mess
        self.web_name = web_name_arg
        self.main_page_link = main_page_link_arg

        self.news_wapper_selector = news_wapper_selector_arg
        self.new_link_selector = new_link_selector_arg
        self.next_page_link_selector = next_page_link_selector_arg
        self.title_selector = title_selector_arg
        self.body_selector = body_selector_arg

        self.link_whitelist = news_links_whitelist_arg
        self.link_blacklist = news_links_blacklist_arg
        self.does_main_needs_sel = does_main_needs_selenium_arg
        self.do_news_needs_sel = do_news_needs_selenium_arg
        self.next_page_base_link = base_next_page_link_arg
        self.news_base_link = base_news_link_arg
        self.encoding = encoding_arg

        self.link_pipeline = Queue()  # Queue of dictionaries in the form of: {Link: "", Status: ""}

    def auto_fill_pipeline(self, link: str = None, min_links=100) -> None:
        """Recursive crawler function. Extracts individual news links from the main page specified by main_page_link.

        Calls itself on the next page until the max_links have been reached. The links obtained will be added to the
        pipeline with status: "Not_Yet_Dispatched"

        :param link: Recursion parameter indicating the page to crawl. Defaults to None, in which case crawls the
            page specified by self->main_page_link
        :param min_links: Lower bound on the number of links added to the pipeline until recursion ends
        """
        # TODO: implement a check so that if the collection of links reaches the first link of the last search, it stops
        if min_links <= 0:
            return
        if link is None:
            link = self.main_page_link
        soup = self._get_soup_from_link(link, use_selenium_arg=self.does_main_needs_sel)
        hrefs = self._get_hrefs(soup)
        if hrefs is None:
            print("auto_fill_pipeline stopped prematurely. "
                  "Either there are not enough link in the page or a selector didnt work")
            return
        self._add_to_pipeline(hrefs)
        next_page_link = self._get_next_page_link(soup)
        if next_page_link is None:
            return
        self.auto_fill_pipeline(next_page_link, min_links=min_links - len(hrefs))

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
        [x.start() for x in threads]
        self.link_pipeline.join()
        self.link_pipeline = failed_links

    def _matches_filters(self, link_arg: str) -> bool:
        """Filters a link based on self's whitelists/blacklists. Yeah, that's it.

        :param link_arg: A string containing the link to be filtered
        :returns: True if the link matches the filters, false if it doesn't. Note that to pass the filters, the link
            must simultaneously be in the whitelists and not be in the whitelists
        """
        if self.link_whitelist is None:
            matches_whitelist = True
        else:
            matches_whitelist = any(map(lambda x: re.match(x, link_arg), self.link_whitelist))
        # True if present in whitelist (or there are no whitelists)
        if self.link_blacklist is None:
            matches_blacklist = False
        else:
            matches_blacklist = any(map(lambda x: re.match(x, link_arg), self.link_blacklist))
        # False if present in blacklist
        return matches_whitelist and not matches_blacklist

    def _format_link(self, relative_link: str, is_next_page_link_arg: bool = False) -> str:
        """Adds the base address to the relative address to get a valis address"""
        # TODO move the ["href"] out of this function
        base_link = self.next_page_base_link if is_next_page_link_arg is True else self.news_base_link
        return base_link + relative_link

    def _add_to_pipeline(self, links_arg: [str], status_arg="Not_Yet_Dispatched"):
        """kinda irrelevant, only used in auto_fill_pipeline. TO BE REMOVED"""
        # TODO refactor this xd
        for x in links_arg:
            self.link_pipeline.put({"link": x, "status": status_arg})
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
                raw_html = stream.content.decode(self.encoding, errors="replace")
        return BeautifulSoup(raw_html, "html.parser")

    def _get_hrefs(self, soup_arg: BeautifulSoup) -> list[str]:
        """Given a soup, find all links in the tags that match the ones in self

        First, the tag in which the links are grouped is fetched.
        Then, the individual links are collected"""
        main_section = soup_arg.select_one(self.news_wapper_selector)
        if main_section is None:
            raise ValueError("Invalid news_wapper_selector")
        relevant_a_tags = main_section.select(self.new_link_selector)

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
        if self.next_page_link_selector is None:
            return None
        next_page_tag = soup_arg.select_one(self.next_page_link_selector)
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
                self.link_pipeline.task_done()
            except Empty:
                return

    def _thread_main(self, parsing_method_arg, failed_links_queue_arg: Queue, status_filter_arg: str) -> None:
        """Consumer thread main function. Processes a link and mutates both the
        link_pipeline and the failed_link queue in-place.

        :except queue.Empty: When self->link_pipeline is finally empty
        """
        curr_link = self.link_pipeline.get(block=False)
        if status_filter_arg is not None and curr_link["status"] != status_filter_arg:
            failed_links_queue_arg.put(curr_link)
            return
        try:
            parsing_method_arg(self, curr_link["link"])
            return
        except ConnectionError:
            curr_link["status"] = "Connection_Error"
        except TypeError or AttributeError:
            curr_link["status"] = "General_Parsing_Error"
        except InvalidCategoryErr:
            curr_link["status"] = "Could_not_Classify_New"
        failed_links_queue_arg.put(curr_link)
        print(f"An error occurred when trying to process a link: {curr_link}")
        return

    def _generic_new_scraping(self, link_arg: str) -> None:
        """Generic extracting method used on news consisting of a title and main body"""
        soup = self._get_soup_from_link(link_arg)
        curr_disaster = self._build_unparsed_disaster(soup, link_arg)
        curr_disaster.classify()
        curr_disaster.extract_data()
        curr_disaster.save_to_database()  # TODO Rn it just prints the data. Add code in each subclass

    def _gdacs_new_scraping(self, link_to_new_arg: str) -> Disaster:
        """call the api I guess"""
        raise NotImplementedError

    def _build_unparsed_disaster(self, soup_arg: BeautifulSoup, link_arg: str) -> Disaster:
        """Disaster instance builder. The returned Disaster type will only have
        the raw_data and link attributes initialized"""
        title = soup_arg.select_one(self.title_selector)
        body = soup_arg.select(self.body_selector)
        parsed_title = re.sub(r'\s+', ' ', title.text)
        parsed_body = re.sub(r'\s+', ' ', "".join([x.text for x in body]))
        return Disaster(unprocessed_data_arg={"title": parsed_title, "body": parsed_body},
                        link_arg=link_arg)
