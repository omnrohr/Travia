"""
This file is to test all API behaviors in the __init__ file
written partially by Obda Al Ahdab
project number 2 in NANO degree for Udacity.
"""
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.DB_USER = os.getenv('DB_USER', 'admin')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'Opadah12')
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
            self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # add question
        self.new_question = {
            'id': 24,
            'question': 'What is my name',
            'answer': 'Obada',
            'difficulty': 2,
            'category': 1,
        }

        # add empty field question
        self.empty_field_qustion = {
            'answer': 'fake',
            'difficulty': 2,
            'category': 1,
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        """Test success request for categories """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        """ Test success get questions """
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_unallowed_page_selection(self):
        '''  Test unallowed requesting page (fail request)   '''
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question(self):
        """ Test seccess crate new question  """
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['question_created'])

    def test_empty_field_create_question(self):
        """ Test fail crate new question """
        res = self.client().post('/questions', json=self.empty_field_qustion)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Missing information')
        self.assertEqual(data['error'], 422)

    def test_delete_question(self):
        """  Test success Delete question  """
        res = self.client().delete('/questions/23')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertTrue(data['total_qustions'])
        self.assertTrue(len(data['qustions']))

    def test_not_valid_id_for_question_id(self):
        """ Test send not valid id for delete a question   """
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_questions(self):
        """   Success Search questions with results    """
        res = self.client().post('/questions/search',
                                 json={'title': 'involving'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertIsInstance(data['questions'], list)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_search_questions_without_results(self):
        """ Success Search questions with no results  """
        res = self.client().post('/questions/search',
                                 json={'title': ';alkdjf'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['questions'], list)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    def test_get_questions_by_category(self):
        """  Success Get questions by category   """
        res = self.client().get('/categories/1/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_request_question_out_range_questions(self):
        """  Fail request category with out range question id """
        res = self.client().get('/categories/1000/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_quizzes_with_missing_data(self):
        """  Fail test with missing data  """
        res = self.client().post('/quizzes', json={
            'previous_questions': [1]
        })
        data = json.loads(res.data)

        # Status code
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Missing values')
        self.assertEqual(data['error'], 404)

    def test_quiz_questions_with_full_data(self):
        """
        Test success quizzes request with data
        """
        res = self.client().post('/quizzes', json={
            'previous_questions': [13, 14],
            'quiz_category': 1
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
