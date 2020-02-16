import sys
sys.path.append('../../')

from skimage.data import astronaut, camera
from sciwx import plt

import numpy as np
import pandas as pd

if __name__ == '__main__':
    plt.imshow(camera())
    plt.imstackshow([astronaut(), 255-astronaut()], cn=0)
    plt.tabshow(pd.DataFrame(np.zeros((100,5))))
    plt.show()
