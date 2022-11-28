from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
"""
t = np.linspace(0, 1, 200, endpoint=False)

sig  = np.cos(2 * np.pi * 7 * t) #+ signal.gausspulse(t - 0.4, fc=2)

widths = np.arange(1, 61)

cwtmatr = signal.cwt(sig, signal.ricker, widths)

plt.imshow(cwtmatr, extent=[0, 1, 61, 1], cmap='PRGn', aspect='auto', vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
plt.savefig('Plane_Wave_Datasets/Wavelet_Test.png', bbox_inches='tight')
plt.show()
"""

from scipy import signal

import matplotlib.pyplot as plt

t, dt = np.linspace(0, 1, 200, retstep=True)

fs = 1/dt

w = 20.

#sig = np.cos(2*np.pi*10*t) + np.cos(2*np.pi*40*t)+5*signal.gausspulse(t - 0.5, fc=20)
sig = 5*signal.gausspulse(t - 0.5, fc=20)

freq = np.linspace(1, fs/2, 100)

widths = w*fs / (2*freq*np.pi)

cwtm = signal.cwt(sig, signal.morlet2, widths, w=w)

plt.pcolormesh(t, freq, np.abs(cwtm), cmap='viridis', shading='gouraud')
plt.savefig('Plane_Wave_Datasets/Wavelet_Test1.png', bbox_inches='tight')
plt.show()
