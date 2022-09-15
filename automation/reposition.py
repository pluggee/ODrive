""" Boot and configure odrive """

import odrive
from odrive.enums import *
import time

# init odrv0
odrv0 = odrive.find_any()

cpr = 2400      # constant


# set motion mode to trajectory control
odrv0.axis0.trap_traj.config.vel_limit = 2
odrv0.axis1.trap_traj.config.vel_limit = 2
odrv0.axis0.trap_traj.config.accel_limit = 1
odrv0.axis1.trap_traj.config.accel_limit = 1
odrv0.axis0.trap_traj.config.decel_limit = 1
odrv0.axis1.trap_traj.config.decel_limit = 1
odrv0.axis0.motor.config.current_lim = 10
odrv0.axis1.motor.config.current_lim = 10
odrv0.axis0.controller.config.vel_limit = 8
odrv0.axis1.controller.config.vel_limit = 8
odrv0.axis0.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ
odrv0.axis1.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ

# load flip hysteresis values
odrv0.axis0.controller.flip_hys = 10
odrv0.axis1.controller.flip_hys = 10


# reposition each motor at flipping threshold
print('Moving motors to threshold positions')
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
time.sleep(0.1)
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
odrv0.axis1.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
print('Sleeping until motors settle ...')
time.sleep(3)

ax0_position = odrv0.axis0.encoder.shadow_count
ax1_position = odrv0.axis1.encoder.shadow_count
ax0_zero = odrv0.axis0.controller.flip_position
ax1_zero = odrv0.axis1.controller.flip_position

ax0_inpos = odrv0.axis0.controller.input_pos
ax1_inpos = odrv0.axis1.controller.input_pos

print('---------------------------------------------')
print('AXIS 0 current position = ' + str(ax0_position))
print('AXIS 0 zero  position   = ' + str(ax0_zero))
print('AXIS 0 delta            = ' + str(ax0_position - ax0_zero))
print('AXIS 0 input_pos        = ' + str(ax0_inpos))
print('---------------------------------------------')
print('AXIS 1 current position = ' + str(ax1_position))
print('AXIS 1 zero  position   = ' + str(ax1_zero))
print('AXIS 1 delta            = ' + str(ax1_position - ax1_zero))
print('AXIS 1 input_pos        = ' + str(ax1_inpos))
print('---------------------------------------------')
print('Positioning to ZERO')
time.sleep(2)

odrv0.axis0.controller.input_pos = ax0_inpos - (ax0_position - ax0_zero)/cpr
odrv0.axis1.controller.input_pos = ax1_inpos - (ax1_position - ax1_zero)/cpr

# wait until position settles

delta0 = odrv0.axis0.encoder.shadow_count - ax0_zero
delta1 = odrv0.axis1.encoder.shadow_count - ax1_zero
while (abs(delta0) > 10) or (abs(delta1) > 10):
    print('delta 0 = ' + str(delta0) + " | delta 1 = " + str(delta1))
    time.sleep(0.5)
    delta0 = odrv0.axis0.encoder.shadow_count - ax0_zero
    delta1 = odrv0.axis1.encoder.shadow_count - ax1_zero

time.sleep(1)
print('Done repositioning ...')

ax0_position = odrv0.axis0.encoder.shadow_count
ax1_position = odrv0.axis1.encoder.shadow_count
ax0_zero = odrv0.axis0.controller.flip_position
ax1_zero = odrv0.axis1.controller.flip_position

ax0_inpos = odrv0.axis0.controller.input_pos
ax1_inpos = odrv0.axis1.controller.input_pos

print('---------------------------------------------')
print(' After ZERO position')
print('---------------------------------------------')
print('AXIS 0 current position = ' + str(ax0_position))
print('AXIS 0 zero  position   = ' + str(ax0_zero))
print('AXIS 0 delta            = ' + str(ax0_position - ax0_zero))
print('AXIS 0 input_pos        = ' + str(ax0_inpos))
print('---------------------------------------------')
print('AXIS 1 current position = ' + str(ax1_position))
print('AXIS 1 zero  position   = ' + str(ax1_zero))
print('AXIS 1 delta            = ' + str(ax1_position - ax1_zero))
print('AXIS 1 input_pos        = ' + str(ax1_inpos))
print('---------------------------------------------')

# print('Giving a headstart ...')
# odrv0.axis0.controller.input_pos += 0.1
# odrv0.axis1.controller.input_pos += 0.1
# time.sleep(2)

print('Starting motion ...')
# place both motors in flipping torque mode
# set motor control mode
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
odrv0.axis1.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
# set input mode
odrv0.axis0.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
odrv0.axis1.controller.config.input_mode = INPUT_MODE_PASSTHROUGH

odrv0.axis0.motor.config.current_lim = 10
odrv0.axis1.motor.config.current_lim = 10
odrv0.axis0.controller.config.vel_limit = 20
odrv0.axis1.controller.config.vel_limit = 20
#odrv0.flipping_torque = 0.1
odrv0.flipping_torque = 0.05
odrv0.start_torque_flip = True
