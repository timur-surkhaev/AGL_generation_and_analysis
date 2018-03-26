#/usr/bin/python

MAX_LEN = 7     # max length of string
MIN_LEN = 5     # min length of string

graph = {'Start': ['1'],
         '1': ['2', '3'],
         '2': ['2', '4'],
         '3': ['3', '5'],
         '4': ['3', '6'],
         '5': ['4', '6'],
         '6': ['End'],
         'End': []}

conv_matrix = {'12':'X',
               '13':'V',
               '22':'M',
               '24':'X',
               '33':'S',
               '35':'V',
               '43':'R',
               '46':'M',
               '54':'S',
               '56':'M'}


def find_all_paths(graph, start, end, length, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    
    paths = []
    for node in graph[start]:
        if len(path) < length:  # to avoid infinite cycle
            newpaths = find_all_paths(graph, node, end, length, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths        

gramm_paths = find_all_paths(graph, 'Start', 'End', MAX_LEN + 3)

gramm_strings = []
for gramm in gramm_paths:
    if len(gramm) >= MIN_LEN+3:
        gramm_strings.append(''.join([conv_matrix[gramm[i] + gramm[i+1]] 
                    for i in range(1, len(gramm) - 2)]))

print len(gramm_strings)

gramm_strings.sort(key = lambda s: len(s))
for string in gramm_strings:
    print string
    

#print(find_all_paths(graph, 'A', 'F'))
