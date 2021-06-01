from flask import render_template, Blueprint, json, request, redirect, url_for, session
import os, random
from .model.question import Question
from .model.result import Result

generated_questions = []
filename = ''

# Display list of module
index_bp = Blueprint('index', __name__, template_folder='templates')
@index_bp.route('/module')
def index():
    return render_template('index.html')


# show 10 quiz questions that are generated randomly
module_bp = Blueprint('module', __name__, template_folder='templates')
@module_bp.route('/module/<module>', methods=['GET', 'POST'])
def get_module(module):
    # POST method when click the submit button
    if request.method == 'POST':
        chosen = []
        for x in range(1, 11):
            chosen.append(request.form[str(x)])
        session['choose'] = chosen
        return redirect(url_for('submit.quiz_result', module=module))
    # load JSON data and display quiz questions
    else:
        questions = []
        global filename
        if module == 'math':
            filename = "Math_Quiz.json"
        elif module == 'english':
            filename = "English_Quiz.json"
        else:
            filename = "Science_Quiz.json"
        prj_root = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(prj_root, "data", filename)
        data = json.load(open(json_url))
        for obj in data:
            questions.append(Question(**obj))
        random.shuffle(questions)  # used random package to shuffle the questions
        questions = questions[:10]
        global generated_questions
        generated_questions = questions
        return render_template('quiz.html', module=module, len=len(questions), Questions=questions)


quiz_submit_bp = Blueprint('submit', __name__, template_folder='templates')
@quiz_submit_bp.route('/module/<module>/result')
def quiz_result(module):
    results = []
    data = session['choose']
    for x in range(10):
        results.append(Result(x, generated_questions[x], data[x]))
    return render_template('result.html', module=module, data=results)
