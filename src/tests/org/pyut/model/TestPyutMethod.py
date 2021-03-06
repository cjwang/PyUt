
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.model.PyutType import PyutType
from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutGloballyDisplayParameters import PyutGloballyDisplayParameters


class TestPyutMethod(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutMethod.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger:      Logger     = TestPyutMethod.clsLogger
        self._pyutMethod: PyutMethod = PyutMethod()

    def tearDown(self):
        pass

    def testStringMethodWithParameters(self):

        pyutMethod: PyutMethod = self._pyutMethod

        PyutMethod.setStringMode(PyutGloballyDisplayParameters.WITH_PARAMETERS)

        self.assertEqual(PyutGloballyDisplayParameters.WITH_PARAMETERS, pyutMethod.getStringMode(), 'Did not get set correctly')

    def testStringMethodWithoutParameters(self):

        pyutMethod: PyutMethod = self._pyutMethod

        PyutMethod.setStringMode(PyutGloballyDisplayParameters.WITHOUT_PARAMETERS)

        self.assertEqual(PyutGloballyDisplayParameters.WITHOUT_PARAMETERS, pyutMethod.getStringMode(), 'Did not get set correctly')

    def testStringMethodWithParametersRepresentation(self):

        pyutMethod:     PyutMethod                = self._pyutMethod
        pyutMethod.returnType = PyutType('float')

        pyutMethod.parameters = self._makeParameters()
        PyutMethod.setStringMode(PyutGloballyDisplayParameters.WITH_PARAMETERS)

        expectedRepresentation: str = '+(intParam: int = 0, floatParam: float = 32.0): float'
        actualRepresentation:   str = pyutMethod.__str__()

        self.assertEqual(expectedRepresentation, actualRepresentation, 'Oops this does not match')

    def testStringMethodWithoutParametersRepresentation(self):

        pyutMethod:     PyutMethod                = self._pyutMethod
        pyutMethod.returnType = PyutType('float')

        pyutMethod.parameters = self._makeParameters
        PyutMethod.setStringMode(PyutGloballyDisplayParameters.WITHOUT_PARAMETERS)

        expectedRepresentation: str = '+(): float'
        actualRepresentation:   str = pyutMethod.__str__()

        self.assertEqual(expectedRepresentation, actualRepresentation, 'Oops this does not match')

    def _makeParameters(self) -> PyutMethod.PyutParameters:

        pyutParameter1: PyutParam                 = PyutParam(name='intParam',   theParameterType=PyutType("int"),   defaultValue='0')
        pyutParameter2: PyutParam                 = PyutParam(name='floatParam', theParameterType=PyutType("float"), defaultValue='32.0')
        parameters:     PyutMethod.PyutParameters = [pyutParameter1, pyutParameter2]

        return parameters


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutMethod))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
