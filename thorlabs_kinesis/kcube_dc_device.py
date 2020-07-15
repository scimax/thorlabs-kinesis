
import ctypes

from . import kcube_dcservo as kdc

class kcube:
    def __init__(self, serial_no):
        '''
        serial_no: str
            String representing the serial number of the device.
        '''
        self.serial_no = serial_no
        self.__serial_no = ctypes.c_char_p(bytes(serial_no, "utf-8"))
        
    def get_device_info(self):
        device_info = kdc.TLI_DeviceInfo()  # container for device info
        kdc.TLI_GetDeviceInfo(self.__serial_no, ctypes.byref(device_info))
        return dict((field, getattr(device_info, field)) for field, _ 
            in device_info._fields_)

    def home(self):
        pass


