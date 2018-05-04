#!/usr/bin/env python

# internal modules
import mimosis_unpacker

# external deps
import click

# Python stdlib
import queue, threading


@click.command()
@click.option('--host', help='Host to listen on.')
@click.option('--port', default=40000, help='Port to listen on.')
@click.option('--buffer-size', default=9000, help='Buffer size for the UDP packets.')
def run(host, port, buffer_size):
    q = queue.Queue()
    # start recv thread
    recv_thread = threading.Thread(target=mimosis_unpacker.udp_receive, args=(host, port, q, buffer_size))
    recv_thread.start()
    # start print thread
    stats_thread = threading.Thread(target=mimosis_unpacker.timed_queue_stats, args=(q, ))
    stats_thread.start()


if __name__ == "__main__": run()
