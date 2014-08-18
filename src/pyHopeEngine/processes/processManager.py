'''
Created on Feb 22, 2014

@author: Devon Arrington
'''

from pyHopeEngine import ProcessState as PS

class ProcessManager(object):
    def __init__(self):
        self.processes = []
    
    def update(self, elapsedTime):
        def checkProcess(process):
            if process.state == PS.UNINITIALIZED:
                process.init()
            
            if process.state == PS.RUNNING:
                process.update(elapsedTime)
            
            if process.isFinished():
                if process.state == PS.SUCCEEDED:
                    process.onSuccess()
                    if process.child:
                        self.addProcess(process.child)
                        process.removeChild()
                
                elif process.state == PS.FAILED:
                    process.onFail()
                elif process.state == PS.ABORTED:
                    process.onAbort()
            else:
                return process
                
        self.processes[:] = [process for process in self.processes if checkProcess(process)]  

    def addProcess(self, process):
        self.processes.append(process)