import re


quad = ""
neighborhoods = {}
f = open("wikipedia/wikipedia-neighborhoods.txt")
for line in f:
    if line[0] == '-':
        quad=line[2:].rstrip()
    else:
        m = re.search('([\w, -.]+)\|(\w+)]', line)
        if m:
            neighborhoods[m.group(2)] = {'quad': quad, 'wiki': m.group(1).replace(' ', '_')}

print neighborhoods['Laurelhurst']
