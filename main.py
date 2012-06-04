#!/usr/bin/env python

# Copyright (C) 2011 XiaoyanZhu
# Authors : Xiaoyan Zhu <xyxyzh@gmail.com>


import getopt
from Database import *
from patch import extract_patch, get_num_hunk

def main(argv):
    # Short (one letter) options. Those requiring argument followed by :
    short_opts = "u:p:d:r:s:e:bf:"
    # Long options (all started by --). Those requiring argument followed by =
    long_opts = ["db-user=", "db-password=",  "db-database=", "repository-id=", "start-time=", "end-time", "--buggy","--filepath"]

    # Default options
    user = None
    passwd = None
    database = None
    repo_id=None
    start_time = None
    end_time = None
    buggy = None
    file_path = None

    try:
        opts, args= getopt.getopt(argv, short_opts, long_opts)
    except getopt.GetoptError, e:
        print(str(e))
        return 1

    for opt, value in opts:
        if opt in("-u", "--db-user"):
            user = value
        elif opt in("-p", "--db-password"):
            passwd = value
        elif opt in("-d", "--db-database"):
            database = value
        elif opt in("-r", "--repository-id"):
            repo_id = value
        elif opt in("-s", "--start-time"):
            start_time = value
        elif opt in("-e","--end-time"):
            end_time = value
        elif opt in("-b","--buggy"):
            buggy = True
        elif opt in("-f","--filepath"):
            file_path = value
    
    try:
        db = Database(user, passwd, database)
        cnn = db.connect()
        cursor = cnn.cursor()
        extract_patch(cursor,db,start_time,end_time,repo_id,buggy,file_path)
        total_num_hunk = get_num_hunk(cursor,db,start_time,end_time,repo_id,buggy,file_path)
        cnn.close()
        print "Finish. Repository: "+ repo_id +", time: " + start_time+"-" +end_time+", bug: "+str(buggy) + ", Num_hunks: "+str(total_num_hunk)
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])

