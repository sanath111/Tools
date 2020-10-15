#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os

machine = ({'hostname': "blue0012", 'ip': "192.168.1.21", 'mac': "9c:5c:8e:85:19:d9"},
           {'hostname': "blue0025", 'ip': "192.168.1.33", 'mac': "70:4d:7b:62:89:31"},
           {'hostname': "blue0034", 'ip': "192.168.1.43", 'mac': "e0:d5:5e:32:af:14"})

# {'hostname': "blue0032", 'ip': "192.168.1.41", 'mac': "1c:1b:0d:d5:7b:6c"},

for x in machine:
    cmd = "/opt/rbhus/rbhus/WOL.py " + x['mac'] + " -i " + x['ip']
    os.system(cmd)

