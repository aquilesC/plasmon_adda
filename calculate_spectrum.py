from subprocess import check_output
from indexes import Au_index, H2O_index
gold = Au_index()
length = 60.
width = 25.
AR = (length-width)/width # Definition of ADDA for Aspect Ratio
medium_n = 1.3330 # Refractive index of Water 
Q_abss = []
C_abss = []
Q_extt = []
C_extt = []

for wavelength in range(500,800):
	wl = wavelength/1000 # change wl to micrometers
	    
	gold_n = gold.r_i(wl)
	wl = wl/medium_n
	gold_n = gold_n / medium_n

	stdout = check_output("adda -shape capsule " + str(AR) + " -size " + str(width/1000) + " -grid 16 -orient 0 90 0 -lambda " + str(wl) + " -m " + str(gold_n.real) + " " + str(gold_n.imag),shell=True)

	# Format the output to a usable format
	std = str(stdout)
	std = std.split('\n')
	Q_abss.append(float(std[-2].split("\t=")[1]))
	C_abss.append(float(std[-3].split("\t=")[1]))
	Q_extt.append(float(std[-4].split("\t=")[1]))
	C_extt.append(float(std[-5].split("\t=")[1]))