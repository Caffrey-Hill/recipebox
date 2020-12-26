from flask import abort
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from .models import add_to_inventory
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
    add_to_inventory(name=request.values["item"])
    return redirect(url_for("inventory.index"))
