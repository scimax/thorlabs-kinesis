import os
import sys
os.environ['PATH'] = "C:\\Program Files\\ThorLabs\\Kinesis" + ";" + os.environ['PATH']
sys.path.append(r"..\thorlabs-kinesis")

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

from thorlabs_kinesis import benchtop_piezo as bp

def homeStages():
    # Home the y and z directions at half-of-travel so they can be used to do slight adjustments
    halfway = c_short(16383)
    zero = c_short(0)
    bp.PBC_SetPosition(serialno,bp.Channel1,zero)
    bp.PBC_SetPosition(serialno,bp.Channel2,halfway)
    bp.PBC_SetPosition(serialno,bp.Channel3,halfway)

def couple():
    maxTravel = 32767 # travel is from 0 to 32767 for 20 um
    jogLength = int(16) # just under 10 nm of travel
    currentPos = int(0)
    Done = False
    while not Done:
        try: 
            if keyboard.is_pressed('q'):    # press q to exit the while loop and stop motion
                print('Pull Complete')
                return
            elif keyboard.is_pressed('w'):  # press w to increase the rate of motion
                jogLength += int(2)
                print("jogLength: ", jogLength)
            elif keyboard.is_pressed('s'):  # press s to decrease the rate of motion
                if jogLength > 4:
                    jogLength -= int(2)
                    print("jogLength: ", jogLength)
        except: 
            continue
        currentPos = int(bp.PBC_GetPosition(serialno,bp.Channel1))
        bp.PBC_SetPosition(serialno,bp.Channel1,c_short(currentPos+jogLength))
        print("current position between 0 and 32767 (short): ",currentPos)
        time.sleep(0.2)

def adjust(channel):
    jogLength = 800 # about half a micron out of 20 um of 
    currentPos = int(0)
    Done = False 
    while not Done:
        try: 
            if keyboard.is_pressed('q'):    # press q to exit the while loop and stop motion
                print('Adjustment Complete')
                return
            elif keyboard.is_pressed('w'):  # press w to increase the rate of motion
                currentPos = int(bp.PBC_GetPosition(serialno,channel))
                bp.PBC_SetPosition(serialno,channel,c_short(currentPos+jogLength))
                print("current position of channel ",channel,": ", currentPos+jogLength)
            elif keyboard.is_pressed('s'):  # press s to decrease the rate of motion
                currentPos = int(bp.PBC_GetPosition(serialno,channel))
                bp.PBC_SetPosition(serialno,channel,c_short(currentPos-jogLength))
                print("current position of channel ",channel,": ", currentPos+jogLength)
        except: 
            continue

def upShift():
    jogLength = int(16)
    currentPos = int(bp.PBC_GetPosition(serialno,bp.Channel1))
    bp.PBC_SetPosition(serialno,bp.Channel1,c_short(currentPos + jogLength))

def downShift():
    jogLength = int(16)
    currentPos = int(bp.PBC_GetPosition(serialno,bp.Channel1))
    bp.PBC_SetPosition(serialno,bp.Channel1,c_short(currentPos - jogLength))


if bp.TLI_BuildDeviceList() == 0:
    print("Device list built (no errors).")
    size = bp.TLI_GetDeviceListSize()
    print(size, "device(s) found.")
    if size > 0:

        # Open Communication
        serialno = c_char_p(bytes("27504851", "utf-8"))
        bp.PBC_Open(serialno)
        bp.PBC_StartPolling(serialno)
        bp.PBC_ClearMessageQueue(serialno)
        time.sleep(1)

        # Initialize/Identify Channels

        # x axis
        bp.PBC_EnableChannel(serialno, bp.Channel1) # enables control of specified channel
        bp.PBC_SetPositionControlMode(serialno, bp.Channel1, bp.CTR_ClosedLoop) # set the channel to closed loop
        bp.PBC_Identify(serialno, bp.Channel1)  # cause the LED readout to blink to identify it
        time.sleep(2)   # remove me after testing
        # y axis
        bp.PBC_EnableChannel(serialno, bp.Channel2)
        bp.PBC_SetPositionControlMode(serialno, bp.Channel2, bp.CTR_ClosedLoop)
        bp.PBC_Identify(serialno, bp.Channel2)
        time.sleep(2)   # remove me after testing
        # z axis
        bp.PBC_EnableChannel(serialno, bp.Channel3)
        bp.PBC_SetPositionControlMode(serialno, bp.Channel3, bp.CTR_ClosedLoop)
        bp.PBC_Identify(serialno, bp.Channel3)

        #Identify Control Mode TODO: remove this code after testing
        print("control type for bp.Channel3: ", bp.PBC_GetPositionControlMode(serialno,bp.Channel1))
        print("control type for bp.Channel2: ", bp.PBC_GetPositionControlMode(serialno,bp.Channel2))
        print("control type for bp.Channel3: ", bp.PBC_GetPositionControlMode(serialno,bp.Channel3))

        Done = False
        while not Done:
            command = input("Enter a key to perform an action (? for help: ")
            if command is 'h':
                homeStages()
            elif command is 'c':
                couple()
            elif command is 'z':
                adjust(bp.Channel3)
            elif command is 'y':
                adjust(bp.Channel2)
            elif command is '?':
                print('\nh -------- home the three axis\nc -------- couple (q to quit, w to speed up, s to slow down\nz -------- adjust z axis (q to quit, w to move up, s to move down\n y -------- adjust y axis (q to quit, w to move up, s to move down\nw -------- jog the x axis up once\ns -------- jog the x axis down once\nq -------- quit')
            
            try: 
                if keyboard.is_pressed('w'):    # press q to exit the while loop and stop motion
                    upShift()
                elif keyboard.is_pressed('s'):
                    downShift()
            except: 
                continue
        
        bp.PBC_StopPolling(serialno)
        if bp.PBC_Disconnect(serialno) == 0:
                print("device disconnected")
        bp.PBC_Close(serialno)
