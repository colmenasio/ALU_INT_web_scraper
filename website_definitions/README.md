# Websites definitions

Collection of `.json` files, 
each one specifiyng CSS selectors, whitelists, links, etc needed for `WebCrawler`
to extract information from a website.

## Building instances
When the factory method `WebCrawler.build_all_from_json()`, each file in `/definitions`
will be used to create an instance of `Website`.

Alternatively, `WebCrawler.build_from_json("web1.json")` builds a single instance from
the `web1.json` file

##

*Note:* The folder containing `.json` definitions 
can be changed by modifyng the class argument: `WebCrawler.DEFINITIONS_PATH = "newpath/files"`