import cmath
from numbers import Complex
from tokenize import Double
from typing import Dict
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import uproot
import numpy

ts_length = 10 # seconds
samp_rate = 100 # sampling rate
noise_scale = 1
amp_x = 1
amp_y = 1

theta_1 = 10
theta_2 = 20
theta_3 = 30

ang_freq = 1
phase_shift_y = cmath.pi/2

X = numpy.empty(1, dtype=numpy.complex_)
Y = numpy.empty(1, dtype=numpy.complex_)
Z = numpy.empty(1, dtype=numpy.complex_)
T = numpy.empty(1)

def wave_generator(t: Double, w: Double, phi: Double) -> Complex:
    i = 1j
    return cmath.exp(i*(w*t - phi))*noise_scale*numpy.random.normal(0, .01)



# Script

r = R.from_euler('zxz', [theta_1, theta_2, theta_3], degrees=True)

for i in range(0, ts_length*samp_rate):
    x = amp_x*wave_generator(i/samp_rate, ang_freq, 0)
    y = amp_y*wave_generator(i/samp_rate, ang_freq, phase_shift_y)
    z = 0
    f = [x, y, z]
    f = r.apply(f)
    X = numpy.append(X,f[0])
    numpy.append(Y,f[1])
    numpy.append(Z,f[2])
    numpy.append(T,i/samp_rate)

print(len(X))
with uproot.recreate("Plane_Wave_Datasets/ts1.root", compression = None) as f:
    f["metadata"] = {"x data":X}
    #f["metadata"] = {"timeseries_length": ts_length, "sampling_rate": samp_rate, "x_amplitude": amp_x, "y_amplitude": amp_y, "angular_frequency": ang_freq, "phase_shift": phase_shift_y, "theta_1": theta_1, "theta_2": theta_2, "theta_3": theta_3}
    #f["tree"] = uproot.newtree({"metadata": Dict, "x_timeseries": list[Complex], "y_timeseries": list[Complex],"z_timeseries": list[Complex]})
    #f["tree"].extend({"metadata": {"timeseries_length": ts_length, "sampling_rate": samp_rate, "x_amplitude": amp_x, "y_amplitude": amp_y, "angular_frequency": ang_freq, "phase_shift": phase_shift_y, "theta_1": theta_1, "theta_2": theta_2, "theta_3": theta_3}, "x_timeseries": X, "y_timeseries": Y,"z_timeseries": Z,})

with uproot.open("Plane_Wave_Datasets/ts1.root") as f:
    print(f.classnames())
    print(f["metadata"])

"""
#print(Xp)
Xr = [item.real for item in Xp]
Xi = [item.imag for item in Xp]
Yr = [item.real for item in Yp]
plt.plot(T, Xr)
plt.plot(T, Yr)

plt.savefig('Plane_Wave_Datasets/foo.png', bbox_inches='tight')


"""