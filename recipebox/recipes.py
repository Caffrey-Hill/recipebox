from flask import Blueprint, render_template, flash, redirect, url_for, request, abort

from .models import db, Recipe, Inventory, Ingredient

recipes = Blueprint('recipes', __name__, template_folder='templates')

@recipes.route("/")
def index():
    recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=recipes)

def parse_ingredients():
    """ Helper to retrieve ingredents from form data in request
    
    TODO: There is probably a more intuitive way to do this

    :return: All the ingredients described in the request
    :type: A list of Ingredients
    """
    ingredients = []
    amounts = request.form.getlist("ingredient_amount[]")
    for (i, name) in enumerate(request.form.getlist('ingredient[]')):
        inventory = Inventory.query.filter_by(name=name).first()
        if inventory is None:
            inventory = Inventory(name=name)
            db.session.add(inventory)
        ingredients.append(Ingredient(inventory=inventory, amount=amounts[i]))
    return ingredients
    
@recipes.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        if 'title' not in request.values or 'directions' not in request.values:
            abort(400)
        recipe = Recipe(title=request.values['title'],
                         directions=request.values['directions'])
        recipe.ingredients = parse_ingredients()
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for("recipes.index"))
    return render_template("recipe_form.html")

@recipes.route("/view")
def view():
    if 'id' not in request.values:
        abort(400)
    recipe = Recipe.query.filter_by(id=request.values['id']).first()
    if recipe is None:
        abort(404)
    return render_template("view_recipe.html", recipe=recipe)
