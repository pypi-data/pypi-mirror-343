"""
Executor - Handles concurrent resource loading (threaded or multiprocess).
"""

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

class Executor:
    """
    Executor for running tasks concurrently.
    Supports multithreading and multiprocessing.
    """

    def __init__(self, max_concurrent=5, multithreading=True, multiprocessing=False):
        """
        Initialize the executor.

        Args:
            max_concurrent (int): Maximum number of parallel workers.
            multithreading (bool): Use threads if True (default).
            multiprocessing (bool): Use processes if True (overrides threading if enabled).
        """
        self.max_concurrent = max_concurrent
        self.multithreading = multithreading
        self.multiprocessing = multiprocessing

    def submit_all(self, tasks):
        """
        Submit multiple callables concurrently and return results as they complete.

        Args:
            tasks (list of callables): Functions to execute.

        Returns:
            list: List of results (completed order).
        """
        results = []

        if self.multiprocessing:
            ExecutorClass = ProcessPoolExecutor
        else:
            ExecutorClass = ThreadPoolExecutor  # fallback default

        with ExecutorClass(max_workers=self.max_concurrent) as executor:
            futures = [executor.submit(task) for task in tasks]
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    print(f"Error: {e}")
                    results.append(e)

        return results
