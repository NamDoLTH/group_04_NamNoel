# Skeleton project for the final project of the EEN060/EEN065 courses

<h2 style="color: red;">
Attention! You must not clone this repository. Instead, you must create a private one using this as a template.
</h2>

Skeleton/template for the final project of EEN060/EEN065 courses.

## Create a virtual environment

At this state, you should have already installed the correct version of Python in your computer.
Then, you can run the following command in your terminal:

```bash
python -m venv venv
```

Then, select the `venv` as the current Python version in the VSCode project.

Finally, install the dependencies running the following command in the terminal:

```bash
pip install -r requirements.txt
```

Official documentation: https://docs.python.org/3/library/venv.html

## Setup the .env file

Copy the `.env_example` file into a new file called `.env` and place the content with the password and your specific database number.

## Running this project

In order to run this project, you should open a terminal.
Make sure your virtual environment is active.
Then, type the following command:

`python manage.py run`

Alternatively, you can run it by going to the *Run and Debug* tab (CTRL/CMD+SHIFT+D) and *start debugging* (F5).

## Installing dependencies

You should have already installed all dependencies within the `venv` environment.
If you face `ModuleNotFound` issues, double-check if the `venv` environment is active.
If issues continue, you can try installing dependencies again with the command:

```bash
pip install -r requirements.txt
```


## Files to be modified

Here is list of the files that you will need to change:
- [models.py](codeapp/models.py): file where you should create your dataclass.
- [utils.py](codeapp/utils.py): file responsible for downloading the dataset and extracting the statistics.
- [routes.py](codeapp/routes.py): file responsible for serving the web page and the plot.
- [about.html](codeapp/templates/about.html): file where you should add your names and the objective of your project.
- [base.html](codeapp/templates/base.html): file where you should put your names in the copyright.


## Sequence of steps

Here is the recommended sequence of steps that you need to follow to complete your final project:

1. Setup your database configuration
  - Create a new file called `.env` and copy the content of the [.env_example](.env_example) into it.
  - Set your DB number in the newly created [.env](.env) file.
  - Run `pytest -k database` to test if the connection is successful. You should see a green message with *1 passed*.
2. Create the class that models the object of your database in the file [models.py](codeapp/models.py).
  - Note that this class needs to be a `dataclass`.
  - To test if this step is correct, run `pytest -k models`. You should see a green message with *1 passed*.
3. Populate the [utils.py](codeapp/utils.py) with the correct code to obtain and save the dataset.
  - To test if this step is correct, run `pytest -k data_list`.
  - To test if you are saving correctly to the database, run `pytest -k use_database`.
4. Debug your implementation of the utils.py functions using the [debug_implementation.ipynb](debug_implementation.ipynb) file.
5. Create the routes for the web services by implementing the functions `get_json_dataset` and `get_json_stats` in the [routes.py](codeapp/routes.py) file.
6. Implement the route for the web page.
  - Start with the table by implementing the route `home` in the [routes.py](codeapp/routes.py) file.
  - Implement the visualization code for the table in the [home.html](codeapp/templates/home.html). To test this step, run `pytest -k html`.
  - Implement the `image` route in the [routes.py](codeapp/routes.py) file. To test this part, run `pytest -k image`.


## Useful links and commands

### Pick the color for your project

You can get the HEX code for the colors in your plot through this Google tool:
https://g.co/kgs/ydsBD9

### Validating your entire project

To validate your project, you can run in the terminal the following command.

For MS Windows:

`.\validate.ps1`

For macOS or Linux:

`./validate.sh`

or

`sh validate.sh`

### Validating your project manually

You can validate your project manually by running the following commands:

1. Code quality validation step 1:

```
flake8 .
```

2. Code quality validation step 2:

```
pylint -s n codeapp
```

3. Code quality validation step 3:

```
black . --check
```

If `black` shows some issues, you can ask it to try to fix the issues with the command:

```
black .
```

4. Code quality step 4 (type hints):

```
mypy .
```

5. Code quality step 5 (imports):

```
isort . --check-only --diff
```

You can also ask `isort` to try to fix the issues using the command:

```
isort .
```

6. To run the tests of your project, without running the entire validation suite, you can run in the terminal:

```
pytest
```
