import os
import sys
import importlib.resources
from confz import BaseConfig, FileSource
from .constants import APP_NAME


def createConfigFile(configFile: str, type: str = "config") -> None:
    """
    Create the config file if it doesn't exist.
    """
    try:
        if not os.path.exists(path=configFile):
            dir_name: str = os.path.dirname(configFile)
            if dir_name:
                os.makedirs(
                    name=dir_name,
                    exist_ok=True,
                )

            # Use importlib.resources to get asset path
            with (
                importlib.resources.files("dockmate")
                .joinpath(f"assets/config.yaml")
                .open(mode="rb") as src_file
            ):
                with open(file=configFile, mode="wb") as dst_file:
                    dst_file.write(src_file.read())

    except Exception as e:
        print(f"Error creating config file: {e}")
        sys.exit(1)


class AppConfig(BaseConfig):
    CONFIG_SOURCES = FileSource(
        file=os.path.join(
            os.path.expanduser(path="~"), ".config", f"{APP_NAME}", "config.yaml"
        )
    )

    docker_host: str  # Docker host URL
    containers: list[str]  # List of containers to monitor
    pushover: bool  # Enable Pushover notifications
    time_main_loop: int  # Time interval for the main loop in seconds


if __name__ == "__main__":
    pass
