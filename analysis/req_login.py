#!/usr/bin/python
# -*- coding: utf8 -*-

import requests

params = {'firstname': 'feng', 'lastname': 'wei'}
r = requests.post('http://pythonscraping.com/files/processing.php', data=params)
print(r.text)

