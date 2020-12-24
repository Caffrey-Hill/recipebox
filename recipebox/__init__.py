from flask import Flask, render_template

def create_app(config=None):
    app = Flask(__name__)
    if isinstance(config, dict):
        for key in config:
            app.config[key] = config[key]
    app.config.from_object('recipebox.default_settings')
    app.config.from_envvar('RECIPEBOX_SETTINGS', silent=True)

    from .models import db
    db.init_app(app)

    from .recipes import recipes
    app.register_blueprint(recipes, url_prefix="/recipes")

    from .groceries import groceries
    app.register_blueprint(groceries, url_prefix="/groceries")

    from .meal_plan import meal_plan
    app.register_blueprint(meal_plan, url_prefix="/meal_plan")

    from .inventory import inventory
    app.register_blueprint(inventory, url_prefix="/inventory")

    from .api import api
    app.register_blueprint(api, url_prefix="/api")
    
    @app.route("/")
    def index():
        return render_template("welcome.html")
    
    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(500)
    def handle_error(error):
        return render_template("error.html", error=error), error.code
    from .cli import init_db
    app.cli.add_command(init_db)

    return app
