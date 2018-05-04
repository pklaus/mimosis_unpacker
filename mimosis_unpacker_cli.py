#!/usr/bin/env python

import socket
import click

@click.command()
@click.option('--host', help='Host to listen on.')
@click.option('--port', default=40000, help='Port to listen on.')
def run(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    while True:
        data, addr = sock.recvfrom(4096)
        print("received message of length:", len(data))

if __name__ == "__main__": run()
