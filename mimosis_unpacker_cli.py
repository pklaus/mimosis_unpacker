#!/usr/bin/env python

# internal modules
import mimosis_unpacker

# external deps
import click
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.misc

# Python stdlib
import queue, threading, time


@click.group()
@click.option('--host', required=True, help='Host to listen on.')
@click.option('--port', default=40000, help='Port to listen on.')
@click.option('--buffer-size', default=9000, help='Buffer size for the UDP packets.')
@click.pass_context
def cli(ctx, host, port, buffer_size):
    ctx.obj['HOST'] = host
    ctx.obj['PORT'] = port
    ctx.obj['BUFFER_SIZE'] = buffer_size

@cli.command()
@click.pass_context
@click.option('--interval', default=1.0, help='The interval to print the stats.')
def timed_stats(ctx, interval):
    q = queue.Queue()
    # start recv thread
    args = (ctx.obj['HOST'], ctx.obj['PORT'], q, ctx.obj['BUFFER_SIZE'])
    recv_thread = threading.Thread(target=mimosis_unpacker.udp_receive, args=args)
    recv_thread.start()
    # start print thread
    stats_thread = threading.Thread(target=mimosis_unpacker.timed_queue_stats, args=(q, interval))
    stats_thread.start()

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
    m = np.ndarray(shape=(64,1024), dtype=np.float)#np.uint64)
    stop_event = threading.Event()
    fill_matrix_thread = threading.Thread(target=mimosis_unpacker.fill_matrix, args=(q, m, stop_event))
    fill_matrix_thread.start()
    try:
        while True: time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    stop_event.set()
    fill_matrix_thread.join()
    m = m[0:15, :]
    m_nan = m.copy()
    m_nan[m_nan == 0.] = np.nan
    # save matplotlib plot
    plt.figure(figsize=(40,10))
    plt.imshow(m_nan, interpolation='nearest')
    plt.colorbar()
    plt.savefig(filename)
    print("saved", filename)
    # save 1:1 image
    # https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.misc.imsave.html
    # https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.misc.toimage.html
    m = np.log10(m_nan)
    m = np.interp(m, (np.nanmin(m), np.nanmax(m)), (0, 255))
    np.nan_to_num(m, copy=False)
    m = m.astype(np.uint64)
    print(m)
    scipy.misc.imsave(filename + ".scipy.png", m)
    print("saved", filename + ".scipy.png")

if __name__ == "__main__": cli(obj={})
