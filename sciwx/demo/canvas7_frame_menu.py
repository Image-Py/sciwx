import sys, wx
sys.path.append('../../')
from scipy.ndimage import gaussian_filter
from sciwx.canvas import CanvasFrame
from sciwx.action import ImgAction
from sciwx.app.manager import App
from sciwx.widgets import MenuBar

class TestFrame(CanvasFrame, App):
    def __init__ (self, parent):
        CanvasFrame.__init__(self, parent)
        App.__init__(self)

        self.Bind(wx.EVT_ACTIVATE, self.init_image)
        
    def init_image(self, event):
        self.add_img(self.canvas.image)

    def add_menubar(self):
        menubar = MenuBar(self)
        self.SetMenuBar(menubar)
        return menubar

class Gaussian(ImgAction):
    title = 'Gaussian'
    note = ['auto_snap', 'preview']
    para = {'sigma':2}
    view = [(float, 'sigma', (0, 30), 1, 'sigma', 'pix')]

    def run(self, ips, img, snap, para):
        gaussian_filter(snap, para['sigma'], output=img)

class Undo(ImgAction):
    title = 'Undo'
    def run(self, ips, img, snap, para):
        print(ips.img.mean(), ips.snap.mean())
        ips.swap()

if __name__=='__main__':
    from skimage.data import camera, astronaut
    from skimage.io import imread

    app = wx.App()
    cf = TestFrame(None)
    cf.set_img(camera())
    cf.set_cn(0)
    bar = cf.add_menubar()
    bar.load(('menu',[('Filter',[('Gaussian', Gaussian),
                                 ('Unto', Undo)]),
                      ]))
    cf.Show()
    app.MainLoop()
