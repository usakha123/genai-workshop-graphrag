# This will test the environment to ensure that the .env file is set up 
# correctly and that the OpenAI and Neo4j connections are working.
import os
import unittest

from dotenv import load_dotenv
load_dotenv()

class TestEnvironment(unittest.TestCase):

    skip_openai_test = True
    skip_neo4j_test = True

    def env_variable_exists(self, variable_name):
        self.assertIsNotNone(
            os.getenv(variable_name),
            f"{variable_name} not found in .env file")

    def test_openai_variables(self):
        self.env_variable_exists('OPENAI_API_KEY')
        TestEnvironment.skip_openai_test = False

    def test_neo4j_variables(self):
        self.env_variable_exists('NEO4J_URI')
        self.env_variable_exists('NEO4J_USERNAME')
        self.env_variable_exists('NEO4J_PASSWORD')
        TestEnvironment.skip_neo4j_test = False

    def test_openai_connection(self):
        if TestEnvironment.skip_openai_test:
            self.skipTest("Skipping OpenAI test")

        from openai import OpenAI, AuthenticationError

        llm = OpenAI()
        
        try:
            models = llm.models.list()
        except AuthenticationError as e:
            models = None
        self.assertIsNotNone(
            models,
            "OpenAI connection failed. Check your API key in .env file.")

    def test_neo4j_connection(self):
        if TestEnvironment.skip_neo4j_test:
            self.skipTest("Skipping Neo4j connection test")

        from neo4j import GraphDatabase

        driver = GraphDatabase.driver(
            os.getenv('NEO4J_URI'),
            auth=(os.getenv('NEO4J_USERNAME'), 
                  os.getenv('NEO4J_PASSWORD'))
        )
        try:
            driver.verify_connectivity()
            connected = True
        except Exception as e:
            connected = False

        driver.close()

        self.assertTrue(
            connected,
            "Neo4j connection failed. Check your NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD in .env file."
            )
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEnvironment('test_openai_variables'))
    suite.addTest(TestEnvironment('test_neo4j_variables'))
    suite.addTest(TestEnvironment('test_openai_connection'))
    suite.addTest(TestEnvironment('test_neo4j_connection'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
    