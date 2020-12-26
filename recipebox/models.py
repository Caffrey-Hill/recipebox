from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from .math import parse_amount

db = SQLAlchemy()

class Recipe(db.Model):
    """ Represents a saved recipe """

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    directions = db.Column(db.Text, nullable=False)
    ingredients = db.relationship("Ingredient", back_populates="recipe")
    meal_plan = db.relationship("MealPlan", back_populates="recipe")
   
    def __repr__(self):
        return "<Recipe '%s'>" % (self.title)


class Inventory(db.Model):
    """ Represents an item that is either acquired or mentioned a recipe

    It keeps tracks of what is in stock.
    """

    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    amount = db.Column(db.String(120))
    grocery = db.relationship("Grocery", uselist=False, back_populates="inventory")
    recipe_usage = db.relationship("Ingredient", back_populates="inventory")

    def __repr__(self):
        return "<Inventory '%s'>" % (self.name)

class Ingredient(db.Model):
    """ Represents recipe mentions of inventory items """

    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(120))
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'))
    inventory = db.relationship("Inventory", back_populates="recipe_usage")
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    recipe = db.relationship("Recipe")

    def __repr__(self):
        return "<Ingredient '%s' in '%s'>" % (self.name, self.recipe.title)

class Grocery(db.Model):
    """ Represents items on the grocery list """

    __tablename__ = 'groceries'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(120))
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'))
    inventory = db.relationship("Inventory", back_populates="grocery")

    def __repr__(self):
        return "<Grocery '%s'>" % (self.inventory.name)


class MealPlan(db.Model):
    """ Represents the current meal plan """

    __tablename__ = 'meal_plan'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    recipe = db.relationship("Recipe")

def add_to_inventory(name, amount=None):
    inventory = Inventory.query.filter_by(name=name).first()
    if not inventory:
        inventory = Inventory(name=name)
        db.session.add(inventory)
    if amount and parse_amount(amount):
        inventory.amount = amount
    db.session.commit()
    return inventory

def add_grocery(name, amount=1):
    inventory = add_to_inventory(name)
    grocery = Grocery.query.filter_by(inventory=inventory).first()
    if grocery:
        original_amount = parse_amount(grocery.amount)
        additional_amount = parse_amount(amount)
        total_amount = original_amount + additional_amount
        grocery.amount = fraction_to_mixed(total_amount)
    else:
        grocery = Grocery(inventory=inventory)
        parse_amount(amount) # This will throw an exceptin if invalid
        grocery.amount = amount
        db.session.add(grocery)
    db.session.commit()

def clear_groceries(ids):
    if ids:
        Grocery.query.filter(Grocery.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
