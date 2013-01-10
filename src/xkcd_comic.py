__author__ = 'michaela'

from MemHTMLParser import MemHTMLParser
import urllib2

WEBSITE_URL = 'http://xkcd.com/'

if __name__ == '__main__':
    target_url = WEBSITE_URL
    save_location_img = 'xkcd.jpg'

    print 'requesting %s' % target_url
    url = urllib2.urlopen(target_url)
    html_data = url.read()

    print 'parsing HTML information'
    parser = MemHTMLParser()
    parser.feed(html_data)

    if 'div' in parser.nodes:
        filtered_divs = [node for node in parser.nodes['div'] if 'id' in node.attributes and node.attributes['id']=='comic']

        if len(filtered_divs) > 0:
            # Get the Image URL
            image_url = '%s' % (filtered_divs[0].children[0].attributes['src'])
            request = urllib2.urlopen(image_url)

            print 'downloading %s (%s bytes)' % (image_url, request.headers['Content-Length'])

            image_file = open(save_location_img,'wb')
            image_file.write(request.read())
            image_file.close()

            print 'Successfully downloaded the Picture of the Day to %s' % save_location_img
    else:
        print 'There was an error locating the background image to download'