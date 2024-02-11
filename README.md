<a name="readme-top"></a>

# Disaster Information Web Scraper
Web Scraper, built in Python using [`BeautifulSoup`](https://pypi.org/project/beautifulsoup4/) for html parsing and [`openAI`](https://openai.com/) for information extraction.
Despite being originaly built for disaster news websites, can be easily tweaked to work with any type of news website


This proyect was done as a "alumno interno" task (plz change this line asap...)

## Getting Started
1. Creating a `WebCrawler` instance:
    - The crawler needs the relevant selectors and metadata needed for, well, crawling the web. Said parameters are provided during instanciation. Either specify them directly...
      ```py
      # Example
      generic_web = WebCrawler(
          "web_name": "example",
          "main_page_link": "https://example.com/news",
          "news_wapper_selector": "main.articles",
          "new_link_selector": ".article > a",
          "next_page_link_selector": "a.next_page",
          "title_selector": "h1.title",
          "body_selector": "div.content > p",
          "news_links_blacklist": ["https://example.com/unrelated_stuff/.+"],
          )
      ```
      ...or use one of the provided builders for convinience:
      ```py
      generic_web = WebCrawler.build_from_json("example.json")
      ```
      
      The public interface of the `WebCrawler` class is incredibly minimalistic. Its mainly consists of two methods: `auto_fill_pipeline` and `dispatch_links`
      
    - The method  `auto_fill_pipeline` crawls through the main pages of the news site, scraping news links according to the filters specified when creating the Website instance
      ```py
      # Example
      generic_web.auto_fill_pipeline(min_links=10)
      ```
      And so, the pipeline of links is full.

    - Once the pipeline is full, `dispatch_links` scrapes, parses, and uses the openai API to extract data and later send it to the database
      ```py
      # Example
      generic_web.dispatch_links(n_of_threads_arg=5)
      ```
      And now, the script is done.


<!-- ROADMAP -->
## Roadmap

- [x] Methods to fetch links to news from the main page
    - [x] Switch to CSS selectors as any normal human being would
- [x] Serialize news in a parse-able format
    - [ ] Implement API for particular webs that offer it 
- [x] AI analysis yayyy:
    - [ ] Improve AI precision:
        - [x] Better propts
        - [ ] Fine-tuning the model, perhaps?
- [x] For the love of god please write propper tests (kinda done)
- [ ] Serialization/Database implementation


<!-- Doctumentation  -->
## Full Documentation

Most documentation is provided via docstrings, for more examples, please refer to the [Documentation folder](/documentation)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

 
