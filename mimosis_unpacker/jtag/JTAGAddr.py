"""
File: JTAGAddr.py
Description: Class of JTAG address
Authors: F.Morel(IPHC)
Version:0.1
History:
    - 0.1: First Release
"""

class JTAGAddr():
    """ Class to define JTAG address 
        attributes:
          - param: dictionary to have correspondance between address and field name
          
        methods:
          - ir_from_add: get IR name (Instruction Register) from address
          - field_from_add: get field name from address

    """
    
    def __init__(self):
        """Constructor"""
        # Initialize
        self.param={
            'DAC':{
                'ADD':1,
                'MAX':2**8,
                'FIELD':{
                    'VPULSEHIGH':0,
                    'VPULSELOW':1,
                    'VRESET':2,
                    'VCLIP':3,
                    'VCASN2':4,
                    'VCASN':5,
                    'VCASP':6,
                    'NU7':7,
                    'IDB':8,
                    'ITHR':9,
                    'IBIAS':10,
                    'BIASBUFFER':11,
                    'BIASSF':12
                    }
                },
            'LIMITA':{
                'ADD':2,
                'MAX':2**16,
                'FIELD':{
                    'CMD[0]':0,
                    'CMD[1]':1,
                    'CMD[2]':2,
                    'CMD[3]':3,
                    'CMD[4]':4,
                    'CMD[5]':5,
                    'CMD[6]':6,
                    'CMD[7]':7
                    }
                },
            'LIMITB':{
                'ADD':3,
                'MAX':2**16,
                'FIELD':{
                    'CMD[0]':0,
                    'CMD[1]':1,
                    'CMD[2]':2,
                    'CMD[3]':3,
                    'CMD[4]':4,
                    'CMD[5]':5,
                    'CMD[6]':6,
                    'CMD[7]':7
                    }
                },
            'POLARITY':{
                'ADD':4,
                'MAX':2**1,
                'FIELD':{
                    'CMD[0]':0,
                    'CMD[1]':1,
                    'CMD[2]':2,
                    'CMD[3]':3,
                    'CMD[4]':4,
                    'CMD[5]':5,
                    'CMD[6]':6,
                    'CMD[7]':7
                    }
                },
            'FRAMELENGTH':{
                'ADD':5,
                'MAX':2**16,
                'FIELD':{
                    'FIELD0':0
                    }
                },
            'MAXFRAME':{
                'ADD':6,
                'MAX':2**16,
                'FIELD':{
                    'FIELD0':0
                    }
                },
            'SELANA':{
                'ADD':7,
                'MAX':144,
                'FIELD':{
                    'FIELD0':0
                    }
                },
            'PATTERN':{
                'ADD':8,
                'MAX':2**30,
                'FIELD':{
                    'FIELD0':0
                    }
                },
            'DACCONFIG':{
                'ADD':9,
                'MAX':2**1,
                'FIELD':{
                    'TRIMREF0':0,
                    'TRIMREF1':1,
                    'TRIMREF2':2,
                    'ENIREFEXT':3,
                    'ENBUFVACN2':4,
                    'ENBUFVCASN':5,
                    'ENBUFVCASP':6,
                    'ENBUFVCLIP':7,
                    'EXTVCASN2':8,
                    'EXTVCASN':9,
                    'EXTVCASP':10,
                    'EXTVCLIP':11,
                    'EXTIBIAS':12,
                    'EXTIDB':13,
                    'EXTITHR':14,
                    'PADVCASN2':16,
                    'PADVCASN':17,
                    'PADVCASP':18,
                    'PADVCLIP':19,
                    'PADIBIAS':20,
                    'PADIDB':21,
                    'PADITHR':22,
                    'ENBG':31
                    }
                },
            'MODECONFIG':{
                'ADD':10,
                'MAX':2**1,
                'FIELD':{
                    'SELECT_PE[0]':0,
                    'SELECT_PE[1]':1,
                    'SELECT_PE[2]':2,
                    'SELECT_PE[3]':3,
                    'NU1':4,
                    'EN_PATTERN':5,
                    'EN_LATCH':6,
                    'DISABLE_COL_PE':7
                    }
                },
            'PULSEPIXELROW':{
                'ADD':11,
                'MAX':2**32,
                'FIELD':{
                    'FIELD0':0,
                    'FIELD1':1,
                    'FIELD2':2,
                    'FIELD3':3,
                    'FIELD4':4,
                    'FIELD5':5,
                    'FIELD6':6,
                    'FIELD7':7,
                    'FIELD8':8,
                    'FIELD9':9,
                    'FIELD10':10,
                    'FIELD11':11,
                    'FIELD12':12,
                    'FIELD13':13,
                    'FIELD14':14,
                    'FIELD15':15
                    }
                },
            'MASKPIXELROW':{
                'ADD':12,
                'MAX':2**32,
                'FIELD':{
                    'FIELD0':0,
                    'FIELD1':1,
                    'FIELD2':2,
                    'FIELD3':3,
                    'FIELD4':4,
                    'FIELD5':5,
                    'FIELD6':6,
                    'FIELD7':7,
                    'FIELD8':8,
                    'FIELD9':9,
                    'FIELD10':10,
                    'FIELD11':11,
                    'FIELD12':12,
                    'FIELD13':13,
                    'FIELD14':14,
                    'FIELD15':15
                    }
                },
            'PULSEPIXELCOL':{
                'ADD':13,
                'MAX':2**32,
                'FIELD':{
                    'FIELD0':0
                    }
                },
            'MASKPIXELROW':{
                'ADD':14,
                'MAX':2**16,
                'FIELD':{
                    'FIELD0':0
                    }
                },
            'IDCODE':{
                'ADD':15,
                'MAX':2**32,
                'FIELD':{
                    'FIELD0':0
                    }
                }
            }

    def ir_from_add(self,id_add):
        """get IR name (Instruction Register) from address
            inputs:
             - ir address number
            
            output:
             - ir address name
        """
        id_name=next((k for k,v in self.param.items() if v['ADD']==id_add),None)
        
        return id_name
    
    def field_from_add(self,id_add,field_add):
        """get IR name (Instruction Register) from address
            inputs:
             - ir address number
             - field address number
            output:
             - tuple (ir address name,field address name)
        """
        id_name=next((k for k,v in self.param.items() if v['ADD']==id_add),None)
        try:
            field_name=next((k for k,v in self.param[id_name]['FIELD'].items() if v==field_add),None)
        except KeyError:
            field_name=None
        
        return id_name, field_name
