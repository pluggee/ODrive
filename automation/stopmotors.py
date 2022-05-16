""" Boot and configure odrive """

import odrive
from odrive.enums import *
import time

# init odrv0
odrv0 = odrive.find_any()
odrv0.clear_errors()


print('---------------------------------------------------------------')
print('| stopping all motors')

# # place both motors in flipping torque mode
odrv0.flipping_torque = 0
odrv0.start_torque_flip = True

odrv0.axis0.controller.flip_torque = False
odrv0.axis1.controller.flip_torque = False
