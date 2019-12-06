#!/usr/bin/python
# -*- coding: UTF-8 -*-
#将某个文件夹下的name@2x.png,name@3x.png文件移动到指定文件夹，移动的结果是在目的文件夹生成name.imageset文件夹，该文件夹内含有相应2倍，3倍图片(如果源路径有的话),并生成XCode可读取的Contents.json文件
#该脚本主要用于将资源自动移动到xcode
#调用方法: 首先修改该文件的权限chmod u+x batmvicon.py 然后batmvicon.py src dst,其中src是源图片文件夹路径，dst是xcode项目Assets.xcassets路径
import os

import shutil

import sys

import json
def list_all_files(rootdir):
    import os
    _files = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
              _files.append(path)
    return _files

def cp(src,dst):
    files = list_all_files(src)
    createdfolders = []
    for path in files:
        if path[-3:] == 'png':
            createdfolders.append(path)
    finaldst = ''
    if dst[-1:] == '/':
        finaldst = dst
    else:
        finaldst = dst + '/'
    dstfolders = []
    for path in createdfolders:
        filepath, fullflname = os.path.split(path)
        result = "@2x" in fullflname or "@3x" in fullflname;
        if result == True:
            foldername = fullflname[:-7]
            dstfold = finaldst + foldername + '.imageset'
            if dstfold not in dstfolders:
                dstfolders.append(dstfold)
            if os.path.exists(dstfold):
                shutil.copy(path, dstfold)
            else:
                os.makedirs(dstfold)
                shutil.copy(path, dstfold)
    for path in dstfolders:
        paths = list_all_files(path)
        files = []
        meta = {"info": {"version": 1, "author": "xcode"}}
        images = []
        for file in paths:
            filename = os.path.basename(file)
            if filename[-3:] == 'png':
                if filename[-6:-4] == '2x' or filename[-6:-4] == '3x':
                    image = {'idiom': 'universal','filename': filename, 'scale': filename[-6:-4]}
                    images.append(image)
                else:
                    image = {'idiom': 'universal', 'filename': filename, 'scale': '1x'}
                    images.append(image)
        meta['images'] = images
        str = json.dumps(meta)
        fd = open(path + '/Contents.json', 'w')
        fd.write(str)
        fd.close()

if __name__ == '__main__':
    params = sys.argv
    if len(params) == 0:
        print '请输入源地址与目的地址'
    elif len(params) == 1:
        print  '请输入源地址目的地址'
    elif len(params) == 3:
        src = params[1]
        dst = params[2]
        cp(src,dst)
    else:
        print '参数数目不正确'
