""" Boot and configure odrive """

import odrive
from odrive.enums import *
import time

# init odrv0
odrv0 = odrive.find_any()


def set_velocity(vset):
    odrv0.axis0.trap_traj.config.vel_limit = vset
    odrv0.axis1.trap_traj.config.vel_limit = vset
    odrv0.axis0.trap_traj.config.accel_limit = 5*vset
    odrv0.axis1.trap_traj.config.accel_limit = 5*vset
    odrv0.axis0.trap_traj.config.decel_limit = 5*vset
    odrv0.axis1.trap_traj.config.decel_limit = 5*vset
    odrv0.axis0.controller.config.vel_limit = 5*vset
    odrv0.axis1.controller.config.vel_limit = 5*vset


vstart = 4
vstop = 40
vstep = 4
sleep_duration = 5

for v in range(vstart, vstop, vstep):
    set_velocity(v)
    print('Setting angular velocity to ' + str(v))
    time.sleep(sleep_duration)

print('---------')
print('Setting velocity to starting point again = ' + str(vstart))
set_velocity(vstart)
