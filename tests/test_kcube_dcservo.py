import os
import sys
import ctypes
import time

os.environ['PATH'] = "C:\\Program Files\\ThorLabs\\Kinesis" + ";" + os.environ['PATH']
sys.path.append(r"..\thorlabs-kinesis")
# sys.path.append(r"..\devices")

class Static_Vars:
    steps_per_mm = 34304

from thorlabs_kinesis.devices.kcube_dc import kcube_dc
from thorlabs_kinesis import kcube_dcservo as kcdc

if __name__ == "__main__":
    serial_no = "27256231"
    serial_no = "27000001"

    if kcdc.TLI_BuildDeviceList() == 0:
        print("Device list built (no errors).")
    else:
        raise ConnectionError("Device list could not be built.")

    size = kcdc.TLI_GetDeviceListSize()
    print(size, "device(s) found.")

    serialnos = ctypes.create_string_buffer(100)
    kcdc.TLI_GetDeviceListExt(serialnos, 100)
    serialnos = list(filter(None, serialnos.value.decode("utf-8").split(',')))
    print("Serial #'s:", serialnos)

    device = kcube_dc(serial_no)

    # device.print_device_info()
    # print(device.get_device_info())
    
    print("velocity: {:.4f} mm/s".format(1688183* kcube_dc.velocity_scaling_to_mm_per_sec))
    print("acceleration: {:.4f} mm/s^2".format(393 * kcube_dc.acc_scaling_to_mm_per_sec2))
    
    with device as dev:
        # print("\nIdentify...")
        # dev.identify(wait=0.5)
        # print("\nIdentified.")

        print("Start polling...")
        if dev.start_polling(100):
            print("Successfully started polling.")
        dev.clear_msg_queue()
        time.sleep(1)
        print("Current Position: {:7.4f} mm".format(dev.get_position(in_mm=True)))
        print("Current Position: {:7} encoder steps".format(dev.get_position()))
        print("Current Polling duration (ms): ", dev.get_polling_duration())
        
        if dev.can_home():
            dev.home()

        # else:
        #     print("Device can't be homed.")
        jog_acc, jog_max_vel = dev.get_jog_vel_params()
        print("jog acc: {},     jog max. velocity: {}".format(jog_acc.value, 
            jog_max_vel.value))
        move_acc, move_max_vel = dev.get_move_vel_params()
        print("move acc: {},     move max. velocity: {}".format(move_acc.value, 
            move_max_vel.value))
        print("velocity using encouters:", move_max_vel.value/dev.steps_per_mm)
        
        print("Stop polling")
        dev.stop_polling()

    # serialno = ctypes.c_char_p(bytes(serial_no, "utf-8"))
    # accel_param = ctypes.c_int()
    # vel_param = ctypes.c_int()
    # message_type = WORD()
    # message_id = WORD()
    # message_data = DWORD()
    # current_motor_pos = 0

    # move_pos=2000
    # motor_command = c_int(move_pos)

    # # Open Communication
    # kcdc.CC_Open(serialno)
    # kcdc.CC_StartPolling(serialno, c_int(20))
    # kcdc.CC_ClearMessageQueue(serialno)
    # time.sleep(3)
    # homeable = bool(kcdc.CC_CanHome(serialno))
    # print(homeable)
    # #Get Motor Position
    # kcdc.CC_GetJogVelParams(serialno, ctypes.byref(accel_param), ctypes.byref(vel_param))
    # print(accel_param.value)
    # current_motor_pos = kcdc.CC_GetPosition(serialno)
    # print(current_motor_pos)
    # # #kcdc.CC_Home(serialno)

    # # Start Move Test
    # kcdc.CC_ClearMessageQueue(serialno)
    # kcdc.CC_MoveToPosition(serialno, motor_command)
    # kcdc.CC_WaitForMessage(serialno, byref(message_type), byref(message_id), byref(message_data))

    # while (int(message_type.value) != 2) or (int(message_id.value) != 1):
    #     kcdc.CC_WaitForMessage(serialno, byref(message_type), byref(message_id), byref(message_data))
    #     kcdc.CC_RequestPosition(serialno)
    #     # I Get correct position feedback here
    #     print("TEST", kcdc.CC_GetPosition(serialno))

    # # But I dont get correct position feedback here. I just get 0.
    # kcdc.CC_RequestPosition(serialno)
    # time.sleep(0.1)
    # current_motor_pos = kcdc.CC_GetPosition(serialno)
    # print(current_motor_pos)
    # # Close Communication
    # kcdc.CC_StopPolling(serialno)
    # kcdc.CC_Close(serialno)