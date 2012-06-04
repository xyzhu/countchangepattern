#!/usr/bin/env python

# Copyright (C) 2011 XiaoyanZhu
# Authors : Xiaoyan Zhu <xyxyzh@gmail.com>

import os,re
import string


def count_statement(file_path,num_hunk):
    r = [0 for i in range(0,19)]
    statements = ["call","if","for","while","do","switch","case","continue",
                 "break","return","else","function","function_decl","decl_stmt",
                 "constructor","try","catch","throw"]
    diff = hunk_source_to_xml(file_path,num_hunk)
    leng = len(statements)
    for i in range(0,leng):
        statement = statements[i]
        r[i] = string.count(diff,"<"+statement+">") + string.count(diff,"/"+statement+"[")
    r[18] = count_assignment(file_path,num_hunk)
    return r

def hunk_source_to_xml(file_path,num_hunk):
    diff = ""
    for i in range(1,num_hunk):
        file_name = file_path + str(i)
        os.system(file_path+"src2srcml -l Java "+file_name+"_old.java -o "+file_name+"_old.xml")
        os.system(file_path+"src2srcml -l Java "+file_name+"_new.java -o "+file_name+"_new.xml")
        diff += compare_xml(file_name)
    return diff
def compare_xml(file_name):
    diff = os.popen("xmldiff "+file_name+"_old.xml "+file_name+"_new.xml").read()
    return diff

def count_assignment(file_path,num_hunk):
    num_assign = 0
    for i in range(1,num_hunk):
        file_name = file_path +str(i)
        diff = os.popen("diff "+file_name+"_old.java "+file_name+"_new.java").read()
        diff_lines = re.split("\n",diff)
        leng = len(diff_lines)
        line_number = 0
        countnew = True
        while line_number<leng-1:
            one_diff = diff_lines[line_number]
            if "c" in one_diff or "d" in one_diff:
                countnew = False
            line_number = line_number+1
            if countnew == True:
                while line_number<leng-1:
                    if diff_lines[line_number].startswith(">"):
                        one_diff += diff_lines[line_number]
                        line_number = line_number+1
                    else:
                        break
            else:
                while line_number<leng-1:
                    if diff_lines[line_number].startswith("<"):
                        one_diff += diff_lines[line_number]
                        line_number = line_number+1
                    else:
                        break
            num_assign += string.count(one_diff,"=")
    return num_assign