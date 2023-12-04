import logging
import colorlog

# Set up the colored formatter
log_format = (
    "[%(asctime)s] - "
    "%(log_color)s%(levelname)-8s: "
    "%(message)s%(reset)s"
)

colored_formatter = colorlog.ColoredFormatter(
    log_format,
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
)

# Get the logger
logger = logging.getLogger(__name__)

# Add the colored formatter to the stream handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(colored_formatter)

# Add the stream handler to the logger
logger.addHandler(stream_handler)

# Set the logging level
logger.setLevel(logging.INFO)