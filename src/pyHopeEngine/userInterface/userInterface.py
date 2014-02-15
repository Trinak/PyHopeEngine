'''
Created on Jul 1, 2013

@author: Devon

Defines the base UI
'''

import pygame

from pgu.gui import App
from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import BaseTable

class BaseUI(App):
    '''Main UI widget to hold other widgets'''
    def __init__(self, **params):
        '''Create new BaseUI to hold widgets
        
        Keyword arguments:
            x, y -- position UI
            width, height -- size of UI
            align, valign -- alignment
        '''
        super().__init__(**params)
        self.owner = None
        self.visible = True
        self.widget = BaseTable(**params)
        self.screen = pygame.display.get_surface()
        
    def init(self, widget = None, screen = None, area = None):
        if screen == None:
            screen = self.screen
        
        if area is not None:
            area = pygame.Rect(area)

        super().init(widget, screen, area)
    
    def render(self):
        if self.visible:
            self.paint()
        
        if ECOM.Debug.TABLE:
            self.widget.debugDraw(self.appArea)
    
    def onPygameEvent(self, event):
        self.event(event)        
            
    def cleanUp(self):
        pass
        