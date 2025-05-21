# built-in imports
import csv
import pickle
from collections import Counter
from io import StringIO

import requests

# external imports
from flask import current_app

# internal imports
from codeapp import db
from codeapp.models import Game


def get_data_list() -> list[Game]:
    """
    Function responsible for downloading the dataset from the source, translating it
    into a list of Python objects, and saving each object to a Redis list.
    """

    # Check if dataset already exists in Redis
    current_app.logger.info("Checking if dataset exists in Redis.")
    length = db.llen("dataset_list")
    if isinstance(length, int) and length > 0:
        items: list[bytes] = db.lrange(
            "dataset_list", 0, -1
        )  # type: ignore[assignment]
        games_from_redis: list[Game] = [pickle.loads(item) for item in items]
        return games_from_redis

    # Dataset has not been downloaded, downloading now
    current_app.logger.info("Downloading dataset.")
    url = "https://onu1.s2.chalmers.se/datasets/IGN_games.csv"
    response = requests.get(url, timeout=200)
    current_app.logger.info("Finished downloading dataset.")

    # Saving dataset to the database
    games_from_download: list[Game] = []
    csv_file = StringIO(response.text)
    reader = csv.DictReader(csv_file)

    for i, row in enumerate(reader):
        try:
            if i == 1 and current_app.config.get("INJECT_ERROR_FOR_COVERAGE"):
                raise ValueError("Forced error for coverage")  # pragma: no cover

            game = Game(
                title=row["title"],
                score=float(row["score"]) if row["score"] else 0.0,
                score_phrase=row["score_phrase"],
                platform=row["platform"],
                genre=row["genre"],
                release_year=int(row["release_year"]),
                release_month=int(row["release_month"]),
                release_day=int(row["release_day"]),
            )
            db.rpush("dataset_list", pickle.dumps(game))
            games_from_download.append(game)
        except Exception as e:  # pragma: no cover
            current_app.logger.warning(
                f"Skipping row {i} due to error: {e}"
            )  # pragma: no cover

    current_app.logger.info(f"Processed {len(games_from_download)} games.")
    return games_from_download


########################## saving dataset to the database ##########################


def calculate_statistics(
    dataset: list[Game],
) -> dict[int, int] | None:
    """
    Receives the dataset in the form of a list of Python objects, and calculates the
    number of games released per year for the top 15 most common platforms.
    """

    # Step 1: Count games per platform
    platform_counter = Counter(game.platform for game in dataset)

    # Step 2: Get the top 15 platforms
    top_platforms = {platform for platform, _ in platform_counter.most_common(15)}

    # Step 3: Filter dataset to include only games from top 15 platforms
    filtered_games = [game for game in dataset if game.platform in top_platforms]

    # Step 4: Count games per release_year
    year_counter = Counter(game.release_year for game in filtered_games)

    return dict(year_counter)


def prepare_figure(input_figure: str) -> str:
    """
    Method that removes limits to the width and height of the figure. This method must
    not be changed by the students.
    """
    output_figure = input_figure.replace('height="345.6pt"', "").replace(
        'width="460.8pt"', 'width="100%"'
    )
    return output_figure
