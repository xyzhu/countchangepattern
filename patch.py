#!/usr/bin/env python

import os,re,string
from hunk import split_patch_to_hunk, get_num_hunk_from_patch
from statementcount import count_statement

def get_num_hunk(cursor,db,start_time,end_time,repo_id,buggy,file_path):
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
    num_hunk = 0
    for i in range(0, len(patches)):
        patch = patches[i][0]
        num_hunk += get_num_hunk_from_patch(patch,file_path)
    return num_hunk
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
    pattern = [ [0 for i in range(0,19)] for j in range(0,19)]
    #if n(n>1) of s statement changed in a patch, result_num should add n while result_time should add 1
    result_num = [0 for i in range(0,19)]
    result_time = [0 for i in range(0,19)]
    r = [0 for i in range(0,18)]
    result = [0 for i in range(0,19)]
    num_hunk = 0
    for i in range(0, len(patches)):
        patch = patches[i][0]
        num_assignment = count_assignment(patch)
        num_hunk = split_patch_to_hunk(patch,file_path)
        r = count_statement(file_path,num_hunk)
        for j in range(0,18):
            result[j] = r[j]
        result[18] = num_assignment
        for j in range(0,19):
            if result[j]!=0:
                    result_num[j] += result[j]
                    result_time[j] += 1
        pattern = mine_pattern(result, pattern)
    save_result(result_num,result_time,file_path,repo_id,num_hunk,pattern,start_time)

def count_assignment(patch):
    num_assign = 0
    patch_split = re.split("\n",patch)
    leng = len(patch_split)
    for i in range(0,leng):
        patch_line = patch_split[i]
        if (patch_line.startswith("+") or patch_line.startswith("-")) and (patch_line.startswith("+++")==False and patch_line.startswith("---")==False):
            num_assign += string.count(patch_line,"=") - string.count(patch_line,"==")*2 - string.count(patch_line,"!=") - string.count(patch_line,">=") - string.count(patch_line,"<=") - string.count(patch_line,"?=")
    return num_assign

def save_result(result_num,result_time,file_path,repo_id,num_hunk,pattern,start_time):
    s_num = start_time+","
    s_time = start_time+","
    p = ""
    for i in range(0,19):
        s_num += str(result_num[i])+","
        s_time += str(result_time[i])+","
        for j in range(0,19):
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
def mine_pattern(result,pattern):
    for i in range(0,19):
        if result[i] != 0:
            for j in range(i+1,19):
                if result[j] != 0:
                    pattern[i][j] = pattern[i][j]+1
    return pattern