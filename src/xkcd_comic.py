__author__ = 'michaela'

from MemHTMLParser import MemHTMLParser
import urllib2
import argparse

WEBSITE_URL = 'http://xkcd.com/'

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Download XKCD Comics over command line")
    parser.add_argument('-f', '--file', type=str, required=True, help="Specify the filename to save to")
    parser.add_argument('-c', '--comic-id', type=int, required=False, help="Specify a specific comic to download by id")
    
    args = parser.parse_args()
    
    if args.comic_id:
        target_url = '%s%s' % (WEBSITE_URL, args.comic_id)
    else:
        target_url = WEBSITE_URL
        
    save_location_img = args.file

    print 'requesting %s' % target_url
    url = urllib2.urlopen(target_url)

    print 'parsing HTML information'
    parser = MemHTMLParser()
    parser.feed(url.read())

    # Traverse the HTML in an EXPECTED format
    if 'div' in parser.nodes:
        filtered_divs = [node for node in parser.nodes['div'] if 'id' in node.attributes and node.attributes['id']=='comic']

        if len(filtered_divs) > 0:
            # Get the Image URL
            image_url = filtered_divs[0].children[0].attributes['src']
            request = urllib2.urlopen(image_url)

            print 'downloading %s (%s bytes)' % (image_url, request.headers['Content-Length'])

            image_file = open(save_location_img,'wb')
            image_file.write(request.read())
            image_file.close()

            print 'Successfully downloaded the Picture of the Day to %s' % save_location_img
    else:
        print 'There was an error locating the image to download (Unexpected format)'
