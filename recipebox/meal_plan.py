from flask import Blueprint, render_template, flash, redirect, url_for, request, abort

from .models import db, Recipe

meal_plan = Blueprint('meal_plan', __name__, template_folder='templates')

@meal_plan.route("/")
def index():
    recipes = Recipe.query.all()
    return render_template("meal_plan.html", recipes=recipes)
