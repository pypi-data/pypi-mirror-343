from matplotlib import pyplot as plt
import numpy as np

def plot_signal(sig_arr:np.ndarray, fs=None,
                figsize=(20,4), xlim=[0,-1], ylim=[None, None]):
    plt.figure(figsize=figsize)
    
    sig_arr_len = len(sig_arr)
    x_axis = np.linspace(0, sig_arr_len/fs, sig_arr_len) if fs is not None else np.arange(sig_arr_len, dtype=np.int32)
    
    plt.plot(x_axis, sig_arr)
    # xlim setting
    if xlim[1] == -1:
        xlim[1] = x_axis[-1]
    plt.xlim(xlim)
    # ylim setting
    sig_plot_range = sig_arr[xlim[0]:xlim[1]] if fs is None else sig_arr[int(xlim[0]*fs):int(xlim[1]*fs)]
    if None in ylim:
        mn, mx = sig_plot_range.min(), sig_plot_range.max()
        dynamic_range = abs(mn-mx)
        if ylim[0] is None:
            ylim[0] = mn - dynamic_range*0.05
        if ylim[1] is None:
            ylim[1] = mx + dynamic_range*0.05
    plt.ylim(ylim)
    
    plt.grid()