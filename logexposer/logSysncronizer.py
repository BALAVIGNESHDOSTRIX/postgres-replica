#!/usr/bin/env python
# encoding: utf-8

class LogMaintainer:
    def MessageCatcher(self, mess, sysmess=None):
        print(" ")
        if sysmess != None:
            print(mess, sysmess)
        else:
            print(mess)

    def FormalMessageCatcher(self, mess, dots,sysmess=None):
        print(mess, dots, sysmess)
        
        
