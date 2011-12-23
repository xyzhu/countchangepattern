#!/usr/bin/env python

# Copyright (C) 2011 XiaoyanZhu
# Authors : Xiaoyan Zhu <xyxyzh@gmail.com>

import re

def save_hunk_to_database(commit_id, hunk, old_hunk, new_hunk, db, cursor):
    query = "insert into hunk_content(commit_id, content, old_content, new_content) values(?, ?, ?, ?)"
    db.execute_statement_with_param(query, (commit_id, hunk, old_hunk, new_hunk),cursor)
    
    
def parse_patch_content(commit_id, patch_content, db, cursor):
    patch_split = re.split("diff\s--git.*", patch_content)
    for i in range(1,len(patch_split)):
        file_patch = patch_split[i]
        if re.search("@@.*@@",file_patch)!=None:
            file_patch_split = re.split("@@.*@@", file_patch)
            hunk = file_patch_split[0]
            hunkline = hunk.split('\n')
            oldfile = None
            newfile = None
            for l in range(1, len(hunkline)):
                if hunkline[l].startswith("---"):
                    oldfile = hunkline[l]
                if hunkline[l].startswith("+++"):
                    newfile = hunkline[l]
            if oldfile.endswith(".java") or newfile.endswith(".java"):
                for j in range(1,len(file_patch_split)):
                    hunk = file_patch_split[j]  
#                    pattern = re.compile('|\n\+.*\n')
                    old_hunk = re.sub('(?<=\n)\+.*\n','',hunk)
                    old_hunk = re.sub("\n\-","\n ",old_hunk)
#                    pattern = re.compile("\n\-.*\n")
                    new_hunk = re.sub('(?<=\n)\-.*\n','',hunk)
                    new_hunk = re.sub("\n\+","\n ",new_hunk)
                    save_hunk_to_database(commit_id, hunk, old_hunk, new_hunk, db, cursor)
            
    