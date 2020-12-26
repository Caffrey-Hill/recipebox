from flask import Blueprint, render_template, flash, redirect, url_for, request, abort

from .math import fraction_to_mixed
from .math import parse_amount
from .models import Grocery
from .models import MealPlan
from .models import add_grocery
from .models import clear_groceries

groceries = Blueprint('groceries', __name__, template_folder='templates')

@groceries.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.values["action"] == "add":
            add_grocery(request.values["grocery"], request.values.get("amount", 1))
        elif request.values["action"] == "clear":
            clear_ingredients(request.form.getlist('grocery[]'))
        elif request.values["action"] == "add_from_meal_plan":
            planned_meals = MealPlan.query.all()
            for meal in planned_meals:
                for ingredient in meal.recipe.ingredients:
                    add_grocery(ingredient.inventory.name, ingredient.amount)
        else:
            abort(400)
    groceries = Grocery.query.all()
    return render_template("groceries.html", groceries=groceries)
