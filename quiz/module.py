from flask import render_template
from flask import Blueprint


bp = Blueprint('simple_page', __name__, template_folder='templates')
@bp.route('/quiz/<module>')
def get_module(module):
    return render_template('quiz.html', keys=module, value=module)
