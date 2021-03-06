
from logging import Logger
from logging import getLogger

from os import sep as osSep

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase
from tests.TestBase import TEST_DIRECTORY

from org.pyut.plugins.FieldExtractor import FieldExtractor


class TestFieldExtractor(TestBase):
    """
    """
    TEST_FILE_NAME: str = f'{TEST_DIRECTORY}{osSep}testclass{osSep}Opie.py'
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestFieldExtractor.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestFieldExtractor.clsLogger

    def tearDown(self):
        pass

    def testBasicFieldFind(self):

        fe: FieldExtractor = FieldExtractor(filename=TestFieldExtractor.TEST_FILE_NAME)

        fields = fe.getFields(className='Opie')

        expectedFieldCount: int = 3
        actualFieldCount:   int = len(fields)
        self.assertEqual(expectedFieldCount, actualFieldCount, 'Field counts do not match')
        self.logger.info(f'Found {len(fields)} fields')

        for name, init in fields.items():
            self.logger.info(f'{name} = {init}')

    def testRemoveExtraneousNameParts(self):

        fe: FieldExtractor = FieldExtractor(filename=TestFieldExtractor.TEST_FILE_NAME)

        nameToClean: str = '.([,-*/%'
        cleanedName: str = fe._removeExtraneousNameParts(nameToClean=nameToClean)

        expectedLength: int = 0
        actualLength:   int = len(cleanedName)

        self.assertEqual(expectedLength, actualLength, 'Name was not cleaned')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestFieldExtractor))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
