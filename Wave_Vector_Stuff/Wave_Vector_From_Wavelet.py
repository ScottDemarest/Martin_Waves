import numpy as np
import uproot
import matplotlib.pyplot as plt
import math
from scipy import signal


with uproot.open("Plane_Wave_Datasets/ts1.root") as f:
    x = [float(n) for n in f["x_data"].split()]
    y = [float(n) for n in f["y_data"].split()]
    z = [float(n) for n in f["z_data"].split()]
    kx = float(f["kx"])
    ky = float(f["ky"])
    kz = float(f["kz"])
    samp_rate = int(f["sampling_rate"])
    T = int(f["timeseries_length"])

print("starting")

w = 40.

freq = np.linspace(.00001, .01*samp_rate/2, 100)

widths = w*samp_rate / (2*freq*np.pi)
t = np.linspace(0, T-1,num=T-1, retstep=True)[0]
cwtm = signal.cwt(x, signal.morlet2, widths, w=w)

plt.pcolormesh(t, freq, np.abs(cwtm), cmap='viridis', shading='gouraud')
plt.savefig('Plane_Wave_Datasets/Wavelet_Test_X.png', bbox_inches='tight')
#plt.show()
print("x done")
cwtm = signal.cwt(y, signal.morlet2, widths, w=w)

plt.pcolormesh(t, freq, np.abs(cwtm), cmap='viridis', shading='gouraud')
plt.savefig('Plane_Wave_Datasets/Wavelet_Test_Y.png', bbox_inches='tight')
#plt.show()
print("y done")
cwtm = signal.cwt(z, signal.morlet2, widths, w=w)

plt.pcolormesh(t, freq, np.abs(cwtm), cmap='viridis', shading='gouraud')
plt.savefig('Plane_Wave_Datasets/Wavelet_Test_Z.png', bbox_inches='tight')
#plt.show()
print("z done")



XY = np.multiply(x, np.conjugate(y))
XZ = np.multiply(x, np.conjugate(z))
YZ = np.multiply(y, np.conjugate(z))

print(len(XY),len(XY[0])) # TODO: Elementwise Multiplication

print("done")


"""
Y = np.fft.fft(y)
Z = np.fft.fft(z)




Xr = [item.real for item in X]
Yr = [item.real for item in Y]
Zr = [item.real for item in Z]
plt.plot(np.absolute(X))
plt.savefig('Plane_Wave_Datasets/fft.png', bbox_inches='tight')


print(kx,ky,kz)

#assert np.argmax(Xr) == np.argmax(Yr) and np.argmax(Xr) == np.argmax(Zr)
m = np.argmax(Xr)

XY = np.multiply(X, np.conjugate(Y))
XZ = np.multiply(X, np.conjugate(Z))
YZ = np.multiply(Y, np.conjugate(Z))

a = XY[m].imag.real
b = XZ[m].imag.real
c = YZ[m].imag.real
mag = math.pow(a*a + b*b + c*c , .5)


Kx = c/mag
Ky = -1*b/mag
Kz = a/mag

Erx = 100*(Kx - kx)/kx
Ery = 100*(Ky - ky)/ky
Erz = 100*(Kz - kz)/kz

print(Kx,Ky,Kz)
print(Erx, Ery, Erz)
"""