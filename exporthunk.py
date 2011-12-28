#!/usr/bin/env python

# Copyright (C) 2011 XiaoyanZhu
# Authors : Xiaoyan Zhu <xyxyzh@gmail.com>


def save_change_to_file(hunk, old_hunk, new_hunk, m):
    f = open("/home/xyzhu/change-pattern/source/"+str(m)+".java",'w+',)
    f.write(str(hunk))
    f.close()
    f = open("/home/xyzhu/change-pattern/source/"+str(m)+"_old.java",'w+',)
    f.write(str(old_hunk))
    f.close()
    f = open("/home/xyzhu/change-pattern/source/"+str(m)+"_new.java",'w+',)
    f.write(str(new_hunk))
    f.close()
    return m+1

    