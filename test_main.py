from test_wifi import WifiConfirmTester
from test_half_duplex import MyTestCase
from test_choosing_devices import ChoosingDevicesTester
from test_retrying_ack import RetryingAckTester
from test_interface_knrm import OnBoardInterfaceTester
import unittest

def main():
    test_classes = [WifiConfirmTester(), ChoosingDevicesTester(), MyTestCase(), RetryingAckTester(), OnBoardInterfaceTester()]
    function_names_of_test_classes = {test_class:get_function_names_startwith_test(test_class) for test_class in test_classes}

    test_name = input("Welke test wilt u uitvoeren? ")
    test_suite = get_test_suite(test_name, function_names_of_test_classes)
    
    if not test_suite: 
        return
    else:
        unittest.TextTestRunner(verbosity=2).run(test_suite)

"""
    This function loops through all the attributes _class and. If the attribute is a function of _class append the function_name to function_names.
    After that filter the function names that start with "test". Now you have a list of the function names that start with "test" and belong to _class.
"""
def get_function_names_startwith_test(_class):
    import types

    functionNames = []
    for entry, value in _class.__class__.__dict__.items():
        if (isinstance(value, types.FunctionType)):
            functionNames.append(entry)
    
    return [function_name for function_name in functionNames if function_name.startswith("test")]

"""
    Takes in the desired test to be included in the testsuite and a dict with the test_classes and its function names
    It returns a testsuite if the test_name is included in the incoming dict as a value. Otherwise return False.
"""
def get_test_suite(test_name, function_names_of_test_classes):
    suite = unittest.TestSuite()

    for test_class, function_names in function_names_of_test_classes.items():
        if test_name in function_names:
            suite.addTest(test_class.__class__(test_name))
            return suite
    else:
        print("Test name entered not an exisiting test name!")
        return False

if __name__ == '__main__':
    main()