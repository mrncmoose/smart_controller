'''
Created on Feb 19, 2018

@author: fdunaway

requires Python 3.5 or higher.
'''
import unittest
import sys

from ThermalPrediction import PredictDeltaTemp

class Test(unittest.TestCase):

    def testSecToTemp(self):
        uot = PredictDeltaTemp.thermalCalculations
        secsToTemp = uot.secondsToTemp(self, 8.8)
        print('Secs to temp:', secsToTemp, ' for 8.8C delta')
        self.assertAlmostEqual(5000, secsToTemp , -2, 'Incorrect number of seconds to temp')

    def testSecToTempLarger(self):
        uot = PredictDeltaTemp.thermalCalculations
        secsToTemp = uot.secondsToTemp(self, 20)
        print('Secs to temp:', secsToTemp, ' for 20C delta')
        self.assertAlmostEqual(8500, secsToTemp , -2, 'Incorrect number of seconds to temp')
        
    def testdeltaTemp(self):
        uot = PredictDeltaTemp.thermalCalculations
        #should pass:  2.70 degrees rise in 1000 seconds
        self.assertAlmostEqual(2.70, uot.deltaTemp(self, 1000), 2, 'Incorrect detlaT')

    def testNotDeltaTemp(self):
        uot = PredictDeltaTemp.thermalCalculations
        #~8.8 degrees rise in 5000 seconds.
        self.assertNotAlmostEqual(2.70, uot.deltaTemp(self, 5000), 2, 'Incorrect detlaT')
                               
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
