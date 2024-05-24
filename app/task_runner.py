import json
import os
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

class ThreadPool:
	"""
	Class representing a thread pool for executing tasks asynchronously.
	"""
	def __init__(self):
		"""
		Initialize the ThreadPool with the number of threads defined in the environment variable TP_NUM_OF_THREADS.
		If the environment variable is not set use the number of threads your hardware concurrency allows.
		"""
		if 'TP_NUM_OF_THREADS' in os.environ:
			self.num_threads = int(os.environ.get('TP_NUM_OF_THREADS'))
		else:
			self.num_threads = os.cpu_count()

		self.thread_pool = ThreadPoolExecutor(max_workers=self.num_threads)
		self.job_counter = 1
		self.data = {}

	def update_task_status(self, future):
		"""
		Update task status and save result to a JSON file.

		Parameters:
			future (concurrent.futures.Future): The future object representing the result of a task.

		Returns:
			None
		"""
		task_result = future.result()
		job_id = task_result[0]
		data = task_result[1]

		with open(f"results/{job_id}.json", "w") as f:
			json.dump(data, f)

		self.data[str(job_id)] = {"status": "done"}

	def add_task(self, data, query):
		"""
		Add a task to the thread pool for execution.

		Parameters:
			data (dict): Data to be passed to the task.
			query (callable): The function to be executed asynchronously.

		Returns:
			int: The ID of the added task.
		"""
		def callback(future):
			self.update_task_status(future)

		job = TaskRunner(self.job_counter, data, query)
		self.job_counter += 1
		self.data[str(job.job_id)] = {"status": "running"}

		future = self.thread_pool.submit(job.execute)
		future.add_done_callback(callback)

		return job.job_id

	def get_task_status(self, job_id):
		"""
		Get the status of a specific task.

		Parameters:
			job_id (str): The ID of the task.

		Returns:
			dict: A dictionary containing the status of the task.
		"""
		if job_id not in self.data:
			return {"status": "not found"}
		return self.data[job_id]

	def graceful_shutdown(self):
		"""
		Gracefully shutdown the thread pool.
		"""
		self.thread_pool.shutdown()

class TaskRunner(Thread):
	"""
	Class representing a task runner thread.
	"""
	def __init__(self, job_id, data, query):
		"""
		Initialize the TaskRunner with job ID, data, and query.

		Parameters:
			job_id (int): The ID of the task.
			data (dict): Data to be passed to the task.
			query (callable): The function to be executed asynchronously.
		"""
		Thread.__init__(self)
		self.job_id = job_id
		self.data = data
		self.query = query

	def execute(self):
		"""
		Execute the task.

		Returns:
			tuple: A tuple containing the job ID and the result of the task.
		"""
		result = self.query(self.data)
		job_result = (self.job_id, result)
		return job_result
