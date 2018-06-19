"""
File: JTAGCom.py
Description:  Class to comunicate to MIMOSISOSC JTAG software through COM
Authors: F.Morel(IPHC)
Version:0.1
History:
    - 0.1: First Release
"""

import pythoncom, win32com.client
import numpy as np
import ctypes
import subprocess

from JTAGAddr import *

MIMOSIS0_JTAG_EXE="C:/CCMOS_SCTRL/MIMOSIS0_SC/MIMOSIS0_SC.exe"

class JTAGCom():
    """ Class to comunicate to MIMOSISOSC JTAG software and PXI acquisition software through COM 
        attributes:
          - prog_id: ProgID for COM (default "MIMOSIS0.MIMOSIS0SC")
          - conf_path: Path of config files for JTAG exe (default "C:/CCMOS_SCTRL/MIMOSIS0_SC/config_files")
          - mcf_file: MCF file (default "MIMOSIS0_DEF_TEMPLATE.mcf")
          - handle: handle for JTAG COM
          - addr: object of Class JTAGAddr used to manipulate JTAG field
          - pjtag: subprocess object of JTAG software
        methods:
          - start:
          - stop:
    """
    def __init__(self):
        """Constructor"""
        # Initialize
        self.addr=JTAGAddr()
        self._handle=None
        self.prog_id="MIMOSIS0.MIMOSIS0SC"
        self.conf_path="C:/CCMOS_SCTRL/MIMOSIS0_SC/config_files"
        self._mcf_file="MIMOSIS0_DEF_TEMPLATE.mcf"
        self.pjtag=subprocess.Popen(MIMOSIS0_JTAG_EXE)

    def _get_handle(self):
        """get JTAG COM handle"""
        return self._handle
    
    def _get_mcf_file(self):
        """get default MCF file"""
        return self._mcf_file
    
    handle=property(_get_handle)
    mcf_file=property(_get_mcf_file)

    def stop(self):
        """stop JTAG COM"""
        del self._handle
        # used to allow threading
        pythoncom.CoUninitialize()
        self._handle=None
        try:
            self.pjtag.terminate()
        except:
            pass
    
    def start(self):
        """start JTAG COM"""
        pythoncom.CoInitialize()
        self._handle= win32com.client.Dispatch(self.prog_id)
    
    def load_master(self):
        """load master config file"""
        ret=self._handle.MasterConfLoadFile(self.conf_path+"/"+self._mcf_file)
        return ret
    
    def load(self):
        """load JTAG config to MIMOSIS0"""
        ret=self._handle.MasterConfUpdateAll()
        if ret!=0:
            print("Error on JTAG loading: "+str(ret))
        return ret
    
    def set_by_add(self,ir_add,field_add,value):
        """set JTAG field value based on address number
            inputs:
             - ir address number
             - field address number
             - value
            output:
             - tuple:(value,error)
        """
        ret=self._handle.DeviceValueSet(0,ir_add,field_add,ctypes.c_long(ctypes.c_ulong(value).value).value)
        if ret[1]!=0:
            print("Error on JTAG field setting: "+str(ret))
        return ret
    
    def set_by_name(self,ir_name,field_name,value):
        """set JTAG field value based on address name
            inputs:
             - ir address name
             - field address name
             - value
            output:
             - tuple:(value,error)
        """
        ir_add=self.addr.param[ir_name]['ADD']
        field_add=self.addr.param[ir_name]['FIELD'][field_name]
        ret=self.set_by_add(ir_add,field_add,value)
        
        return ret

    
    def get_by_add(self,ir_add,field_add):
        """get JTAG field value based on address number
            inputs:
             - ir address number
             - field address number
            output:
             - tuple (write field value, read field value, error code)
        """
        ret=self._handle.DeviceValueGet(0,ir_add,field_add)
        if ret[2]!=0:
            print("Error on JTAG field setting: "+str(ret))
        return ret
    
    def get_by_name(self,ir_name,field_name):
        """get JTAG field value based on address name
            inputs:
             - ir address name
             - field address name
            output:
             - tuple (write field value, read field value, error code)
        """
        ir_add=self.addr.param[ir_name]['ADD']
        field_add=self.addr.param[ir_name]['FIELD'][field_name]
        ret=self.get_by_add(ir_add,field_add)
        
        return ret
