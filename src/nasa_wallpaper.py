'''
Created on Jan 9, 2013

@author: Mike
'''

#POD = Picture of the Day

import sys
import urllib2
from datetime import datetime
from MemHTMLParser import MemHTMLParser

WEBSITE_URL = 'http://apod.nasa.gov/apod'

if __name__ == '__main__':
    save_location_folder = None
    target_date = None
    
    if len(sys.argv) > 1:
        # Parse any arguments passed
        i = 1
        while i < len(sys.argv):
            
            if sys.argv[i] == '--date':
                # Allow user to specify the date of the pod to download
                i = i + 1
                target_date = datetime.strptime(sys.argv[i], '%d/%m/%y')
            if sys.argv[i] == '--folder':
                # Allow the user to specify the folder to save to
                i = i + 1
                save_location_folder = sys.argv[i]
        
            i = i + 1
        
    # If a target date hasn't been specified, assign a default one
    if target_date is None:
        target_date = datetime.now()

    filename = target_date.strftime('%d%m%y')

    # If a save location hasn't been specified, assign a default one
    if save_location_folder is None:
        save_location_img = filename + '.jpg'
        save_location_info = filename + '.txt'
    else:
        save_location_img = '%s/%s.jpg' % (save_location_folder, filename)
        save_location_info = '%s/%s.txt' % (save_location_folder, filename)
    
    print 'target date = %s' % target_date
    target_url = '%s/ap%s.html' % (WEBSITE_URL, target_date.strftime('%y%m%d'))

    # BEGIN HTML REQUESTS AND IMAGE DOWNLOADING

    print 'requesting %s' % target_url
    url = urllib2.urlopen(target_url)
    html_data = url.read()
     
    print 'parsing HTML information'
    parser = MemHTMLParser()
    parser.feed(html_data)
    
    # Try find the Explanation node in order to display to the user
    expl_list = [node for node in parser.nodes['b'] if ' Explanation: ' in node.children]
    
    if expl_list:
        info_file = open(save_location_info, 'w')
        info_file.write(expl_list[0].parent.get_data())
        info_file.close()
    
    if 'img' in parser.nodes:
        image = parser.nodes['img'][0]
        
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
