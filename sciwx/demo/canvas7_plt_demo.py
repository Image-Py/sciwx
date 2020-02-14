import sys
sys.path.append('../../')

from skimage.data import astronaut, camera
from sciwx.canvas import util as plt

if __name__ == '__main__':
    plt.imshow(camera())
    plt.imstackshow([astronaut(), 255-astronaut()], cn=0)
    plt.show()
