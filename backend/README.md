# Full Stack Trivia API Project
This project is a game where users can test their knowledge answering trivia questions. The task for the project was to create an API and test suite for implementing the following functionality:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started

### Installing Dependencies
Developers using this project should already have Python3, pip, node, and npm installed.

#### Frontend Dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### Backend Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

## Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Running the Server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
Omit the dropdb command the first time you run tests.

## API Reference

### Getting Started

* Base URL: This application hosted locally. @ `http://127.0.0.1:5000/`
* Authentication: Not required.

### Error Handling

Errors are returned as JSON for example:<br>
```
    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }
```
### There are three types of return JSON:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessable

### Endpoints

#### GET method '/categories'

* General: Return all categories in list shape.
* Run: `curl localhost/categories`<br>
```
        {
            "categories": {
                "1": "Science", 
                "2": "Art", 
                "3": "Geography", 
                ....
            }, 
            "success": true
        }
```

#### GET method '/questions'

* General:
  * Returns:
    * paginated dictionary of 10 questions.
    * request type (success: True, False).
    * total question.
    * categories
  
* Run: `curl localhost/questions`<br>
* The result:<br>
```
   {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }, 
        "questions": [
            {
            "answer": "Maya Angelou", 
            "category": 4, 
            "difficulty": 2, 
            "id": 5, 
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            }, 
            {
            "answer": "Muhammad Ali", 
            "category": 4, 
            "difficulty": 1, 
            "id": 9, 
            "question": "What boxer's original name is Cassius Clay?"
            }, 
            {
            "answer": "Apollo 13", 
            "category": 5, 
            "difficulty": 4, 
            "id": 2, 
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            }, 
            {
            "answer": "Tom Cruise", 
            "category": 5, 
            "difficulty": 4, 
            "id": 4, 
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }, 
            {
            "answer": "Edward Scissorhands", 
            "category": 5, 
            "difficulty": 3, 
            "id": 6, 
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            }, 
            {
            "answer": "Brazil", 
            "category": 6, 
            "difficulty": 3, 
            "id": 10, 
            "question": "Which is the only team to play in every soccer World Cup tournament?"
            }, 
            {
            "answer": "Uruguay", 
            "category": 6, 
            "difficulty": 4, 
            "id": 11, 
            "question": "Which country won the first ever soccer World Cup in 1930?"
            }, 
            {
            "answer": "George Washington Carver", 
            "category": 4, 
            "difficulty": 2, 
            "id": 12, 
            "question": "Who invented Peanut Butter?"
            }, 
            {
            "answer": "Lake Victoria", 
            "category": 3, 
            "difficulty": 2, 
            "id": 13, 
            "question": "What is the largest lake in Africa?"
            }, 
            {
            "answer": "The Palace of Versailles", 
            "category": 3, 
            "difficulty": 3, 
            "id": 14, 
            "question": "In which royal palace would you find the Hall of Mirrors?"
            }
        ], 
        "success": true, 
        "total_questions": 19
        }
```
        
#### DELETE method '/questions/<int:id\>'

* General:
  * Deletes a question by id.
  * Returns:
    * Request type (success: True, False).
    * Deleted question ID.
    * total questions after delete.
    * Dictionary of paginated qustions.
* Try: `curl -X DELETE localhost/questions/19`<br>


#### POST method '/questions'
* General:
  * Creates a new question.
  * Returns:
    * Request type (success: True, False).
    * ID of the new qustion created.
    * The created qustion data.
    * Total of qustions after created.

* Try: <br>

```
>>> $ curl --header "Content-Type: application/json" \
>>> --request POST \
>>> --data '{"question":"<your qustion>","answer":"<your answer>", "category": <category>, "difficulty":<difficulty>}' \
>>> localhost/questions'
```

#### POST method '/questions/search?<title='searchTerm'>'

* General:
  * Searches for questions using search term in url with title term in JSON request parameters.
  * Returns JSON object with paginated matching questions.
* Sample: ```curl -X POST localhost/questions/search  -H "Content-Type: application/json" -d '{"title": "Egyptians"}'```<br>
* The result:<br>
```
            "questions": [
                {
                "answer": "Maya Angelou", 
                "category": 4, 
                "difficulty": 2, 
                "id": 5, 
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                }, 
                {
                "answer": "Muhammad Ali", 
                "category": 4, 
                "difficulty": 1, 
                "id": 9, 
                "question": "What boxer's original name is Cassius Clay?"
                }, 
                ...
                ], 
            "success": true, 
            "total_questions": Integer
        }
```


#### GET method '/categories/\<int:id\>/questions'

* General:
  * Gets questions by category id using url parameters.
  * Returns:
    * Request type (success: True, False).
    * Dictionary of paginated qustions.
    * Total qustions.
    * Category.

* Try: `curl localhost/categories/1/questions`


#### POST Method '/quizzes'

* General:
  * Get a new qustion to play the game.
  * The request should be in JSON of category and previous questions data.
  * Returns a new question based on previous questions in data provided.
* Try:<br>
`curl -X POST localhost/quizzes  -H "Content-Type: application/json" -d {"previous_questions": [20, 21], "quiz_category": 1`

### note:
    If:`curl localhost/` dose not work for you, try to use: `curl http://127.0.0.1:5000/`.

## Author

Obada Al Ahdab authored the API (`__init__.py`), test suite (`test_flaskr.py`), and this README.<br>
This project was created by [Udacity](https://www.udacity.com/) as a part of the [Full Stack Web Developer Nanodegree].
