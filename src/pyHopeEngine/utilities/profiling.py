'''
Created on Aug 21, 2013

@author: Devon

Profiler using pycallgraph
'''

import pycallgraph

class Profiler:
    included = None
    excluded = ['pycallgraph.*', 'pydev*', '_handle_fromlist',
                'SourceFileLoader.*', 'new_module', '_find_and_load*',
                '_ImportLock*', '_find_module*', '_get_loader',
                '_open_registry', 'cache_from_source', '_path*',
                '_relax_case', '_call_with*', '_ModuleLock*',
                '_verbose*', '_r_long', '_get_module*',
                '_search_registry', 'FileFinder*', 'find_module',
                'ExtensionFileLoader.*', 'load_module', 'type.*',
                'set_package_wrapper', '<genexpr>', 'xml.*' ]
    excludedSTD = ['traceback*', 'encodings*', 'linecach*',
                   'sre_parse*', 'sre_compile*', 're.*',
                   'ntpath*', 'genericpath*', 'codecs*', 'locale*',
                   'stat.*']
    excludedLibs = []
    
    def __init__(self):
        Profiler.excludedLibs = self.setExcludedLibs(mastermind = False)
        Profiler.excluded = Profiler.excluded + Profiler.excludedSTD + Profiler.excludedLibs
        self.filter = pycallgraph.GlobbingFilter(include = Profiler.included, exclude = Profiler.excluded)
        
    def start(self):
        pycallgraph.start_trace(filter_func = self.filter)
    
    def stop(self):
        pycallgraph.stop_trace()
    
    def makeGraph(self, name = "graph.png"):
        pycallgraph.make_dot_graph(name)
    
    def setExcludedLibs(self, glyph = True, mastermind = True, pgu = True, pygame = True, pymunk = True):
        excludeList = []
        if glyph:
            excludeList.append('glyph.*')
        if mastermind:
            excludeList.append('_mm_server.*')
            excludeList.append('_mm_client.*')
            excludeList.append('socket.*')
        if pgu:
            excludeList.append('pgu.*')
        if pygame:
            excludeList.append('pygame.*')
        if pymunk:
            excludeList.append('pymunk.*')
            excludeList.append('_weakrefset.*')
            excludeList.append('ctypes.*')
        
        return excludeList