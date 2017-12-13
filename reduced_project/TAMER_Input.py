import threading
import queue
import tkinter
import tkinter.ttk

class TAMERInput(threading.Thread):
    '''
    This is an asynchronous thread dedicated to accepting human feedback as a reward signal for a supervised learner, as per the TAMER framework.
    It waits for input from the user, then checks the input queue for the most recent state-action pair taken by the learner. It maps the user
    input to a numerical reward signal, then places it in the output queue to be processed by the learner.
    '''
    def positive(self):
        try:
            # non-blocking get is probably unnecessary, but timeout is there in case of multiple key presses in one timeframe
            # Popping the S/A pair off the queue ensures we only get one signal per frame
            state_action = self.in_q.get(block = False, timeout = 0.05) 
            
            # not sure of the format the supervised learner is gonna want for the feedback; that should be fixed here
            self.out_q.put((state_action,1))
            
        # If the queue is empty, we've already given feedback this frame, so do nothing
        except queue.Empty:
            return
            
        
    def negative(self):
        try:
            # non-blocking get is probably unnecessary, but timeout is there in case of multiple key presses in one timeframe
            # Popping the S/A pair off the queue ensures we only get one signal per frame
            state_action = self.in_q.get(block = False, timeout = 0.05) 
            
            # not sure of the format the supervised learner is gonna want for the feedback; that should be fixed here
            self.out_q.put((state_action,-1))
            
        # If the queue is empty, we've already given feedback this frame, so do nothing
        except queue.Empty:
            return        
    
    def __init__(self, in_q, out_q):
        super(TAMERInput, self).__init__()
        
        self.in_q = in_q 
        self.out_q = out_q 
        self.stoprequest = threading.Event()
        
        self.start()
        
    # Must be called to actually start the window
    def run(self):
        # Set up the tkinter window
        self.tkroot = tkinter.Tk()
        self.tkroot.title("TAMER Feedback")
        self.mainframe = tkinter.ttk.Frame(self.tkroot, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky='nesw')
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        tkinter.ttk.Button(self.mainframe, text="+", command=self.positive).grid(column=0, row=0,sticky='n')
        tkinter.ttk.Button(self.mainframe, text="-", command=self.negative).grid(column=0, row=1,sticky='s')
        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
        # Allow the user to use the up and down arrows instead of clicking
        self.tkroot.bind('<Up>', lambda event: self.positive())
        self.tkroot.bind('<Down>', lambda event: self.negative())
        self.tkroot.mainloop()

    # Can be called instead of closing the window to end the process
    def join(self, timeout = None):
        self.stoprequest.set()
        super(TAMERInput, self).join(timeout)
        
