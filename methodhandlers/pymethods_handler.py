#!/usr/bin/env python
# encoding: utf-8

from . import regxhandler as regrex

class MethodsProvider:

    def __init__(self):
        self.regrex = regrex.RegularExpressionHanler()

    def ListParser(self, List):
        for item in List:
            yield item
    
    def List2Tuple(self, List):
        tuple_list = []
        iter_c = 0
        for item in List:
            item_str = '{x}'.format(x=item)
            if iter_c > 0:
                tuple_list.append((item_str[:item_str.index('='):], item_str[item_str.index('=')+1:].replace('"', "")))
            iter_c+=1
        if tuple_list:
            return True,tuple_list

    #Get the "/r/n" Removed tuple List
    def PureListTupleMaker(self, contTuple):
        tuple_list = []
        for key,value in contTuple:
            tuple_list.append((key, self.regrex.Remove_r_n(value)))
        if tuple_list:
            return True,tuple_list

    #TupleList to Dictionary
    def TupleList2Dict(self, TupleList):
        pure_dict = {}
        for key,value in TupleList:
            pure_dict[key] = value
        if pure_dict:
            return True,pure_dict

    #Removing the /r/n from given array items then return pure item list
    def Remove_r_n_FList(self, ListObj):
        temp = []
        for item in ListObj:
            temp.append(self.regrex.Remove_r_n(item))
        if temp:
            return True,temp 

    



