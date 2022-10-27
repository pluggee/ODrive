""" Boot and configure odrive """

import odrive
from odrive.enums import *
import time

# init odrv0
odrv0 = odrive.find_any()

cpr = 2400      # constant

# setup for battery assisted operation, disable brake resistance
odrv0.config.brake_resistance = 0
odrv0.config.dc_max_positive_current = 100
odrv0.config.dc_max_negative_current = -100
odrv0.config.enable_brake_resistor = False

# set motion mode to trajectory control
odrv0.axis0.trap_traj.config.vel_limit = 2
odrv0.axis1.trap_traj.config.vel_limit = 2
odrv0.axis0.trap_traj.config.accel_limit = 10
odrv0.axis1.trap_traj.config.accel_limit = 10
odrv0.axis0.trap_traj.config.decel_limit = 10
odrv0.axis1.trap_traj.config.decel_limit = 10
odrv0.axis0.motor.config.current_lim = 100
odrv0.axis1.motor.config.current_lim = 100
odrv0.axis0.controller.config.vel_limit = 10
odrv0.axis1.controller.config.vel_limit = 10
# odrv0.axis0.config.motor.current_soft_max = 100
# odrv0.axis1.config.motor.current_soft_max = 100
odrv0.axis0.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ
odrv0.axis1.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ

odrv0.traj_count_error = 10

# reposition each motor at flipping threshold
print('Moving motors to threshold positions')
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
time.sleep(0.1)
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
odrv0.axis1.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
print('Sleeping until motors settle ...')
time.sleep(3)

turn_angle = 0.2
cpr0 = odrv0.axis0.encoder.config.cpr
cpr1 = odrv0.axis1.encoder.config.cpr


z0_count = odrv0.axis0.encoder.shadow_count
z1_count = odrv0.axis1.encoder.shadow_count
z0_pos = z0_count/cpr0
z1_pos = z1_count/cpr1

a0_count = z0_count + turn_angle * cpr0
a1_count = z1_count + turn_angle * cpr1
a0_pos = a0_count / cpr0
a1_pos = a1_count / cpr1

b0_count = z0_count - turn_angle * cpr0
b1_count = z1_count - turn_angle * cpr1
b0_pos = b0_count / cpr0
b1_pos = b1_count / cpr1

# load a/b count positions
odrv0.count_a0 = a0_count
odrv0.count_a1 = a1_count
odrv0.count_b0 = b0_count
odrv0.count_b1 = b1_count

print('---------------------------------------------')
print('z0_count    = ' + str(z0_count))
print('a0_count    = ' + str(a0_count))
print('b0_count    = ' + str(b0_count))
print('a0_pos      = ' + str(a0_pos))
print('b0_pos      = ' + str(b0_pos))
print('---------------------------------------------')
print('z1_count    = ' + str(z0_count))
print('a1_count    = ' + str(a0_count))
print('b1_count    = ' + str(b0_count))
print('a1_pos      = ' + str(a0_pos))
print('b1_pos      = ' + str(b0_pos))
print('---------------------------------------------')
print('Positioning to start points')

odrv0.axis0.controller.input_pos = a0_pos
odrv0.axis1.controller.input_pos = a1_pos
print('Sleeping before beginning motion')
time.sleep(3)
a0_count_meas = odrv0.axis0.encoder.shadow_count
a1_count_meas = odrv0.axis1.encoder.shadow_count

odrv0.axis0.controller.input_pos = b0_pos
odrv0.axis1.controller.input_pos = b1_pos
print('Sleeping before beginning motion')
time.sleep(3)
b0_count_meas = odrv0.axis0.encoder.shadow_count
b1_count_meas = odrv0.axis1.encoder.shadow_count

print()
print(' -- Measurement report')
print('a0 count delta = ' + str(a0_count - a0_count_meas))
print('a1 count delta = ' + str(a1_count - a1_count_meas))
print('b0 count delta = ' + str(b0_count - b0_count_meas))
print('b1 count delta = ' + str(b1_count - b1_count_meas))

odrv0.axis0.controller.input_pos = a0_pos
odrv0.axis1.controller.input_pos = a1_pos
print('Sleeping before starting automatic motion')
time.sleep(3)

odrv0.enable_traj_ctrl = True

odrv0.axis0.controller.input_pos = b0_pos
odrv0.axis1.controller.input_pos = b1_pos


# wait until position settles

# delta0 = odrv0.axis0.encoder.shadow_count - ax0_zero
# delta1 = odrv0.axis1.encoder.shadow_count - ax1_zero
# while (abs(delta0) > 10) or (abs(delta1) > 10):
#     print('delta 0 = ' + str(delta0) + " | delta 1 = " + str(delta1))
#     time.sleep(0.5)
#     delta0 = odrv0.axis0.encoder.shadow_count - ax0_zero
#     delta1 = odrv0.axis1.encoder.shadow_count - ax1_zero

# time.sleep(1)
# print('Done repositioning ...')

# ax0_position = odrv0.axis0.encoder.shadow_count
# ax1_position = odrv0.axis1.encoder.shadow_count
# ax0_zero = odrv0.axis0.controller.flip_position
# ax1_zero = odrv0.axis1.controller.flip_position

# ax0_inpos = odrv0.axis0.controller.input_pos
# ax1_inpos = odrv0.axis1.controller.input_pos

# print('---------------------------------------------')
# print(' After ZERO position')
# print('---------------------------------------------')
# print('AXIS 0 current position = ' + str(ax0_position))
# print('AXIS 0 zero  position   = ' + str(ax0_zero))
# print('AXIS 0 delta            = ' + str(ax0_position - ax0_zero))
# print('AXIS 0 input_pos        = ' + str(ax0_inpos))
# print('---------------------------------------------')
# print('AXIS 1 current position = ' + str(ax1_position))
# print('AXIS 1 zero  position   = ' + str(ax1_zero))
# print('AXIS 1 delta            = ' + str(ax1_position - ax1_zero))
# print('AXIS 1 input_pos        = ' + str(ax1_inpos))
# print('---------------------------------------------')

# # print('Giving a headstart ...')
# # odrv0.axis0.controller.input_pos += 0.1
# # odrv0.axis1.controller.input_pos += 0.1
# # time.sleep(2)

# print('Starting motion ...')
# # place both motors in flipping torque mode
# # set motor control mode
# odrv0.axis0.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
# odrv0.axis1.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
# # set input mode
# odrv0.axis0.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
# odrv0.axis1.controller.config.input_mode = INPUT_MODE_PASSTHROUGH

# odrv0.axis0.motor.config.current_lim = 10
# odrv0.axis1.motor.config.current_lim = 10
# odrv0.axis0.controller.config.vel_limit = 20
# odrv0.axis1.controller.config.vel_limit = 20
# odrv0.flipping_torque = 0.15
# # odrv0.flipping_torque = 0.05
# odrv0.start_torque_flip = True
