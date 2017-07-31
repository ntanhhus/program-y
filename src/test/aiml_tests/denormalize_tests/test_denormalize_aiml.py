import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.sections.brain.file import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = os.path.dirname(__file__)
        self.configuration.brain_configuration.files._denormal = os.path.dirname(__file__)+ os.sep + "denormal.txt"

class DenormalizeAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        DenormalizeAIMLTests.test_client = BasicTestClient()

    def test_denormalize(self):
        response = DenormalizeAIMLTests.test_client.bot.ask_question("test",  "TEST DENORMALIZE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "keithsterling.com")

    def test_newdev7_say(self):
        response = DenormalizeAIMLTests.test_client.bot.ask_question("test",  "SAY abc dot com")
        self.assertIsNotNone(response)
        self.assertEqual(response, "abc.com")
