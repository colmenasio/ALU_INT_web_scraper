from WebCrawler import WebCrawler

# TODO implement "https://gdacs.org/Alerts/default.aspx" api

flood_list = WebCrawler.build_from_json("flood_list.json")
print("RUNNING")
flood_list.auto_fill_pipeline(min_links=2)
print("DISPATCHING LINKS")
flood_list.dispatch_links(n_of_threads_arg=1, extracting_method_arg="generic")
