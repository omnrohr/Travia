"""
This file is to run and configure all API's for a Trivia game
written partially by Obda Al Ahdab
project number 2 in NANO degree for Udacity.
"""
# --------------------------------------------------------------------------------------#
# Import your dependencies
# --------------------------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify
from flask.globals import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.sql.expression import join
# import sys
from models import setup_db, Question, Category


# --------------------------------------------------------------------------------------#
#  Implement pagniation
# --------------------------------------------------------------------------------------#

QUESTIONS_PER_PAGE = 10


def paginate_question_with_limits(request):
    '''Used for query_all() methods to reduce query memory space'''
    items_limit = request.args.get('limit', QUESTIONS_PER_PAGE, type=int)
    selected_page = request.args.get('page', 1, type=int)
    current_index = selected_page - 1

    current_qustions = \
        Question.query.order_by(Question.id).limit(
            items_limit).offset(current_index * items_limit).all()
    formatd_current_qustion = [question.format()
                               for question in current_qustions]

    return formatd_current_qustion


def paginate_question(request, selection):
    '''Used in filter_by() method to minimize code'''
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    qustions = [question.format() for question in selection]
    current_qustions = qustions[start:end]

    return current_qustions


# --------------------------------------------------------------------------------------#
# Define the create_app function
# --------------------------------------------------------------------------------------#

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app, allow all origins)
    CORS(app, resources={r"/api/*": {"origins": "*"}})


# --------------------------------------------------------------------------------------#
# Use the after_request decorator to set Access-Control-Allow
# --------------------------------------------------------------------------------------#

    # CORS Headers


    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH"
        )
        return response


# --------------------------------------------------------------------------------------#
# handle GET requests for all available categories.
# --------------------------------------------------------------------------------------#

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        categories_dict = {}

        for category in categories:
            categories_dict[category.id] = category.type

        if (len(categories_dict) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories_dict
        })

# --------------------------------------------------------------------------------------#
# handle GET requests for questions, including pagination (every 10 questions).
# This endpoint should return a list of questions, number of total questions, current category, categories.
# --------------------------------------------------------------------------------------#

    @app.route('/questions')   # the default method is GET
    def get_questions():
        total_questions = len(Question.query.all())
        current_questions = paginate_question_with_limits(request)

        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        if (len(current_questions) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'categories': categories_dict
        })


# --------------------------------------------------------------------------------------#
# DELETE question using a question ID
#
# --------------------------------------------------------------------------------------#

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_qustion(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            if not question:
                print(
                    'No question match the provided number, please check and try again.')
                abort(404)

            else:
                question.delete()
                current_questions = paginate_question_with_limits(request)

                return jsonify({
                    'success': True,
                    'deleted': question_id,
                    'total_qustions': len(Question.query.all()),
                    'qustions': current_questions
                })

        except Exception as e:
            print("Errors:", e)
            abort(422)


# --------------------------------------------------------------------------------------#
# POST a new question, which will require the question and answer text,
# category, and difficulty score.
# --------------------------------------------------------------------------------------#

    @app.route('/questions', methods=['POST'])
    def post_new_question():

        body = request.get_json()
        new_qustion = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')
        if (new_qustion == None) or (new_answer == None) or (new_category == None) or (new_difficulty == None):
            return jsonify({
                'success': False,
                'message': 'Missing information',
                "error": 422
            })

        try:
            new_question = Question(question=new_qustion, answer=new_answer,
                                    difficulty=new_difficulty, category=new_category)
            new_question.insert()

            current_questions = paginate_question_with_limits(request)

            return jsonify({
                'success': True,
                'created': new_question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'question_created': new_question.question
            })

        except:
            abort(422)


# --------------------------------------------------------------------------------------#
# Create a GET endpoint to get questions based on category.

# --------------------------------------------------------------------------------------#

    @app.route('/categories/<int:catogory_id>/questions')
    def get_questions_by_category(catogory_id):

        category = Category.query.filter_by(id=catogory_id).one_or_none()

        if (category is None):
            abort(400)

        selection = Question.query.filter_by(category=category.id).all()

        paginated = paginate_question(request, selection)

        return jsonify({
            'success': True,
            'questions': paginated,
            'total_questions': len(Question.query.all()),
            'current_category': category.type
        })

# --------------------------------------------------------------------------------------#
# get questions based on a search term.
# It should return any questions for whom the search term is a substring of the question.
# --------------------------------------------------------------------------------------#

    @app.route('/questions/search', methods=['POST'])
    def find_qustion_by_title():
        body = request.get_json()
        title = body.get('title')
        if not title:
            abort(404)

        try:
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike('%{}%'.format(title))).all()
            paginated_search_result = paginate_question(request, selection)

            return jsonify({
                'success': True,
                'questions': paginated_search_result,
                'total_questions': len(selection)
            })

        except:
            abort(404)

# --------------------------------------------------------------------------------------#
# to get questions to play the quiz.
# This endpoint should take category and previous question parameters
# and return a random questions within the given category,
# if provided, and that is not one of the previous questions.
# --------------------------------------------------------------------------------------#

    @app.route('/quizzes', methods=['POST'])
    def get_random_question():
        body = request.get_json()
        previous = body.get('previous_questions')
        category = body.get('quiz_category')

        if not previous or not category:
            return jsonify({
                'success': False,
                'message': 'Missing values',
                'error': 404
            })

        questions = Question.query.filter_by(category=category).all()
        total_qustions = len(questions)

        # to get a new qustion
        def new_qustion(questions):
            return questions[random.randrange(0, len(questions))]

        quiz = (new_qustion(questions))

        # check if the question is used before
        def check_if_used():
            if len(previous) >= 1:
                used = False
                if quiz.id in previous:
                    used == True
                else:
                    used == False
                return used

        # keep the searching for a new question
        while (check_if_used()):
            quiz = new_qustion()

            # break the loop if all questions used
            if (len(previous) == total_qustions):
                return jsonify({
                    'success': True,
                    'message': 'You finished all questions'
                })

        return jsonify({
            'success': True,
            'question': quiz.format()
        })


# --------------------------------------------------------------------------------------#
# error handlers for all expected errors including 404 and 422.
#
# --------------------------------------------------------------------------------------#


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
