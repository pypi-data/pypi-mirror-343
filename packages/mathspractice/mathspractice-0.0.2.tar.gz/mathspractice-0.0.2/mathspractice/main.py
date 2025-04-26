def run():

    import os

    from datetime import timedelta

    from flask import Flask, render_template

    secret_key = os.environ.get('SECRET_KEY', 'ThisIsNotSecret')

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=secret_key,
        PERMANENT_SESSION_LIFETIME=timedelta(days=365),
    )

    from . import lesson1
    app.register_blueprint(lesson1.bp, url_prefix='/lesson1')
    from . import lesson2
    app.register_blueprint(lesson2.bp, url_prefix='/lesson2')
    from . import lesson3
    app.register_blueprint(lesson3.bp, url_prefix='/lesson3')

    @app.route('/')
    def index():
        return render_template('index.html')

    app.run()
