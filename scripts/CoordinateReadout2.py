import time, threading
from mimosis_unpacker.jtag.JTAGCom import *
from mimosis_unpacker import *
from mimosis_unpacker.output import *
import numpy as np
import matplotlib.pyplot as plt
import math


def clear_pulse(jtag):
    """ Clear all pulses by setting all fields of PULSEPIXELROW at 0
    """
    for field in range(16):
        jtag.set_by_name('PULSEPIXELROW','FIELD'+str(field),0)
        
def find_meanValuePosition(myList):
    k=0
    for i in range (myList.shape[0]):
        k+=i* myList[i]
        l=myList.sum()
    if np.abs(l)<0.001:
        return -1
        # To catch devision by zero. Return error flag.
    else:
        return k/l
              

def find_std(myList, meanValuePosition):
    if meanValuePosition<-0.9:
        return -1
        # Mean value not valid, return error flag

    k=0
    for i in range (myList.shape[0]):
        if myList[i]>0:
            k+=(i - meanValuePosition)*(i - meanValuePosition) * myList[i]
            # ignore negative entries <=> consider them zero
        
    return math.sqrt(k)/myList.sum()     

def compute_fixedPattern(mCDS, pedestalNoise):
    for i in range(mCDS.shape[1]):
        for j in range (mCDS.shape[2]):
            pedestalNoise[0,i,j]=find_meanValuePosition(mCDS[:,i,j])
            
def compute_HFNoise(mCDS, pedestalNoise):

    for i in range(mCDS.shape[1]):
        for j in range (mCDS.shape[2]):
            pedestalNoise[1,i,j]=find_std(mCDS[:,i,j],pedestalNoise[0,i,j])

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
minAmplitude=115
maxAmplitude=135

mResultSummary = np.ndarray(shape=(2,(maxAmplitude-minAmplitude)), dtype=np.float32)
hitCountArray=[]

qInput = queue.Queue()
qOutput = queue.Queue()

stop_event = threading.Event()
forwarding_enable = threading.Event()

start_readout (host, port, qInput, forwarding_enable, stop_event, bufferSize)

m = np.ndarray(shape=(32, 504), dtype=np.uint64)
mMemory=np.ndarray(shape=(maxAmplitude-minAmplitude,32,4),dtype=np.float32)

set_pulsed_pixel_Nmb(jtag,10,14)

for amplitude in range(minAmplitude,maxAmplitude,1):
    set_pulse_amplitude (jtag, amplitude)
    time.sleep(1)
    print("PulseAmplitude set to: " , amplitude)
    read_nFrames (qInput, qOutput, forwarding_enable, nFrames)
   
    m[:] = 0
    fill_matrix_with_nFrames(qOutput, m, hitCountArray, stop_event, nFrames)
    print(m[:,9:15]/nFrames)
    mMemory[amplitude-minAmplitude]=m[:,10:14];
    mResultSummary[0,amplitude-minAmplitude]=np.mean(m[:,10:14])/nFrames;
    mResultSummary[1,amplitude-minAmplitude]=np.std(m[:,10:14])/nFrames;
    
    print("Reading completed")

#save_matrix_outputs_win(m, "test")

mCDS=mMemory[1:maxAmplitude-minAmplitude]-mMemory[0:maxAmplitude-minAmplitude-1]
pedestalNoise=np.ndarray(shape=(2,32,4),dtype=np.float32)
pedestalNoise[:,:,:]=0;

compute_fixedPattern(mCDS, pedestalNoise)
compute_HFNoise(mCDS, pedestalNoise)

pedestalFlat=pedestalNoise[0].reshape(pedestalNoise.shape[1]* pedestalNoise.shape[2])
noiseFlat= pedestalNoise[1].reshape(pedestalNoise.shape[1]* pedestalNoise.shape[2])

pedestalFlat[:]=pedestalFlat[:]+minAmplitude
plt.hist(pedestalFlat)
plt.xlabel('VPULSEHIGH')
plt.ylabel('Entries')
plt.show()

plt.hist(noiseFlat, bins=np.arange(0,0.5,0.01))
plt.xlabel('Noise [PulseHightUnits]')
plt.ylabel('Entries')
plt.show()



# test=input()
    
stop_event.set()
