#!/usr/bin/env python
# encoding: utf-8

def DeleteFile_C(file_dir):
    open(file_dir, 'w').close()
    return True
