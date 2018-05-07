#!/usr/bin/env python

# internal modules
#none yet

# external deps
#none yet

# Python stdlib
import socket, time, queue
from datetime import datetime as dt


def udp_receive(host, port, q, buffer_size=9000):
    """ q: queue.Queue() to put the data to """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    while True:
        # potentially more efficient: sock.recvfrom_into(buf)
        data, addr = sock.recvfrom(buffer_size)
        if data:
            q.put({'ts': dt.now(), 'payload': data, 'addr': addr})
    print("done with udp_receive(...)")

def timed_queue_stats(q, interval=1.0):
    last = time.time()
    while True:
        while (time.time() - last) < interval:
            time.sleep(0.01)
        last += interval
        all_packets = []
        while not q.empty():
            all_packets.append(q.get())
        total_payload_len = sum(len(packet['payload']) for packet in all_packets)
        print("Received ", total_payload_len, " bytes in the last ", interval, " seconds.")
        print("Data Rate: {dr:.3f} Mbit/s".format(dr=8*total_payload_len/interval*1e-6))
        print("Number of packets received: ", len(all_packets))
        print("Packet Rate: {pr:.1f} pkts/s".format(pr=len(all_packets)/interval))
