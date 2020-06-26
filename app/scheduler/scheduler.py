import threading

from datetime import datetime
import time


# Fixed Scheduler class
class FixedScheduler():
    
    # Constructor.
    #   > precision:    delay between every check.
    #   > debug:        if True, displays logging messages  
    def __init__(self, precision=0.1):
        self.precision = precision
        
        self._tasks = []
        self._schedThread = threading.Thread(target=self._scheduler, args=())
        self._schedStopped = True


    # Add a task to the scheduler. If it's already running, it has to be restarted
    #   > seconds:      the seconds of delay
    #   > function:     the function that has to be executed
    #   > args:         the arguments of the function (in tuple)
    def addTask(self, seconds, function, args=()):
        self._tasks.append(
            {
                'function'  : function,
                'arguments' : args,
                'seconds'   : seconds
            }
        )


    # Start the scheduler. It'll be started in a new thread
    def start(self):
        if not self._schedThread.isAlive():
            self._schedStopped = False
            self._schedThread.start()


    # Stop the scheduler.
    def stop(self):
        if self._schedThread.isAlive():
            self._schedStopped = True


    # Clock for the scheduler. Every second, checks if there are tasks to be executed.
    # In this particular scheduler the seconds are fixed and relative to the system's clock.
    # Example: a task with a delay of 5 seconds will be executed at 00:00:05, 00:00:10, 00:00:15, ...
    def _scheduler(self):
        seconds = 1 # Check every second (like a clock!)
        #Loop until the process has to be stopped
        while not self._schedStopped:

            #Wait until the start of the next second
            start_time = int(time.time())
            while(int(time.time())-start_time < seconds):
                time.sleep(self.precision)
            
            #Save the current second (epoch format)
            current_second = int(time.time())

            #For every task, check if it has to be executed
            for task in self._tasks:
                #Check if the current time (epoch format) is a multiple of the seconds of the task
                if(current_second % task['seconds'] == 0):
                    threading.Thread(target=task['function'], args=task['arguments']).start()
                    # task['function'](*task['arguments'])    #Task is executed with arguments unpacked
                else:
                    pass                                    #Task is not executed
