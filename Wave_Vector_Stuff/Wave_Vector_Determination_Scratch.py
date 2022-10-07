import numpy as np
import uproot
import matplotlib.pyplot as plt
import math

#fd = np.linspace(0, 10, 10)


with uproot.open("Plane_Wave_Datasets/ts1.root") as f:
    x = [float(n) for n in f["x_data"].split()]
    y = [float(n) for n in f["y_data"].split()]
    z = [float(n) for n in f["z_data"].split()]
    kx = float(f["kx"])
    ky = float(f["ky"])
    kz = float(f["kz"])


X = np.fft.fft(x)
Y = np.fft.fft(y)
Z = np.fft.fft(z)

X = X[0: len(X) - 30]
Y = Y[0: len(Y) - 30]
Z = Z[0: len(Z) - 30]


Xr = [item.real for item in X]
Yr = [item.real for item in Y]
Zr = [item.real for item in Z]
plt.plot(np.absolute(X))
plt.savefig('Plane_Wave_Datasets/fft.png', bbox_inches='tight')

#print(np.amax(np.absolute(X)))
#print(np.amax(np.absolute(Y)))
#print(np.amax(np.absolute(Z)))
#print(np.argmax(Xr))

print(kx)
print(ky)
print(kz)

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