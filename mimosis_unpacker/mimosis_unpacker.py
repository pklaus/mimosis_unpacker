#!/usr/bin/env python

# internal modules
#none yet

# external deps
#none yet

# Python stdlib
import socket, time, queue, threading
from collections import Counter
from datetime import datetime as dt
import numpy as np


def udp_receive(host, port, q, forwarding_enable, stop_event, buffer_size=4096):
    """ q: queue.Queue() to put the data to """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.settimeout(0.005)
    sock.bind((host, port))

    while not stop_event.is_set():
        # potentially more efficient: sock.recvfrom_into(buf)
        data, addr = sock.recvfrom(buffer_size)
        if (data and forwarding_enable.is_set()):
            q.put({'ts': dt.now(), 'payload': data, 'addr': addr})
    print("done with udp_receive(...)")


def timed_queue_stats(q, stop_event, interval=1.0):
    last = time.time()
    while not stop_event.is_set():
        while (time.time() - last) < interval:
            time.sleep(0.01)
        duration = time.time() - last
        last += interval
        all_packets = []
        while not (stop_event.is_set() or q.empty()):
            all_packets.append(q.get())
        total_payload_len = sum(len(packet['payload']) for packet in all_packets)
        print(":)")
        print("Received {} bytes in the last {:.3f} seconds.".format(total_payload_len, duration))
        print("Data Rate: {dr:.3f} Mbit/s".format(dr=8*total_payload_len/duration*1e-6))
        print("Number of packets received: ", len(all_packets))
        print("Packet Rate: {pr:.1f} pkts/s".format(pr=len(all_packets)/duration))
        print("=======================")


def mimosis_words(data):
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]
    length = len(data)
    length = length // 4 * 4
    return chunks(data[0:length], 4)

def fill_matrix_with_nFrames(q, m, stop_event, nFrames):
    """ q: queue.Queue, m: np.ndarray, stop_event: threading.Event() """

    
    strange_words = Counter()
    framesProcessed=0
    maxCol=m.shape[0]
    maxRow=m.shape[1]
    
   
    while not q.empty() and not stop_event.is_set():
            qsize = q.qsize()
            #if qsize > 1: print("Queue (FIFO buffer) size > 1: ", qsize)
            packet = q.get()
            
            for word in mimosis_words(packet['payload']):
                if framesProcessed>nFrames:
                    pass 
                    #stop recording data once nFrames frames are processed
                    #but keeps emptying the queue
                if word.startswith(b'\x00\x0b'):
                    #print("BEGIN of new frame, header from sensor")
                    framesProcessed+=1; #count frames. Indirectly: Start processing once the start of the first frame is detected.
                elif (framesProcessed == 0 or framesProcessed>nFrames) :
                    pass #ignore words, which arrive before the first frame header is found and words arriving beyond the last frame
                elif word.startswith (b'\xff\xff'):
                    pass #ignore header from TRB
                elif word.startswith(b'\x00\x03') and framesProcessed>0:
                    col = (word[2] & 0b11111100) >> 2
                    row = ((word[2] & 0b11) << 8) + word[3]
                    # Disentangle double column topology
                    col_add = 1 if row % 4 in (0, 3) else 0
                    col = 2*col + col_add
                    row = row//2
                    # Store hit by incrementing matrix entry
                    if (col >= maxCol or row >= maxRow):
                        print("Warning: Bad encoding: ", word.hex())
                        strangeWords[word]+= 1
                        pass
                    else: 
                        m[col, row] += 1
                else:
                    strange_words[word] += 1
    if strange_words:
        print("Found a couple of strange words: {}".format(strange_words))
    print("done with fill_matrix(...)")
    
    
    

def fill_matrix(q, m, stop_event):
    strange_words = Counter()
   
    
    while not stop_event.is_set():
        while not q.empty():
            qsize = q.qsize()
            #if qsize > 1: print("Queue (FIFO buffer) size > 1: ", qsize)
            packet = q.get()
            for word in mimosis_words(packet['payload']):
                if word.startswith(b'\x00\x0b'):
                    #print("BEGIN of new frame")
                    pass
                elif word.startswith(b'\x00\x03'):
                    col = (word[2] & 0b11111100) >> 2
                    row = ((word[2] & 0b11) << 8) + word[3]
                    # Disentangle double column topology
                    col_add = 1 if row % 4 in (0, 3) else 0
                    col = 2*col + col_add
                    row = row//2
                    # Store hit by incrementing matrix entry
                    m[col, row] += 1
                else:
                    strange_words[word] += 1
    if strange_words:
        print("Found a couple of strange words: {}".format(strange_words))
    print("done with fill_matrix(...)")
    
def start_readout (host, port, q, forwarding_enable, stop_event, buffer_size=9000):
    # starts the readout and puts it on stand by 
    # set forwarding_enable in order to switch it fully on.
    
    forwarding_enable.clear()
    stop_event.clear()
    
    args = (host, port, q, forwarding_enable, stop_event, buffer_size) 
    
    recv_thread = threading.Thread(target=udp_receive, args=args)
    recv_thread.start() 
    print("Readout started")
        


        
def read_nFrames (qInput, qOutput, forwarding_enable, nFrames=5000):
    
    #qInput must be the q as provided to udp_receive
    #qOutput is to contain a certain and controlled number of frames
    nFramesRecorded=0 
    #Stop data taking
    forwarding_enable.clear()
    
    #flush queues in order to avoid that data taken with different
    #settings are mixed.
    
    while not qInput.empty():
        packet=qInput.get()
        
    while not qOutput.empty():
        packet=qOutput.get()
    
    #Activate data taking
    forwarding_enable.set()
    
    #Receive packets until nFrames frames are recorded
    while True:
        #Keep listening even if data is missing
        
        while not qInput.empty():
            #if there is some data, scan it for frame headers and count them
            packet = qInput.get()
            for word in mimosis_words(packet['payload']):
                #print(word.hex())
                
                if word.startswith(b'\x00\x0b'): #Frame Header found
                    nFramesRecorded+=1
                    if ((nFramesRecorded %100) == 0):
                        print("Frames Recorded = ",nFramesRecorded)
            #and copy the related packet to the output buffer            
            qOutput.put(packet)
            
            #in case all frames are taken stop working
            if nFramesRecorded>nFrames: break
        
        #Just in case the input buffer was running empty, sleep in order 
        #to collect new data with reduced CPU load
        time.sleep(0.01)
        
        #And if we are full, stop listening
        if nFramesRecorded>nFrames: break

    #put data taking to stand by    
    forwarding_enable.clear()