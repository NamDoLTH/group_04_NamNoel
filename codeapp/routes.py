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
from codeapp.models import Game
from codeapp.utils import calculate_statistics, get_data_list, prepare_figure

# define the response type
Response = str | FlaskResponse | WerkzeugResponse

bp = Blueprint("bp", __name__, url_prefix="/")


################################### web page routes ####################################


@bp.get("/")  # root route
def home() -> Response:
    dataset: list[Game] = get_data_list()
    if dataset is None:
        return render_template(
            "home.html", table="No data available"
        )  # pragma: no cover
    stats = calculate_statistics(dataset)
    if stats is None:
        return render_template(
            "home.html", table="No statistics available"
        )  # pragma: no cover

    stats_list = list(sorted(stats.items()))
    html_table = tabulate(
        stats_list, headers=["Year", "Number of Games"], tablefmt="html"
    )
    bootstrap_table = html_table.replace(
        "<table>", """<table class="table table-bordered table-hover">"""
    )
    return render_template("home.html", table=bootstrap_table)


@bp.get("/data/")
def data() -> Response:
    dataset: list[Game] | None = get_data_list()
    if dataset is None or len(dataset) == 0:
        return render_template(
            "data.html", table="No data available"
        )  # pragma: no cover

    table_data = [
        [
            game.title,
            game.score,
            game.score_phrase,
            game.platform,
            game.genre,
            game.release_year,
            game.release_month,
            game.release_day,
        ]
        for game in dataset[:100]
    ]

    html_table = tabulate(
        table_data,
        headers=[
            "title",
            "score",
            "score_phrase",
            "platform",
            "genre",
            "release_year",
            "release_month",
            "release_day",
        ],
        tablefmt="html",
    )

    bootstrap_table = html_table.replace(
        "<table>", """<table class="table table-bordered table-hover">"""
    )

    return render_template("data.html", table=bootstrap_table)


@bp.get("/image")
def image() -> Response:
    dataset: list[Game] | None = get_data_list()
    if dataset is None or len(dataset) == 0:
        return render_template(  # pragma: no cover
            "image.html", error="No data available to generate image"
        )

    stats = calculate_statistics(dataset)
    if stats is None:
        return render_template(  # pragma: no cover
            "image.html", error="No statistics available to generate image"
        )

    fig = Figure()
    ax = fig.subplots()
    ax.bar(list(stats.keys()), list(stats.values()))
    ax.set_title("Number of Games per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Games Released")
    fig.tight_layout()

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
    dataset: list[Game] | None = get_data_list()
    if dataset is None:
        return jsonify([])  # pragma: no cover
    return jsonify([game.__dict__ for game in dataset])


@bp.get("/json-stats")  # root route
def get_json_stats() -> Response:
    dataset: list[Game] | None = get_data_list()
    if dataset is None:
        return jsonify({})  # pragma: no cover
    stats = calculate_statistics(dataset)
    if stats is None:
        return jsonify({})  # pragma: no cover
    return jsonify(stats)
