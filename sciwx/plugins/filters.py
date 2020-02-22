from sciwx.event import ImgEvent
from scipy.ndimage import gaussian_filter

class Gaussian(ImgEvent):
    name = 'Gaussian'
    note = ['auto_snap', 'preview']
    para = {'sigma':2}
    view = [(float, 'sigma', (0, 30), 1, 'sigma', 'pix')]

    def run(self, ips, img, snap, para):
        gaussian_filter(snap, para['sigma'], output=img)

class Undo(ImgEvent):
    name = 'Undo'
    def run(self, ips, img, snap, para): ips.swap()