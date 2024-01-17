<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links -->

# Disaster Information Web Scraper
Python web scraper script for extracting disaster information from news portals.
The scrip relies on `beautifulsoup` for html parsing and on `openAI` for information extraction
This proyect was done as a "alumno interno" task

THIS VERSION IS INCOMPLETE; ITS MISSING NLP METHODS TO NORMALIZE THE INFORMATION;


## Getting Started
1. Creating a Website instance:
    - To get started, specify the location of relevants link, as well as specify whitelists and other parameters:
      ```py
      # Example
      generic_web = Website(web_name_arg="Just a Website",
                     main_page_link_arg="https://thingies.com/news",
                     news_tag_type_arg="main",
                     news_tag_attr_arg={"class": "site-main"},
                     new_link_tag_type_arg="h2",
                     new_link_tag_attr_arg={"class": "entry-title"},
                     next_page_tag_attr_arg={"class": "next page-numbers"},
                     title_tag_type_arg="h1",
                     title_tag_attr_arg={"itemprop": "headline"},
                     body_tag_type_arg="div",
                     body_tag_attr_arg={"itemprop": "articleBody"},
                     news_links_blacklist_arg=["https://website/not_related_stuff/.+"],
                     encoding_arg="UTF-8"
                     )
      ```
      The public interface of the Website class is incredibly minimalistic. Its mainly consists of two methods: `get_links` and `dispatch_links`
      
    - The method  `get_links` crawls through the main pages of the news site, scraping news links according to the filters specified when creating the Website instance
      ```py
      # Example
      generic_web.get_links(max_links=10)
      ```
      And so, the pipeline of links is full.

    - Once the pipeline is full, `dispatch_links` scrapes, parses, and uses the openai API to extract data and later send it to the database
      ```py
      # Example
      generic_web.dispatch_links(n_of_threads=5)
      ```
      And now, the script is done.


<!-- ROADMAP -->
## Roadmap

- [x] Method to fetch links to news from the main page
- [x] Serialize news in a parse-able format
    - [ ] Implement API for particular webs that offer it 
- [x] AI analysis yayyy:
    - [ ] Improve AI precision:
        - [ ] Better propts
        - [ ] Fine-tuning the model, perhaps?
- [ ] Serialization/Database implementation


<!-- Doctumentation  -->
## Full Documentation

_For more examples, please refer to the [a relative link](Documentation())
NOTE THAT THE DOCUMENTATION, RN, IS EXTREMELY OUTDATED. THE CODE COMMENTS THEMSELF ACT AS A BETTER DOCUMENTATION

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Readme Template: https://github.com/othneildrew/Best-README-Template/tree/master

<p align="right">(<a href="#readme-top">back to top</a>)</p>

 
