import wx
from numpy import ndarray
import wx.lib.agw.aui as aui
from .canvas import Canvas
from sciapp.object.image import Image
from sciapp.action import Tool, ImageTool, ShapeTool

class ICanvas(Canvas):
    def __init__(self, parent, autofit=False):
        Canvas.__init__(self, parent, autofit)
        self.images.append(Image())
        self.images[0].back = Image()

    def get_obj_tol(self):
        return self.image, ImageTool.default
        
    def set_img(self, img, b=False):
        isarr = isinstance(img, ndarray)
        if b and not isarr: self.images[0].back = img
        if not b and not isarr: self.images[0] = img
        if b and isarr: self.images[0].back.img = img
        if not b and isarr: self.images[0].img = img
        self.update()

    def set_log(self, log, b=False):
        if b: self.back.log = log
        else: self.image.log = log
        
    def set_rg(self, rg, b=False):
        if b: self.back.rg = rg
        else: self.image.rg = rg
    
    def set_lut(self, lut, b=False):
        if b: self.back.lut = lut
        else: self.image.lut = lut

    def set_cn(self, cn, b=False):
        if b: self.back.cn = cn
        else: self.image.cn = cn

    def set_mode(self, mode):
        self.image.mode = mode

    def set_tool(self, tool):
        self.tool = tool

    @property
    def image(self): return self.images[0]

    @property
    def back(self): return self.images[0].back

class VCanvas(Canvas):
    def __init__(self, parent, autofit=False, ingrade=True, up=True):
        Canvas.__init__(self, parent, autofit, ingrade, up)

    def get_obj_tol(self):
        return self.shape, ShapeTool.default

    def set_shp(self, shp):
        self.marks['shape'] = shp
        self.update()

    def set_tool(self, tool): self.tool = tool

    @property
    def shape(self): 
        if not 'shape' in self.marks: return None
        return self.marks['shape']

class SCanvas(wx.Panel):
    def __init__(self, parent, autofit=False):
        wx.Panel.__init__(self, parent)
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

        sizer = wx.BoxSizer( wx.VERTICAL )
        self.lab_info = wx.StaticText( self, wx.ID_ANY,
            'information', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lab_info.Wrap( -1 )
        # self.lab_info.Hide()
        sizer.Add( self.lab_info, 0, wx.ALL, 0 )
        
        self.canvas = VCanvas(self, autofit = autofit)
        sizer.Add( self.canvas, 1, wx.EXPAND |wx.ALL, 0 )
        self.SetSizer(sizer)
        self.set_shp = self.canvas.set_shp

        self.Bind(wx.EVT_IDLE, self.on_idle)

    def on_idle(self, event):
        if self.shape is None: return
        if self.shape.dirty: self.update()
        self.shape.dirty = False

    def update(self):
        if self.shape is None: return
        self.canvas.update()
        if self.lab_info.GetLabel()!=self.shape.info:
            self.lab_info.SetLabel(self.shape.info)

    def Fit(self):
        wx.Panel.Fit(self)
        self.GetParent().Fit()

    @property
    def shape(self): return self.canvas.shape

    @property
    def name(self): return self.canvas.shape.name


class MCanvas(wx.Panel):
    def __init__(self, parent=None, autofit=False):
        wx.Panel.__init__ ( self, parent)
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

        sizer = wx.BoxSizer( wx.VERTICAL )
        self.lab_info = wx.StaticText( self, wx.ID_ANY,
            'information', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lab_info.Wrap( -1 )
        # self.lab_info.Hide()
        sizer.Add( self.lab_info, 0, wx.EXPAND, 0 )
        
        self.canvas = ICanvas(self, autofit = autofit)
        sizer.Add( self.canvas, 1, wx.EXPAND |wx.ALL, 0 )

        self.sli_chan = wx.Slider( self, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, 
            wx.SL_HORIZONTAL| wx.SL_SELRANGE| wx.SL_TOP)
        sizer.Add( self.sli_chan, 0, wx.ALL|wx.EXPAND, 0 )
        self.sli_chan.SetMaxSize( wx.Size( -1,18 ) )
        self.sli_chan.Hide()

        self.sli_page = wx.ScrollBar( self, wx.ID_ANY,
                                  wx.DefaultPosition, wx.DefaultSize, wx.SB_HORIZONTAL)
        self.sli_page.SetScrollbar(0,0,0,0, refresh=True)
        sizer.Add( self.sli_page, 0, wx.ALL|wx.EXPAND, 0 )
        self.sli_page.Hide()

        self.SetSizer(sizer)
        self.Layout()
        self.sli_page.Bind(wx.EVT_SCROLL, self.on_scroll)
        self.sli_chan.Bind(wx.EVT_SCROLL, self.on_scroll)
        self.Bind(wx.EVT_IDLE, self.on_idle)
        
        #self.Fit()
        self.set_rg = self.canvas.set_rg
        self.set_lut = self.canvas.set_rg
        self.set_log = self.canvas.set_log
        self.set_mode = self.canvas.set_mode
        self.set_tool = self.canvas.set_tool

        self.chans, self.pages, self.cn = -1, -1, -1

    def set_img(self, img, b=False):
        self.canvas.set_img(img, b)
        self.update()

    def set_cn(self, cn, b=False):
        self.canvas.set_cn(cn, b)
        self.update()
        
    @property
    def image(self): return self.canvas.image

    @property
    def name(self): return self.canvas.image.name

    def set_imgs(self, imgs, b=False):
        if b: self.canvas.back.imgs = imgs
        else: self.canvas.image.imgs = imgs
        self.canvas.update_box()
        self.update()

    def Fit(self):
        wx.Panel.Fit(self)
        self.GetParent().Fit()
        
    def slider(self):
        slices = self.image.slices
        channels = self.image.channels
        if slices != self.pages:
            print('set slices')
            if slices==1 and self.sli_page.Shown:
                self.sli_page.Hide()
            if slices>1 and not self.sli_page.Shown:
                self.sli_page.Show()
            self.sli_page.SetScrollbar(0, 0, slices-1, 0)
            self.pages = slices
        if channels != self.chans or self.cn != self.image.cn:
            print('set channels')
            if not isinstance(self.image.cn, int) and self.sli_chan.Shown:
                self.sli_chan.Hide()
            if isinstance(self.image.cn, int) and channels>1:
                if not self.sli_chan.Shown: self.sli_chan.Show()
            self.sli_chan.SetMax(channels-1)
            self.chans,self.cn = channels, self.canvas.image.cn
        
    def on_idle(self, event):
        if self.image.dirty: self.update()
        self.image.dirty = False

    def update(self):
        if self.image.img is None: return
        self.slider()
        self.canvas.update()
        if self.lab_info.GetLabel()!=self.image.info:
            self.lab_info.SetLabel(self.image.info)
        self.Layout()

    def on_scroll(self, event):
        self.image.cur = self.sli_page.GetThumbPosition()
        if isinstance(self.image.cn, int):
            self.image.cn = self.sli_chan.GetValue()
        self.update()
    
    def __del__(self):
        print('canvas panel del')

if __name__=='__main__':
    from skimage.data import camera, astronaut
    from skimage.io import imread
    
    app = wx.App()
    frame = wx.Frame(None, title='MCanvas')
    mc = MCanvas(frame, autofit=False)
    mc.set_img(astronaut())
    mc.set_cn(0)
    frame.Show()
    app.MainLoop()
