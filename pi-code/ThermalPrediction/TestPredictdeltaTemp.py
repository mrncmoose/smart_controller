'''
Created on Feb 19, 2018

@author: fdunaway
'''
import unittest
from ThermalPrediction import PredictDeltaTemp


class Test(unittest.TestCase):


    def testdeltaTemp(self):
        uot = PredictDeltaTemp.thermalCalculations
        self.assertAlmostEqual(2.70, uot.deltaTemp(self, 1000), 2, 'Incorrect detlaT')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()