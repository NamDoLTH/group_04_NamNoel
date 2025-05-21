# built-in imports
import inspect
import json
from dataclasses import is_dataclass
from typing import Any, Generator, Optional

# external imports
import pytest
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask.testing import FlaskClient

# internal imports
import codeapp.models as models
from codeapp import create_app, db
from codeapp.utils import get_data_list

# the URL below is for the service deployed at Chalmers
url_html_validator = "https://onu1.s2.chalmers.se/nu/?out=json"
# url_html_validator = "https://validator.w3.org/nu/?out=json"


def test_database_connection() -> None:
    assert db.ping(), "Database failed to connect!"
    db.delete("dataset_list")


def test_models() -> None:
    num_dataclasses = 0
    num_fields = 6
    my_class: Optional[Any] = None  # type: ignore
    for _class in inspect.getmembers(models, inspect.isclass):
        if is_dataclass(_class[1]):
            num_dataclasses += 1
            my_class = _class[1]
    assert num_dataclasses == 1, (
        "The number of dataclasses in the model is wrong. "
        + f"Expecting 1, got {num_dataclasses}."
    )
    if my_class is not None:
        assert len(my_class.__dataclass_fields__) >= num_fields, (
            f"The number of fields should be at least {num_fields}. "
            + f"You have only {len(my_class.__dataclass_fields__)}."
        )


def test_get_data_list(app: Flask) -> None:
    with app.app_context():
        from_list = get_data_list()
        assert isinstance(
            from_list, list
        ), f"Expected to have a list, got a {type(from_list)}."
        assert len(from_list) > 0, "You must populate the list!"
        assert not isinstance(from_list[0], bytes), (
            "You must convert the bytes from the database into objects the first "
            "time we call the function."
        )

        from_list = get_data_list()
        assert isinstance(
            from_list, list
        ), f"Expected to have a list, got a {type(from_list)}."
        assert len(from_list) > 0, "You must populate the list!"
        assert not isinstance(from_list[0], bytes), (
            "You must convert the bytes from the database into objects after the "
            "dataset has been downloaded."
        )


def test_use_database(app: Flask) -> None:
    with app.app_context():
        db.delete("dataset_list")
        from_list = get_data_list()
        assert isinstance(
            from_list, list
        ), f"Expected to have a list, got a {type(from_list)}."
        assert len(from_list) > 0, "You must populate the list!"
        assert not isinstance(from_list[0], bytes), (
            "You must convert the bytes from the database into objects the first "
            "time we call the function."
        )
        assert db.llen("dataset_list") > 0, "You seem to not be using the database"


def test_html_home(client: FlaskClient) -> None:
    response = client.get("/")
    assert response.status_code == 200, "The `home` route failed to load"
    page = BeautifulSoup(response.text, "html.parser")
    assert page.find("table"), "The home page is missing the `table`"
    td = page.find_all("td")
    assert len(td) > 0, "You must have cells in your table"
    th = page.find_all("th")
    assert len(th) > 0, "You are missing the headers of your table"
    assert_html(response.data.decode("utf-8"))


def test_data(client: FlaskClient) -> None:
    response = client.get("/data/")
    assert response.status_code == 200, "The `home` route failed to load"
    page = BeautifulSoup(response.text, "html.parser")
    assert page.find("table"), "The home page is missing the `table`"
    td = page.find_all("td")
    assert len(td) > 0, "You must have cells in your table"
    th = page.find_all("th")
    assert len(th) > 0, "You are missing the headers of your table"


def test_image(client: FlaskClient) -> None:
    response = client.get("/image")
    assert response.status_code == 200, "The `image` route failed to load"
    assert len(response.data) > 0, "There is nothing inside the image"


def test_about(client: FlaskClient) -> None:
    response = client.get("/about")
    assert response.status_code == 200, "The `about` route failed to load"
    assert_html(response.data.decode("utf-8"))


def test_webservices_dataset(client: FlaskClient) -> None:
    response = client.get("/json-dataset")
    assert response.status_code == 200, "The `json-dataset` route failed to load"
    # tries to convert the JSON, and checks if it's the right format
    data = json.loads(response.data)
    assert len(data) > 0, "The data from the webservice did not bring any results"

    # testing the load for a second time
    response = client.get("/json-dataset")
    assert response.status_code == 200, "The `json-dataset` route failed to load"
    # data_2 = json.loads(response.data)
    # assert len(data) == len(data_2), "The webservice is returning inconsistent data"


def test_webservices_stats(client: FlaskClient) -> None:
    response = client.get("/json-stats")
    assert response.status_code == 200, "The `json-dataset` route failed to load"
    # tries to convert the JSON, and checks if it's the right format
    data = json.loads(response.data)
    assert len(data) > 0, "The data from the webservice did not bring any results"


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    _app = create_app()
    # _app.config.update(
    #     {
    #         "TESTING": True,
    #     }
    # )

    # other setup can go here

    yield _app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def assert_html(initial_html: str) -> BeautifulSoup:
    html_to_test = remove_svg(initial_html)

    response_html = requests.post(
        url_html_validator,
        headers={"Content-Type": "text/html; charset=UTF-8"},
        data=html_to_test,
        timeout=30,
    )
    message = ""
    with open("response.html", "wt") as file:
        file.write(response_html.text)
    with open("test.html", "wt") as file:
        file.write(html_to_test)
    has_error = False
    if response_html.json()["messages"]:
        for key, value in response_html.json().items():
            if not isinstance(value, list):
                message += key + " |-> " + value + "\n"
                # has_error = True
            else:
                error_number = 1
                html_split = html_to_test.split("\n")
                for i in value:
                    if (
                        "This document appears to be written" in i["message"]
                        and "Lorem ipsum text" in i["message"]
                    ):
                        continue
                    has_error = True
                    message += "\n"
                    if "type" in i:
                        if i["type"] == "error":
                            message += f"\tError {error_number}:" + "\n"
                        elif i["type"] == "warning":
                            message += f"\tWarning {error_number}:" + "\n"
                        else:
                            message += f"""\t{i["type"]} {error_number}:\n"""
                        if error_number == 1:
                            message += (
                                "\t\tThis is probably the one to look for first!" + "\n"
                            )
                        message += "\t\tMessage: " + i["message"] + "\n"
                        initial_line = max(0, i["lastLine"] - 3)
                        end_line = min(len(html_split) - 1, i["lastLine"] + 2)
                        message += f"""\t\tLine with problem: {i["lastLine"] - 1}\n"""
                        message += "\t\tCheck the code below:\n"
                        for j in range(initial_line, end_line):
                            mark = ""
                            if j + 1 == i["lastLine"]:
                                mark = ">>"
                            message += f"""\t\t{j}: {mark}\t{html_split[j]}\n"""
                        error_number += 1
                    else:
                        for k2, v2 in i.items():
                            message += "\t" + str(k2) + " -> " + str(v2) + "\n\n"
    if has_error:
        raise ValueError(f"HTML error:\n{message}")
    soup = BeautifulSoup(html_to_test, "html.parser")
    return soup


def remove_svg(input_html: str) -> str:
    lines: list[str] = input_html.split("\n")
    start_svg = 0
    end_svg = 0
    for i, line in enumerate(lines):
        if i > 0:
            if "?xml" in line:
                start_svg = i
            elif "</svg>" in line:
                end_svg = i + 1
                break
    output_lines = lines[0:start_svg]
    output_lines.extend(lines[end_svg:])
    return "\n".join(output_lines) + "\n"
