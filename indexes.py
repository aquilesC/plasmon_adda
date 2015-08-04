import numpy as np
from scipy import interpolate # For spline interpolation

class Au_index():
    def __init__(self):                
        #Read the file
        data = np.loadtxt('METALS_Gold_Johnson.txt',skiprows=1,unpack=True)
        wavelength = data[0]
        real_index = data[1]
        imag_index = data[2]
        # Spline interpolation of real and imaginary parts        
        ind = wavelength.argsort()
        wavelength = wavelength[ind]
        real_index = real_index[ind]
        imag_index = imag_index[ind]
        self.real_tck = interpolate.splrep(wavelength,real_index)
        self.imag_tck = interpolate.splrep(wavelength,imag_index)
        
    def r_i(self,wavelength):   
        """ Returns the real and imaginary values of the refractive index evaluated in the desired
        wavelength. 
        """
        real = float(interpolate.splev(wavelength,self.real_tck))
        imaginary = float(interpolate.splev(wavelength,self.imag_tck))
        return complex(real,imaginary)
    
class H2O_index():
    def __init__(self):                
        #Read the file
        data = np.loadtxt('LIQUIDS_Water_Hale.txt',skiprows=1,unpack=True)
        wavelength = data[0]
        real_index = data[1]
        imag_index = data[2]
        # Spline interpolation of real and imaginary parts        
        ind = wavelength.argsort()
        wavelength = wavelength[ind]
        real_index = real_index[ind]
        imag_index = imag_index[ind]
        self.real_tck = interpolate.splrep(wavelength,real_index)
        self.imag_tck = interpolate.splrep(wavelength,imag_index)
        
    def r_i(self,wavelength):   
        """ Returns the real and imaginary values of the refractive index evaluated in the desired
        wavelength. 
        """
        real = float(interpolate.splev(wavelength,self.real_tck))
        imaginary = float(interpolate.splev(wavelength,self.imag_tck))
        return complex(real,imaginary)
