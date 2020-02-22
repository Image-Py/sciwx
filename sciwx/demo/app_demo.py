import wx, sys
sys.path.append('../../')
from sciwx.app import SciApp
from sciwx.canvas import CanvasFrame
from sciwx.event import ImgEvent, Tool, DefaultTool

from sciwx.plugins.filters import Gaussian, Undo
from sciwx.plugins.pencil import Pencil
from sciwx.plugins.io import Open, Save

if __name__ == '__main__':
    from skimage.data import camera
    
    app = wx.App(False)
    frame = SciApp(None)
    frame.Show()
    frame.load_menu(('menu',[('File',[('Open', Open),
                                      ('Save', Save)]),
                             ('Filters', [('Gaussian', Gaussian),
                                          ('Undo', Undo)])]))
    frame.load_tool(('tools',[('standard', [('P', Pencil),
                                            ('D', DefaultTool)]),
                              ('draw', [('X', Pencil),
                                        ('X', Pencil)])]), 'draw')
    frame.show_img(camera())
    frame.show_img(camera())
    app.MainLoop()
