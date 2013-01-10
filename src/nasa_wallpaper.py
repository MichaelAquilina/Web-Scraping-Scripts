"""
Simple Python Script that provides a command line interface for downloading NASA's Picture of the Day (POD).
"""

__author__ = 'Michael Aquilina'

from MemHTMLParser import MemHTMLParser
from datetime import datetime
import urllib2
import argparse
import random
import sys

MAX = 3000
MAX_ATTEMPTS = 10

WEBSITE_URL = 'http://apod.nasa.gov/apod'

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Download NASAs Astronomy Pictures of the Day over command line")
    parser.add_argument('-f', '--file', type=str, required=True, help="Specify the filename to save to")
    parser.add_argument('-c', '--date', type=str, required=False, help="Specify a specific day to download an image")
    parser.add_argument('-r', '--random', action="store_true", required=False, help="Download a random comic from XKCD")
    parser.add_argument('-i', '--info', type=str, required=False, help="Save the information text to a user-specified text file")
    
    args = parser.parse_args()
    
    retry = True
    attempts = 0
    
    while retry and attempts < MAX_ATTEMPTS:
        try:
            retry = False
        
            if args.date:
                dateid = datetime.strptime(args.date, '%d/%m/%y')
                target_url = '%s/ap%s.html' % (WEBSITE_URL, dateid.strftime('%y%m%d'))
            elif args.random:
                random_id = random.randint(1,MAX)
                target_url = '%s/ap%s.html' % (WEBSITE_URL, random_id)
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
        print 'Unable to download POD from NASA'
        sys.exit()

    print 'parsing HTML information'
    parser = MemHTMLParser()
    parser.feed(url.read())

    # Traverse the HTML in an EXPECTED format
    if 'img' in parser.nodes:

        # Get the Image URL
        anchor_tag = parser.nodes['img'][0].parent
        img_url = '%s/%s' % (WEBSITE_URL, anchor_tag.attributes['href'])
        
        request = urllib2.urlopen(img_url)

        print 'downloading %s (%s bytes)' % (img_url, request.headers['Content-Length'])

        image_file = open(save_location_img,'wb')
        image_file.write(request.read())
        image_file.close()
        
        if args.info:
            # Try find the Explanation node in order to display to the user
            expl_list = [node for node in parser.nodes['b'] if ' Explanation: ' in node.children]
            
            if expl_list:
                info_file = open(args.info, 'w')
                info_file.write(expl_list[0].parent.get_data())
                info_file.close()

        print 'Successfully downloaded and saved the NASA POD to %s' % save_location_img
    else:
        print 'There was an error locating the image to download (Unexpected format)'
