#!/usr/bin/env python

# Copyright (C) 2011 XiaoyanZhu
# Authors : Xiaoyan Zhu <xyxyzh@gmail.com>


import getopt
from Database import *
from hunkcontent import parse_patch_content
from exporthunk import save_change_to_file

def main(argv):
    # Short (one letter) options. Those requiring argument followed by :
    short_opts = "u:p:d:r:s:e:"
    # Long options (all started by --). Those requiring argument followed by =
    long_opts = ["db-user=", "db-password=",  "db-database=", "repository-id=", "start-time=", "end-time"]

    # Default options
    user = None
    passwd = None
    database = None
    repo_id=None
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
        elif opt in("-r", "--repository-id"):
            repo_id = value
        elif opt in("-s", "--start-time"):
            start_time = value
        elif opt in("-e","--end-time"):
            end_time = value
    
    try:
        db = Database(user, passwd, database)
        cnn = db.connect()
        cursor = cnn.cursor()
        query = """select patch from patches,scmlog,files where patches.commit_id 
                = scmlog.id and scmlog.commit_date >= ? and scmlog.commit_date < ?
                and scmlog.repository_id=? and patches.file_id=files.id and 
                file_name like ? and scmlog.is_bug_fix=1;"""
        db.execute_statement_with_param(query, (start_time, end_time, repo_id, "%.java"), cursor)
        result = cursor.fetchall()
        for i in range(0, len(result)):
            patch_content = result[i][0]
            parse_patch_content(patch_content, i)
        #save_change_to_file(db, cursor, start_time, end_time)
        print("Finished save to files.")
        cnn.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])

