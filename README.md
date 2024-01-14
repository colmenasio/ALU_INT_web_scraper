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
This proyect was done as a "alumno interno" task

THIS VERSION IS INCOMPLETE; ITS MISSING NLP METHODS TO NORMALIZE THE INFORMATION;


## Main Features
1. Website class:
    - To get started, create an instance of the Website class, specifying the location of relevant link, whitelists, and other parameters:
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
    - Each Website intance has an url pipeline of links to be scraped. The method  `get_links` fill the pipeline with links from the main page specified
      ```py
      # Example
      flood_list.get_links(max_links=10)
      ```
    - Once the pipeline is full, `dispatch_links` scrapes, parses, and (in the future) uses NLP to extract data and send it to a database
      ```py
      # Example
      flood_list.dispatch_links(n_of_threads=5)
      ```


<!-- ROADMAP -->
## Roadmap

- [x] Method to fetch links to news from the main page
- [x] Parsing method to standazise said news
- [ ] NLP analysis
    - [ ] Implement API for particular webs
- [ ] Database Integration

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Doctumentation  -->
## Full Documentation

_For more examples, please refer to the [Documentation](https://example.com)_

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Readme Template: https://github.com/othneildrew/Best-README-Template/tree/master

<p align="right">(<a href="#readme-top">back to top</a>)</p>

 
