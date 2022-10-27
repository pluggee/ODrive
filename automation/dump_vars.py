""" Boot and configure odrive """

import odrive
from odrive.enums import *
import time

# init odrv0
odrv0 = odrive.find_any()

tmp = odrv0.enable_traj_ctrl
print('enable_traj_ctrl           : ' + str(tmp))

tmp = odrv0.traj_ab
print('traj_ab                    : ' + str(tmp))

tmp = odrv0.traj_count_error
print('traj_count_error           : ' + str(tmp))

print('----------------------------------------------')
tmp = odrv0.count_error0
print('count_error0               : ' + str(tmp))

tmp = odrv0.count_a0
print('count_a0                   : ' + str(tmp))

tmp = odrv0.count_b0
print('count_b0                   : ' + str(tmp))

tmp = odrv0.axis0.encoder.shadow_count
print('axis0.encoder.shadow_count : ' + str(tmp))

print('----------------------------------------------')
tmp = odrv0.count_error1
print('count_error1               : ' + str(tmp))

tmp = odrv0.count_a1
print('count_a1                   : ' + str(tmp))

tmp = odrv0.count_b1
print('count_b1                   : ' + str(tmp))

tmp = odrv0.axis1.encoder.shadow_count
print('axis0.encoder.shadow_count : ' + str(tmp))
print('----------------------------------------------')

ip0 = odrv0.axis0.controller.input_pos
print('axis0.controller.input_pos : ' + str(ip0))

ip1 = odrv0.axis1.controller.input_pos
print('axis1.controller.input_pos : ' + str(ip1))

# print(' --- writing the same input_position data')
# odrv0.axis0.controller.input_pos = ip0
# odrv0.axis1.controller.input_pos = ip1
