'''
Created on Jan 9, 2013

@author: Mike
'''
import sys
import urllib2
from datetime import datetime
from HTMLParser import HTMLParser

WEBSITE_URL = 'http://apod.nasa.gov/apod'

class HTMLNode(object):
    """
    Class representation of an HTML Node that would be found in a
    typical html file.
    """
    
    def __init__(self, tag, pos=-1):
        self.tag = tag
        self.children = []
        self.attributes = {}
        self.parent = None
        self.data = None
        self.pos = pos
        
    def __repr__(self):
        return '<{tag}: Attributes={attributes}, Pos={pos}>'.format(
            tag=self.tag,
            pos=self.pos,
            attributes=len(self.attributes))

class MemHTMLParser(HTMLParser):
    """
    Builds an in-memory representation of a given html file through the use of
    HTMLNode objects that are easily accessible through the nodes instance variable.
    """
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.nodes = {}
        self._node_stack = []
        
    def _peek_stack(self):
        return self._node_stack[len(self._node_stack)-1]
    
    def handle_starttag(self, tag, attrs):
        node = HTMLNode(tag, self.getpos())
        node.attributes = dict(attrs)
        
        if tag not in self.nodes:
            self.nodes[tag] = []
        self.nodes[tag].append(node)
        
        if len(self._node_stack) > 0:
            # Append to the item at the top of the stack
            parent = self._peek_stack()
            parent.children.append(node)
            node.parent = parent
        
        self._node_stack.append(node)
    
    def handle_data(self, data):
        self._peek_stack().data = data
    
    def handle_endtag(self, tag):
        self._node_stack.pop()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Allow user to specify the date of the pod to download
        target_date = datetime.strptime(sys.argv[1], '%d/%m/%y') 
    else:
        target_date = datetime.now()
    
    print 'target date = %s' % target_date
    target_url = '%s/ap%s.html' % (WEBSITE_URL, target_date.strftime('%y%m%d'))
    
    print 'requesting %s' % target_url
    url = urllib2.urlopen(target_url)
    html_data = url.read()
     
    print 'parsing html information'
    parser = MemHTMLParser()
    parser.feed(html_data)
    
    if 'img' in parser.nodes:
        image = parser.nodes['img'][0]
        
        # Get the High Resolution URL
        image_url = '%s/%s' % (WEBSITE_URL, image.parent.attributes['href'])
        print 'downloading %s' % image_url
        
        save_location = target_date.strftime('%d%m%y.jpg')
        
        request = urllib2.urlopen(image_url)
        image_file = open(save_location,'wb')
        image_file.write(request.read())
        image_file.close()
        
        print 'Successfully downloaded the Picture of the Day to %s' % save_location
    else:
        print 'There was an error locating the background image to download'
