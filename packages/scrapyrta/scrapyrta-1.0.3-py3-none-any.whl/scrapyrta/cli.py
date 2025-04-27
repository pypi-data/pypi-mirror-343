import argparse
import os
import sys
from configparser import ConfigParser, NoOptionError, NoSectionError

import uvicorn
from scrapy.utils.conf import closest_scrapy_cfg

from scrapyrta.app.app import create_app
from scrapyrta.app.core.config import Settings, app_settings
from scrapyrta.app.core.log import logger


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Async HTTP API server for Scrapy project.",
    )

    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=int,
        default=9080,
        help="Port number to listen on",
    )
    parser.add_argument(
        "-i",
        "--ip",
        dest="ip",
        default="localhost",
        help="IP address the server will listen on",
    )
    parser.add_argument(
        "--project",
        dest="project",
        default="default",
        help="Project name from scrapy.cfg",
    )
    parser.add_argument(
        "-S",
        "--settings",
        dest="settings",
        metavar="project.settings",
        help="Custom project settings module path",
    )

    return parser.parse_args()


def find_scrapy_project(project) -> str:
    project_config_path = closest_scrapy_cfg()
    if not project_config_path:
        raise RuntimeError("Cannot find scrapy.cfg file")

    project_config = ConfigParser()
    project_config.read(project_config_path)

    try:
        project_settings = project_config.get("settings", project)
    except (NoSectionError, NoOptionError) as e:
        raise RuntimeError(str(e)) from e

    if not project_settings:
        raise RuntimeError("Cannot find scrapy project settings")

    project_location = os.path.dirname(project_config_path)
    sys.path.append(project_location)

    return project_settings


def run_application(arguments: argparse.Namespace, app_settings: Settings) -> None:
    app = create_app()
    app_settings.freeze()

    uvicorn.run(
        app,
        host=arguments.ip,
        port=arguments.port,
    )


def execute():
    sys.path.insert(0, os.getcwd())
    arguments = parse_arguments()

    if arguments.settings:
        app_settings.setmodule(arguments.settings)

    app_settings.set(
        "PROJECT_SETTINGS",
        find_scrapy_project(arguments.project),
    )

    if app_settings.DEBUG:
        logger.info("Runnign in DEBUG mode...")

    run_application(arguments, app_settings)


def run():
    try:
        execute()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
