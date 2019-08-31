#!/usr/bin/env python
# encoding: utf-8

from systemhandlers import sysexecutor as sys 
from logexposer import logSysncronizer as log
from replicators import master_config as msconfig
from methodhandlers import pymethods_handler as pyhandler
from systemhandlers import masterSysconfigHelper as sysinfo 
from config import sysparameter as sysparam
from config import file_config as File_C
from replicators import psql_query_executor as PSQL_C
from filehandlers import fileparser as file_h
from filehandlers import file_handler as Fh_
from pyfiglet import Figlet
import time 


class MasterMachine:

    def __init__(self):
        self._ip_addr = None 
        self._sysusername = None
        self._syspassword = None 
        self._masterconobj = None 
        self.sysexecObj = sys.SysCommandor()
        self.logObj = log.LogMaintainer()
        self.msconfigObj = msconfig.MasterConfigMaster()
        self.pymethodHObj = pyhandler.MethodsProvider()
        self.sysinfo = sysinfo.SysInfoManager()
        self.sysparam = sysparam.SystemParameters()
        self.psql_Q_Exec = PSQL_C.PostgresManager()
        self.file_handler = file_h.FileHandler()
        Fh_.DeleteFile_C(self.msconfigObj.LocalPostgresqlDIR())

    @property
    def getmasterhost(self):
        return self._ip_addr

    @property
    def getsysusername(self):
        return self._sysusername

    @property
    def getsyspassword(self):
        return self._syspassword

    @property
    def getsysconObj(self):
        return self._masterconobj
    

    #Setter 
    @getmasterhost.setter
    def set_ip(self, ip):
        self._ip_addr = ip

    @getsysusername.setter 
    def set_sysusername(self, sysusername):
        self._sysusername = sysusername

    @getsyspassword.setter 
    def set_syspassword(self, syspassword):
        self._syspassword = syspassword

    @getsysconObj.setter 
    def set_masterConObj(self, conObj):
        self._masterconobj = conObj

    #Establish the Master Connection 
    def EstablishMasterCon(self):
        con_obj = self.sysexecObj.ConEStablisher(self.getmasterhost, self.getsyspassword, self.getsyspassword)
        if con_obj[0]:
            self.set_masterConObj = con_obj[1]
            return True
        else:
            return False

    #Get the system OS Version
    def GetMasterOS_V(self):
        result = self.sysexecObj.ComExecutor(self.msconfigObj.MasSysVersionQuery(), self.getsysconObj, self.getsyspassword)
        if result[0]:
             sys_info_dict = self.sysinfo.ParseSystemV(self.pymethodHObj.ListParser(result[1]))
             self.logObj.MessageCatcher(self.sysinfo.GetSystemInfo(sys_info_dict, self.sysparam.getOS_VID()))
        else:
            self.logObj.MessageCatcher("Error")

    #Get the system Full details
    def GetAllMasterOS_Info(self):
        result = self.sysexecObj.ComExecutor(self.msconfigObj.MasSysVersionQuery(), self.getsysconObj, self.getsyspassword)
        if result[0]:
             sys_info_dict = self.sysinfo.ParseSystemV(self.pymethodHObj.ListParser(result[1]))
             self.logObj.FormalMessageCatcher(self.sysparam.getOSName(), ':', self.sysinfo.GetSystemInfo(sys_info_dict, self.sysparam.getOSName()))
             self.logObj.FormalMessageCatcher(self.sysparam.getOSVersion(), ':', self.sysinfo.GetSystemInfo(sys_info_dict, self.sysparam.getOSVersion()))
             self.logObj.FormalMessageCatcher(self.sysparam.getOS_ID(), ':', self.sysinfo.GetSystemInfo(sys_info_dict, self.sysparam.getOS_ID()))
             self.logObj.FormalMessageCatcher(self.sysparam.getOS_Base(), ':', self.sysinfo.GetSystemInfo(sys_info_dict, self.sysparam.getOS_Base()))
             self.logObj.FormalMessageCatcher(self.sysparam.getOS_VID(), ':', self.sysinfo.GetSystemInfo(sys_info_dict, self.sysparam.getOS_VID()))
             self.logObj.FormalMessageCatcher(self.sysparam.getOS_V_CODENAME(), ':', self.sysinfo.GetSystemInfo(sys_info_dict, self.sysparam.getOS_V_CODENAME()))
             self.logObj.FormalMessageCatcher(self.sysparam.getUBUNTU_CODENAME(), ':', self.sysinfo.GetSystemInfo(sys_info_dict, self.sysparam.getUBUNTU_CODENAME()))
        else:
            self.logObj.MessageCatcher("Error")

    #Get the Postgresql Version 
    def GetPostgresql_V(self):
        result = self.sysexecObj.ComExecutor(self.msconfigObj.MasSysPostgresql_VQuery(), self.getsysconObj, self.getsyspassword)
        if result[0]:
            pure_v_item_obj = self.sysinfo.ParsePsql_V(result[1])
            psql_v = self.sysinfo.ScrapePsql_V(pure_v_item_obj)
            if psql_v[0]:
                self.logObj.FormalMessageCatcher("PSQL Version", ':', psql_v[1])
            else:
                self.logObj.MessageCatcher("Can not View the PSQL Version")

    #Create Postgres SuperUser Process
    #Stop the postgresqlservice
    def StopPostgresService(self):
        result = self.sysexecObj.ComExecutor(self.msconfigObj.MasPostgresServiceStopQuery(), self.getsysconObj, self.getsyspassword)
        if result[0]:
            self.logObj.MessageCatcher("Successfully Stopped the posgreql service....") 
        else:
            self.logObj.MessageCatcher("Unable to Stop the PSQL Service...")

    #Start the postgreqlservice start
    def StartPostgreqService(self):
        result = self.sysexecObj.ComExecutor(self.msconfigObj.MasPostgresServiceStartQuery(), self.getsysconObj, self.getsyspassword)
        if result[0]:
            self.logObj.MessageCatcher("Successfully Started the postgresql sevice....")
        else:
            self.logObj.MessageCatcher("Unable to Start the PSQL Service...")

    #Restart the postgresql service restart
    def RestartPostgresqlService(self):
        result = self.sysexecObj.ComExecutor(self.msconfigObj.MasPostgresServiceRestatQuery(), self.getsysconObj, self.getsyspassword)
        if result[0]:
            self.logObj.MessageCatcher("Successfully Restrated the postgresql service....")
        else:
            self.logObj.MessageCatcher("Unable to Restart the PSQL Service...")

    #Set the Relication UserPassword
    def SetSuperPassword(self):
        res = self.psql_Q_Exec.ReplicatePassAssigner(self.msconfigObj.GetDBUsername, self.msconfigObj.GetStandByMachineIP, self.msconfigObj.GetDBUserPassword, self.msconfigObj.GetReplicationUserN, self.msconfigObj.GetReplicaUserPassword, self.getsysconObj, self.getsyspassword)
        return res


    #Create the Replication SuperUser
    def CreateReplicaSuperUser(self):
        rep_user_query = self.msconfigObj.MakeReplicaUserQuery(self.msconfigObj.GetReplicationUserN, self.msconfigObj.GetReplicaSlaveCount)
        result = self.sysexecObj.ComExecutor(rep_user_query, self.getsysconObj, self.getsyspassword)
        if result[0]:
            return True
        else:
            return False

    
    #Create Replication Archive Directory
    def CreateReplicaArchiveDir(self, dir=None):
        def ExecuteRelicaArchiveCommand(query):
            res = self.sysexecObj.ComExecutor(query, self.getsysconObj, self.getsyspassword)
            if res[0]:
                return True 
            else:
                return False

        if dir:
            dir_c = self.msconfigObj.MakeReplicaDIRQuery(dir)
            if ExecuteRelicaArchiveCommand(dir_c):
                dir_check = self.msconfigObj.CheckReplicaDirIsAvail(dir)
                dir_avail_res = self.sysexecObj.ComExecutor(dir_check, self.getsysconObj, self.getsyspassword)
                if dir_avail_res[0]:
                    pure_L = self.sysinfo.MakePureList(dir_avail_res[1])
                    if self.sysinfo.ListParser(pure_L, "True"):
                        self.logObj.MessageCatcher("The Archive Directory Was Successfully Created...")
                        return True,"True"
                    else:
                        self.logObj.MessageCatcher("Unable to create a Archive Directory...")
                        return False,"UNAB-CRE-DIR"
            else:
                self.logObj.MessageCatcher("Unable to create a Archive Directory...")
                return False, "UNAB-CRE-DIR"
        else:
            self.logObj.MessageCatcher("Directory path Not Set")
            return False, "COM-NOT-FOU"

    #Create Replication Entry
    def MakeEntryHBA(self):
        pga_dir = self.msconfigObj.GetHbaFileDIR(self.msconfigObj.GetMasterPostgresVersion)
        pga_entry_Q = self.msconfigObj.PGHBA_EntryMaker(pga_dir, self.msconfigObj.GetStandByMachineIP, self.msconfigObj.GetReplicationUserN)
        exec_result = self.sysexecObj.ComExecutor(pga_entry_Q, self.getsysconObj, self.getsyspassword)
        if exec_result[0]:
            pga_entry_checker_Q = self.msconfigObj.PGHBA_Entry_Checker(self.msconfigObj.GetReplicaEntryLine(self.msconfigObj.GetReplicationUserN, "192.168.0.139"), self.msconfigObj.GetHbaFileDIR(self.msconfigObj.GetMasterPostgresVersion))
            entry_exec_result = self.sysexecObj.ComExecutor(pga_entry_checker_Q, self.getsysconObj, self.getsyspassword)
            if entry_exec_result[0]:
                exec_res_pure_list = self.sysinfo.MakePureList(entry_exec_result[1])
                if self.sysinfo.CheckEntry_PGHBA(exec_res_pure_list):
                    return True 
                else:
                    return False 



    #def Get postgresql file from slave
    def GetPostgresqlConf(self):
        psql_conf_dir = self.msconfigObj.PostgresqlDIR(self.msconfigObj.GetMasterPostgresVersion)
        result = self.msconfigObj.GetPostgresql_confile(psql_conf_dir, self.getsysconObj)
        return result 
    
    #Edit the postgresql.conf
    def EditPSQLCONF(self):
        #Change the posgresql.conf permission 
        permit_query = self.msconfigObj.ChangepostgresqlPermit(self.msconfigObj.GetMasterPostgresVersion)
        permit_ch_res = self.sysexecObj.ComExecutor(permit_query, self.getsysconObj, self.getsyspassword)
        if permit_ch_res[0]:
            if self.GetPostgresqlConf():
                all_file_lines = self.file_handler.ReturnConfigLines(self.msconfigObj.LocalPostgresqlDIR())
                if Fh_.DeleteFile_C(self.msconfigObj.LocalPostgresqlDIR()):
                    edit_result = self.msconfigObj.ConfigLineFeeder(all_file_lines, self.msconfigObj.LocalPostgresqlDIR())
                    if edit_result:
                        transf_res = self.sysexecObj.FileTransfer(self.getsysconObj, "POST", self.msconfigObj.LocalPostgresqlDIR(), self.msconfigObj.PostgresqlDIR(self.msconfigObj.GetMasterPostgresVersion))
                        if transf_res[0]:
                            permit_exec_res = self.sysexecObj.ComExecutor(self.msconfigObj.MakePostgresql_confPermit(self.msconfigObj.GetMasterPostgresVersion), self.getsysconObj, self.getsyspassword)
                            if permit_exec_res[0]:
                                self.logObj.MessageCatcher("Successfully Configuration Has been Changed")
                                return True,True
                            else:
                                False,"PUT-PER-CH-ERR"
                        else:
                            False,"CONF-TRANS-ERR"
                    else:
                        False,"CONF-EDT-ERR"
            else:
                False,"CONF-FILE-Q-ERR"
        else:
            False,"PER-CH-ERR"


        



if __name__ == "__main__":
    
    def main(master):
        def conMaker(master):
            if master.EstablishMasterCon():
                master.logObj.MessageCatcher("Successfully Master Machine Connected...")
                return True 
            else:
                master.logObj.MessageCatcher("Connection Failed...")
                return False

        def MethodInvocker(master):
            res = str(input("Do you want to see the System Info & PSQL_V(yes/no): "))
            if res == "yes":
                master.GetAllMasterOS_Info()
                master.GetPostgresql_V()
                return True
            elif res == "no":
                master.logObj.MessageCatcher(
                    "Warning You should Aware About PSQL & OS-V")
                resx = str("Do you want to see Once Again (yes/no): ")
                if resx == "yes":
                    MethodInvocker(master)
                else:
                    return True

        def EDITERROR_Collector(key,master):
            res = {
                "PUT-PER-CH-ERR" : "Standby Machine postgresql.conf file Permission Changing error",
                "CONF-TRANS-ERR" : "postgresql.conf edited file transfer is failed",
                "CONF-EDT-ERR" : "Postgresql.conf editing is failed.",
                "CONF-FILE-Q-ERR" : "Directory of postgresql.conf unable to get",
                "PER-CH-ERR" : "postgresql.conf file on standby machine read permission change error."
                }
            master.logObj.MessageCatcher(res.get(key))

        def DBConfigSyncronizer(master):
            #Create Replication User
            def CreateReplicaUser(master):
                if master.CreateReplicaSuperUser():
                    master.logObj.MessageCatcher("Successfully created the Replica User")
                    if master.SetSuperPassword():
                        master.logObj.MessageCatcher("Password Has been Setuped for Replica User")
                        return True,"True"
                    else:
                        master.logObj.MessageCatcher("Unable to Set the password for Replica User")
                        return False,"REPU-CRE-ERR"
                else:
                    master.logObj.MessageCatcher("Unable to Create the Replication User")
                    return False,"REPU-PASS-ERR"

            

            repuser_c_res = CreateReplicaUser(master)
            if repuser_c_res[0]:
                arc_res = master.CreateReplicaArchiveDir(master.msconfigObj.GetArchiveDir)
                if arc_res[0]:
                    #Make HBA Entry
                    master.logObj.MessageCatcher("Successfully Archive Directory Created")
                    if master.MakeEntryHBA():
                        master.logObj.MessageCatcher("Successfully Standby Machine IP Entry Created")
                        edit_res = master.EditPSQLCONF()
                        if edit_res[0]:
                            master.logObj.MessageCatcher("Successfully postgresql.conf Configured")
                            return True
                        else:
                            EDITERROR_Collector(edit_res[1], master)
                            choice = str( input("Enter Your choice for Try Again(yes/no): "))
                            if choice == "yes":
                                master.EditPSQLCONF()
                            elif choice == "no":
                                master.logObj.MessageCatcher("Please Edit postgresql.conf Manually on Standby Machine Or Else Remaining Process Totally Waste if may Proceed.")
                            return False
                    else:
                        choice = str(input("Enter Your choice for Try Again(yes/no): "))
                        if choice == "yes":
                            master.MakeEntryHBA()
                        elif choice == "no":
                            master.logObj.MessageCatcher("Please Create HBA Replica Entry Manually Or Else Remaining Process Totally Waste if may Proceed.")
                else:
                    choice = str(input("Enter Your choice for Try Again(yes/no): "))
                    if choice == "yes":
                        master.CreateReplicaArchiveDir(master.msconfig.GetArchiveDir)
                    elif choice == "no":
                        master.logObj.MessageCatcher("Please Create Archive Directory Manually Or Else Remaining Process Totally Waste if may Proceed.")
            else:
                choice = str(input("Enter Your choice for Try Again(yes/no): "))
                if choice == "yes":
                    CreateReplicaUser(master)
                elif choice == "no":
                    master.logObj.MessageCatcher("Please Create the SuperUser Manually Or Else Remaining Process Totally Waste if may Proceed.")

            


        if conMaker(master):
            if MethodInvocker(master):
                if DBConfigSyncronizer(master):
                    master.logObj.MessageCatcher("Thank you For used Master Configuration Tool")


def MasterInitializer():
    master = MasterMachine()
    f = Figlet(font='small')
    print(f.renderText('Master Configuration'))
    master.set_ip = str(input("Enter the Master IP: "))
    master.set_sysusername = str(input("Enter the Master Username: "))
    master.set_syspassword = str(input("Enter the Master Password: "))
    master.msconfigObj.setDBUsername = str(input("Enter the Database Username: "))
    master.msconfigObj.setDBUserPassword = str(input("Enter the Database Password: "))
    master.msconfigObj.setReplicaUserName = str(input("Enter the ReplicaUserName: "))
    master.msconfigObj.setReplicaSaleveCount = str(input("Enter the Replica Connection Count: "))
    master.msconfigObj.setReplicaUserPassword = str(input("Enter the ReplicaUser Password: "))
    master.msconfigObj.setReplicaArchiveDir = File_C.File_Config().PSQLArchiveDir()
    master.msconfigObj.setMaxWalSender = str(input("Enter the MaxWal Sender count: "))
    master.msconfigObj.setMasterPostgresVersion = str(input("Enter the Master Postgresql Version: "))
    master.msconfigObj.setStandByMachineIP = str(input("Enter the StandBy Machine IP: "))
    time.sleep(3)
    main(master)

         



 


    


