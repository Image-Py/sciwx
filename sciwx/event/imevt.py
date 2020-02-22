from .event import SciEvent
from ..widgets import ParaDialog

class ImgEvent(SciEvent):
    title = 'Image Event'
    note, para, view = [], None, None

    def __init__(self, app):
        self.app = app
        self.ips = app.get_img()

    def show(self):
        dialog = ParaDialog(self.app.get_img_win(), self.title)
        dialog.init_view(self.view, self.para, 'preview' in self.note, modal=True)
        ips, img, snap = self.ips, self.ips.img, self.ips.snap
        f = lambda p: self.run(ips, img, snap, p) or self.ips.update()
        dialog.Bind('cancel', lambda x=self.ips:self.cancel(x))
        dialog.Bind('parameter', f)
        status = dialog.ShowModal()==5100
        dialog.Destroy()
        return status

    def cancel(self, ips):
        ips.img[:] = ips.snap
        ips.update()

    def run(self, ips, img, snap, para):
        print('I am running!!!')

    def start(self, para=None, callback=None):
        print('Image Event Started!')
        if 'auto_snap' in self.note: self.ips.snapshot()
        if para!=None:
            self.run(self.ips, self.ips.img, self.ips.snap, para)
        elif self.view==None and self.__class__.show is ImgEvent.show:
            self.run(self.ips, self.ips.img, self.ips.snap, para)
        elif self.show():
            self.run(self.ips, self.ips.img, self.ips.snap, self.para)
        elif 'auto_snap' in self.note: self.cancel(self.ips)
        self.ips.update()
