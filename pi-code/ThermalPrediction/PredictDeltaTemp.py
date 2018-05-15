'''
Created on Feb 18, 2018

@author: fdunaway
'''

class thermalCalculations:
    
# Formula to calculate thermal rise rate:
#f(x)=1.11676445E-14 * x^4 - 1.313037E-10 * x^3 + 4.08270207E-07 * x^2 + 0.00141231184 * x + 0.9994399220259089
# takes the number of seconds and returns the temperature rise of the heater.
    def deltaTemp(self, nSeconds):
        return ((1.11676445E-14 * nSeconds ** 4) 
                - (1.313037E-10 * nSeconds ** 3) 
                + (4.08270207E-7 * nSeconds ** 2) 
                + (0.00141231184 * nSeconds)
                + 0.9994399220259089)
    
#dTimeSeconds = 1000
#dTempC = deltaTemp(dTimeSeconds)

#print('Expected temperature rise for {:1.2f} seconds is {:1.2f} C'.format(dTimeSeconds, dTempC))
