# Websites definitions

Collection of `.json` files, 
each one specifiyng CSS selectors, whitelists, links, etc needed for `WebCrawler`
to extract information from a website.

## Building instances
The factory method `WebCrawler.build_from_json("web1.json")` builds a single `WebCrawler` instance from
the `web1.json` file.

Alternatively, `WebCrawler.build_all_from_json()`, will return a list of `WebCrawler` instances, 
each built from a `.json` in `/definitions`

##

*Note:* The folder containing `.json` definitions 
can be changed by modifyng the class argument: `WebCrawler.DEFINITIONS_PATH = "newpath/files"`
