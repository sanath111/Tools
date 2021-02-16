#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os

machine = ({'hostname': "blue0020", 'ip': "192.168.1.28", 'mac': "34:97:f6:8d:8f:76"},
           {'hostname': "blue0025", 'ip': "192.168.1.33", 'mac': "70:4d:7b:62:89:31"},
           {'hostname': "blue0031", 'ip': "192.168.1.40", 'mac': "1c:1b:0d:d5:7a:94"},
           {'hostname': "blue0036", 'ip': "192.168.1.45", 'mac': "e0:d5:5e:32:af:df"},
           {'hostname': "blue0037", 'ip': "192.168.1.46", 'mac': "e0:d5:5e:30:48:36"})

# {'hostname': "blue0012", 'ip': "192.168.1.21", 'mac': "9c:5c:8e:85:19:d9"}
# {'hostname': "blue0016", 'ip': "192.168.1.24", 'mac': "34:97:f6:8d:8f:88"}
# {'hostname': "blue0032", 'ip': "192.168.1.41", 'mac': "1c:1b:0d:d5:7b:6c"}
# {'hostname': "blue0034", 'ip': "192.168.1.43", 'mac': "e0:d5:5e:32:af:14"}

for x in machine:
    cmd = "/opt/rbhus/rbhus/WOL.py " + x['mac'] + " -i " + x['ip']
    os.system(cmd)

