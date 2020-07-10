import os
os.environ['PATH'] = "C:\\Program Files\\ThorLabs\\Kinesis" + ";" + os.environ['PATH']
#print(os.environ['PATH'])
from threading import Thread
import thorlabs_kinesis as tk
import time
import keyboard
from ctypes import (
    c_short,
    c_char_p,
    c_void_p,
    byref,
    c_int,
    create_string_buffer,
)
from ctypes.wintypes import (
    DWORD,
    WORD,
)
class Static_Vars:
    steps_per_mm = 34304

from thorlabs_kinesis import benchtop_piezo as bp

if bp.TLI_BuildDeviceList() == 0:
    print("Device list built (no errors).")

    size = bp.TLI_GetDeviceListSize()
    print(size, "device(s) found.")

    serialnos = create_string_buffer(100)
    bp.TLI_GetDeviceListByTypeExt(serialnos, 100, 27)
    serialnos = list(filter(None, serialnos.value.decode("utf-8").split(',')))
    print("Serial #'s:", serialnos)

    serialno = c_char_p(bytes("27504851", "utf-8"))
    accel_param = c_int()
    vel_param = c_int()
    message_type = WORD()
    message_id = WORD()
    message_data = DWORD()
    current_motor_pos = 0

    move_pos=2000
    motor_command = c_int(move_pos)

    # Open Communication
    bp.PBC_Open(serialno)
    bp.PBC_StartPolling(serialno)
    bp.PBC_ClearMessageQueue(serialno)
    time.sleep(3)
    # kcdc.CC_Open(serialno)
    # kcdc.CC_StartPolling(serialno, c_int(20))
    # kcdc.CC_ClearMessageQueue(serialno)
    # time.sleep(3)
    # homeable = bool(bp.CC_CanHome(serialno))
    # print(homeable)

    channel1 = int(1)
    channel2 = int(2)
    channel3 = int(3)

    #Identify Channels
    bp.PBC_EnableChannel(serialno, channel1)
    bp.PBC_Identify(serialno,channel1)
    bp.PBC_EnableChannel(serialno, channel2)
    bp.PBC_Identify(serialno,channel2)
    bp.PBC_EnableChannel(serialno, channel3)
    bp.PBC_Identify(serialno,channel3)

    #Identify Control Mode
    print("control type for channel3: ", bp.PBC_GetPositionControlMode(serialno,channel1))
    print("control type for channel2: ", bp.PBC_GetPositionControlMode(serialno,channel2))
    print("control type for channel3: ", bp.PBC_GetPositionControlMode(serialno,channel3))

    bp.PBC_SetPositionControlMode(serialno,channel1,bp.CTR_ClosedLoop)
    bp.PBC_GetPosition(serialno,channel1)

    maxTravel = 32767 # travel is from 0 to 32767 for 20 um
    ten_nm_travel = c_short(16) # just under 10 nm of travel

    currentPos = c_short
    Done = False
    while not Done:
        try: 
            if keyboard.is_pressed('q'):
                print('Pull Complete')
                Done = True
        except: 
            continue
        currentPos = bp.PBC_GetPosition(serialno,channel1)
        bp.PBC_SetPosition(serialno,channel1,currentPos+ten_nm_travel)
        print("current position between 0 and 32767 (short): ",currentPos)
        time.sleep(0.1)
    
    bp.PBC_StopPolling(serialno)
    if bp.PBC_Disconnect(serialno) == 0:
            print("device disconnected")
    bp.PBC_Close(serialno)

    #Get Motor Position
    # kcdc.CC_GetJogVelParams(serialno, byref(accel_param), byref(vel_param))
    # #print(accel_param.value)
    # current_motor_pos = kcdc.CC_GetPosition(serialno)
    # print(current_motor_pos)
    # #kcdc.CC_Home(serialno)

    # Start Move Test
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
