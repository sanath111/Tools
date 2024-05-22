#!/bin/bash

upnpc -a 192.168.1.39 22 9092 tcp
upnpc -a 192.168.1.175 22 9090 tcp
upnpc -a 192.168.1.174 4501 9094 tcp
upnpc -l
