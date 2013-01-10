__author__ = 'michaela'

from MemHTMLParser import MemHTMLParser
import urllib2
import argparse
import random
import sys

MAX = 3000
MAX_ATTEMPTS = 10

WEBSITE_URL = 'http://xkcd.com/'

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Download XKCD Comics over command line")
    parser.add_argument('-f', '--file', type=str, required=True, help="Specify the filename to save to")
    parser.add_argument('-c', '--comic-id', type=int, required=False, help="Specify a specific comic to download by id")
    parser.add_argument('-r', '--random', action="store_true", required=False, help="Download a random comic from XKCD")
    parser.add_argument('-i', '--info', type=str, required=False, help="Save the alternate text to a user-specified text file")
    
    args = parser.parse_args()
    
    retry = True
    attempts = 0
    
    while retry and attempts < MAX_ATTEMPTS:
        try:
            retry = False
        
            if args.comic_id:
                target_url = '%s%s' % (WEBSITE_URL, args.comic_id)
            elif args.random:
                random_id = random.randint(1,MAX)
                target_url = '%s%s' % (WEBSITE_URL, random_id)
            else:
                target_url = WEBSITE_URL
                
            save_location_img = args.file
        
            print 'requesting %s' % target_url
            url = urllib2.urlopen(target_url)
        except urllib2.URLError:
            retry = True
            attempts += 1
    
    # Unable to download HTML file; print error and exit
    if attempts == MAX_ATTEMPTS:
        print 'Unable to download comic of the day from XKCD'
        sys.exit()

    print 'parsing HTML information'
    parser = MemHTMLParser()
    parser.feed(url.read())

    # Traverse the HTML in an EXPECTED format
    if 'div' in parser.nodes:
        filtered_divs = [node for node in parser.nodes['div'] if 'id' in node.attributes and node.attributes['id']=='comic']

        if len(filtered_divs) > 0:
            # Get the Image URL
            img_tag = filtered_divs[0].children[0]
            img_url = img_tag.attributes['src']
            alt_text = img_tag.attributes['alt']
            title_text = img_tag.attributes['title']
            
            request = urllib2.urlopen(img_url)

            print 'downloading %s (%s bytes)' % (img_url, request.headers['Content-Length'])

            image_file = open(save_location_img,'wb')
            image_file.write(request.read())
            image_file.close()
            
            # Show the Comics alternate text
            info = '\'%s\': %s' % (alt_text, title_text)
            print info
            if args.info:
                info_file = open(args.info, 'w')
                info_file.write(info)
                info_file.close()

            print 'Successfully downloaded and saved the Picture of the Day to %s' % save_location_img
    else:
        print 'There was an error locating the image to download (Unexpected format)'
