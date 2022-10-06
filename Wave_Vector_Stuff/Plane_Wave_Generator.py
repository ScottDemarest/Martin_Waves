import cmath
from numbers import Complex
from tokenize import Double
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R

ts_length = 10 # seconds
samp_rate = 100 # sampling rate
amp_x = 1
amp_y = 1

ang_freq = 1
phase_shift_y = cmath.pi/2

Xp = []
Yp = []
Zp = []
T = []

def wave_generator(t: Double, w: Double, phi: Double) -> Complex:
    i = 1j
    return cmath.exp(i*(w*t - phi))

f = [amp_x*wave_generator(0, ang_freq, 0), amp_y*wave_generator(0, ang_freq, phase_shift_y), 0]
r = R.from_euler('zxz', [5, 5, 5], degrees=True)

print(f)
print(r.apply(f))
print(r.apply(f)[0])

# Script
"""
for i in range(0, ts_length*samp_rate):
    Xp.append(amp_x*wave_generator(i/samp_rate, ang_freq, 0))
    Yp.append(amp_y*wave_generator(i/samp_rate, ang_freq, phase_shift_y))
    Zp.append(0)
    T.append(i/samp_rate)


r = rotate('zxz', [5, 5, 5], degrees=True)



#print(Xp)
Xr = [item.real for item in Xp]
Xi = [item.imag for item in Xp]
Yr = [item.real for item in Yp]
plt.plot(T, Xr)
plt.plot(T, Yr)

plt.savefig('Plane_Wave_Datasets/foo.png', bbox_inches='tight')


"""