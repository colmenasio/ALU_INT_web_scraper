from WebCrawler import WebCrawler

# TODO implement "https://gdacs.org/Alerts/default.aspx" api
# TODO implement premium filter for ELPAIS
# TODO implement button data-pagina for EITB (nr it only takes the first page of news)
#  (tb tampoco tiene demasiada informacion igual no vale la pena)

crawler = WebCrawler.build_from_json("relief_web.json")
print("RUNNING")
crawler.auto_fill_pipeline(min_links_arg=1)
print("DISPATCHING LINKS")
crawler.dispatch_links(n_of_threads_arg=1, extracting_method_arg="generic")
