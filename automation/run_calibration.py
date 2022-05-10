""" Boot and configure odrive """

import odrive
from odrive.enums import *
import time

# init odrv0
odrv0 = odrive.find_any()
odrv0.clear_errors()

# First we load all config parameters

# motor current limit
odrv0.axis0.motor.config.current_lim = 50
odrv0.axis1.motor.config.current_lim = 50

# angular velocity limit, turns/s
odrv0.axis0.controller.config.vel_limit = 10
odrv0.axis1.controller.config.vel_limit = 10

# motor pole pairs
odrv0.axis0.motor.config.pole_pairs = 7
odrv0.axis1.motor.config.pole_pairs = 7

# torque constant, 8.27/(motor KV)
odrv0.axis0.motor.config.torque_constant = 8.27/410
odrv0.axis1.motor.config.torque_constant = 8.27/410

# set motor type to high current
odrv0.axis0.motor.config.motor_type = 0
odrv0.axis1.motor.config.motor_type = 0

# encoder config
odrv0.axis0.encoder.config.cpr = 2400
odrv0.axis1.encoder.config.cpr = 2400

# reset motor inputs
odrv0.axis0.controller.input_vel = 0
odrv0.axis0.controller.input_torque = 0
odrv0.axis1.controller.input_vel = 0
odrv0.axis1.controller.input_torque = 0

# set motor control mode
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
odrv0.axis1.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL

# set input mode
odrv0.axis0.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
odrv0.axis1.controller.config.input_mode = INPUT_MODE_PASSTHROUGH

# give controller some time
time.sleep(0.5)

# Read parameters
vbus = odrv0.vbus_voltage
ibus = odrv0.ibus
serialnum = odrv0.serial_number
hw_version = str(odrv0.hw_version_major) + '.' + str(odrv0.hw_version_minor)\
        + '.' + str(odrv0.hw_version_variant)

fw_version = str(odrv0.fw_version_major) + '.' + str(odrv0.fw_version_minor)\
        + '.' + str(odrv0.fw_version_revision)

if (odrv0.fw_version_unreleased != 0):
    fw_release_stat = 'Unreleased'
else:
    fw_release_stat = 'Released'

is_brake_res_armed = odrv0.brake_resistor_armed
is_brake_res_saturated = odrv0.brake_resistor_saturated
brake_res_current = odrv0.brake_resistor_current

time.sleep(0.1)
ax0t = odrv0.axis0.controller.torque_setpoint
ax1t = odrv0.axis1.controller.torque_setpoint

print('---------------------------------------------------------------')
print('| Odrive parameters:')
print('|')
print('| BUS VOLT                 : ' + str(vbus))
print('| BUS CURRENT              : ' + str(ibus))
print('| Serial #                 : ' + str(serialnum))
print('| HW Version               : ' + hw_version)
print('| FW Version               : ' + fw_version)
print('| FW Status                : ' + fw_release_stat)
print('| Brake Resistor Armed     : ' + str(is_brake_res_armed))
print('| Brake Resistor Saturated : ' + str(is_brake_res_saturated))
print('| Brake Resistor Current   : ' + str(brake_res_current))
print('| Axis 0 torque            : ' + str(ax0t))
print('| Axis 1 torque            : ' + str(ax1t))

odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while (odrv0.axis0.current_state != AXIS_STATE_IDLE) or (odrv0.axis1.current_state != AXIS_STATE_IDLE):
    time.sleep(0.1)

print('Calibration complete')

odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
time.sleep(0.1)
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
time.sleep(1)
ax0state = odrv0.axis0.current_state
ax1state = odrv0.axis1.current_state

print('Axis 0 state: ' + str(ax0state))
print('Axis 1 state: ' + str(ax1state))

# load flip hysteresis values
odrv0.axis0.controller.flip_hys = 10
odrv0.axis1.controller.flip_hys = 10

ax0_position = odrv0.axis0.encoder.shadow_count
ax1_position = odrv0.axis1.encoder.shadow_count
print('AXIS 0 position = ' + str(ax0_position))
print('AXIS 1 position = ' + str(ax1_position))

# reposition each motor at flipping threshold
# print('Moving motors to threshold positions')
# odrv0.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
# odrv0.axis1.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL

# place both motors in flipping torque mode
# odrv0.flipping_torque = 0.05 
# odrv0.start_torque_flip = True

