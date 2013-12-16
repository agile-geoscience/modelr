import unittest
import os

def run_tests():

    tests = []
    for root,dirs,files in os.walk( 'modelr' ):

        if 'test' in root:
            tests.append(
                unittest.TestLoader().discover(root,
                                             pattern='*test.py'))

    suite = unittest.TestSuite( tests )

    return(suite)

if ( __name__ == '__main__' ):
    
    suite = run_tests()
    unittest.TextTestRunner(verbosity=2).run(suite)

