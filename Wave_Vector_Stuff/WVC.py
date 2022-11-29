import numpy as np
import uproot
import matplotlib.pyplot as plt
import math
from scipy import signal


with uproot.open("Plane_Wave_Datasets/Simulated_Results_Wide_40.root") as f:
    kx = f["wave_vector_results"]["kx"].array()
    ky = f["wave_vector_results"]["ky"].array()
    kz = f["wave_vector_results"]["kz"].array()
    Kx = f["true_wave_vector"]["kx"].array()[0]
    Ky = f["true_wave_vector"]["ky"].array()[0]
    Kz = f["true_wave_vector"]["kz"].array()[0]


freq_row = 10

fig, ax = plt.subplots()
plt.plot(kx[freq_row,:])
plt.plot(ky[freq_row,:])
plt.plot(kz[freq_row,:])
plt.plot(np.multiply(Kx,np.ones(len(kx[freq_row,:]))))
plt.plot(np.multiply(Ky,np.ones(len(ky[freq_row,:]))))
plt.plot(np.multiply(Kz,np.ones(len(kz[freq_row,:]))))

plt.xlabel("Time (s)")
plt.ylabel("Magnitude")
plt.title("Wave Vectors")
plt.legend(["kx","ky","kz"])
ax.set_ylim(-1,1)
plt.savefig('Plane_Wave_Datasets/Wave_Vector.png', bbox_inches='tight',dpi=300)

kx = np.average(kx[freq_row,:])
ky = np.average(ky[freq_row,:])
kz = np.average(kz[freq_row,:])
#print(kx*kx+ky*ky+kz*kz)
print(kx,ky,kz)
print(Kx,Ky,Kz)
#Erx = Kx-kx
#Ery = Ky-ky
#Erz = Kz-kz

Erx = 100*(Kx-kx)/Kx
Ery = 100*(Ky-ky)/Ky
Erz = 100*(Kz-kz)/Kz



print(Erx,Ery,Erz)

