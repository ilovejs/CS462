#!/usr/bin/python
import re,sys

#match anything hit by the BFS
path = re.compile(r'\s+\d+\|[0-7]\|\d+')

def collect(line, output):
    #if match, then output to file
    if path.search(line):
        output.write(line)

def main():
    lines = open(sys.argv[1], 'r').xreadlines()
    output = open(sys.argv[2], 'w')
    num_nodes = 0
    for line in lines:
        collect(line, output)

main()
