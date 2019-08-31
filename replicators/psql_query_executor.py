#!/usr/bin/env python
# encoding: utf-8

import psycopg2 as psql
import datetime
from subprocess import Popen, run, PIPE
from config.psql_exec_config import ErrorFlags, ExceptionStr
from systemhandlers import sysexecutor as sysExec


class PostgresManager:

    #Constructor
    def __init__(self, db_name=None, db_user=None, db_host=None, db_pass=None):
        self.db_name = db_name
        self.db_user = db_user
        self.db_host = db_host
        self.db_pass = db_pass
        self.sysCExec = sysExec.SysCommandor()
        
    #General Message printing Method
    def DBMessageCatcher(self, mess):
        print(" ")
        print(mess)

   
    #Method For returning what type of Exception is raised
    def ErrorTypeSerializer(self, type):
        if ExceptionStr.get('AUTH') in type:
            return ErrorFlags.get('USRER')
        if ExceptionStr.get('DBEX') in type:
            return ErrorFlags.get('DBERR')
        if ExceptionStr.get('HTRANS') in type:
            return ErrorFlags.get('HTERR')
        if ExceptionStr.get('HCONER') in type:
            return ErrorFlags.get('HTERR')

    #Method for Making the Db Connection and return the connection object
    def DBConMaker(self, db_name=None, db_user=None, db_host=None, db_pass=None):
        try:
            self.db_conn = psql.connect(dbname=db_name,
                                        user=db_user,
                                        host=db_host,
                                        password=db_pass,
                                        port=5432)
            if self.db_conn != None:
                return True, self.db_conn
        except KeyboardInterrupt:
            quit()
        except psql.DatabaseError as ex:
            self.DBMessageCatcher(ex)

     #Method for Creating the Needed DB in the database
    def ReplicatePassAssigner(self, db_user, db_host, db_pass, rep_username, rep_userpass, conObj, syspass):
        try:
            command = "PGPASSWORD={db_pass} psql -U {db_user} -h {db_host} -c {alter_c}".format(db_pass=db_pass,
                                                                                                  db_user=db_user,
                                                                                                  db_host=db_host,
                                                                                                  alter_c="'alter user {new_db} with password {dbs_user};'".format(new_db=rep_username,
                                                                                                                                                                   dbs_user='"c"'.format(c=rep_userpass)))
            result = self.sysCExec.ComExecutor(command, conObj, syspass)
            if result[0]:
                return True
            return False
        except:
            return False
            

    

    

    

    

    
