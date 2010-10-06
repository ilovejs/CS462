#!/usr/bin/python

import re,sys

nodelist = re.compile(r'\s+(\d+)\|\d+\|(.*)')

def create_edgelist(line,output):
    list = nodelist.search(line)
    node = list.group(1)
    node = int(node)
    outlinks = list.group(2).split(';')
    if len(outlinks) == 1 and outlinks[0] == '':
        return
    for link in outlinks:
        output.write(str(node) + " " + str(link) + "\n")

def main():
    lines = open(sys.argv[1], 'r').xreadlines()
    output = open(sys.argv[2], 'w')
    for line in lines:
        create_edgelist(line, output)

main()
