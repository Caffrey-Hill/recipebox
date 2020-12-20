from flask import Blueprint, render_template, flash, redirect, url_for, request, abort

from .models import db, Recipe, MealPlan

meal_plan = Blueprint('meal_plan', __name__, template_folder='templates')

@meal_plan.route("/")
def index():
    recipes = Recipe.query.all()
    meal_plan = MealPlan.query.all()
    return render_template("meal_plan.html", recipes=recipes, meal_plan=meal_plan)

@meal_plan.route("/add", methods=["POST"])
def add():
    if 'recipe' not in request.values:
        abort(400)
    meal = MealPlan.query.filter_by(recipe_id=request.values['recipe']).one_or_none()
    if not meal:
        recipe = Recipe.query.filter_by(id=request.values['recipe']).first()
        if recipe:
            meal = MealPlan()
            meal.recipe = recipe
            db.session.add(meal)
            db.session.commit()
        else:
            abort(400)

    return redirect(url_for("meal_plan.index"))


@meal_plan.route("/clear", methods=["POST"])
def clear():
    ids = request.form.getlist('meal[]')
    if ids:
        acquired = MealPlan.query.filter(MealPlan.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
    return redirect(url_for('meal_plan.index'))
