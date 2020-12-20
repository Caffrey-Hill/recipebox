from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

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

    __table__anme = 'groceries'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(120))
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'))
    inventory = db.relationship("Inventory", back_populates="grocery")

    def __repr__(self):
        return "<Grocery '%s'>" % (self.name)


class MealPlan(db.Model):
    """ Represents the current meal plan """

    __tablename__ = 'meal_plan'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    recipe = db.relationship("Recipe")
