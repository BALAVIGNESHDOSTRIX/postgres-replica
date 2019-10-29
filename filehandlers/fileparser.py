#!/usr/bin/env python
# encoding: utf-8
import os 

class FileHandler:

    def ConfigLineAppender(self, line, file):
        with open(file,'a') as writer:
            writer.write(line + '\n')
            return True 
    
    def ReturnConfigLines(self, files):
        temp = []
        all_lines = open(files).readlines()
        for line in all_lines:
            temp.append(line.rstrip('\n'))
        if temp:
            return temp
