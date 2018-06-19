#!/usr/bin/env python

# internal modules
#none yet

# external deps
#none yet

# Python stdlib
import socket, time, queue
from collections import Counter
from datetime import datetime as dt


def udp_receive(host, port, q, forwarding_enable, stop_event, buffer_size=9000):
    """ q: queue.Queue() to put the data to """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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

def fill_matrix(q, m, stop_event):
    """ q: queue.Queue, m: np.ndarray, stop_event: threading.Event() """

    strange_words = Counter()
    while not stop_event.is_set():
        while not q.empty():
            qsize = q.qsize()
            if qsize > 1: print("Queue (FIFO buffer) size > 1: ", qsize)
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
