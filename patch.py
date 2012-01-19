#!/usr/bin/env python

import os
from hunk import split_patch_to_hunk
from statementcount import count_statement

def extract_patch(cursor,db,start_time,end_time,repo_id,buggy,file_path):
    if buggy:
        query = """select patch from patches,scmlog,files where patches.commit_id 
                 = scmlog.id and scmlog.commit_date >= ? and scmlog.commit_date < ?
                and scmlog.repository_id=? and patches.file_id=files.id and 
                file_name like ? and is_bug_fix=1;"""
    else:
        query = """select patch from patches,scmlog,files where patches.commit_id 
                = scmlog.id and scmlog.commit_date >= ? and scmlog.commit_date < ?
                and scmlog.repository_id=? and patches.file_id=files.id and 
                file_name like ?;"""
    db.execute_statement_with_param(query, (start_time, end_time, repo_id, "%.java"), cursor)
    patches = cursor.fetchall()
    pattern = [ [0 for i in range(0,18)] for j in range(0,18)]
    #if n(n>1) of s statement changed in a patch, result_num should add n while result_time should add 1
    result_num = [0 for i in range(0,18)]
    result_time = [0 for i in range(0,18)]
    r = [0 for i in range(0,18)]
    num_hunk = 0
    for i in range(0, len(patches)):
        patch = patches[i][0]
        num_hunk = split_patch_to_hunk(patch,file_path)
        r = count_statement(file_path,num_hunk)
        for j in range(0,18):
            if r[j]!=0:
                    result_num[j] += r[j]
                    result_time[j] += 1
        pattern = mine_pattern(r, pattern)
    save_result(result_num,result_time,file_path,repo_id,num_hunk,pattern,start_time)

def save_result(result_num,result_time,file_path,repo_id,num_hunk,pattern,start_time):
    s_num = start_time+","
    s_time = start_time+","
    p = ""
    for i in range(0,18):
        s_num += str(result_num[i])+","
        s_time += str(result_time[i])+","
        for j in range(0,18):
            p += str(pattern[i][j])+","
        p += "\n"
    f = open(file_path+"project_"+repo_id+"_num.csv",'a',)
    f.write(s_num+"\n")
    f.close
    f = open(file_path+"project_"+repo_id+"_time.csv",'a',)
    f.write(s_time+"\n")
    f.close
    f = open(file_path+"project_"+repo_id+"_pattern_"+start_time+".csv",'a')
    f.write(p)
    f.close()
    if num_hunk:
        os.system("rm "+file_path+"*.java")
        os.system("rm "+file_path+"*.xml")
def mine_pattern(r,pattern):
    for i in range(0,18):
        if r[i] != 0:
            for j in range(i+1,18):
                if r[j] != 0:
                    pattern[i][j] = pattern[i][j]+1
    return pattern