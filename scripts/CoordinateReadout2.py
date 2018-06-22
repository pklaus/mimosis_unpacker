import time, threading
from mimosis_unpacker.jtag.JTAGCom import *
from mimosis_unpacker import *
from mimosis_unpacker.output import *
import numpy as np
import matplotlib.pyplot as plt


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
        
def start_Sensor_JTAG ():
    # Initialize JTAGCom object (start jtag software)
    jtag=JTAGCom()
    # Initialize COM interface
    jtag.start()
    jtag.mcf_file
    # Load Master Conf file set in object constructor
    jtag.load_master()
    # Load JTAG conf to MIMOSIS0 chip
    jtag.load()
    return jtag

def set_pulsed_pixel_Nmb (jtag, minRow, maxRow):
    clear_pulse(jtag)
    # Set 4 adjacent rows
    pl=list(range(minRow,maxRow))
    set_pulse(jtag,pl)

def set_pulse_amplitude (jtag, amplitude):
    jtag.set_by_name('DAC','VPULSEHIGH',amplitude)
    jtag.load()


jtag=start_Sensor_JTAG()    



ctx={}
host = '192.168.0.18'
port = 40000
bufferSize = 4096
nFrames=100
minAmplitude=120
maxAmplitude=135

mResultSummary = np.ndarray(shape=(2,(maxAmplitude-minAmplitude)), dtype=np.float32)

qInput = queue.Queue()
qOutput = queue.Queue()

stop_event = threading.Event()
forwarding_enable = threading.Event()

start_readout (host, port, qInput, forwarding_enable, stop_event, bufferSize)

m = np.ndarray(shape=(32, 504), dtype=np.uint64)

set_pulsed_pixel_Nmb(jtag,10,14)

for amplitude in range(minAmplitude,maxAmplitude,1):
    set_pulse_amplitude (jtag, amplitude)
    time.sleep(3)
    print("PulseAmplitude set to: " , amplitude)
    read_nFrames (qInput, qOutput, forwarding_enable, nFrames)
   
    m[:] = 0
    fill_matrix_with_nFrames(qOutput, m, stop_event, nFrames)
    print(m[:,9:15])
    mResultSummary[0,amplitude-minAmplitude]=np.mean(m[:,10:14])/nFrames;
    mResultSummary[1,amplitude-minAmplitude]=m.std()/nFrames;
    
    print("Reading completed")

#save_matrix_outputs_win(m, "test")

plt.plot(mResultSummary[0])
plt.ylabel('MeanValue')
plt.show()

test=input()
    
stop_event.set()
