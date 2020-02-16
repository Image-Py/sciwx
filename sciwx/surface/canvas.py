import sys, platform
import moderngl
import numpy as np
import wx, math
import wx.glcanvas as glcanvas
from .mesh import *
import os.path as osp
from pubsub import pub
from .geoutil import *

class Canvas3D(glcanvas.GLCanvas):
    def __init__(self, parent, meshset=None):
        attribList = (glcanvas.WX_GL_CORE_PROFILE, glcanvas.WX_GL_RGBA, glcanvas.WX_GL_DOUBLEBUFFER, glcanvas.WX_GL_DEPTH_SIZE, 24)
        glcanvas.GLCanvas.__init__(self, parent, -1, attribList=attribList[platform.system() == 'Windows':])
        self.init = False
        self.context = glcanvas.GLContext(self)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.meshset = self.meshset = MeshSet() if meshset is None else meshset
        self.size = None

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.lastx, self.lasty = None, None
        #self.update()
        #print('init===========')
        pub.subscribe(self.add_surf, 'add_surf')
        pub.subscribe(self.add_mark, 'add_mark')

    def InitGL(self):
        self.meshset.on_ctx(moderngl.create_context())
        self.DoSetViewport()
        self.meshset.reset()

    def OnDraw(self):
        self.meshset.set_viewport(0, 0, self.Size.width, self.Size.height)
        #self.meshset.count_mvp()
        self.meshset.draw()
        self.SwapBuffers()

    def OnSize(self, event): 
        self.meshset.set_pers()
        self.Refresh(False)

    def DoSetViewport(self):
        size = self.size = self.GetClientSize()
        self.SetCurrent(self.context)
        if not self.meshset is None and not self.meshset.ctx is None:
            self.meshset.set_viewport(0, 0, self.Size.width, self.Size.height)

    def OnPaint(self, event):
        self.SetCurrent(self.context)
        #print(self, '=====', self.init)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.lastx, self.lasty = evt.GetPosition()

    def OnMouseUp(self, evt):
        self.ReleaseMouse()

    def OnMouseMotion(self, evt):
        self.SetFocus()
        if evt.Dragging() and evt.LeftIsDown():
            x, y = evt.GetPosition()
            dx, dy = x-self.lastx, y-self.lasty
            self.lastx, self.lasty = x, y
            angx = self.meshset.angx - dx/200
            angy = self.meshset.angy + dy/200
            self.meshset.set_pers(angx=angx, angy=angy)
            self.Refresh(False)
        if evt.Dragging() and evt.RightIsDown():
            light = self.meshset.light
            x, y = evt.GetPosition()
            dx, dy = x-self.lastx, y-self.lasty
            self.lastx, self.lasty = x, y
            angx, angy = dx/200, dy/200
            vx, vy, vz = self.meshset.light
            ay = math.asin(vz/math.sqrt(vx**2+vy**2+vz**2))-angy
            xx = math.cos(angx)*vx - math.sin(angx)*vy
            yy = math.sin(angx)*vx + math.cos(angx)*vy
            ay = max(min(math.pi/2-1e-4, ay), -math.pi/2+1e-4)
            zz, k = math.sin(ay), math.cos(ay)/math.sqrt(vx**2+vy**2)
            self.meshset.set_light((xx*k, yy*k, zz))
            self.Refresh(False)

    def save_bitmap(self, path):
        context = wx.ClientDC( self )
        memory = wx.MemoryDC( )
        x, y = self.ClientSize
        bitmap = wx.Bitmap( x, y, -1 )
        memory.SelectObject( bitmap )
        memory.Blit( 0, 0, x, y, context, 0, 0)
        memory.SelectObject( wx.NullBitmap)
        bitmap.SaveFile( path, wx.BITMAP_TYPE_PNG )

    def save_stl(self, path):
        from stl import mesh
        objs = [i for i in self.meshset.objs.values() if i.visible]
        vers = [i.vts[i.ids] for i in objs if isinstance(i, Surface)]
        vers = np.vstack(vers)
        model = mesh.Mesh(np.zeros(vers.shape[0], dtype=mesh.Mesh.dtype))
        model.vectors = vers
        model.save(path)

    def OnMouseWheel(self, evt):
        k = 0.9 if evt.GetWheelRotation()>0 else 1/0.9
        self.meshset.set_pers(l=self.meshset.l*k)
        self.Refresh(False)
        #self.update()

    def set_mesh(self, meshset):
        self.meshset = meshset
        self.Refresh()

    def view_x(self, evt): 
        self.meshset.reset(angx=0)
        self.Refresh(False)


    def view_y(self, evt): 
        self.meshset.reset(angx=pi/2)
        self.Refresh(False)

    def view_z(self, evt): 
        self.meshset.reset(angy=pi/2-1e-4)
        self.Refresh(False)

    def set_pers(self, b):
        self.meshset.set_pers(pers=b)
        self.Refresh(False)

    def set_background(self, c):
        self.meshset.set_background(c)
        self.Refresh(False)

    def set_scatter(self, scatter):
        self.meshset.set_bright_scatter(scatter=scatter)
        self.Refresh(False)

    def set_bright(self, bright):
        self.meshset.set_bright_scatter(bright=bright)
        self.Refresh(False)

    def get_obj(self, name):
        return self.meshset.get_obj(name)

    def add_surf_asyn(self, name, vts, fs, ns, cs, mode=None, blend=None, color=None, visible=None):
        wx.CallAfter(pub.sendMessage, 'add_surf', name=name, vts=vts, fs=fs, ns=ns, cs=cs, obj=self,
            mode=mode, blend=blend, color=color, visible=visible)

    def add_surf(self, name, vts, fs, ns, cs, obj=None, mode=None, blend=None, color=None, visible=None):
        if obj!=None and not obj is self:return
        surf = self.meshset.add_surf(name, vts, fs, ns, cs)

        surf.set_style(mode=mode, blend=blend, color=color, visible=visible)
        if len(self.meshset.objs)==1:
            self.meshset.reset()
        self.Refresh(False)

    def add_mark_asyn(self, name, vts, fs, ps, h, cs):
        wx.CallAfter(pub.sendMessage, 'add_mark', name=name, vts=vts, fs=fs, ps=ps, h=h, cs=cs)

    def add_mark(self, name, vts, fs, ps, h, cs):
        surf = self.meshset.add_mark(name, vts, fs, ps, h, cs)
        if len(self.meshset.objs)==1:
            self.meshset.reset()
        self.Refresh(False)

if __name__ == '__main__':
    app = wx.App(False)
    frm = wx.Frame(None, title='GLCanvas Sample')
    canvas = Canvas3D(frm)

    frm.Show()
    app.MainLoop()
