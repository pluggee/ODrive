""" Boot and configure odrive """

import odrive
from odrive.enums import *
import time

# init odrv0
odrv0 = odrive.find_any()

print('Setting zero positions')
odrv0.zero_flip_position = True
