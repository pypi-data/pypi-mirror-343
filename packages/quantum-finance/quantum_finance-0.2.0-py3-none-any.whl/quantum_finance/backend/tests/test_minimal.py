'''
This is a minimal test file to verify that the testing framework is working.
We add extensive notation to track what we're testing and why.
'''

def test_basic_arithmetic():\n    '''\n    This test checks basic arithmetic as a sanity check.\n    If this fails, there's likely an environment or configuration problem.\n    '''\n    x = 2 + 2\n    assert x == 4, 'Expected 2+2 to equal 4'\n 