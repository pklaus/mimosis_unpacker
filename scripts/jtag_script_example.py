import time
from JTAGCom import *

def clear_pulse(jtag):
    """ Clear all pulses by setting all fields of PULSEPIXELROW at 0
    """
    for field in range(16):
        jtag.set_by_name('PULSEPIXELROW','FIELD'+str(field),0)
        


def set_pulse(jtag,plist):
    """ Set pulses by setting the fields of PULSEPIXELROW from plist
    """
    for field in list(set(map(lambda x: x//32,plist))):
        templist=[x-32*(x//32) for x in plist if x//32==field]
        fieldvalue=sum(list(map(lambda x: 2**x,templist)))
        jtag.set_by_name('PULSEPIXELROW','FIELD'+str(field),fieldvalue)

# Number of adjacent rows for each scan
step=4
# Range of rows to scan (all DC pixels for this example)
rngrow=range(0,252,step)
# Range of VPULSEHIGH for the scan of injection
rngscan=range(120,166,1)


# Initialize JTAGCom object (start jtag software)
jtag=JTAGCom()
# Initialize COM interface
jtag.start()
jtag.mcf_file
# Load Master Conf file set in object constructor
jtag.load_master()
# Load JTAG conf to MIMOSIS0 chip
jtag.load()

for p in rngrow:
    # Clear all pulses
    clear_pulse(jtag)
    # Set 4 adjacent rows
    pl=list(range(p,p+step))
    set_pulse(jtag,pl)
    
    # Scan VPULSEHIGH value
    for i in rngscan:
        jtag.set_by_name('DAC','VPULSEHIGH',i)
        jtag.load()
        # Wait the end of acquisition (in this example wait a certain amount of time)
        time.sleep(1)

print("Type a key to exit")
input()
# Stop COM interface and quit JTAG software
jtag.stop()
