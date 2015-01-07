'''
Created on Jul 3, 2013

@author: Devon

Defines various gui widgets
'''

import pygame

from pgu import gui
from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine.utilities.textHelper import createText


class BaseTable(gui.Table):
    '''A Base Table used to organize other widgets'''
    def __init__(self, **params):
        super().__init__(**params)

    def addWidget(self, widget, **params):
        '''Adds a widget to the table'''        
        self.td(widget, **params)
        
    def addButton(self, value, func, isImage = False, **params):
        '''Adds a button to the table'''
        if isImage:
            if isinstance(value, str):
                value = ECOM.engine.resourceManager.getFile(value)
            image = gui.Image(value, **params)
            button = gui.Button(image, **params)
        else:
            button = gui.Button(value, **params)
            
        button.connect(gui.CLICK, func)
        self.addWidget(button, **params)
        
        return button
    
    def addInput(self, value = "", size=20, **params):
        '''Adds a text input to the table'''
        textInput = gui.Input(value, size, **params)
        self.addWidget(textInput, **params)
        
        return textInput
        
    def addImage(self, value, **params):
        '''Adds an image to the table'''
        if isinstance(value, str):
            value = ECOM.engine.resourceManager.getFile(value)
            
        image = gui.Image(value, **params)
        self.addWidget(image, **params)
        
        return image
    
    def addProgressBar(self, value, minValue, maxValue, **params):
        bar = gui.ProgressBar(value, minValue, maxValue, **params)
        self.addWidget(bar)
        
        return bar
    
    def addText(self, text, rect, justify = None, **params):
        '''Adds text to the table as an image'''
        textRect = pygame.Rect(rect)
        textArea = createText(text, textRect, justify)
        image = gui.Image(textArea.image, **params)
        self.addWidget(image, **params)
        
        return image
    
    def addLabel(self, value = "", **params):
        '''Adds a label to the table'''
        label = gui.Label(value, **params)
        self.addWidget(label, **params)
        
        return label
    
    def addSpacer(self, width, height, **params):
        '''Adds a blank space to the table'''
        spacer = gui.Spacer(width, height, **params)
        self.addWidget(spacer, **params)
        
        return spacer
    
    def addSelect(self, value = None, **params):
        '''Adds a drop down select box to the table'''
        select = BaseSelect(value, **params)
        self.addWidget(select, **params)
        
        return select
    
    def connectEvent(self, widget, eventType, func, *params):
        '''Connects a widget to a specific event'''
        widget.connect(eventType, func, *params)
    
    def clearRow(self, rowNum):
        '''Removes all widgets in the given row'''
        for cell in self._rows[rowNum]:
            if isinstance(cell, dict) and cell["widget"] in self.widgets:
                self.widgets.remove(cell["widget"])
        
        for i in range(len(self._rows[rowNum])):
            self._rows[rowNum][i] = None
                        
    def debugDraw(self, area):
        '''Draws the table layout'''
        renderer = ECOM.engine.renderer
        surface = pygame.Surface((area.width, area.height))
        surface.fill(ECOM.Colors.BLACK)
        surface.set_colorkey(ECOM.Colors.BLACK)
        sub = surface.subsurface(self._rect_content)

        for widget in self.widgets:
            pygame.draw.rect(sub, ECOM.Colors.RED, widget.rect, 1)
        
        renderer.render(surface, area)
        pygame.draw.rect(renderer.displaySurface, ECOM.Colors.GREEN, area,  1)


class BaseDialog(gui.Dialog):
    '''A dialog box'''
    def __init__(self, title, main, **params):
        title = gui.Label(title)
        super().__init__(title, main, **params)


class BaseSelect(gui.Select):
    '''A Select box with drop down options'''
    def __init__(self, value = None, **params):
        super().__init__(value, **params)
    
    def getValue(self):
        if self.value is not None:
            return self.value.value
        else:
            return None

        
        