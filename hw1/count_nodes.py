#!/usr/bin/python
import re,sys

path = re.compile(r'\s+\d+\|[0-7]\|\d+')

def count(line):
    count = 0
    if path.search(line):
        count += 1
    return count

def main():
    lines = open(sys.argv[1], 'r').xreadlines()
    num_nodes = 0
    for line in lines:
        num_nodes += count(line)
    print num_nodes

main()
