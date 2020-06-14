from queue import PriorityQueue
import threading
import time

# Automatic PriorityQueue Class
class Queue():

    # Constructor
    def __init__(self):        
        # Priority queue object. It's re-sorted after every insertion
        self._queue = PriorityQueue()

        # Event flag that's used to wake up the queue thread
        self._isEmptyEvent = threading.Event()

        # Thread that manages the execution of the tasks
        self._schedThread = threading.Thread(target=self._executeQueue, args=())
        self._schedThread.start()


    # Method used to add a task to the queue
    #   > priority:     (integer) higher number, lower priority
    #   > function:     function that has to be executed (the task in other words)
    #   > args:         arguments of the function to be executed
    def add(self, priority, function, args=()):
        new_task = Task(function, args)
        self._queue.put((priority, new_task))
        self._isEmptyEvent.set()    # Wakes up the queue thread in case it's sleeping
        return new_task

    # Method executed by the thread. It waits until there's something new into the queue
    # This is possible by using the Event object.
    def _executeQueue(self):
        while True:
            self._isEmptyEvent.wait() #Wait until there are new tasks
            while not self._queue.empty():
                next_task = self._queue.get()[1]
                next_task.execute()
            self._isEmptyEvent.clear()

    def screenshot(self):
        print('\n\n\n') 
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        for task in self._queue.queue:
            print("{:6d} - ".format(task[0]), end='')
            print(task[1])
            print('-------------------------------------------------------------------------')
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print('\n\n\n') 


class Task():

    def __init__(self, function, args):
        self.function = function
        self.args = args
        self.result = None

        self.time_added = time.time() 

        self.taskConcluded = threading.Event()

    def __lt__(self, other):
        return self if self.time_added < other.time_added else other

    def execute(self):
        self.result = self.function(*self.args)
        self.taskConcluded.set()
        return self.result
        
    def getResult(self):
        self.taskConcluded.wait()
        return self.result
