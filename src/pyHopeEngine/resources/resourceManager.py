'''
Created on Aug 20, 2013

@author: Devon

Defines a resource manager
'''

import os
import sys

class ResourceManager:
    '''Retrieves resources from files'''
    def __init__(self):
        self.dataDir = None
            
    def setDataDir(self, currDir, dataDir):
        '''Sets the main data directory. Assumes that it is
        one level above where the main app is located.
        
        Keyword arguments:
            currDir -- current directory of the main app
            dataDir -- data directory location relative to main app
        '''
        
        #Determines if app has been frozen by cx_Freeze module         
        if getattr(sys, 'frozen', False):
            dataDir = os.path.split(dataDir)
            dataDir = dataDir[1]
            self.dataDir = os.path.join(os.path.dirname(sys.executable), dataDir)
        else:
            directory = os.path.join(currDir, dataDir)
            directory = os.path.normpath(directory)
            self.dataDir = directory

    def getFile(self, file):
        '''Returns a file from the data directory'''
        return os.path.join(self.dataDir, file)