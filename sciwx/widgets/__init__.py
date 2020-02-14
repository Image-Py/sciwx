import wx
from .widget import CanvasFrame

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

def show(): app.MainLoop()
