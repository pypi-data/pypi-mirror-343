import os
import unittest
import numpy as np
import pandas as pd

import pymyami

TEST_TOLERANCE = 5  # maximum % difference from original

class MyAMI_V1_crosscheck(unittest.TestCase):

    def test_seawater_correction(self):
        checkfile = os.path.join(os.path.dirname(__file__), 'data/MyAMI_V1_seawatercorrection_checkvals.csv')
        print(checkfile)
        check = pd.read_csv(checkfile, index_col=0)
        check.columns = ['T', 'S', 'Ca', 'Mg', 'KspC', 'K1', 'K2', 'KW', 'KB', 'KspA', 'K0', 'KS']

        new_seawater_correction = pymyami.calculate_seawater_correction(Sal=check.S.values, TempC=check['T'].values, Ca=check.Ca.values, Mg=check.Mg.values)

        Ks = 'K0', 'K1', 'K2', 'KW', 'KB', 'KspA', 'KspC', 'KS'

        print(f'Comparing seawater correction to MyAMI_V1 (must be <{TEST_TOLERANCE:.1f}% max difference)')
        for k in Ks:
            v1 = check[k]
            new = new_seawater_correction[k]

            rdiff = (v1 - new) / v1  # relative difference
            
            maxpercentdiff = 100 * np.max(np.abs(rdiff))
            avgpercentdiff = 100 * np.mean(rdiff)
            
            print(f'  {k}: {maxpercentdiff:.2f}% max, {avgpercentdiff:.2f}% avg')
            self.assertLess(maxpercentdiff, TEST_TOLERANCE, msg=f'Maximum difference in {k} correction factor too large: {maxpercentdiff}%')

if __name__ == "__main__":
    unittest.main()
