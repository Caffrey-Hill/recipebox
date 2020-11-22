from flask import Blueprint, render_template, flash, redirect, url_for, request, abort

from .models import db, Grocery, Inventory

groceries = Blueprint('groceries', __name__, template_folder='templates')

@groceries.route("/")
def index():
    groceries = Grocery.query.all()
    return render_template("groceries.html", groceries=groceries)

@groceries.route("/add", methods=["POST"])
def add():
    if 'grocery' not in request.values:
        abort(400)
    inventory = Inventory.query.filter_by(name=request.values["grocery"]).first()
    if not inventory:
        inventory = Inventory(name=request.values["grocery"])
        db.session.add(inventory)
    grocery = Grocery(inventory=inventory)
    if 'amount' in request.values:
        ''' @todo Check if valid amount '''
        grocery.amount = request.values['amount']

    db.session.add(grocery)
    db.session.commit()
    return redirect(url_for("groceries.index"))

@groceries.route("/acquired", methods=["POST"])
def acquired():
    return redirect(url_for('groceries.index'))
