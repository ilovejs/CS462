#!/usr/bin/python
import re, sys

grouper = re.compile(r'(\d+): (.*)$')
outFile = open('/media/SW_Preload/wiki-links.txt', 'w')

def mod(line):
    groups = grouper.match(line)
    links = groups.group(2).split()

    node = int(groups.group(1))
    linkList = ';'.join(links)

    string = ""
    if(node != 3015959):
        string = str(node)+"|"+str(sys.maxint)+"|"+linkList+"\n"
    if(node == 3015959):
        string = "3015959|0|"+linkList+"\n"

    outFile.write(string)
    
def main():
    lines = open(sys.argv[1], 'r').xreadlines()
    for line in lines:
        mod(line)
    outFile.close()

main()
