class Manager:
    def __init__(self):
        self.objs = []

    def add(self, obj, cname=True):
        if obj in self.objs: self.remove(obj)
        if cname: obj.name = self.name(obj.name)
        self.objs.insert(0, obj)

    def get(self, name=None):
        if len(self.objs)==0:return None
        if name==None:return self.objs[0]
        names = [i.name for i in self.objs]
        if not name in names:return None
        return self.objs[names.index(name)]

    def names(self):
        return [i.name for i in self.objs]
    
    def remove(self, obj):
        if obj in self.objs: self.objs.remove(obj)

    def name(self, name):
        if name==None: name='Undefined'
        names = [i.name for i in self.objs]
        if not name in names : return name
        for i in range(1, 100) : 
            n = "%s-%s"%(name, i)
            if not n in names: return n

    def list(self):
        return [str(i) for i in self.objs]


class App:
    def __init__(self):
        self.img_manager = Manager()
        self.wimg_manager = Manager()
        self.tab_manager = Manager()
        self.wtab_manager = Manager()

    def show_img(self, img): pass
    def show_table(self, img): pass
    def show_md(self, img, title=''): pass
    def show_txt(self, img, title=''): pass
    def plot(self): pass
    def plot3d(self): pass

    def add_img(self, img):
        print('add', img.name)
        self.img_manager.add(img)

    def remove_img(self, img):
        print('remove', img.name)
        self.img_manager.remove(img)

    def add_img_win(self, win):
        self.wimg_manager.add(win, False)

    def remove_img_win(self, win):
        self.wimg_manager.remove(win)
        
    def get_img(self, name=None):
        return self.img_manager.get(name)
    
    def get_img_name(self):
        return self.img_manager.names()
    
    def get_img_win(self, name=None):
        return self.wimg_manager.get(name)

    def get_tab(self, name=None):
        return self.tab_manager.get(name)
    
    def get_tab_name(self):
        return self.tab_manager.names()
    
    def get_tab_win(self, name=None):
        return self.wtab_manager.get(name)

    
