from flask import render_template, Blueprint, json, request, redirect, url_for, session, jsonify
import os, random
from .model.question import Question
from .model.result import Result
from .model.account import User
from .model.score import Score
from werkzeug.security import check_password_hash
from quiz import db

generated_questions = []
filename = ''

# Display list of module
index_bp = Blueprint('index', __name__, template_folder='templates')
@index_bp.route('/module')
def index():
    if session['user'] is not None:
        return render_template('index.html')
    else:
        return redirect(url_for('auth.login'))


# show 10 quiz questions that are generated randomly
module_bp = Blueprint('module', __name__, template_folder='templates')
@module_bp.route('/module/<module>', methods=['GET', 'POST'])
def get_module(module):
    # POST method when click the submit button
    global generated_questions
    if request.method == 'POST':
        chosen = []
        total_score = 0
        for i in range(10):
            if str(generated_questions[i].answer) == request.form[str(i)]:
                total_score += 1
            chosen.append(request.form[str(i)])
        session['choose'] = chosen
        session['total_score'] = total_score
        new_score = Score(name=session['name'], email=session['email'], score=total_score, module=module)
        db.session.add(new_score)
        db.session.commit()
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
        generated_questions = questions
        return render_template('quiz.html', module=module, len=len(questions), Questions=questions)


quiz_submit_bp = Blueprint('submit', __name__, template_folder='templates')
@quiz_submit_bp.route('/module/<module>/result/')
def quiz_result(module):
    results = []
    data = session['choose']
    total = session['total_score']
    for x in range(10):
        results.append(Result(x, generated_questions[x], data[x]))
    scores = Score.query.filter_by(email=session['email'], module=module).order_by(Score.score.desc()).limit(3).all()
    return render_template('result.html', module=module, data=results, totalMark=total, highscore=scores)


auth_bp = Blueprint('auth', __name__, template_folder='templates')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return render_template('login.html', message=True)
        else:
            session['email'] = user.email
            session['name'] = user.name
            return redirect(url_for('index.index'))
    else:
        return render_template('login.html')


