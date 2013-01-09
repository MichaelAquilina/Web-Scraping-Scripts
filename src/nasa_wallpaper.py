'''
Created on Jan 9, 2013

@author: Mike
'''

#POD = Picture of the Day

import sys
import urllib2
from datetime import datetime
from HTMLParser import HTMLParser

WEBSITE_URL = 'http://apod.nasa.gov/apod'

def get_data(html_node):
    """
    Retrieves and extracts the string data contained in the
    HTML node passed in the parameter. The process is recursive
    so the entire string data will be returned.
    """
    data = _extract_data(html_node)
    
    str_buffer = ''
    for item in data:
        str_buffer += item
        
    return str_buffer

def _extract_data(html_node, data=[]):
    for child in html_node.children:
        if type(child) == str:
            data.append(child
                        .replace('\n',' ')      # Remove all occurrances of new lines
                        .strip()                # Remove white spaces at the end
                        .lstrip()               # Remove white spaces at the front
                        )
        else:
            data.append(' ')
            _extract_data(child, data)
            data.append(' ')
            
    return data

class HTMLNode(object):
    """
    Class representation of an HTML Node that would be found in a
    typical HTML file.
    """
    
    def __init__(self, tag, pos=-1):
        self.tag = tag
        self.children = []
        self.attributes = {}
        self.parent = None
        self.pos = pos
        
    def __repr__(self):
        return '<{tag}: Attributes={attributes}, Pos={pos}>'.format(
            tag=self.tag,
            pos=self.pos,
            attributes=len(self.attributes))

class MemHTMLParser(HTMLParser):
    """
    Builds an in-memory representation of a given HTML file through the use of
    HTMLNode objects that are easily accessible through the nodes instance variable.
    The structure built by this class assumes XML compliance (TODO: allow non-XML)
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
            
        # Push the new node on the top of the stack for tracking
        self._node_stack.append(node)
    
    def handle_data(self, data):
        self._peek_stack().children.append(data)
    
    def handle_endtag(self, tag):
        # The node is no longer in context
        self._node_stack.pop()

if __name__ == '__main__':
    save_location_img = None
    save_location_info = None
    target_date = None
    
    if len(sys.argv) > 1:
        # Parse any arguments passed
        i = 1
        while i < len(sys.argv):
            
            if sys.argv[i] == '--date':
                # Allow user to specify the date of the pod to download
                i = i + 1
                target_date = datetime.strptime(sys.argv[i], '%d/%m/%y')
            if sys.argv[i] == '--file':
                # Allow the user to specify the file to save to
                i = i + 1
                save_location_img = sys.argv[i]
        
            i = i + 1
        
    # If a target date hasn't been specified, assign a default one
    if target_date is None:
        target_date = datetime.now()
    
    print 'target date = %s' % target_date
    target_url = '%s/ap%s.html' % (WEBSITE_URL, target_date.strftime('%y%m%d'))
    
    print 'requesting %s' % target_url
    url = urllib2.urlopen(target_url)
    html_data = url.read()
     
    print 'parsing HTML information'
    parser = MemHTMLParser()
    parser.feed(html_data)
    
    # Try find the Explanation node in order to display to the user
    expl_list = [node for node in parser.nodes['b'] if ' Explanation: ' in node.children]
    
    if expl_list:
        print get_data(expl_list[0].parent)
    
    if 'img' in parser.nodes:
        image = parser.nodes['img'][0]
        
        # If a save location hasn't been specified, assign a default one
        if save_location_img is None:
            save_location_img = target_date.strftime('%d%m%y.jpg')
        
        # Get the High Resolution Image URL
        image_url = '%s/%s' % (WEBSITE_URL, image.parent.attributes['href'])
        request = urllib2.urlopen(image_url)
        
        print 'downloading %s (%s bytes)' % (image_url, request.headers['Content-Length'])
        
        image_file = open(save_location_img,'wb')
        image_file.write(request.read())
        image_file.close()
        
        print 'Successfully downloaded the Picture of the Day to %s' % save_location_img
    else:
        print 'There was an error locating the background image to download'
