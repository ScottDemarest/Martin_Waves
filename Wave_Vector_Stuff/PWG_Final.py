import math
from tokenize import Double
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import uproot
import numpy
import numpy.random as rand
from scipy import signal
import numpy as np

# Works by generating a signal plane wave and adding random noise

ts_length = 7200 # seconds
samp_rate = 1 # sampling rate
amp_x = 1
amp_y = 1
noise = .3
theta_1 = -45
theta_2 = 75
theta_3 = 155

ang_freq = 2*math.pi*(1/1000)
relative_phase_shift = math.pi/2
absolute_phase_shift = 0

k = [0, 0, 1]

T = []
X = []
Y = []
Z = []


def noise_generator():
    sigs = []
    for i in range(0,10):
            sigs.append([rand.ranf()*noise, 2*math.pi*samp_rate*.01*rand.ranf(), 2*math.pi*rand.ranf()])
    #sigs = []
    return sigs

def wave_generator(t: Double, w: Double, phi: Double, s: Double, sigs: list) -> Double:
    #x = signal.gausspulse(w*(t-ts_length/2) - phi, fc=20) 
    x = math.cos(w*t - phi - s)
    
    for i in sigs:
        x = x + i[0]*math.cos(i[1]*t - i[2])

    return float(x)



# Script

r = R.from_euler('zxz', [theta_1, theta_2, theta_3], degrees=True)
k = r.apply(k)

s1 = noise_generator()
s2 = noise_generator()
s3 = noise_generator()

for i in range(0, ts_length*samp_rate - 1):
    x = amp_x*wave_generator(i/samp_rate, ang_freq, 0, absolute_phase_shift, s1)
    y = amp_y*wave_generator(i/samp_rate, ang_freq, relative_phase_shift, absolute_phase_shift, s2)
    z = wave_generator(i/samp_rate, 0, 0, math.pi/2, s3)
    f = [x, y, z]
    f = r.apply(f)
    X.append(f[0])
    Y.append(f[1])
    Z.append(f[2])
    T.append(float(i/samp_rate))

plt.plot(T, X)
plt.plot(T, Y)
plt.plot(T, Z)

plt.savefig('Plane_Wave_Datasets/foo.png', bbox_inches='tight',dpi=300)


freq = np.linspace(.00001, .02*samp_rate/2, 100)

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
    f["freq"] = {"deets":freq}

"""
with uproot.open("Plane_Wave_Datasets/ts1.root") as f:
    print(f.classnames())
    print([float(n) for n in f["x_data"].split()])
"""
