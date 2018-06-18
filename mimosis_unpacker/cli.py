#!/usr/bin/env python

# internal modules
import mimosis_unpacker
import mimosis_unpacker.output

# external deps
import click
# click is used to control the command flow from the command line.
# It defined different options to mimosis_unpacker.


import numpy as np

# Python stdlib
import queue, threading, time

# click.group generates a group of commands, which may be carried out from the
# text interpreter. Those commands are


# Defines the host command
@click.group()
@click.option('--host', required=True, help='Host to listen on.')
@click.option('--port', default=40000, help='Port to listen on.')
@click.option('--buffer-size', default=9000, help='Buffer size for the UDP packets.')
@click.pass_context
def cli(ctx, host, port, buffer_size):
    #Builds an object, which contains information on the sender of the data.
    #The arguments host, port, buffer_size are taken from the command line.
    #Host is mandatory, the other parameters are non-madatory.
    #The results are filled into the object ctx, which is called by the main program.
    ctx.obj['HOST'] = host
    ctx.obj['PORT'] = port
    ctx.obj['BUFFER_SIZE'] = buffer_size

# Defines the interval command
@cli.command()
@click.pass_context
@click.option('--interval', default=1.0, help='The interval to print the stats.')
def timed_stats(ctx, interval):
    """
    Reads data from the readout system located at a given host and port.
    The reading process is done in a dedicated thread, which appears to run permanently (no stopping condition found).
    The data received is processed in a second thread.
    """

    # Opens a thread safe queue (= FIFO)
    q = queue.Queue()

    # start recv thread
    args = (ctx.obj['HOST'], ctx.obj['PORT'], q, ctx.obj['BUFFER_SIZE'])
    recv_thread = threading.Thread(target=mimosis_unpacker.udp_receive, args=args)
    recv_thread.start()
    # start print thread
    stats_thread = threading.Thread(target=mimosis_unpacker.timed_queue_stats, args=(q, interval))
    stats_thread.start()

#Defines the output file and activates reading data.
@cli.command()
@click.pass_context
@click.option('--filename', default='output.png', help='The output filename.')
def matrix_image(ctx, filename):
    q = queue.Queue()
    # start recv thread
    args = (ctx.obj['HOST'], ctx.obj['PORT'], q, ctx.obj['BUFFER_SIZE'])
    recv_thread = threading.Thread(target=mimosis_unpacker.udp_receive, args=args, daemon=True)
    recv_thread.start()
    # start fill matrix thread
    stop_event = threading.Event()
    m = np.ndarray(shape=(32, 504), dtype=np.uint64)
    fill_matrix_thread = threading.Thread(target=mimosis_unpacker.fill_matrix, args=(q, m, stop_event))
    fill_matrix_thread.start()
    try:
        while True: time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    stop_event.set()
    fill_matrix_thread.join()
    mimosis_unpacker.output.save_matrix_outputs(m, filename)

#The main program. Does essentially nothing as everything is done by click
def main():
    cli(obj={})

if __name__ == "__main__":
    main()
