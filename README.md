Scripts
=======

A Random set of Python Scripts that can be used on various machines through
a command line interface. They provide the user with the ability to download
key items from various websites using web scraping techniques.

They can be run on any Windows, Linux or Mac machine with a Python interpreter

The following scripts can be found in the src folder:
* Cyanide and Happiness Comic Downloader
* XKCD Comic Downloader
* NASA Picture of the Day Image Downloader

They were originally created by me so that i could download and show the images in a linux program called conky at timed intervals, but they can be used for many other things too.
The two main scripts are xkcd_comic.py and nasa_wallpaper.py. The other script (MemHTMLParser.py) is an implementation of the HTMLParser class in python that stores html elements in memory for quick access and parsing.

The two files support the following command line switches when you run then:
* --random : download a random image
* --file: (Required) specify the filename to save the image to
* --date: (NASA only), specify a particular date to download
* --comicid: (XKCD only), specify a particular comic id to download
* --info: specify a text file to store extra text information about the image

NOTE: It has been suggested by various members of the reddit community that i could have also implemented
these scripts using the beautiful soup library (http://www.crummy.com/software/BeautifulSoup/). Thanks!
