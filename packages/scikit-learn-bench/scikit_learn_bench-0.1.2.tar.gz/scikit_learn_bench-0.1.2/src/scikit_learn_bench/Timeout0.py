import multiprocessing
import time
import os
import signal

"""
Timeout warper kill a function when it is too long. It works internally by warping the function call in a PID.
"""

PATIENCE_FOR_SPAWNING_PROCESS=0.001

def timeout_warp(func, timeout):
    def wrapper(*args, **kwargs):
        output_queue = multiprocessing.Queue()

        def target():
            """this function manage the input/output and kill hierarchically"""
            os.setpgrp()  #all children will belong to the same group of processes
            result = func(*args, **kwargs)
            output_queue.put(result)

        proc = multiprocessing.Process(target=target)
        proc.start()

        proc.join(timeout=timeout) # warning: join in debug mode will always wait `timeout` even if not necessary

        #if proc.is_alive():
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass # it is possible that the process is already killed
        #proc.join()

        if not output_queue.empty():
            return output_queue.get()
        else:
            return None  # Timeout reached, no result

    return wrapper

