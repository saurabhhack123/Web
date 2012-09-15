from gohachi_crawler import graph
from gohachi_crawler import ranks


name_length = 33   # How many letter will have the printed link in each node
font_size_multiplier = 5 # increse / decrease to have bigger/smaller fonts and arrows

def biggest_rank(ranks):
    big = 0.0
    for url in ranks:
        if ranks[url] > big:
            big = ranks[url]
    return big

def node_name(string):
    return '"' + string + '"'

def node_label(string):                                #Handling long string's of links
    if len(string) > name_length:
        return string[:(name_length - 3) / 2] + '...' + string [-(name_length - 3) / 2:]
    else:
        return string

def node_dot(node, ranks):                     #writing string to dot file in dot language format
    result = node_name(node)                   
    result += ' [label="' + node_label(node) + '\\n' + str("%.4f" % ranks[node]) + '"'                 
    result += ', fontsize=' + str(ranks[node] * font_size_multiplier  / biggest_rank(ranks))
    result += ', penwidth=' + str(ranks[node] * font_size_multiplier  / (biggest_rank(ranks) * 10)) 
    result += ', URL=' + node_name(node) 
    result += '];'
    return result

def edge_dot(source, target, ranks, name = ''):
    sr = node_name(source)
    tg = node_name(target)
    dot_string = sr + ' -> ' + tg 
    dot_string += ' ['
    dot_string += 'penwidth=' + str(ranks[source] * font_size_multiplier  / (biggest_rank(ranks) * 10))
    dot_string += ', arrowsize=' + str(ranks[source] * font_size_multiplier / (biggest_rank(ranks) * 10))
    if len(name) > 0:
        dot_string += ', label="' + name + '"'
    dot_string += '];'
    return dot_string

def all_nodes_dot(graph, ranks):
    dot_string = ''
    for node in graph:
        dot_string += node_dot(node, ranks) + '\n'
    return dot_string

def all_edges_dot(graph, ranks):
    dot_string = ''
    for source in graph:
        for target in graph[source]:
            dot_string += edge_dot(source, target, ranks) + '\n'
    return dot_string

def graph_dot(graph, ranks):
    dot_string = 'digraph G {\n'
    dot_string += all_nodes_dot(graph, ranks) + all_edges_dot(graph, ranks)
    dot_string += '}'
    return dot_string

    
def make_dot_file(filename, graph, ranks):
    f = open(filename, "w")
    f.write(graph_dot(graph, ranks))
    f.close()
