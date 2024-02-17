import os
import pathlib

SRC_FOLDER = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
CONFIG_FILE = SRC_FOLDER / 'configs' / 'app_config.yml'
