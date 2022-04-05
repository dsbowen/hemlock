.. Hemlock documentation master file, created by
   sphinx-quickstart on Mon Nov 12 14:17:27 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Hemlock documentation
=====================

Hemlock is your solution for cutting-edge survey methods.

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

.. | 
.. .. image:: https://gitpod.io/button/open-in-gitpod.svg
..    :target: https://gitpod.io/#https://gitlab.com/dsbowen/hemlock

|

.. raw:: html

   <style>
      .container .box {
         display : flex;
         flex-direction : row;
      }

      @media only screen and (max-width: 760px) {
         .container .box {
            display: block;
         }
      }

      .card {
         box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
         transition: 0.3s;
         width: 100%;
         border-radius: 5px;
         text-align: center;
         margin: 10px;
      }

      .heading-font {
         font-size: clamp(20px, 1.66667vw, 28px);
      }

      .card:hover {
         box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
      }

      img {
         border-radius: 5px 5px 0 0;
      }

      .card-body {
         padding: 2px 16px;
      }

      .custom-icon {
         font-size: 100px;
         margin-top: 10px;
      }
   </style>

   <div class="container">
      <div class="box">
         <div class="card">
            <i class="fab fa-python custom-icon"></i>
            <div class="card-body">
               <h4 class="heading-font">Program in Python</h4>
               <p>Program surveys in a powerful, user-friendly language</p>
            </div>
         </div>

         <div class="card">
            <i class="fas fa-rocket custom-icon"></i>
            <div class="card-body">
               <h4 class="heading-font">Create surveys faster</h4>
               <p>Write functions and loops to create surveys faster</p>
            </div>
         </div>

         <div class="card">
            <i class="fas fa-code-branch custom-icon"></i>
            <div class="card-body">
               <h4 class="heading-font">Use cutting-edge methods</h4>
               <p>Easily use adaptive experimentation and interactive machine learning</p>
            </div>
         </div>
      </div>
   </div>

.. raw:: html

   <style>
      .custom-button {
         border: none;
         border-radius: .25rem;
         padding: 7px;
         text-align: center;
         text-decoration: none;
         display: inline-block;
         font-size: 16px;
         margin: 4px 2px;
      }

      .primary-button {
         background-color: #007bff;
         border-color: #007bff;
         color: white;
      }

      .light-button {
         background-color: #f8f9fa;
         border-color: #f8f9fa;
         color: #212529
      }
   </style>

   <button class="custom-button primary-button" onclick="window.location.href='examples.html'">
      See examples
   </button>

   <button class="custom-button light-button" onclick="window.location.href='getting_started.html'">
      Get started
   </button>

|

API reference
=============

.. toctree::
   :maxdepth: 2

   hemlock/index
   Examples <examples>
   Getting started <getting_started>
   Extensions <extensions>
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