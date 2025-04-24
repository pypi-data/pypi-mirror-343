"""
Timer Module.
"""

import time


class Timer:
    """
    Timer class
    """

    def __init__(self):
        """initialize the timer"""
        self.start: float | None = None
        self.stop: float | None = None
        self.elapsed_time: float | None = None

    def __enter__(self):
        """start the tiemr"""
        self.start_timer()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> float:
        """stop the timer"""
        if exc_type:
            print(exc_type)
            print(f"An exception occured: {exc_value}")
            print(traceback)

        elapsed_time: float = self.stop_timer()
        self.elapsed_time = elapsed_time
        return elapsed_time

    def start_timer(self):
        """start the timer"""
        self.start = time.time()

    def stop_timer(self) -> float:
        """stop timer and return the lapsed time"""
        self.stop = time.time()
        return self.stop - self.start
