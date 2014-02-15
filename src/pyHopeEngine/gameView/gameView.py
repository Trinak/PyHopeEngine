'''
Created on Aug 1, 2013

@author: Devon

Defines base view
'''


class GameView:
    def __init__(self):
        pass
    
    
    def cleanUp(self):
        raise NotImplementedError("cleanUp not implemented.")
    
    
    def update(self):
        raise NotImplementedError("update not implemented.")
    
    
    def render(self):
        raise NotImplementedError("render not implemented.")
    
    
    def onPygameEvent(self, event):
        raise NotImplementedError("onPygameEvent not implemented.")