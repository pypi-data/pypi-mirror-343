import unittest
import pandas as pd
import numpy as np
import copy

from povertyInequalityMeasures import inequality

def crazycat( df, times ):
    """
    This just creates an array which is `times` stacked copies of `df`
    """
    dof = copy.deepcopy(df)
    for i in range(0,times-1):
        dof = pd.concat([dof, df], axis=0)
    return dof

class TestPovertyMeasures(unittest.TestCase):
    def test_gini(self):
        """
        Test the gini coefficient function
        """
        data = pd.DataFrame({'total_expenditure': [7,10,15,18], 'weight':np.ones((4,), dtype=float)})
        result = inequality.get_gini(data, "total_expenditure","weight")
        self.assertEqual(result, 0.225)
    
    def test_palma(self):
        """
        Test the Palma coefficient function
        """
        data = pd.DataFrame({'total_expenditure': np.ones((10,), dtype=float), 'weight':np.ones((10,), dtype=float)})
        result = inequality.get_palma(data, "total_expenditure","weight")
        self.assertEqual(result, 0.25)

    def test_from_julia(self):
        """
        Test the headline poverty function
        """
        # tests from Julia version
        c1 = pd.DataFrame({'inc':[10, 15, 20, 25, 40, 20, 30, 35, 45, 90 ],'weight':np.ones(10)})
        c2 = crazycat( c1, 2) # 2x obs should be same
        c3 = copy.deepcopy( c1 )
        c3.loc[:,'weight'] = 10_000.0 # uniform weight should make no difference
        # very unbalanced copy of dataset 1 with 64 weight1 copies of 1:6 and 4 weight 64 7:10
        c64 = crazycat( c1.iloc[0:7], 64 )
        cx = copy.deepcopy(c1.iloc[7:])
        cx.weight = 64
        c64 = pd.concat( [c64, cx], axis=0 )
        gini1 = inequality.get_gini( data=c1, target_col='inc', weight_col='weight' )
        gini2 = inequality.get_gini( data=c2, target_col='inc', weight_col='weight' )
        gini3 = inequality.get_gini( data=c3, target_col='inc', weight_col='weight' )
        gini64 = inequality.get_gini( data=c64, target_col='inc', weight_col='weight' )
        # weighting and multiplying should make no difference
        print( "gini1");print( gini1 )
        print( "gini2");print( gini2 )
        print( "gini3");print( gini3 )
        print( "gini64");print( gini64 )
        self.assertAlmostEqual( gini1,  0.3272727)
        self.assertAlmostEqual( gini1,  gini2 )
        self.assertAlmostEqual( gini1,  gini3 )
        self.assertAlmostEqual( gini1,  gini64 )

if __name__ == '__main__':
    unittest.main()