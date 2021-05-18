from flask import render_template
from flask import Blueprint


module_bp = Blueprint('module', __name__, template_folder='templates')
@module_bp.route('/quiz/<module>')
def get_module(module):
    return render_template('quiz.html', keys=module, value=module)


index_bp = Blueprint('index', __name__, template_folder='templates')
@index_bp.route('/quiz')
def index():
    return render_template('index.html')
