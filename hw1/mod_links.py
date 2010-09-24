#!/usr/bin/python
import re, sys

grouper = re.compile(r'(\d+): (.*)$')
outFile = open('wiki-links.txt', 'w')

def mod(line):
    groups = grouper.match(line)
    links = groups.group(2).split()

    node = int(groups.group(1))
    linkList = ';'.join(links)

    string = ""
    if(node != 5250701):
        string = str(node)+"|"+str(sys.maxint)+"|"+linkList+"\n"
    if(node == 5250701):
        string = "5250701|0|"+linkList+"\n"

    outFile.write(string)
    
def main():
    lines = open(sys.argv[1], 'r').read().splitlines()
    print sys.argv[1]
    for line in lines:
        mod(line)
    outFile.close()

main()
