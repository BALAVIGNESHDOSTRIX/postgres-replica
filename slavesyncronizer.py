#!/usr/bin/env python
# encoding: utf-8

from systemhandlers import sysexecutor as sys
from logexposer import logSysncronizer as log
from replicators import master_config as msconfig
from replicators import slave_config as svconfig 
from methodhandlers import pymethods_handler as pyhandler
from systemhandlers import masterSysconfigHelper as sysinfo
from config import sysparameter as sysparam
from config import file_config as File_C
from replicators import psql_query_executor as PSQL_C
from filehandlers import fileparser as file_h
from filehandlers import file_handler as Fh_
from pyfiglet import Figlet
import time

class SlaveMachine:
    def __init__(self):
        self._ip_addr = None
        self._sysusername = None
        self._syspassword = None
        self._slaveconobj = None
        self.sysexecObj = sys.SysCommandor()
        self.logObj = log.LogMaintainer()
        self.msconfigObj = msconfig.MasterConfigMaster()
        self.svconfigObj = svconfig.SlaveConfiger()
        self.pymethodHObj = pyhandler.MethodsProvider()
        self.sysinfo = sysinfo.SysInfoManager()
        self.sysparam = sysparam.SystemParameters()
        self.psql_Q_Exec = PSQL_C.PostgresManager()
        self.file_handler = file_h.FileHandler()
        Fh_.DeleteFile_C(self.svconfigObj.LocalPostgresqlDIR())
        Fh_.DeleteFile_C(self.svconfigObj.LocalRecoveryDIR())

    @property
    def getslavehost(self):
        return self._ip_addr

    @property
    def getsysusername(self):
        return self._sysusername

    @property
    def getsyspassword(self):
        return self._syspassword

    @property
    def getsysconObj(self):
        return self._slaveconobj

    #Setter
    @getslavehost.setter
    def set_ip(self, ip):
        self._ip_addr = ip

    @getsysusername.setter
    def set_sysusername(self, sysusername):
        self._sysusername = sysusername

    @getsyspassword.setter
    def set_syspassword(self, syspassword):
        self._syspassword = syspassword

    @getsysconObj.setter
    def set_slaveConObj(self, conObj):
        self._slaveconobj = conObj

    #Establish the Slave Connection
    def EstablishSlaveCon(self):
        con_obj = self.sysexecObj.ConEStablisher(self.getslavehost, self.getsyspassword, self.getsyspassword)
        if con_obj[0]:
            self.set_slaveConObj = con_obj[1]
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
        result = self.sysexecObj.ComExecutor(
            self.msconfigObj.MasSysVersionQuery(), self.getsysconObj, self.getsyspassword)
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

   
    #Stop the postgresqlservice

    def StopPostgresService(self):
        result = self.sysexecObj.ComExecutor(
            self.msconfigObj.MasPostgresServiceStopQuery(), self.getsysconObj, self.getsyspassword)
        if result[0]:
            self.logObj.MessageCatcher("Successfully Stopped the posgreql service....")
        else:
            self.logObj.MessageCatcher("Unable to Stop the PSQL Service...")

    #Start the postgreqlservice start
    def StartPostgreqService(self):
        result = self.sysexecObj.ComExecutor(
            self.msconfigObj.MasPostgresServiceStartQuery(), self.getsysconObj, self.getsyspassword)
        if result[0]:
            self.logObj.MessageCatcher("Successfully Started the postgresql sevice....")
        else:
            self.logObj.MessageCatcher("Unable to Start the PSQL Service...")

    #Restart the postgresql service restart
    def RestartPostgresqlService(self):
        result = self.sysexecObj.ComExecutor(
            self.msconfigObj.MasPostgresServiceRestatQuery(), self.getsysconObj, self.getsyspassword)
        if result[0]:
            self.logObj.MessageCatcher("Successfully Restrated the postgresql service....")
        else:
            self.logObj.MessageCatcher("Unable to Restart the PSQL Service...")


    #BACKUP UTILITY
    def MakeBackupUtil_Prc(self):
        back_rename_Q = self.svconfigObj.Rename_DB_Source_Q_(self.svconfigObj.GetSlavePostgresVersion)
        rename_P_S = self.sysexecObj.ComExecutor(back_rename_Q, self.getsysconObj, self.getsyspassword)
        if rename_P_S[0]:
            PG_Q_ = self.svconfigObj.PGBackup_Q(self.svconfigObj.GetSlavePostgresVersion, 
                                        self.svconfigObj.getmaster_IP, self.svconfigObj.getmasrepuser,
                                        self.svconfigObj.getmasrepuserpass)
            backup_res = self.sysexecObj.ComExecutor(PG_Q_, self.getsysconObj, self.getsyspassword)
            if backup_res[0]:
                self.logObj.MessageCatcher("Successfully restored")

    #def Get postgresql file from slave
    def GetPostgresqlConf(self):
        psql_conf_dir = self.svconfigObj.PostgresqlDIR(self.svconfigObj.GetSlavePostgresVersion)
        result = self.svconfigObj.GetPostgresql_confile(psql_conf_dir, self.getsysconObj)
        return result

    #Edit the postgresql.conf
    def EditPSQLCONF(self):
        #Change the posgresql.conf permission
        permit_query = self.svconfigObj.ChangepostgresqlPermit(self.svconfigObj.GetSlavePostgresVersion)
        permit_ch_res = self.sysexecObj.ComExecutor(permit_query, self.getsysconObj, self.getsyspassword)
        if permit_ch_res[0]:
            if self.GetPostgresqlConf():
                all_file_lines = self.file_handler.ReturnConfigLines(self.svconfigObj.LocalPostgresqlDIR())
                if Fh_.DeleteFile_C(self.svconfigObj.LocalPostgresqlDIR()):
                    edit_result = self.svconfigObj.ConfigLineFeeder(all_file_lines, self.svconfigObj.LocalPostgresqlDIR())
                    if edit_result:
                        transf_res = self.sysexecObj.FileTransfer(self.getsysconObj, "POST", self.svconfigObj.LocalPostgresqlDIR(), self.svconfigObj.PostgresqlDIR(self.svconfigObj.GetSlavePostgresVersion))
                        if transf_res[0]:
                            permit_exec_res = self.sysexecObj.ComExecutor(self.svconfigObj.MakePostgresql_confPermit(self.svconfigObj.GetSlavePostgresVersion), self.getsysconObj, self.getsyspassword)
                            if permit_exec_res[0]:
                                self.logObj.MessageCatcher("Successfully Configuration Has been Changed")
                                return True, True
                            else:
                                False, "PUT-PER-CH-ERR"
                        else:
                            False, "CONF-TRANS-ERR"
                    else:
                        False, "CONF-EDT-ERR"
            else:
                False, "CONF-FILE-Q-ERR"
        else:
            False, "PER-CH-ERR"


    #Create the recovery configuration file
    def MakeRecoveryFile(self):
        tansfer_Q = self.svconfigObj.TransferRecoveryConf_Q(self.svconfigObj.GetSlavePostgresVersion)
        transfer_P = self.sysexecObj.ComExecutor(tansfer_Q, self.getsysconObj, self.getsyspassword)
        if transfer_P[0]:
            rec_permit_revert_st = self.sysexecObj.ComExecutor(self.svconfigObj.ChangepostgresqlRecoveryPermit(self.svconfigObj.GetSlavePostgresVersion), self.getsysconObj, self.getsyspassword)
            if rec_permit_revert_st[0]:
                if self.svconfigObj.GetRecovery_confile(self.svconfigObj.RecoveryConfDir(self.svconfigObj.GetSlavePostgresVersion), self.getsysconObj):
                    all_file_lines = self.file_handler.ReturnConfigLines(self.svconfigObj.LocalRecoveryDIR())
                    if Fh_.DeleteFile_C(self.svconfigObj.LocalRecoveryDIR()):
                        edit_result = self.svconfigObj.RecFeeder(all_file_lines, self.svconfigObj.LocalRecoveryDIR())
                        if edit_result:
                            transf_res = self.sysexecObj.FileTransfer(self.getsysconObj, "POST", self.svconfigObj.LocalRecoveryDIR(), self.svconfigObj.RecoveryF_DesDIR(self.svconfigObj.GetSlavePostgresVersion))
                            if transf_res[0]:
                                rec_permit_st = self.sysexecObj.ComExecutor(self.svconfigObj.MakePostgresql_RecoveryPermit(self.svconfigObj.GetSlavePostgresVersion), self.getsysconObj, self.getsyspassword)
                                if rec_permit_st[0]:
                                    rec_transf_st = self.sysexecObj.ComExecutor(self.svconfigObj.MoveRecovery_Dest(self.svconfigObj.GetSlavePostgresVersion), self.getsysconObj, self.getsyspassword)
                                    if rec_transf_st[0]:
                                        self.logObj.MessageCatcher("Successfully Recovery Configuration Has been Changed")
                                        return True

def SlaveIntializer():
    slave = SlaveMachine()
    f = Figlet(font='small')
    print(f.renderText('Slave Configuration'))
    slave.set_ip = str(input("Enter the Slave IP: "))
    slave.set_sysusername = str(input("Enter the Username: "))
    slave.set_syspassword = str(input("Enter the Password:"))
    slave.svconfigObj.setmaster_IP = str(input("Enter the Master IP: "))
    slave.svconfigObj.setmasrepuser = str(input("Enter the Replica User Name: "))
    slave.svconfigObj.setmasrepuserpass = str(input("Enter the Replica User Password: "))
    slave.svconfigObj._slave_postgres_version = input("Enter the Slave Machine Postgres Version: ")
    slave.EstablishSlaveCon()
    slave.StopPostgresService()
    slave.EditPSQLCONF()
    slave.MakeRecoveryFile()
    slave.MakeBackupUtil_Prc()
    slave.StartPostgreqService()

