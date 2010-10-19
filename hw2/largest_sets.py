#!/usr/bin/python

import re,sys
from operator import itemgetter

#matches the keys in the graphml file
extract_data = re.compile(r'<data key=\"(.*)\">(.*)<')

#extracts (key,size) data from the graph
def set_data(line):
    result = extract_data.search(line)
    if result == None:
        return None

    #not important if key is one of these words
    if result.group(1) == "title" or result.group(1) == "original_num":
        return None

    #find and extract
    if result != None:
        list_size = re.split(', ', result.group(2))
        list_size = len(list_size)
        return (result.group(1), list_size)

def main():
    graph = open("wiki.graphml",'r').xreadlines()
    data = []

    for line in graph:
        temp = set_data(line)
        if temp != None:
            data.append(temp)

    #sort data in descending order based on size of set
    data = sorted(data, key=itemgetter(1), reverse=True)
    print data[:10]
    for name in [result[0] for result in data[:10]]:
        print name + " ",
main()
