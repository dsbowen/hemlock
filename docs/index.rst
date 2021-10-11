.. Hemlock documentation master file, created by
   sphinx-quickstart on Mon Nov 12 14:17:27 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Hemlock documentation
===========================================

A framework for creating online surveys and experiments.

.. image:: https://gitlab.com/dsbowen/hemlock/badges/master/pipeline.svg
   :target: https://gitlab.com/dsbowen/hemlock/-/commits/master
.. image:: https://gitlab.com/dsbowen/hemlock/badges/master/coverage.svg
   :target: https://gitlab.com/dsbowen/hemlock/-/commits/master
.. image:: https://badge.fury.io/py/hemlock-survey.svg
   :target: https://badge.fury.io/py/hemlock-survey
.. image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gl/dsbowen%2Fhemlock/HEAD?urlpath=lab
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

..
   .. image:: https://img.shields.io/badge/License-MIT-brightgreen.svg
      :target: https://gitlab.com/dsbowen/hemlock/-/blob/master/LICENSE

Installation
============

.. code-block:: console

   $ pip install hemlock-survey

Quickstart
==========

Let's create a simple app to ask users for their name and then greet them. Put the following in ``app.py``.

.. code-block::

   from hemlock import User, Page, create_app, socketio
   from hemlock.functional import validate
   from hemlock.questions import Input, Label
   from sqlalchemy_mutable.utils import partial


   @User.route("/survey")
   def seed():
      return [
         Page(
            name_input:=Input(
               "What's your name?",
               validate=validate.require_response("Please enter your name.")
            )
         ),
         Page(
            Label(compile=partial(greet_user, name_input))
         )
      ]


   def greet_user(greet_label, name_input):
      greet_label.label = f"Hello, {name_input.response}!"


   app = create_app()

   if __name__ == "__main__":
      socketio.run(app)


Run the app with

.. code-block:: console

   $ python app.py

Open http://localhost:5000 in your browser. Open http://localhost:5000/admin-status to see users' progress and download data.

.. toctree::
   :maxdepth: 2

   hemlock/index
   Changelog <changelog>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Citations
=========

.. code-block::

   
   @software(bowen2021hemlock,
      title={ Hemlock },
      author={ Bowen, Dillon },
      year={ 2021 },
      url={ https://dsbowen.gitlab.io/hemlock }
   )

License
=======

Hemlock currently has a closed-source license requiring written permission from its original author, Dillon Bowen, for use and distribution. I intend for hemlock to be an open-research software: free for academics and non-profit use but not for commercial purposes. The closed-source license is temporary until I have an appropriate open-research license. Until then, please feel free to use hemlock for academic and non-profit purposes and for personal use.