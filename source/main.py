from WebCrawler import WebCrawler

# TODO implement "https://gdacs.org/Alerts/default.aspx" api

general_whitelists = [".+quake.+", ".+flood.+", ".+volcan.+", ".+hurricane.+", ".+drought.+", ".+fire.+", ".+tsunami.+",
                      ".+disease.+", ".+pandem.+", ".+water.+", ".+ rain.+", ".+outbreak.+"]

# relief_web = WebCrawler(web_name_arg="Relief Web",
#                         main_page_link_arg="https://reliefweb.int/updates?list=Updates%20%28Headlines%29&view=headlines",
#                         news_tag_type_arg="section",
#                         news_tag_attr_arg={"class": "[ cd-flow ] rw-river rw-river--river-list", "id": "river-list"},
#                         new_link_tag_type_arg="h3",
#                         new_link_tag_attr_arg={"class": "rw-river-article__title", "lang": "en"},
#                         next_page_tag_attr_arg={"title": "Go to next page", "rel": "next"},
#                         title_tag_type_arg="h1",
#                         title_tag_attr_arg={"class": "rw-article__title rw-page-title"},
#                         body_tag_type_arg="div",
#                         body_tag_attr_arg={"class": "rw-article__content"},
#                         news_links_whitelist_arg=general_whitelists,
#                         base_next_page_link_arg="https://reliefweb.int/updates",
#                         encoding_arg="UTF-8"
#                         )
#
# # WARNING!!! ICSaMD has a single main page so when extracting links from it, the pipeline gets full with idk 800 links
# # Basically it gets kinda slow when dispaching cause, yk, its 800 links
# ICSaMD = WebCrawler(web_name_arg="International Charter Space and Major Disasters",
#                     main_page_link_arg="https://disasterscharter.org/web/guest/"
#                                        "charter-activations?from=01+01+2000&to=27+11+2023",
#                     news_tag_type_arg="div",
#                     news_tag_attr_arg={"class": "timeline"},
#                     new_link_tag_type_arg="div",
#                     new_link_tag_attr_arg={"class": "activations"},
#                     title_tag_type_arg="h3",
#                     title_tag_attr_arg={"class": "asset-title content activation-title"},
#                     body_tag_type_arg="div",
#                     body_tag_attr_arg={"class": "col-md-12 activation-description-text"},
#                     does_main_needs_selenium_arg=True,
#                     base_news_link_arg="https://disasterscharter.org/",
#                     encoding_arg="UTF-8"
#                     )
#
# reuters = WebCrawler(web_name_arg="Reuters",
#                      main_page_link_arg="https://www.reuters.com/news/archive/tsunami",
#                      news_tag_type_arg="section",
#                      news_tag_attr_arg={"class": "module-content"},
#                      new_link_tag_type_arg="div",
#                      new_link_tag_attr_arg={"class": "story-content"},
#                      next_page_tag_attr_arg={"class": "control-nav-next"},
#                      title_tag_type_arg="h1",
#                      title_tag_attr_arg={"data-testid": "Heading"},
#                      body_tag_type_arg="div",
#                      body_tag_attr_arg={"class": "article-body__content__17Yit"},
#                      news_links_whitelist_arg=general_whitelists,
#                      base_news_link_arg="https://www.reuters.com",
#                      base_next_page_link_arg="https://www.reuters.com/news/archive/tsunami",
#                      do_news_needs_selenium_arg=True,
#                      encoding_arg="UTF-8"
#                      )

# TODO UPDATE THE README AND DOCUMENTATION TO THE NEW INTERFACE (selectors)

flood_list2 = WebCrawler.build_from_json("flood_list.json")
print("Running")
flood_list2.auto_fill_pipeline(min_links=2)
print("DISPATCHING LINKS")
flood_list2.dispatch_links(n_of_threads_arg=1, extracting_method_arg="generic")
