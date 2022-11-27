import math
from tokenize import Double
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import uproot
import numpy
import numpy.random as rand

# Works by generating many random plane waves


ts_length = 7200 # seconds
samp_rate = 1 # sampling rate
amp_x = 1
amp_y = 1
noise = 1
theta_1 = -45
theta_2 = 75
theta_3 = 8

ang_freq = 2*math.pi*(1/1000)
relative_phase_shift = math.pi/2
absolute_phase_shift = 0

k = [0, 0, 1]

T = []
X = []
Y = []
Z = []

# Generate Parameters for Noise Plane Waves
num_sigs = 20
sigs = []
for i in range(0,num_sigs):
    sigs.append([.2*rand.ranf(), 2*math.pi*.02*rand.ranf(), 2*math.pi*rand.ranf(),
    720*(rand.ranf()-.5),720*(rand.ranf()-.5),720*(rand.ranf()-.5)])
#sigs = []

def wave_generator(t: Double, w: Double, phi: Double, s: Double) -> Double:
    return math.cos(w*t - phi - s)


# Script

r = R.from_euler('zxz', [theta_1, theta_2, theta_3], degrees=True)
k = r.apply(k)

# Generate Signal
for i in range(0, ts_length*samp_rate - 1):
    x = amp_x*wave_generator(i/samp_rate, ang_freq, 0, absolute_phase_shift)
    y = amp_y*wave_generator(i/samp_rate, ang_freq, relative_phase_shift, absolute_phase_shift)
    z = 0
    f = [x, y, z]
    f = r.apply(f)
    X.append(f[0])
    Y.append(f[1])
    Z.append(f[2])
    T.append(float(i/samp_rate))

# Add Noise
for i in sigs:
    for j in range(0, ts_length*samp_rate - 1):
        [.2*rand.ranf(), 2*math.pi*.02*rand.ranf(), 2*math.pi*rand.ranf(),
    720*(rand.ranf()-.5),720*(rand.ranf()-.5),720*(rand.ranf()-.5)]
        
        x = rand.ranf()*wave_generator(j/samp_rate, 2*math.pi*.02*rand.ranf(), 0, 2*math.pi*rand.ranf())
        y = rand.ranf()*wave_generator(j/samp_rate, 2*math.pi*.02*rand.ranf(), relative_phase_shift, 2*math.pi*rand.ranf())
        z = wave_generator(i/samp_rate, 0, 0, math.pi/2)
        f = [x, y, z]
        f = r.apply(f)
        X.append(f[0])
        Y.append(f[1])
        Z.append(f[2])



plt.plot(T, X)
plt.plot(T, Y)
plt.plot(T, Z)

plt.savefig('Plane_Wave_Datasets/foo.png', bbox_inches='tight')

with uproot.recreate("Plane_Wave_Datasets/ts1.root", compression = None) as f:
    f["x_data"] = " ".join(str(x) for x in X)
    f["y_data"] = " ".join(str(y) for y in Y)
    f["z_data"] = " ".join(str(z) for z in Z)
    f["timeseries_length"] = str(ts_length)
    f["sampling_rate"] = str(samp_rate)
    f["x_amplitude"] = str(amp_x)
    f["y_amplitude"] = str(amp_y)
    f["angular_frequency"] = str(ang_freq)
    f["relative_phase_shift"] = str(relative_phase_shift)
    f["absolute_phase_shift"] = str(absolute_phase_shift)
    f["theta_1"] = str(theta_1)
    f["theta_2"] = str(theta_2)
    f["theta_3"] = str(theta_3)
    f["kx"] = str(k[0])
    f["ky"] = str(k[1])
    f["kz"] = str(k[2])

"""
with uproot.open("Plane_Wave_Datasets/ts1.root") as f:
    print(f.classnames())
    print([float(n) for n in f["x_data"].split()])
"""
