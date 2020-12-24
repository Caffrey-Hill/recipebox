from flask import Blueprint
from flask import jsonify
from .models import Inventory

api = Blueprint('api', __name__, template_folder='templates')


@api.route("/inventory/names")
def inventory_names():
    inventory = Inventory.query.all()
    results = [ item.name for item in inventory ]
    return jsonify(results)
