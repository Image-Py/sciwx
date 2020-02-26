import sys, wx
sys.path.append('../../')
from scipy.ndimage import gaussian_filter
from skimage.draw import line
from sciwx.canvas import CanvasFrame
from sciwx.action import ImgAction, Tool, DefaultTool
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
    def run(self, ips, img, snap, para): ips.swap()

class Pencil(Tool):
    title = 'Pencil'
    def __init__(self):
        self.status = False
        self.oldp = (0,0)
        
    def mouse_down(self, ips, x, y, btn, **key):
        self.status = True
        self.oldp = (y, x)
        ips.snapshot()
    
    def mouse_up(self, ips, x, y, btn, **key):
        self.status = False
    
    def mouse_move(self, ips, x, y, btn, **key):
        if not self.status:return
        se = self.oldp + (y,x)
        rs,cs = line(*[int(i) for i in se])
        rs.clip(0, ips.shape[1], out=rs)
        cs.clip(0, ips.shape[0], out=cs)
        ips.img[rs,cs] = 255
        self.oldp = (y, x)
        key['canvas'].update()
        
    def mouse_wheel(self, ips, x, y, d, **key):pass
    
if __name__=='__main__':
    from skimage.data import camera, astronaut
    from skimage.io import imread

    app = wx.App()
    cf = TestFrame(None)
    cf.set_img(camera())
    cf.set_cn(0)
    bar = cf.add_menubar()
    bar.load(('menu',[('Filter',[('Gaussian', Gaussian),
                                 ('Unto', Undo)]),]))
    
    bar = cf.add_toolbar()
    bar.add_tool('M', DefaultTool)
    bar.add_tool('P', Pencil)
    cf.Show()
    app.MainLoop()
