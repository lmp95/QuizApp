import os

from flask import Flask
from flask import render_template


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import module
    app.register_blueprint(module.module_bp)
    app.register_blueprint(module.index_bp)

    @app.route('/')
    def hello():
        return render_template('base.html', title='Home')

    return app
