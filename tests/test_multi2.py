#! /usr/bin/env python
# vi:ts=4:et
# $Id: test_multi2.py,v 1.9 2003/01/21 16:36:59 mfx Exp $

import os, sys, time
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import pycurl


urls = (
    "http://curl.haxx.se",
    "http://www.python.org",
    "http://pycurl.sourceforge.net",
    "http://pycurl.sourceforge.net/tests/403_FORBIDDEN",  # that actually exists ;-)
    "http://pycurl.sourceforge.net/tests/404_NOT_FOUND",
)

# Read list of URIs from file specified on commandline
try:
    urls = open(sys.argv[1], "rb").readlines()
except IndexError:
    # No file was specified
    pass

# init
m = pycurl.CurlMulti()
m.handles = []
for url in urls:
    c = pycurl.Curl()
    # save info in standard Python attributes
    c.url = url
    c.body = StringIO()
    c.http_code = -1
    m.handles.append(c)
    # pycurl API calls
    c.setopt(c.URL, c.url)
    c.setopt(c.WRITEFUNCTION, c.body.write)
    m.add_handle(c)

# get data
while 1:
    ret, num_handles = m.perform()
    if num_handles == 0:
        break
    # currently no more I/O is pending, could do something in the meantime
    # (display a progress bar, etc.)
    time.sleep(0.01)

# close handles
for c in m.handles:
    # save info in standard Python attributes
    c.http_code = c.getinfo(c.HTTP_CODE)
    # pycurl API calls
    m.remove_handle(c)
    c.close()
m.close()

# print result
for c in m.handles:
    data = c.body.getvalue()
    if 0:
        print "**********", c.url, "**********"
        print data
    else:
        print "%-53s http_code %3d, %6d bytes" % (c.url, c.http_code, len(data))

