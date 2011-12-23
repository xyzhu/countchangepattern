#!/usr/bin/env python

# Copyright (C) 2011 XiaoyanZhu
# Authors : Xiaoyan Zhu <xyxyzh@gmail.com>


import getopt
from Database import *
from hunkcontent import parse_patch_content
from exporthunk import save_change_to_file

def main(argv):
    # Short (one letter) options. Those requiring argument followed by :
    short_opts = "nu:p:d:s:e:"
    # Long options (all started by --). Those requiring argument followed by =
    long_opts = ["no-parse", "db-user=", "db-password=",  "db-database=", "start-time=", "end-time"]

    # Default options
    user = None
    passwd = None
    database = None
    no_parse = None
    start_time = None
    end_time = None

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
        elif opt in ("-n"):
            no_parse = True
        elif opt in("-s", "--start-time"):
            start_time = value
        elif opt in("-e","--end-time"):
            end_time = value
    
    try:
        db = Database(user, passwd, database)
        cnn = db.connect()
        cursor = cnn.cursor()
        if not no_parse:
            db.create_tables(cursor)
            query = """select commit_id, patch from patches;"""
            db.execute_statement(query, cursor)
            result = cursor.fetchall()
            for i in range(0, len(result)):
                commit_id = result[i][0]
                patch_content = result[i][1]
                parse_patch_content(commit_id, patch_content, db, cursor)
        save_change_to_file(db, cursor, start_time, end_time)
        print("Finished")
        cnn.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])

