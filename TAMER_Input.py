import time
import threading
import msvcrt
import Queue

POSITIVE = 'z' # Key binding to positive reward
NEGATIVE = '/' # Key binding to negative reward

class TAMERInput(threading.Thread):
    
    def __init__(self, in_q, out_q):
        super(TAMERInput, self).__init__()
        self.in_q = in_q
        self.out_q = out_q
        self.stoprequest = threading.Event()
        
    def run(self):
        while not self.stoprequest.isSet():
            key = msvcrt.getche()
            if key == NEGATIVE:
                reward = -1
            elif key == POSITIVE: 
                reward = 1
            else:
                continue
            
            #send reward back to the supervised learner
            try:
                state_action = self.in_q.get()
                self.out_q.put((state_action,reward))
            except Queue.Empty:
                continue
            
    def join(self, timeout = None):
        self.stoprequest.set()
        super(TAMERInput, self).join(timeout)