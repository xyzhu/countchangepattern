#!/usr/bin/env python

# Copyright (C) 2011 XiaoyanZhu
# Authors : Xiaoyan Zhu <xyxyzh@gmail.com>

import os
import string


def count_statement(file_path,num_hunk):
    r = [0 for i in range(0,18)]
    statements = ["call","if","for","while","do","switch","case","continue",
                 "break","return","else","function","function_del","decl_stmt",
                 "constructor","try","catch","throw"]
    diff = hunk_source_to_xml(file_path,num_hunk)
    leng = len(statements)
    for i in range(0,leng):
        statement = statements[i]
        r[i] = string.count(diff,"<"+statement+">") + string.count(diff,"/"+statement+"[")
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
    