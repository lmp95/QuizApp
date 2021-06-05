import os

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    FontAwesome(app)

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

    app.config['SECRET_KEY'] = 'cXVpemFwcGtleQ=='
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    from . import module
    app.register_blueprint(module.module_bp)
    app.register_blueprint(module.index_bp)
    app.register_blueprint(module.quiz_submit_bp)
    app.register_blueprint(module.auth_bp)
    app.secret_key = '9e389504-c096-11eb-8529-0242ac130003'

    @app.route('/')
    def hello():
        return render_template('base.html', title='Home')

    return app
