# external deps
import numpy as np
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.misc

# Python stdlib
import os

def add_to_file_name(old_name, addition):
    fragments = os.path.splitext(old_name)
    return fragments[0] + addition + fragments[1]

def save_matrix_outputs_win(m, filename):
    m = m.astype(np.float)
    m = m[0:32, :]
    m_nan = m.copy()
    m_nan[m_nan == 0.] = np.nan
    # save matplotlib plot
    plt.figure(figsize=(40,10))
    plt.imshow(m_nan, interpolation='nearest')
    plt.colorbar()
    print("Trying to save: ", filename)
    plt.savefig(filename)
    print("saved", filename)
       
    
def save_matrix_outputs(m, filename):
    m = m.astype(np.float)
    m = m[0:32, :]
    m_nan = m.copy()
    m_nan[m_nan == 0.] = np.nan
    # save matplotlib plot
    plt.figure(figsize=(40,10))
    plt.imshow(m_nan, interpolation='nearest')
    plt.colorbar()
    print("Trying to save: ", filename)
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
    newname = add_to_file_name(filename, "_scipy")
    scipy.misc.imsave(newname , m)
    print("saved", newname)
    oldname = newname
    newname = add_to_file_name(oldname, "_color")
    os.system("to_color_scale -s tillscale {}".format(oldname))
    oldname = newname
    newname = add_to_file_name(oldname, "_3x6")
    os.system("convert {} -scale 300%x600% {}".format(oldname, newname))

