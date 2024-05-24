import logging
import os
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from logging.handlers import RotatingFileHandler

webserver = Flask(__name__)

webserver.tasks_runner = ThreadPool()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1

from app import routes

# Creating 'results' directory if it doesn't exist
if not os.path.exists('results'):
	os.mkdir('results')

# Creating 'webserver.log' file if it doesn't exist
if not os.path.exists('webserver.log'):
	with open('webserver.log', 'w') as f:
		pass

# Setting up logging for the web server
webserver.logger = logging.getLogger('webserver_logger')

# Setting the lowest severity level to handle
webserver.logger.setLevel(logging.DEBUG)

# Creating a formatter with a specific format for log messages GMT time
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Creating a file handler that rotates log files when they reach 0.2 MB
handler = RotatingFileHandler('./webserver.log', maxBytes=20000, backupCount=5)

# Setting the formatter for the file handler
handler.setFormatter(formatter)

# Adding the file handler to the logger
webserver.logger.addHandler(handler)
