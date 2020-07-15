import os
import sys
os.environ['PATH'] = "C:\\Program Files\\ThorLabs\\Kinesis" + ";" + os.environ['PATH']
sys.path.append(r"..\thorlabs-kinesis")

from thorlabs_kinesis import kcube_solenoid as kcso
import ctypes



if __name__ == "__main__":
    if kcso.TLI_BuildDeviceList() == 0:
        print("Device list built (no errors).")

        size = kcso.TLI_GetDeviceListSize()
        print(size, "Kcube Solenoid device(s) found.")

        serialnos = ctypes.create_string_buffer(200)
        kcso.TLI_GetDeviceListExt(serialnos, 200)
        serialnos = list(filter(None, serialnos.value.decode("utf-8").split(',')))
        print("Serial #'s:", serialnos)

        serial_no_str= "68001047"
        serial_no_c = ctypes.c_char_p(bytes(serial_no_str, "utf-8"))
        device_info = kcso.TLI_DeviceInfo()  # container for device info
        kcso.TLI_GetDeviceInfo(serial_no_c, ctypes.byref(device_info))
        print("typeID: ", device_info.typeID)
        print("Description: ", device_info.description)
        print("Serial No: ", device_info.serialNo)
        print("Motor Type: ", device_info.motorType)
        print("USB PID: ", device_info.PID)
        print("Max Number of  Channels: ", device_info.maxChannels)


        openErrorCode =  kcso.SC_Open(serial_no_c)
        if openErrorCode == 0:
            connStatus = kcso.SC_CheckConnection(serial_no_c)
            print("Connection Status:", connStatus)
            # successfully opened
            print("\nIdentify...")
            kcso.SC_Identify(serial_no_c)
            import time
            time.sleep(2)

            print("\nRequest LED Switches...")
            print(kcso.SC_RequestLEDswitches(serial_no_c))
            print("LED switch:", kcso.SC_GetLEDswitches(serial_no_c))
        else:
            print("Could not be opened. Error Code:", openErrorCode)

        kcso.SC_Close(serial_no_c)
