
#!/usr/bin/env python
# encoding: utf-8

from methodhandlers import pymethods_handler as method 

class SysInfoManager:

    def __init__(self):
        self.methodHL = method.MethodsProvider()

    #Parsing the System Info details
    def ParseSystemV(self, iterObj):
        tuple_l = self.methodHL.List2Tuple(iterObj)
        if tuple_l[0]:
            pure_tuple = self.methodHL.PureListTupleMaker(tuple_l[1])
            if pure_tuple[0]:
                sysinfo_dict = self.methodHL.TupleList2Dict(pure_tuple[1])
                if sysinfo_dict[0]:
                    return sysinfo_dict[1]

    #Returning the Needed System info from given system info dictionary
    def GetSystemInfo(self, sysinfoDict, whois):
        return sysinfoDict.get(whois)

    #Parse the Master Postgresql Return string to get the PSQL Version
    def ParsePsql_V(self, ListObj):
        pure_L = self.methodHL.Remove_r_n_FList(ListObj)
        if pure_L[0]:
            return pure_L[1]

    #scrape the psql version from the list items
    def ScrapePsql_V(self, pureListobj):
        item_c = 1
        for item in pureListobj:
            if item_c == 2:
                return True,item
            item_c += 1
        return False,False

    def MakePureList(self, ListObj):
        pure_L = self.methodHL.Remove_r_n_FList(ListObj)
        if pure_L[0]:
            return pure_L[1]

    #List Parser
    def ListParser(self, ListObj, needitem):
        for items in ListObj:
            if items == needitem:
                return True 
        return False

    #PGA_Entry checker
    def CheckEntry_PGHBA(self, ListObj):
        for item in ListObj:
            if item == 0 or '0':
                return True 
        return False
        

        
        


        

            
