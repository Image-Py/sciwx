from .action import SciAction

class Tool(SciAction):
    title = 'Base Tool'
    default = None
    def mouse_down(self, image, x, y, btn, **key): pass
    def mouse_up(self, image, x, y, btn, **key): pass
    def mouse_move(self, image, x, y, btn, **key): pass
    def mouse_wheel(self, image, x, y, d, **key): pass
    def start(self, app): 
        self.app = app
        Tool.default = self
        if not app is None: app.tool = self

class DefaultTool(Tool):
    title = 'Move And Scale'
    def __init__(self): 
        self.oldxy = None
        
    def mouse_down(self, image, x, y, btn, **key):
        if btn==1: self.oldxy = key['px'], key['py']
        if btn==3: key['canvas'].fit()
        
    def mouse_up(self, image, x, y, btn, **key):
        self.oldxy = None
    
    def mouse_move(self, image, x, y, btn, **key):
        if self.oldxy is None: return
        ox, oy = self.oldxy
        key['canvas'].move(key['px']-ox, key['py']-oy)
        self.oldxy = key['px'], key['py']
    
    def mouse_wheel(self, image, x, y, d, **key):
        if d>0: key['canvas'].zoomout(x, y, coord='data')
        if d<0: key['canvas'].zoomin(x, y, coord='data')

DefaultTool().start(None)