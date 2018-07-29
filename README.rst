===============================
CramCrew
===============================

The smart way to study.


Quickstart
----------
First, make sure you install pipenv_ via brew or fedora. 

.. _pipenv: https://docs.pipenv.org/

Run the following commands to bootstrap your environment ::

    git clone https://github.com/avneesh1mehta/cramcrew.git
    cd cramcrew
    pipenv install --dev
    pipenv shell
    npm install
    npm start

If you are using virtualenv, replace the pipenv steps with ::

    virtualenv cramcrew
    source cramcrew/bin/activate
    pip install -r requirements.txt

To exit the virtual environment, type `exit` for pipenv and `deactivate` for virtualenv. 

Navigate to http://localhost:5000/ to view the app. Type Ctrl-C to stop the server.

If that doesn't work, you may need to migrate the db before starting the server ::

    flask db init # only do if you get an error after running the next two commands first
    flask db migrate
    flask db upgrade
    npm start


Deployment
----------
Commit your changes on a new branch and raise a pull request to be merged with master. After merging with master, I will retrigger a build for the deployed version. ::

    git add .
    git commit -m "message"
    git push origin dev-branch

Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``.


Running Tests
-------------

To run all tests, run ::

    flask test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands ::

    flask db migrate

This will generate a new migration script. Then run ::

    flask db upgrade

To apply the migration.

For a full migration command reference, run ``flask db --help``.


Asset Management
----------------

Files placed inside the ``assets`` directory and its subdirectories
(excluding ``js`` and ``css``) will be copied by webpack's
``file-loader`` into the ``static/build`` directory, with hashes of
their contents appended to their names.  For instance, if you have the
file ``assets/img/favicon.ico``, this will get copied into something
like
``static/build/img/favicon.fec40b1d14528bf9179da3b6b78079ad.ico``.
You can then put this line into your header::

    <link rel="shortcut icon" href="{{asset_url_for('img/favicon.ico') }}">

to refer to it inside your HTML page.  If all of your static files are
managed this way, then their filenames will change whenever their
contents do, and you can ask Flask to tell web browsers that they
should cache all your assets forever by including the following line
in your ``settings.py``::

    SEND_FILE_MAX_AGE_DEFAULT = 31556926  # one year
