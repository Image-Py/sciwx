import numpy as np

default_lut = np.arange(256*3, dtype=np.uint8).reshape((3,-1)).T
        
class Image:
    def __init__(self, img=None):
        self.name = 'Image'
        self.imgs = [img]
        self.cn = 0
        self.rg = (0,255)
        self.lut = default_lut
        self.log = False
        self.mode = 'set'
        self.cur = 0
        self.dirty = False
        self.snap = None

    @property
    def title(self): return self.name
    
    @property
    def img(self): return self.imgs[self.cur]

    @img.setter
    def img(self, value): self.imgs[self.cur] = value

    @property
    def channels(self):
        if self.imgs[self.cur].ndim==2: return 1
        else: return self.imgs[0].shape[2]

    @property
    def slices(self): return len(self.imgs)

    @property
    def nbytes(self):
        return sum([i.nbytes for i in self.imgs])

    @property
    def dtype(self): return self.img.dtype

    @property
    def shape(self): return self.img.shape[:2]

    @property
    def info(self):
        return '%sx%s  S:%s/%s  C:%s/%s'%(*self.shape,
            self.cur+1, self.slices, self.cn, self.channels)

    def update(self): self.dirty = True

    def snapshot(self):
        if self.snap is None:
            self.snap = self.img.copy()
        else: self.snap[:] = self.img

    def swap(self):
        if self.snap is None:return
        buf = self.img.copy()
        self.img[:], self.snap[:] = self.snap, buf
        print('swap')

if __name__ == '__main__':
    img = Image(np.zeros((5,5)))
