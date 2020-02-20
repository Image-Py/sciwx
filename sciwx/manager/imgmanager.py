class WImageManager:
    wins = []

    @classmethod
    def add(cls, win):
        if win in cls.wins: cls.remove(win)
        cls.wins.insert(0, win)

    @classmethod
    def get(cls, name=None):
        if len(cls.wins)==0:return None
        if name==None:return cls.wins[0]
        names = [i.image.name for i in cls.wins]
        if not name in names:return None
        return cls.wins[names.index(name)]

    @classmethod
    def remove(cls, win):
        for i in cls.wins:
            if i == win: cls.wins.remove(i)

class ImageManager:
    imgs = []

    @classmethod
    def add(cls, ips):

        cls.remove(ips)
        ips.name = cls.name(ips.name)
        print('image add!')
        cls.imgs.insert(0, ips)
        
    @classmethod
    def remove(cls, ips):
        if ips in cls.imgs: cls.imgs.remove(ips)
        print('image removed!')
            
    @classmethod
    def get(cls, name=None):
        if len(cls.imgs)==0:return None
        if name==None:return cls.imgs[0]
        names = [i.name for i in cls.imgs]
        if not name in names:return None
        return cls.imgs[names.index(name)]
          
    @classmethod
    def get_names(cls):
        return [i.name for i in cls.imgs]

    @classmethod
    def name(cls, name):
        if name==None: name='Undefined'
        names = [i.name for i in cls.imgs]
        if not name in names : return name
        for i in range(1, 100) : 
            n = "%s-%s"%(name, i)
            if not n in names: return n