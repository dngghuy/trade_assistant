import logging
import logging.config
import os


def setup_logging():
    path = os.getenv("PYTHON_LOGGING_CONFIG", "./config/logging.yaml")
    if not os.path.exists(path):
        print(f'Logging config file {path} not found!')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s: %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S%z',
        )
        return

    with open(path, 'rt') as f:
        try:
            import yaml
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        except Exception as e:
            print(e)
            print('Error in Logging Configuration. Using default configs')
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s %(levelname)s %(name)s: %(message)s',
                datefmt='%Y-%m-%dT%H:%M:%S%z',
            )