import wx, numpy as np
from .boxutil import cross, multiply, lay, mat
from .imutil import mix_img
from .mark import drawmark
from .image import Image
from ..event import Tool, DefaultTool
from time import time

class Canvas (wx.Panel):
    scales = [0.03125, 0.0625, 0.125, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 8, 10, 15, 20, 30, 50]
    
    def __init__(self, parent, autofit=False):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY,
            pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.TAB_TRAVERSAL )

        self.winbox = None
        self.conbox = None
        self.oribox = None
        
        self.outbak = None
        self.outimg = None
        self.outrgb = None
        self.outbmp = None
        self.outint = None
        self.buffer = None

        self.first = True

        self.image = Image()
        self.back = Image()
        self.marks = {}
        self.tool = None
        
        self.scaidx = 6
        self.autofit = autofit
        self.scrbox = wx.DisplaySize()
        self.bindEvents()

    def bindEvents(self):
        for event, handler in [ \
                (wx.EVT_SIZE, self.on_size),
                (wx.EVT_MOUSE_EVENTS, self.on_mouse),
                (wx.EVT_IDLE, self.on_idle),
                (wx.EVT_PAINT, self.on_paint)]:
            self.Bind(event, handler)

    def on_mouse(self, me):
        px, py = me.GetX(), me.GetY()
        x, y = self.to_data_coor(px, py)
        btn, img, tool = me.GetButton(), self.image, self.tool
        ld, rd, md = me.LeftIsDown(), me.RightIsDown(), me.MiddleIsDown()
        if me.Moving() and not (ld or md or rd): pass
        if tool==None: tool = Tool.default
        sta = [me.AltDown(), me.ControlDown(), me.ShiftDown()]
        others = {'alt':sta[0], 'ctrl':sta[1],
            'shift':sta[2], 'px':px, 'py':py, 'canvas':self}
        if me.ButtonDown():
            tool.mouse_down(img, x, y, btn, **others)
        if me.ButtonUp():
            tool.mouse_up(img, x, y, btn, **others)
        if me.Moving():
            tool.mouse_move(img, x, y, None, **others)
        btn = [ld, md, rd,True]
        btn  = (btn.index(True) +1) %4
        wheel = np.sign(me.GetWheelRotation())
        if me.Dragging():
            tool.mouse_move(img, x, y, btn, **others)
        if wheel!=0:
            tool.mouse_wheel(img, x, y, wheel, **others)
        if hasattr(self.tool, 'cursor'):
            self.SetCursor(wx.Cursor(tool.cursor))
        else : self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
            
    def initBuffer(self):
        box = self.GetClientSize()
        self.buffer = wx.Bitmap(*box)
        self.winbox = [0, 0, *box]

    def fit(self):
        oriw = self.oribox[2]-self.oribox[0]
        orih = self.oribox[3]-self.oribox[1]
        if not self.autofit: a,b,c,d = self.winbox
        else: 
            (a,b),(c,d) = (0,0), self.scrbox
            c, d = c*0.9, d*0.9
        for i in self.scales[6::-1]:
            if oriw*i<c-a and orih*i<d-b: break
        self.scaidx = self.scales.index(i)
        self.zoom(i, 0, 0)
        self.update()

    def update_box(self):
        shp = list(self.image.img.shape[1::-1])
        if self.oribox and self.oribox[2:] == shp: return
        self.conbox = [0, 0, *shp]
        self.oribox = [0, 0, *shp]

    def update(self, counter = [0,0]):
        self.update_box()
        if None in [self.winbox, self.conbox]: return
        if self.first:
            self.first = False
            return self.fit()
        counter[0] += 1
        start = time()
        lay(self.winbox, self.conbox)
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.SetBackground(wx.Brush((255,255,255)))
        dc.Clear()
        self.draw_image(dc, self.image.img, self.back.img, 0)
        for i in self.marks:
            if self.marks[i] is None: continue
            if callable(self.marks[i]):
                self.marks[i](dc, self.to_panel_coor, k = self.scale)
            else:
                drawmark(dc, self.to_panel_coor, self.marks[i], k=self.scale)
        dc.UnMask()
        counter[1] += time()-start
        if counter[0] == 10:
            #print('frame rate:',int(10/max(0.001,counter[1])))
            counter[0] = counter[1] = 0

    def set_img(self, img, b=False):
        isarr = isinstance(img, np.ndarray)
        if b and not isarr: self.back = img
        if not b and not isarr: self.image = img
        if b and isarr: self.back.img = img
        if not b and isarr: self.image.img = img
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
    def scale(self):
        conw = self.conbox[2]-self.conbox[0]
        oriw = self.oribox[2]-self.oribox[0]
        conh = self.conbox[3]-self.conbox[1]
        orih = self.oribox[3]-self.oribox[1]
        l1, l2 = conw**2+conh**2, oriw**2+orih**2
        return l1**0.5 / l2**0.5

    def move(self, dx, dy, coord='win'):
        if coord=='data':
            dx,dy = dx*self.scale, dy*self.scale
        arr = np.array(self.conbox)
        arr = arr.reshape((2,2))+(dx, dy)
        self.conbox = arr.ravel().tolist()
        self.update()

    def on_size(self, event):
        if max(self.GetClientSize())>20:
            self.initBuffer()
        if self.image.img is None: return
        self.update()

    def on_idle(self, event):
        if not self.image.dirty: return
        else:
            self.image.dirty = False
            return self.update()

    def on_paint(self, event):
        if self.buffer is None: return
        wx.BufferedPaintDC(self, self.buffer)

    def draw_image(self, dc, img, back, mode):
        out, bak, rgb = self.outimg, self.outbak, self.outrgb
        csbox = cross(self.winbox, self.conbox)
        shp = csbox[3]-csbox[1], csbox[2]-csbox[0]
        o, m = mat(self.oribox, self.conbox, csbox)
        shp = tuple(np.array(shp).round().astype(np.int))
        if out is None or (out.shape, out.dtype) != (shp, img.dtype):
            self.outimg = np.zeros(shp, dtype=img.dtype)
        if not back is None and (
            bak is None or (bak.shape, bak.dtype) != (shp, back.dtype)):
            self.outbak = np.zeros(shp, dtype=back.dtype)
        if rgb is None or rgb.shape[:2] != shp:
            self.outrgb = np.zeros(shp+(3,), dtype=np.uint8)
            self.outint = np.zeros(shp, dtype=np.uint8)
            buf = memoryview(self.outrgb)
            self.outbmp = wx.Bitmap.FromBuffer(*shp[::-1], buf)
        
        mix_img(back, m, o, shp, self.outbak, 
            self.outrgb, self.outint, self.back.rg, self.back.lut,
            self.back.log, cns=self.back.cn, mode='set')
        
        mix_img(img, m, o, shp, self.outimg,
            self.outrgb, self.outint, self.image.rg, self.image.lut,
            self.image.log, cns=self.image.cn, mode=self.image.mode)
        self.outbmp.CopyFromBuffer(memoryview(self.outrgb))
        dc.DrawBitmap(self.outbmp, *csbox[:2])
        
    def center(self, x, y, coord='win'):
        if coord=='data':
            x,y = self.to_panel_coor(x, y)
        dx = (self.winbox[2]-self.winbox[0])/2 - x
        dy = (self.winbox[3]-self.winbox[1])/2 - y
        for i,j in zip((0,1,2,3),(dx,dy,dx,dy)):
            self.conbox[i] += j
        lay(self.winbox, self.conbox)
        
    def zoom(self, k, x, y, coord='win'):
        if coord=='data':
            x,y = self.to_panel_coor(x, y)
        box = np.array(self.conbox).reshape((2,2))
        box = (box - (x,y)) / self.scale * k + (x, y)
        self.conbox = box.ravel().tolist()
        lay(self.winbox, self.conbox)
        if not self.autofit: return
        a,b,c,d = self.conbox
        if c-a<self.scrbox[0]*0.9 and d-b<self.scrbox[1]*0.9:
            self.SetInitialSize((c-a+4, d-b+4))
        self.GetParent().Fit()
        
    def zoomout(self, x, y, coord='win', grade=True):
        self.scaidx = min(self.scaidx + 1, len(self.scales)-1)
        self.zoom(self.scales[self.scaidx], x, y, coord)
        self.update()

    def zoomin(self, x, y, coord='win'):
        self.scaidx = max(self.scaidx - 1, 0)
        self.zoom(self.scales[self.scaidx], x, y, coord)
        self.update()

    def to_data_coor(self, x, y):
        x = (x - self.conbox[0])/self.scale
        y = (y - self.conbox[1])/self.scale
        return x, y

    def to_panel_coor(self, x, y):
        x = x * self.scale + self.conbox[0]
        y = y * self.scale + self.conbox[1]
        return x, y

    def __del__(self):
        # self.img = self.back = None
        print('========== canvas del')

if __name__=='__main__':
    from skimage.data import astronaut, camera
    import matplotlib.pyplot as plt

    app = wx.App()
    frame = wx.Frame(None, title='Canvas')
    canvas = Canvas(frame, autofit=False)
    canvas.set_img(camera())
    canvas.set_cn(0)
    frame.Show(True)
    app.MainLoop()
