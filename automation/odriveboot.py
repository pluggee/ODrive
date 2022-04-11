""" Boot and configure odrive """

import odrive
from odrive.enums import *
import time

# init odrv0
odrv0 = odrive.find_any()

# First we load all config parameters

# motor current limit
odrv0.axis0.motor.config.current_lim = 10
odrv0.axis1.motor.config.current_lim = 10

# angular velocity limit, turns/s
odrv0.axis0.controller.config.vel_limit = 10000
odrv0.axis1.controller.config.vel_limit = 10000

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

# set motor control mode
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
odrv0.axis1.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL

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

odrv0.axis0.controller.input_torque = 1
odrv0.axis1.controller.input_torque = 1
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
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

time.sleep(1)

ax0state = odrv0.axis0.current_state
ax1state = odrv0.axis1.current_state

print('Axis 0 state: ' + str(ax0state))
print('Axis 1 state: ' + str(ax1state))
