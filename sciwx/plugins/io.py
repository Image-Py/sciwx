from sciwx.event import SciEvent, ImgEvent
from skimage.io import imread, imsave

class Open(SciEvent):
	name = 'Open'
	def start(self, para=None):
		path = self.app.getpath('Open', ['png','bmp','jpg'], 'open')
		if path is None: return
		self.app.show_img(imread(path))

class Save(ImgEvent):
	name = 'Save'
	para = {'path':''}

	def show(self):
		path = self.app.getpath('Open', ['png','bmp','jpg'], 'save')
		if path is None: return
		self.para['path'] = path
		return True

	def run(self, ips, img, snap, para):
		imsave(para['path'], img)