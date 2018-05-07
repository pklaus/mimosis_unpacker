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
        duration = time.time() - last
        last += interval
        all_packets = []
        while not q.empty():
            all_packets.append(q.get())
        total_payload_len = sum(len(packet['payload']) for packet in all_packets)
        print("Received {} bytes in the last {:.3f} seconds.".format(total_payload_len, duration))
        print("Data Rate: {dr:.3f} Mbit/s".format(dr=8*total_payload_len/duration*1e-6))
        print("Number of packets received: ", len(all_packets))
        print("Packet Rate: {pr:.1f} pkts/s".format(pr=len(all_packets)/duration))
        print("=======================")

def fill_matrix(q, m, stop_event):
    """ q: queue.Queue, m: np.ndarray, stop_event: threading.Event() """

    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    while not stop_event.is_set():
        while not q.empty():
            qsize = q.qsize()
            if qsize > 1: print(qsize)
            #print("begin of packet")
            packet = q.get()
            length = len(packet['payload'])
            length = length // 4 * 4
            for chunk in chunks(packet['payload'][0:length], 4):
                if chunk.startswith(b'\x00\x0b'):
                    #print("BEGIN of new frame")
                    pass
                else:
                    #print("0x{0:02X}{1:02X}".format(chunk[2], chunk[3]))
                    #col = chunk[2]
                    col = (chunk[2] & 0b11111100) >> 2
                    #row = chunk[3]
                    row = ((chunk[2] & 0b11) << 8) + chunk[3]
                    #print((col, row))
                    m[col, row] += 1
            #print("end of packet")
    print("done with fill_matrix(...)")
