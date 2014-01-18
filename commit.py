#! /usr/local/env python

import urllib
import urllib2
import time
url = 'http://localhost:8080/danmu/commit/'

for i in range (1,100000):
	url_t = url + str(i)
	print url_t

	values = {'obs_year':'2011','obs_month':'March',
	                                       'obs_day':'8','start_year':'2011'
	                                       ,'start_month':'March','start_day':'8'
	                                       ,'start_hour':'All Hours','stop_year':'2011'
	                                       ,'stop_month':'March','stop_day':'8'
	                                       ,'stop_hour':'All Hours','xsize':'All'
	                                       ,'ysize':'All','wave':'all'
	                                       ,'filter':'all','object':'all'
	                                       ,'xbin':'all','ybin':'all'
	                                       ,'highc':'all'}
	data = urllib.urlencode(values)
	print data
	req = urllib2.Request(url_t, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	print the_page
	#time.sleep(1)