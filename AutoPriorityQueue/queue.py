from queue import PriorityQueue
import threading


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
        self._queue.put((priority, function, args))
        self._isEmptyEvent.set()    # Wakes up the queue thread in case it's sleeping


    # Method executed by the thread. It waits until there's something new into the queue
    # This is possible by using the Event object.
    def _executeQueue(self):
        while True:
            self._isEmptyEvent.wait() #Wait until there are new tasks    
            while not self._queue.empty():
                next_task = self._queue.get()
                next_task[1](*next_task[2])
            self._isEmptyEvent.clear()



# Automatic PriorityQueue Class
class Task():

    # Constructor
    def __init__(self, function, args=()):        
        self._function = function
        self._args = args

        