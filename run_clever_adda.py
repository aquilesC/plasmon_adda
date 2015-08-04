"""
    runs ADDA package in a clever way, minimizing the calculations in places 
    where no spectral features are present.. 
"""

from numpy import linspace, array, savetxt, column_stack, abs
from subprocess import check_output
from indexes import Au_index, H2O_index
import os
import sys 

filename = sys.argv[1] # The filename of the config file for the simulations

conf_param = []
# Reads the parameters and ignores the comments
for line in open(str(filename)):
    li = line.strip()
    if not li.startswith("#"):
        conf_param.append(line.rstrip())
    
starting_wavelength = int(conf_param[0])
init_length = float(conf_param[1])
init_width = float(conf_param[2])
etching = float(conf_param[3])

print("Starting Simulation with the following parameters:")
print("Starting wavelength: {}nm.".format(starting_wavelength))
print("Initial length: {}nm. Initial width: {}nm".format(init_length, init_width))
print("Etching step: {}nm. Total number of simulations: {}\n".format(etching, number_simulations))



#total_wl = 200 # Total number of wavelengths
#start_wl = 600 # Starting wavelength in nm
#stop_wl = 800  # Ending wavelength in nm


gold = Au_index()
water = H2O_index()


#init_length = 60 # Initial length in nm
#init_width = 25 # Initial width in nm
#etching = .5 # Etching rate between simulations
#number_simulations = 20

directory = str(init_length) + "X" + str(init_width)

if not os.path.exists(directory):
    os.mkdir(str(init_length) + "X" + str(init_width))

# Variables to store the data
Q_abss = []
C_abss = []
Q_extt = []
C_extt = []
wavelength = []
length = init_length
width = init_width
AR = (length-width)/width # Definition of ADDA for Aspect Ratio
run_simulation = True # Need to define a criteria for stopping the simulations
i = 0
peak = False # To mark if gone through the peak
wl_start_peak = 0
difference = 0
while run_simulation:
    if i == 0: # First simulation
        wl = starting_wavelength/1000 # change wl to micrometers
        i = i+1
    elif i == 1:
        wl = wl + 15./1000 # Second simulation is 15nm away from the first
        i=i+1
    else:
        # Calculate the next wavelength based on the available information
        deltay = Q_ext[i-1]-Q_ext[i-2]
        deltax = wavelength[i-1]-wavelength[i-2]
        difference = abs(deltay/deltax) # Slope
        # If hasn't reached the peak yet
        if not peak:
            if difference < 0.05:
                wl = wl + 15./1000 
            if difference >= 0.05 and difference < 0.09:
                wl = wl + 10./1000
            if difference >= 0.09 and difference < 0.20:
                wl = wl + 5./1000
            if difference >= 0.20:
                wl = wl + 2./1000
                if deltay/deltax > 0:
                    peak = True
                    wl_start_peak = wl*1000

        # Once the peak is reached, the simulations continue in small steps
        else:
            wl = wl + 2./1000
            # Once we reach the side of the peak we continue with usual parameters
            if deltay/deltax < 0 and difference >= 0.20:
                peak = False
        
        # Criteria for stopping the simulation. Namely it should be 100nm passed the peak
        if wl_start_peak != 0 and wl*1000-wl_start_peak > 100:
            run_simulation = False
        i = i+1
          
            
    wavelength.append(wl*1000)    
    print('    --->{} with wavelength {}nm. and delta {}.'.format(i,wl*1000,difference))

    # Now is time for the simulations

    medium_n = 1.3330 # Refractive index of Water
    gold_n = gold.r_i(wl) # Refractive index of Gold

    # Normalize according to medium refractive index
    wl1 = wl/medium_n
    gold_n = gold_n / medium_n
    
    stdout = check_output("adda -shape capsule " + str(AR) + " -size " + str(width/1000) + " -grid 16 -orient 0 90 0 -lambda " + str(wl1) + " -m " + str(gold_n.real) + " " + str(gold_n.imag),shell=True)
    std = str(stdout)
    std = std.split('\n')
    Q_abss.append(float(std[-2].split("\t=")[1]))
    C_abss.append(float(std[-3].split("\t=")[1]))
    Q_extt.append(float(std[-4].split("\t=")[1]))
    C_extt.append(float(std[-5].split("\t=")[1]))
    
    Q_abs = array(Q_abss)
    C_abs = array(C_abss)
    Q_ext = array(Q_extt)
    C_ext = array(C_extt)
    
    data = column_stack([wavelength[0:i+1], C_ext, C_abs, Q_ext, Q_abs])
    savetxt(directory + "/Data_" + str(length) + "X" + str(width) + ".dat",data) # Saves data in each iteration so it is easy to check the progress
    

#"mpiexec -n 2 -host localhost ../mpi/adda_mpi
#../seq/adda
