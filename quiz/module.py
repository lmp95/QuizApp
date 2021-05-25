from flask import render_template, Blueprint, json
import os, random
from .model.question import Question


index_bp = Blueprint('index', __name__, template_folder='templates')
@index_bp.route('/quiz')
def index():
    return render_template('index.html')


module_bp = Blueprint('module', __name__, template_folder='templates')
@module_bp.route('/quiz/<module>')
def get_module(module):
    questions = []
    prj_root = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(prj_root, "data", "Math_Quiz.json")
    data = json.load(open(json_url))
    for obj in data:
        questions.append(Question(**obj))
    random.shuffle(questions)
    questions = questions[:10]
    return render_template('quiz.html', module=module, len=len(questions), Questions=questions)
