import click
from flask.cli import with_appcontext

from .models import db

@click.command("init-db", help='Initalizes a RecipeBox database')
@with_appcontext
def init_db():
    db.create_all()
    click.echo("Initialized the database.")

