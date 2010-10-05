#!/usr/bin/python
import re,sys

#matches anything that was reached in the BFS
path = re.compile(r'\s+\d+\|[0-7]\|\d+')

def count(line):
    count = 0

    #if there is a match, increase count
    if path.search(line):
        count += 1
    return count

def main():
    lines = open(sys.argv[1], 'r').xreadlines()
    num_nodes = 0
    for line in lines:
        num_nodes += count(line)

    #print total number of nodes
    print num_nodes

main()
