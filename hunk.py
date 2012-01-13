#!/usr/bin/env python

# Copyright (C) 2011 XiaoyanZhu
# Authors : Xiaoyan Zhu <xyxyzh@gmail.com>

import re

def split_patch_to_hunk(patch,file_path):
    patch_split = re.split("@@.*@@", patch)
    num_hunk = len(patch_split)
    for i in range(1,num_hunk): 
        hunk = patch_split[i]
        old_hunk = re.sub('(?<=\n)\+.*\n','',hunk)
        old_hunk = re.sub("\n\-","\n ",old_hunk)
        new_hunk = re.sub('(?<=\n)\-.*\n','',hunk)
        new_hunk = re.sub("\n\+","\n ",new_hunk)
        save_hunk_to_file(hunk, old_hunk, new_hunk, file_path, i)
    return num_hunk
        
def save_hunk_to_file(hunk, old_hunk, new_hunk, file_path, i):
    #f = open(filepath+str(m)+".java",'w+',)
    #f.write(str(hunk))
    #f.close()
    file_name = file_path + str(i)
    f = open(file_name+"_old.java",'w+',)
    f.write(str(old_hunk))
    f.close()
    f = open(file_name+"_new.java",'w+',)
    f.write(str(new_hunk))
    f.close()