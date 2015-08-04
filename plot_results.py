# Plot results ADDA

from pylab import *
import numpy as np
import os
import glob
from time import sleep

folder = '75.0X25.0'
current_folder = os.getcwd()

while True:
    files = glob.glob(current_folder + '/' + folder + '/*.dat')
    for j in range(len(files)):
        data = np.loadtxt(files[j])
        plot(data[:,0],data[:,4]-data[:,2],'.')
        xlabel('Wavelength (nm)')
        ylabel('Intensity (A.U.)')
        draw()
    sleep(20)
    print('Repeat')

