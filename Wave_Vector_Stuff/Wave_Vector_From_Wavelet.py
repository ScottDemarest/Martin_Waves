import numpy as np
import uproot
import matplotlib.pyplot as plt
import math
from scipy import signal


with uproot.open("Plane_Wave_Datasets/Simulated_Data.root") as f:
    x = f["timeseries"]["x_data"].array()
    y = f["timeseries"]["y_data"].array()
    z = f["timeseries"]["z_data"].array()
    kx = f["signal_specs"]["kx"].array()[0]
    ky = f["signal_specs"]["ky"].array()[0]
    kz = f["signal_specs"]["kz"].array()[0]
    frequency = f["signal_specs"]["frequency"].array()
    samp_rate = f["ts_metadata"]["sampling_rate"].array()[0]
    T = f["ts_metadata"]["length"].array()[0]


print("starting")
# how do widths effect accuracy?
w = 40.

freq = np.linspace(.00001, .02*samp_rate/2, 100)

widths = w*samp_rate / (2*freq*np.pi)
t = np.linspace(0, T-1,num=T-1, retstep=True)[0]

w = int(w)

X = signal.cwt(x, signal.morlet2, widths, w=w)

plt.pcolormesh(t, freq, np.abs(X), cmap='viridis', shading='gouraud')
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.savefig('Plane_Wave_Datasets/X_Axis_Width_'+str(w)+'.png', bbox_inches='tight',dpi=300)
print("x done")
Y = signal.cwt(y, signal.morlet2, widths, w=w)

plt.pcolormesh(t, freq, np.abs(Y), cmap='viridis', shading='gouraud')
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.savefig('Plane_Wave_Datasets/Y_Axis_Width_'+str(w)+'.png', bbox_inches='tight',dpi=300)
print("y done")
Z = signal.cwt(z, signal.morlet2, widths, w=w)

plt.pcolormesh(t, freq, np.abs(Z), cmap='viridis', shading='gouraud')
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.savefig('Plane_Wave_Datasets/Z_Axis_Width_'+str(w)+'.png', bbox_inches='tight',dpi=300)
print("z done")


XY = np.multiply(X, np.conjugate(Y))
XZ = np.multiply(X, np.conjugate(Z))
YZ = np.multiply(Y, np.conjugate(Z))


plt.pcolormesh(t, freq, np.abs(XY), cmap='viridis', shading='gouraud')
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.savefig('Plane_Wave_Datasets/XY_Cross_Width_'+str(w)+'.png', bbox_inches='tight',dpi=300)
print("x done")

plt.pcolormesh(t, freq, np.abs(XZ), cmap='viridis', shading='gouraud')
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.savefig('Plane_Wave_Datasets/XZ_Cross_Width_'+str(w)+'.png', bbox_inches='tight',dpi=300)
print("y done")

plt.pcolormesh(t, freq, np.abs(YZ), cmap='viridis', shading='gouraud')
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.savefig('Plane_Wave_Datasets/YZ_Cross_Width_'+str(w)+'.png', bbox_inches='tight',dpi=300)
print("z done")

a = XY.imag.real
b = XZ.imag.real
c = YZ.imag.real
mag = np.sqrt(np.multiply(a,a) + np.multiply(b,b) + np.multiply(c,c))

Kx = np.divide(c,mag)
Ky = np.divide(b,(-1*mag))
Kz = np.divide(a,mag)



with uproot.recreate("Plane_Wave_Datasets/Simulated_Results_Wide_"+str(w)+".root", compression = None) as f:
    f["wavelet_transforms_abs"] = {"x": np.abs(X), "y": np.abs(Y), "z": np.abs(Z)}
    f["cross_spectra_abs"] = {"xy": np.abs(XY), "xz": np.abs(XZ), "yz": np.abs(YZ)}
    f["wave_vector_results"] = {"kx": Kx, "ky": Ky, "kz": Kz}
    f["true_wave_vector"] = {"kx": [kx], "ky": [ky], "kz": [kz]}
    f["signal_specs"] = {"frequency": [frequency]}
    f["sampling_rate"] = {"sampling_rate": [samp_rate]}


