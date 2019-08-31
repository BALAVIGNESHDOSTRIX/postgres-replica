#!/usr/bin/env python
# encoding: utf-8

class ConfigInspector:
    _ErrorStr = {
        'ipfalse': "IN VALID IP ADDRESS",
        'passfalse': "IN VALID CREDINTIALS",
        'sshfalse': "SSH Connection Failed"
    }

    @classmethod
    def ReturnIPErr(self):
        return self._ErrorStr.get('ipfalse')

    @classmethod
    def ReturnPassErr(self):
        return self._ErrorStr.get('passfalse')

    @classmethod
    def ReturnSSHErr(self):
        return self._ErrorStr.get('sshfalse')
