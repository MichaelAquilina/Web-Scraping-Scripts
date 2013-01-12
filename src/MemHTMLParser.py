from HTMLParser import HTMLParser

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

    def get_data(self):
        """
        Retrieves and extracts the string data contained in the
        HTML node passed in the parameter. The process is recursive
        so the entire string data will be returned.
        """
        data = self._extract_data()

        str_buffer = ''
        for item in data:
            str_buffer += item

        return str_buffer

    def _extract_data(self, data=[]):
        """
        Recursive function that traverses all child nodes in a Depth-First
        manner in order to retrieve all the content found in the the html tags.
        Uses the 'data' list parameter as a buffer for storing found content.
        """
        for child in self.children:
            if type(child) == str:
                lines = child.split('\n')
                for line in lines:
                    fmt_line = line
                    if fmt_line:
                        data.append(fmt_line)      
            else:
                child._extract_data(data)
                
        return data
        
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
        if len(self._node_stack) > 0:
            return self._node_stack[len(self._node_stack)-1]
        else:
            return None

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
        topnode = self._peek_stack()

        # Only add the data if it has actual content other than only whitespace
        if topnode and data.strip():
            topnode.children.append(data)
    
    def handle_endtag(self, tag):
        # The node is no longer in context
        self._node_stack.pop()
