#
# Number of links to be followed from the seed page 
crawl_depth = 5           # You can change it as well like if you want more results into the graph but keep in mind if depth > 25 you need fast internet speed and also sufficient amount of memory
split_list = " !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"

def compute_ranks(graph):                        #This algorithm is somewhat similar to pagerank algorithm(Google Mark)
    d = 0.8 # damping factor                     #This implies that a random web server looking for on current page first rather than some random page
    numloops = 10                                #This is Just for accuracy (since web pages may be change's after some time and Hence Link's) 
    
    ranks = {}                                   #dictionary data type {url:rank,url:rank,......}
    npages = len(graph)                          #total no of pages i.e total no of node's( or total no. of links)
    for page in graph:                           #for node's in graph
        ranks[page] = 1.0 / npages               #Initialize rank's each page (1.0 instead of 1 since we want rank's in floating point(more accurate))
    
    for i in range(0, numloops):                  
        newranks = {}                            
        for page in graph:                       
            newrank = (1 - d) / npages           #initializing newrank will be due to others outlink's (simply a probability of page due inbound link from other page)
            for node in graph:                   #graph = {url:[url1,url2,...],url:[url1,.....],..} i.e list of pages it links to
                if page in graph[node]:          # if page(link) is inbound linked to some page than it's time to update 
                    newrank += d * (ranks[node] / len(graph[node]))        #newrank will be now probability factor(d)*it's rank in a pool of links((ranks[node] / len(graph[node]))  
            newranks[page] = newrank                                        
        ranks = newranks
    return ranks

def crawl_web(seed, max_depth = crawl_depth): # returns index, graph of inlinks
    tocrawl = [[seed, 0]]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl: 
        page, depth = tocrawl.pop()
        if page not in crawled and depth <= max_depth:
            content = get_page(page)
            #add_page_to_index(index, page, content)
            outlinks = get_all_links(content) 
            graph[page] = outlinks
            for link in outlinks:
                tocrawl.append([link, depth + 1])
            crawled.append(page)
    return graph


def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""


def get_next_target(page):
    start_link = page.find('href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

graph = crawl_web('http://www.vit.ac.in')         #crawling my college website or you can change as well
ranks = compute_ranks(graph)

