#!/usr/bin/python2
# *-* coding: utf-8 *-*

import MySQLdb
import MySQLdb.cursors
import debug
import sys
import time
import yaml

conf = open("/etc/grantha/grantha.conf","r")
confDict = yaml.safe_load(conf)

host = "blues2"
database = "INVENTORY"

class dbGrantha:

    def __init__(self):
        self.__conn = None

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        try:
            self.__conn.close()
            debug.info("Database connection closed")
        except:
            debug.info(str(sys.exc_info()))

    def _connInventory(self):
        while(1):
            try:
                conn = MySQLdb.connect(host=host,db=database)
                conn.autocommit(1)
                debug.info("Database connected")
                return(conn)
            except:
                debug.info("Database not connected: "+ str(sys.exc_info()))
            time.sleep(1)

    def execute(self,query,dictionary=False):
        while(1):
            try:
                self.__conn = self._connInventory()
                if(dictionary):
                    cur = self.__conn.cursor(MySQLdb.cursors.DictCursor)
                else:
                    cur = self.__conn.cursor()
                debug.info(query)
                cur.execute(query)
                if (dictionary):
                    try:
                        rows = cur.fetchall()
                    except:
                        debug.info("Fetching failed: "+ str(sys.exc_info()))
                    cur.close()
                    self.disconnect()
                    if(rows):
                        return (rows)
                    else:
                        return (0)
                else:
                    cur.close()
                    self.disconnect()
                    return (1)
            except:
                debug.info("Failed query : " + str(query) + " : " + str(sys.exc_info()))
                if (str(sys.exc_info()).find("Can't connect to MySQL") >= 0):
                    time.sleep(1)
                    try:
                        cur.close()
                    except:
                        pass
                    self.disconnect()
                    self.__conn = self._connInventory()
                    continue
                if (str(sys.exc_info()).find("Duplicate entry") >= 0):
                    try:
                        cur.close()
                    except:
                        pass
                    self.disconnect()
                    return(str(sys.exc_info()))
                if (str(sys.exc_info()).find("foreign key constraint fails") >= 0):
                    try:
                        cur.close()
                    except:
                        pass
                    self.disconnect()
                    return(str(sys.exc_info()))
                else:
                    try:
                        cur.close()
                    except:
                        pass
                    self.disconnect()
                    raise

