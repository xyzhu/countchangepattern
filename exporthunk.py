#!/usr/bin/env python

# Copyright (C) 2011 XiaoyanZhu
# Authors : Xiaoyan Zhu <xyxyzh@gmail.com>


def save_change_to_file(db, cursor, start_time, end_time):
    if not start_time:
        query = """select content, old_content, new_content from hunk_content;"""
        db.execute_statement(query, cursor)
    else:
        query = """select content, old_content, new_content from hunk_content, scmlog where 
                hunk_content.commit_id = scmlog.id and scmlog.commit_date >= ? and scmlog.commit_date < ?;"""
        db.execute_statement_with_param(query,(start_time, end_time), cursor)
    result = cursor.fetchall()
    old_content = ""
    new_content = ""
    for i in range(0, len(result)-1):
        content  = result[i][0]
        old_content = result[i][1]
        new_content = result[i][2]
        f = open("/home/xyzhu/change-pattern/source/"+str(i)+".java",'w+',)
        f.write(str(content))
        f.close()
        f = open("/home/xyzhu/change-pattern/source/"+str(i)+"_old.java",'w+',)
        f.write(str(old_content))
        f.close()
        f = open("/home/xyzhu/change-pattern/source/"+str(i)+"_new.java",'w+',)
        f.write(str(new_content))
        f.close()

    