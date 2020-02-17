import wx
from .canvas import CanvasFrame
from .grid import GridFrame
from .text import MDFrame, TextFrame

app = None

def new_app():
    global app
    if app is None: app = wx.App()

def imshow(img, cn=0, autofit=True):
    new_app()
    cf = CanvasFrame(None, autofit)
    cf.set_img(img)
    cf.set_cn(cn)
    cf.Show()
    return cf

def imstackshow(imgs, cn=0, autofit=True):
    new_app()
    cf = CanvasFrame(None, autofit)
    cf.set_imgs(imgs)
    cf.set_cn(cn)
    cf.Show()
    return cf

def tabshow(tab):
    new_app()
    gf = GridFrame(None)
    gf.set_data(tab)
    gf.Show()
    return gf

def txtshow(txt):
    new_app()
    tf = TextFrame(None)
    tf.append(txt)
    tf.Show()
    return tf
def mdshow(txt):
    new_app()
    new_app()
    mf = MDFrame(None)
    mf.set_cont(txt)
    mf.Show()
    return mf

def show(): app.MainLoop()
