import time
import threading
import msvcrt
import queue

POSITIVE = 'z' # Key binding to positive reward
NEGATIVE = '/' # Key binding to negative reward

class TAMERInput(threading.Thread):
    '''
    This is an asynchronous thread dedicated to accepting human feedback as a reward signal for a supervised learner, as per the TAMER framework.
    It waits for input from the user, then checks the input queue for the most recent state-action pair taken by the learner. It maps the user
    input to a numarical reward signal, then places it in the output queue to be processed by the learner.
    '''
    
    def __init__(self, in_q, out_q):
        super(TAMERInput, self).__init__()
        self.in_q = in_q # should be a LIFO queue so we guarantee the most recent state is checked
        self.out_q = out_q # FIFO queue for feedback
        self.stoprequest = threading.Event()
        
    def run(self):
        while not self.stoprequest.isSet():
            # blocks the thread until a key is pressed, which means we only look for state/action if the user tries to send feedback
            key = msvcrt.getche() 
            if key == NEGATIVE:
                reward = -1
            elif key == POSITIVE: 
                reward = 1
            else: # ignore any key presses that aren't valid feedback keys
                continue
            
            #send reward back to the supervised learner
            #if the queue is empty, we've already sent a signal this frame, so we ignore this key press
            try:
                # non-blocking get is probably unnecessary, but timeout is there in case of multiple key presses in one timeframe
                # Popping the S/A pair off the queue ensures we only get one signal per frame
                state_action = self.in_q.get(block = False, timeout = 0.05) 
                
                # not sure of the format the supervised learner is gonna want for the feedback; that should be fixed here
                self.out_q.put((state_action,reward))
            except Queue.Empty:
                continue
            
    def join(self, timeout = None):
        self.stoprequest.set()
        super(TAMERInput, self).join(timeout)
