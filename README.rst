recipebox: A collaborative, recipe and kitchen inventory app
==================================================

recipebox is a `Flask <https://palletsprojects.com/p/flask/>`_-based recipe
and kitchen inventory app for managing recipes and kitchen inventory. 

Requirements
------------

Required packages include: Flask, Flask-SQLAlchemy, Flask-Login

How to run
-------------

If you're using gunicorn for your production server, you can run::

  gunicorn recipebox:app

If you're using uswgi for your production server, you can run::

  uwsgi --socket 0.0.0.0:5000 --protocol=http -w recipebox:app

Configuration file
-------------------

To configure your instance, you need to create a config file in python and
set the environment variable RECIPEBOX_SETTINGS to it's location.

An example configuration file.

.. code-block:: python

  SQLALCHEMY_DATABASE_URI="sqlite:////var/lib/mysite/site.db"
  SECRET_KEY="39238ebacc4e2e83c6d9c32add2516c6"
