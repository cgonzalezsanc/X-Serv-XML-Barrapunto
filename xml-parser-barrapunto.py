#!/usr/bin/python

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string

def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return string.join(string.split(text), ' ')

class CounterHandler(ContentHandler):

    def __init__ (self):
        self.inContent = 0
        self.theContent = ""
        self.isANew = 0  # variable que indica si el titular es de una noticia

    def startElement (self, name, attrs):
        if name == 'item':
            self.link = normalize_whitespace(attrs.get('rdf:about'))
            self.isANew = 1
        elif name == 'title':
            if self.isANew:
                self.inContent = 1
            
    def endElement (self, name):
        if self.inContent:
            self.theContent = normalize_whitespace(self.theContent)
        if name == 'item':
            print ""
        elif name == 'title':
            if self.isANew:
                self.response = "<p><a href='" + self.link + "'>" + \
                                self.theContent + "</a></p><br>" 
                print self.response
        if self.inContent:
            self.inContent = 0
            self.isANew = 0
            self.theContent = ""
        
    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog

if len(sys.argv)<2:
    print "Usage: python xml-parser-jokes.py <document>"
    print
    print " <document>: file name of the document to parse"
    sys.exit(1)
    
# Load parser and driver

JokeParser = make_parser()
JokeHandler = CounterHandler()
JokeParser.setContentHandler(JokeHandler)

# Ready, set, go!

xmlFile = open(sys.argv[1],"r")
JokeParser.parse(xmlFile)

print "Parse complete"
