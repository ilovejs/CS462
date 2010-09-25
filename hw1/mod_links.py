#!/usr/bin/python
import re, sys

# matches (#: # # # ... #)
grouper = re.compile(r'(\d+): (.*)$')

def mod(line):
    groups = grouper.match(line)
    links = groups.group(2).split()

    node = int(groups.group(1))
    linkList = ';'.join(links)

    # create string node#|DIST|outlink;list;#
    # 3015959 == node with most outlinks (predetermined)
    string = ""
    if(node != 3015959):
        string = str(node)+"|"+str(sys.maxint)+"|"+linkList+"\n"
    if(node == 3015959):
        string = "3015959|0|"+linkList+"\n"

    # write new line to output
    output.write(string)
    
def main():
    lines = open(sys.argv[1], 'r').xreadlines()
    output = open(sys.argv[2], 'w')
    for line in lines:
        mod(line, output)
    output.close()

main()
