import json
from decimal import Decimal

from flask import request, jsonify

from app import webserver

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
	if request.method == 'POST':
		# Assuming the request contains JSON data
		data = request.json
		print(f"got data in post {data}")

		# Process the received data
		# For demonstration purposes, just echoing back the received data
		response = {"message": "Received data successfully", "data": data}

		# Sending back a JSON response
		return jsonify(response)
	else:
		# Method Not Allowed
		return jsonify({"error": "Method not allowed"}), 405

def check_data_for_logging(data, message_error, message_success):
	"""
	Check data for logging. If data is None,
	then it means that the request was not received properly.

	Parameters:
		data (any): The data to check.
		message_error (str): Error message to log if data is None.
		message_success (str): Success message to log if data is not None.

	Returns:
		None
	"""
	if data is None:
		return webserver.logger.error(message_error)

	return webserver.logger.info(message_success)

def check_job_id(job_id, message_error, message_success):
	"""
	Check job_id for logging. If job_id is None,
	then it means that the job was not added to the queue or
	the job_id is invalid.

	Parameters:
		job_id (any): The job_id to check.
		message_error (str): Error message to log if job_id is None.
		message_success (str): Success message to log if job_id is not None.

	Returns:
		None
	"""
	if job_id is None:
		return webserver.logger.error(message_error)

	return webserver.logger.info(message_success)

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
	"""
	Handle the GET request for the results of a job.

	Parameters:
		job_id (str): The job_id to get the results for.

	Returns:
		JSON: The status of the job and the data if the job is done.
	"""
	status = webserver.tasks_runner.get_task_status(job_id)["status"]
	data = None

	check_job_id(job_id, f"Failed to get job_id {job_id}", f"Got job_id {job_id}")

	if status == "not found":
		return jsonify({"status": "error","reason": "Invalid job_id"})

	if status == "done":
		with open(f"results/{job_id}.json", "r") as f:
			data = json.load(f)

	check_job_id(job_id, f"Failed to get data from job_id {job_id}", \
			  f"Got data from job_id {job_id}")

	return jsonify({'status': status,'data': data})

def api_states_mean(data):
		"""
		Calculate the mean of the data for each state for a given question.

		Parameters:
			data (dict): The data containing the question.

		Returns:
			dict: The mean of the data for each state for the given question.
		"""
		data_frame = webserver.data_ingestor.data
		filtered_data = data_frame[data_frame['Question'] == data['question']]

		state_question_means = filtered_data.groupby(['LocationDesc', 'Question']) \
		['Data_Value'].mean().reset_index()

		result = state_question_means.set_index('LocationDesc')['Data_Value'].to_dict()

		return result

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
	"""
	Handle the POST request for the mean of the data for each state for a given question.

	Returns:
		JSON: The job_id of the task.
	"""
	data = request.json

	check_data_for_logging(data, "Failed to get request", f"Got request {data}")

	if data['question'] in webserver.data_ingestor.questions:
		job_id = webserver.tasks_runner.add_task(data, api_states_mean)

	check_job_id(job_id, "Failed to add job to the queue", f"Job {job_id} added to the queue")

	return jsonify({"job_id" : job_id})

def api_state_mean(data):
	"""
	Calculate the mean of the data for a given state for a given question.

	Parameters:
		data (dict): The data containing the state and the question.

	Returns:
		dict: The mean of the data for the given state for the given question.
	"""
	data_frame = webserver.data_ingestor.data

	filtered_data = data_frame[(data_frame['LocationDesc'] == data['state'])
							  & (data_frame['Question'] == data['question'])]

	result = filtered_data.groupby('LocationDesc')['Data_Value'].mean().to_dict()

	return result


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
	"""
	Handle the POST request for the mean of the data for a given state for a given question.

	Returns:
		JSON: The job_id of the task.
	"""
	data = request.json

	check_data_for_logging(data, "Failed to get request", f"Got request {data}")

	if data['question'] in webserver.data_ingestor.questions:
		job_id = webserver.tasks_runner.add_task(data, api_state_mean)

	check_job_id(job_id, "Failed to add job to the queue", f"Job {job_id} added to the queue")

	return jsonify({"job_id" : job_id})

def api_best5(data):
	"""
	Calculate the best 5 states for a given question by mean.

	Parameters:
		data (dict): The data containing the question.

	Returns:
		dict: The best 5 states for the given question.
	"""
	data_frame = webserver.data_ingestor.data
	filtered_data = data_frame[data_frame['Question'] == data['question']]

	state_question_means = filtered_data.groupby(['LocationDesc', 'Question']) \
		['Data_Value'].mean().reset_index()

	if data['question'] in webserver.data_ingestor.questions_best_is_min:
		result = state_question_means.set_index('LocationDesc')['Data_Value'] \
												.sort_values().head(5).to_dict()
	else:
		result = state_question_means.set_index('LocationDesc')['Data_Value'] \
									.sort_values(ascending=False).head(5).to_dict()

	return result

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
	"""
	Handle the POST request for the best 5 states for a given question by mean.

	Returns:
		JSON: The job_id of the task.
	"""
	data = request.json

	check_data_for_logging(data, "Failed to get request", f"Got request {data}")

	if data['question'] in webserver.data_ingestor.questions:
		job_id = webserver.tasks_runner.add_task(data, api_best5)

	check_job_id(job_id, "Failed to add job to the queue", f"Job {job_id} added to the queue")

	return jsonify({"job_id" : job_id})

def api_worst5(data):
	"""
	Calculate the worst 5 states for a given question by mean.

	Parameters:
		data (dict): The data containing the question.

	Returns:
		dict: The worst 5 states for the given question.
	"""
	data_frame = webserver.data_ingestor.data
	filtered_data = data_frame[data_frame['Question'] == data['question']]

	# Calculăm media pentru fiecare combinație de 'LocationDesc' și 'QuestionID'
	state_question_means = filtered_data.groupby(['LocationDesc', 'Question']) \
											['Data_Value'].mean().reset_index()

	if data['question'] in webserver.data_ingestor.questions_best_is_min:
		result = state_question_means.set_index('LocationDesc')['Data_Value'] \
											.sort_values().tail(5).to_dict()
	else:
		result = state_question_means.set_index('LocationDesc')['Data_Value'] \
								.sort_values(ascending=False).tail(5).to_dict()

	return result

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
	"""
	Handle the POST request for the worst 5 states for a given question by mean.

	Returns:
		JSON: The job_id of the task.
	"""
	data = request.json

	check_data_for_logging(data, "Failed to get request", f"Got request {data}")

	if data['question'] in webserver.data_ingestor.questions:
		job_id = webserver.tasks_runner.add_task(data, api_worst5)

	check_job_id(job_id, "Failed to add job to the queue", f"Job {job_id} added to the queue")

	return jsonify({"job_id" : job_id})

def api_global_mean(data):
	"""
	Calculate the global mean for a given question.

	Parameters:
		data (dict): The data containing the question.

	Returns:
		dict: The global mean for the given question.
	"""
	data_frame = webserver.data_ingestor.data
	filtered_data = data_frame[data_frame['Question'] == data['question']]
	mean = filtered_data['Data_Value'].mean()
	result = {"global_mean": mean}
	return result

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
	"""
	Handle the POST request for the global mean for a given question.

	Returns:
		JSON: The job_id of the task.
	"""
	data = request.json

	check_data_for_logging(data, "Failed to get request", f"Got request {data}")

	if data['question'] in webserver.data_ingestor.questions:
		job_id = webserver.tasks_runner.add_task(data, api_global_mean)

	check_job_id(job_id, "Failed to add job to the queue", f"Job {job_id} added to the queue")

	return jsonify({"job_id" : job_id})


def api_diff_from_mean(data):
	"""
	Calculate the difference between the global mean and the mean for each state for a given
	question.

	Parameters:
		data (dict): The data containing the question.

	Returns:
		dict: The difference between the global mean and the mean for each state for the given
		question.
	"""
	data_frame = webserver.data_ingestor.data
	filtered_data = data_frame[data_frame['Question'] == data['question']]
	global_mean = filtered_data['Data_Value'].mean()
	state_means = filtered_data.groupby('LocationDesc')['Data_Value'].mean()
	result = global_mean - state_means

	return result.to_dict()

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
	"""
	Handle the POST request for the difference between the global mean and the
	mean for each state for a given question.

	Returns:
		JSON: The job_id of the task.
	"""
	data = request.json

	check_data_for_logging(data, "Failed to get request", f"Got request {data}")

	if data['question'] in webserver.data_ingestor.questions:
		job_id = webserver.tasks_runner.add_task(data, api_diff_from_mean)

	check_job_id(job_id, "Failed to add job to the queue", f"Job {job_id} added to the queue")

	return jsonify({"job_id" : job_id})

def api_state_diff_from_mean(data):
	"""
	Calculate the difference between the global mean and the mean for a given state for a given
	question.

	Parameters:
		data (dict): The data containing the state and the question.

	Returns:
		dict: The difference between the global mean and the mean for the given state for the given
		question.
	"""
	data_frame = webserver.data_ingestor.data

	# Convertim valorile din data_frame în Decimal pentru precizie mai mare
	data_frame['Data_Value'] = data_frame['Data_Value'].apply(Decimal)

	# Calculăm media pentru statul dat și media globală
	state_mean = data_frame[(data_frame['LocationDesc'] == data['state'])
						   & (data_frame['Question'] == data['question'])]['Data_Value'].mean()
	global_mean = data_frame[data_frame['Question'] == data['question']]['Data_Value'].mean()

	# Calculăm diferența dintre media globală și media statului
	result = float(global_mean - state_mean)

	# {"Virgin Islands": -5.858706315144083}
	return {data['state']: result}

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
	"""
	Handle the POST request for the difference between the global mean and the mean for a
	given state for a given question.

	Returns:
		JSON: The job_id of the task.
	"""
	data = request.json

	check_data_for_logging(data, "Failed to get request", f"Got request {data}")

	if data['question'] in webserver.data_ingestor.questions:
		job_id = webserver.tasks_runner.add_task(data, api_state_diff_from_mean)

	check_job_id(job_id, "Failed to add job to the queue", f"Job {job_id} added to the queue")

	return jsonify({"job_id" : job_id})

def api_mean_by_category(data):
	"""
	Calculate the mean of the data for each category for a given question.

	Parameters:
		data (dict): The data containing the question.

	Returns:
		dict: The mean of the data for each category for the given question.
	"""
	data_frame = webserver.data_ingestor.data
	filtered_data = data_frame[data_frame['Question'] == data['question']]
	result = filtered_data.groupby(['LocationDesc', 'StratificationCategory1', \
								 'Stratification1'])['Data_Value'].mean().to_dict()
	return {str(key): value for key, value in result.items()}

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
	"""
	Handle the POST request for the mean of the data for each category for a given question.

	Returns:
		JSON: The job_id of the task.
	"""
	data = request.json

	check_data_for_logging(data, "Failed to get request", f"Got request {data}")

	if data['question'] in webserver.data_ingestor.questions:
		job_id = webserver.tasks_runner.add_task(data, api_mean_by_category)

	check_job_id(job_id, "Failed to add job to the queue", f"Job {job_id} added to the queue")

	return jsonify({"job_id" : job_id})

def api_state_mean_by_category(data):
	"""
	Calculate the mean of the data for each category for a given question for a given state.

	Parameters:
		data (dict): The data containing the state and the question.

	Returns:
		dict: The mean of the data for each category for the given question for the given state.
	"""
	data_frame = webserver.data_ingestor.data
	filtered_data = data_frame[(data_frame['LocationDesc'] == data['state']) & \
							(data_frame['Question'] == data['question'])]
	result = filtered_data.groupby(['StratificationCategory1', 'Stratification1']) \
		['Data_Value'].mean().to_dict()
	return {data['state']: {str(key): value for key, value in result.items()}}

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
	"""
	Handle the POST request for the mean of the data for each category for a given question
	for a given state.

	Returns:
		JSON: The job_id of the task.
	"""
	data = request.json

	check_data_for_logging(data, "Failed to get request", f"Got request {data}")

	if data['question'] in webserver.data_ingestor.questions:
		job_id = webserver.tasks_runner.add_task(data, api_state_mean_by_category)

	check_job_id(job_id, "Failed to add job to the queue", f"Job {job_id} added to the queue")

	return jsonify({"job_id" : job_id})

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
	"""
	Handle the GET request to shut down the server gracefully.

	Returns:
		JSON: A message indicating whether the server is shutting down gracefully.
	"""
	successful = webserver.tasks_runner.graceful_shutdown()
	if successful:
		webserver.logger.info("Shutting down the server gracefully")
		return jsonify({"message": "Shutting down the server gracefully"})

	webserver.logger.error("Failed to shut down the server gracefully")
	return jsonify({"error": "Failed to shut down the server gracefully"}), 500

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
	"""
	Handle the GET request to get the jobs.

	Returns:
		JSON: The data containing the jobs.
	"""
	webserver.logger.info("Received request for jobs")
	return jsonify(webserver.tasks_runner.data)

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
	"""
	Handle the GET request to get the number of jobs.

	Returns:
		JSON: The number of jobs.
	"""
	webserver.logger.info("Received request for number of jobs")
	return jsonify({"num_jobs": len(webserver.tasks_runner.data)})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
	routes = get_defined_routes()
	msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

	# Display each route as a separate HTML <p> tag
	paragraphs = ""
	for route in routes:
		paragraphs += f"<p>{route}</p>"

	msg += paragraphs
	return msg

def get_defined_routes():
	routes = []
	for rule in webserver.url_map.iter_rules():
		methods = ', '.join(rule.methods)
		routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
	return routes
