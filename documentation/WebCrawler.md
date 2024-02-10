# Module: **WebCrawler**

<!--class_WebCrawler-->
## Class: `WebCrawler`
Each instance of this class will represent a single website, and contain the 
css selectors and metadata needed to extract links 
to individual links from said website.

Instances can be initialized either normally, with a dictionary (`WebCrawler.build_from_dict(stuff)`)
or from a json file in the `definitions` directory (`WebCrawler.build_from_json("stuff.json")`)

Each instance also contains a protected `self._pipeline` that will hold links to
individial news for future processing and their status

<!--methods-->
## Public Interface

### `Builders`

- `__init__()`
- `build_from_dict(dictionary)`
- `build_from_json(filename)` or `build_all_from_json()`: The json files, by default ,
are expected to be found in the `"root/website_definitions/definitions"`. Check its README for more info

### `auto_fill_pipeline(self, link: str = None, min_links=100) -> None:`
The website in question is supposed to have a main article page, in which links 
to individual links reside, as well a link to the "next page" of news.

This method extracts those links accordinly to the selectors provided and recursively
visits subsequent "next page"s until the minimun of links is reached.

This function adds the collected news links to the pipeline, with status `"Not_Yet_Dispatched"`

`link` is a recursion argument and should be ignored

### `dispatch_links(self, extracting_method_arg: str = "generic", n_of_threads_arg: int = 1, status_filter_arg: str = None) -> None:`
Initializes a number of consumer threads that will apply certain function 
to each of the links in the pipeline.

The function to be applied is specified in a string (either "generic" or "only print", 
more to be added in the future for specific, more structured websites)

Within the pipline, each link has a status. If only links matching a certain status
are to be dispatched, a filter can be specified as an argument. Defaults to `None` (Matches all status)

## Private Methods
adsndf #TODO explain the private methods