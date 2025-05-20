# built-in imports
from datetime import date, datetime
import collections
import math
import pickle

# external imports
from flask import current_app
import requests

# internal imports
from codeapp import db
from codeapp.models import Any  # TODO: change this part


def get_data_list() -> list[Any] | None:  # change here
    """
    Function responsible for downloading the dataset from the source, translating it
    into a list of Python objects, and saving each object to a Redis list.
    """

    ##### check if dataset already exists, and if so, return the existing dataset  #####
    # TODO: implement here

    ################# dataset has not been downloaded, downloading now #################
    # TODO: implement here

    ########################## saving dataset to the database ##########################
    # TODO: implement here

    return None  # TODO: implement here


def calculate_statistics(
    dataset: list[Any],
) -> dict[int, int] | None:  # TODO: implement here
    """
    Receives the dataset in the form of a list of Python objects, and calculates the
    statistics necessary.
    """
    # create the counter
    # TODO: implement here

    return None  # TODO: implement here


def prepare_figure(input_figure: str) -> str:
    """
    Method that removes limits to the width and height of the figure. This method must
    not be changed by the students.
    """
    output_figure = input_figure.replace('height="345.6pt"', "").replace(
        'width="460.8pt"', 'width="100%"'
    )
    return output_figure
