#!/usr/bin/env python
# encoding: utf-8

class SystemParameters:

    _sysinfos = ["NAME", "VERSION", "ID", "ID_LIKE", "VERSION_ID", "VERSION_CODENAME", "UBUNTU_CODENAME", "/etc/os-release"]

    @classmethod
    def getOSName(self):
        return self._sysinfos[0]

    @classmethod
    def getOSVersion(self):
        return self._sysinfos[1]

    @classmethod
    def getOS_ID(self):
        return self._sysinfos[2]

    @classmethod
    def getOS_Base(self):
        return self._sysinfos[3]

    @classmethod
    def getOS_VID(self):
        return self._sysinfos[4]

    @classmethod 
    def getOS_V_CODENAME(self):
        return self._sysinfos[5]

    @classmethod
    def getUBUNTU_CODENAME(self):
        return self._sysinfos[6]

    @classmethod
    def getOS_RELEASE_Q(self):
        return self._sysinfos[7]



