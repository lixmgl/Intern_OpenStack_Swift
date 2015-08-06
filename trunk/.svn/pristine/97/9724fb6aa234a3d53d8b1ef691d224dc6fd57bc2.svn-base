from Queue import Queue
import threading

class WorkerQueue(threading.Thread):
    """ w = WorkerQueue() 
        w.start()
        w.send(work)
        w.close() """
    
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.input_queue = Queue()
        
    def send(self, item):
        self.input_queue.put(item)
        
    def close(self):
        self.input_queue.put(None)
        self.input_queue.join()
        
    def run(self):
        while True:
            item = self.input_queue.get()
            if item is None:
                break
            print(item)
            self.input_queue.task_done()
        self.input_queue.task_done()
        return