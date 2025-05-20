# pylint: disable=cyclic-import
"""
File that contains all the routes of the application.
This is equivalent to the "controller" part in a model-view-controller architecture.
In the final project, you will need to modify this file to implement your project.
"""
# built-in imports
import io

# external imports
from flask import Blueprint, jsonify, render_template
from flask.wrappers import Response as FlaskResponse
from matplotlib.figure import Figure
from tabulate import tabulate
from werkzeug.wrappers.response import Response as WerkzeugResponse

# internal imports
from codeapp.models import Any  # TODO: implement here
from codeapp.utils import calculate_statistics, get_data_list, prepare_figure

# define the response type
Response = str | FlaskResponse | WerkzeugResponse

bp = Blueprint("bp", __name__, url_prefix="/")


################################### web page routes ####################################


@bp.get("/")  # root route
def home() -> Response:
    # gets dataset
    # TODO: implement here

    # get the statistics that is supposed to be shown
    # TODO: implement here

    # convert the dictionary into a list of tuples
    # TODO: implement here

    # generate the HTML table
    html_table = ""  # TODO: implement here

    # make nice formatting -- always use this line
    bootstrap_table = html_table.replace(
        "<table>", """<table class="table table-bordered table-hover">"""
    )

    # render the page
    return render_template("home.html", table=bootstrap_table)


@bp.get("/data/")
def data() -> Response:
    # gets dataset
    dataset: list[Any] = get_data_list()  # TODO: implement here

    # generate the table
    html_table = tabulate(
        dataset[0:100],
        headers=[
            # TODO: implement here
        ],
        tablefmt="html",
    )

    # make nice formatting -- always use this line
    bootstrap_table = html_table.replace(
        "<table>", """<table class="table table-bordered table-hover">"""
    )

    # render the page
    return render_template("data.html", table=bootstrap_table)


@bp.get("/image")
def image() -> Response:
    # gets dataset
    dataset: list[Any] = get_data_list()  # TODO: implement here

    # get the statistics that is supposed to be shown
    # TODO: implement here

    # creating the plot

    fig = Figure()
    # TODO: implement here

    ################ START -  THIS PART MUST NOT BE CHANGED BY STUDENTS ################
    # create a string buffer to hold the final code for the plot
    output = io.StringIO()
    fig.savefig(output, format="svg")
    # output.seek(0)
    final_figure = prepare_figure(output.getvalue())
    return FlaskResponse(final_figure, mimetype="image/svg+xml")


@bp.get("/about")
def about() -> Response:
    return render_template("about.html")


################################## web service routes ##################################


@bp.get("/json-dataset")  # root route
def get_json_dataset() -> Response:
    # gets dataset
    dataset: list[Any] = get_data_list()  # TODO: implement here

    # render the page
    return jsonify(dataset)


@bp.get("/json-stats")  # root route
def get_json_stats() -> Response:
    # gets dataset
    # TODO: implement here

    # get the statistics that is supposed to be shown
    # TODO: implement here

    # render the page
    return None  # jsonify(counter) # TODO: implement here
