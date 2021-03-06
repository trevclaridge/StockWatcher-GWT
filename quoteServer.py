#!/usr/bin/env python2.4
#
# Copyright 2007 Google Inc. All Rights Reserved.

import BaseHTTPServer
import SimpleHTTPServer
import urllib
import random

MAX_PRICE = 100.0
MAX_PRICE_CHANGE = 0.02

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

  def do_GET(self):
    form = {}
    if self.path.find('?') > -1:
      queryStr = self.path.split('?')[1]
      form = dict([queryParam.split('=') for queryParam in queryStr.split('&amp;')])

      body = '['

      if 'q' in form:
        quotes = []

        for symbol in urllib.unquote_plus(form['q']).split(' '):
          price = random.random() * MAX_PRICE
          change = price * MAX_PRICE_CHANGE * (random.random() * 2.0 - 1.0)
          quotes.append(('{"symbol":"%s","price":%f,"change":%f}'
                       % (symbol, price, change)))

        body += ','.join(quotes)

      body += ']'

      if 'callback' in form:
        body = ('%s(%s);' % (form['callback'], body))

    self.send_response(200)
    self.send_header('Content-Type', 'text/javascript')
    self.send_header('Content-Length', len(body))
    self.send_header('Expires', '-1')
    self.send_header('Cache-Control', 'no-cache')
    self.send_header('Pragma', 'no-cache')
    self.end_headers()

    self.wfile.write(body)
    self.wfile.flush()
    self.connection.shutdown(1)

bhs = BaseHTTPServer.HTTPServer(('', 8000), MyHandler)
bhs.serve_forever()