# python built-in imports
import logging
import os
from logging.config import dictConfig
from typing import Dict

# python external imports
from dotenv import load_dotenv
from flask import Flask
from redis import Redis

# loading configuration
load_dotenv()

# connecting to the database
host: str = os.getenv("DATABASE_HOST", "127.0.0.1")
port: int = int(os.getenv("DATABASE_PORT", "6379"))
db_number: int = int(os.getenv("DATABASE_DB", "-1"))
password = os.getenv("DATABASE_PASSWORD", "")
assert password != "", "The database configuration seems wrong. Check your `.env` file."
db: Redis = Redis(host=host, port=port, db=db_number, password=password)
if not db.ping():
    raise ValueError("Database could not connect! Check DB parameters and try again.")

# configuring the logging
# for more info, check:
# https://docs.python.org/3.10/howto/logging.html
# this configuration writes to a file and to the console
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] [%(name)s] "
                "[%(module)s:%(lineno)s] - %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "to_file": {
                "level": "DEBUG",
                "formatter": "default",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/messages.log",
                "maxBytes": 5000000,
                "backupCount": 10,
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "to_file"],
        },
    }
)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    if os.getenv("APP_MODE") == "PRODUCTION":
        os.environ["FLASK_DEBUG"] = "0"  # pragma: no cover
    else:
        os.environ["FLASK_DEBUG"] = "1"  # pragma: no cover

    # register blueprints
    from codeapp.routes import bp  # pylint: disable=import-outside-toplevel

    app.register_blueprint(bp)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx() -> Dict[str, object]:  # pragma: no cover
        return {"app": app, "db": db}

    return app
