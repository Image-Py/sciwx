from ..manager import ImageManager, WImageManager

triggers = {
    'on_img_new' : [lambda x: print('on_img_new', x)],
    'on_img_active' : [lambda x: print('on_img_active', x)],
    'on_img_remove' : [lambda x: print('on_img_remove', x)],

    'on_wimg_new' : [lambda x: print('on_wimg_new', x)],
    'on_wimg_active' : [lambda x: print('on_wimg_active', x)],
    'on_wimg_remove' : [lambda x: print('on_wimg_remove', x)],

    'on_tab_new' : [lambda x: print('on_tab_new', x)],
    'on_tab_active' : [lambda x: print('on_tab_active', x)],
    'on_tab_remove' : [lambda x: print('on_tab_remove', x)],
}

def subscribe(chan, func):
    if not func in triggers[chan]:
        triggers[chan].append(func)

def unsubscribe(chan, func):
    if func in triggers[chan]:
        triggers[chan].remove(func)

def publish(chan, *para):
    for i in triggers[chan]: i(*para)

def add_default_sub():
    for i in triggers.values(): del i[:]
    subscribe('on_img_new', ImageManager.add)
    subscribe('on_img_active', ImageManager.add)
    subscribe('on_img_remove', ImageManager.remove)
    subscribe('on_wimg_new', WImageManager.add)
    subscribe('on_wimg_active', WImageManager.add)
    subscribe('on_wimg_remove', WImageManager.remove)

add_default_sub()