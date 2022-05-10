""" Boot and configure odrive """

import odrive
from odrive.enums import *
import time

# init odrv0
odrv0 = odrive.find_any()
odrv0.clear_errors()


print('---------------------------------------------------------------')
print('| stopping all motors')

odrv0.axis0.requested_state = AXIS_STATE_IDLE
odrv0.axis1.requested_state = AXIS_STATE_IDLE

odrv0.axis0.controller.flip_torque = False
odrv0.axis1.controller.flip_torque = False

