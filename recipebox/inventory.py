from flask import abort
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from .models import db
from .models import Inventory

inventory = Blueprint('inventory', __name__, template_folder='templates')

@inventory.route("/")
def index():
    inventory = Inventory.query.all()
    return render_template("inventory.html", inventory=inventory)

@inventory.route("/add", methods=["POST"])
def add():
    if 'item' not in request.values:
        abort(400)
    inventory = Inventory.query.filter_by(name=request.values["item"]).first()
    if not inventory:
        inventory = Inventory(name=request.values["grocery"])
        db.session.add(inventory)
        db.session.commit()
    return redirect(url_for("inventory.index"))
