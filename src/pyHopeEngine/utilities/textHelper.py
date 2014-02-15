'''
Created on Jul 1, 2013

@author: Devon

Creates text that can be wrapped, justified, 
colored, and other options using the Glyph module.
'''

from glyph import Macros, Glyph
from pygame.font import SysFont
from pyHopeEngine import engineCommon as ECOM

Macros['black'] = ('color', ECOM.Colors.BLACK)
Macros['white'] = ('color', ECOM.Colors.WHITE)
Macros['gray'] = ('color', ECOM.Colors.GRAY)
Macros['red'] = ('color', ECOM.Colors.RED)
Macros['green'] = ('color', ECOM.Colors.GREEN)
Macros['blue'] = ('color', ECOM.Colors.BLUE)
Macros['teal'] = ('color', ECOM.Colors.TEAL)
Macros['olive'] = ('color', ECOM.Colors.OLIVE)
Macros['purple'] = ('color', ECOM.Colors.PURPLE)
Macros['silver'] = ('color', ECOM.Colors.SILVER)
Macros['defaultFont'] = ('font', SysFont('tahoma', 24))
Macros['largeFont'] = ('font', SysFont('tahoma', 32))
Macros['largerFont'] = ('font', SysFont('tahoma', 48))
        
def createText(text, rect, justify = None):
    glyph = Glyph(rect)
    glyph.input(text, justify)
    glyph.update()
    
    return glyph