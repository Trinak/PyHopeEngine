'''
Created on Nov 21, 2013

@author: Devon Arrington
'''

from pyHopeEngine.userInterface.userInterface import BaseUI


class HealthBar(BaseUI):
    def __init__(self, area, value, minValue, maxValue, **params):
        super().__init(**params)
        self.widget.addProgressBar(value, minValue, maxValue, **params)
        self.init(area = area)