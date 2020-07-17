
import ctypes
import time

from . import kcube_dcservo as kdc

class kcube:
    steps_per_mm = 34304    # class object
    def __init__(self, serial_no):
        '''
        serial_no: str
            String representing the serial number of the device.
        '''
        self.serial_no = serial_no
        self.__serial_no = ctypes.c_char_p(bytes(serial_no, "utf-8"))
        # self.steps_per_mm = 34304

    def identify(self, wait=5):
        kdc.CC_Identify(self.__serial_no)
        time.sleep(wait)

    def __query_device_info(self):
        self.device_info = kdc.TLI_DeviceInfo()  # container for device info
        kdc.TLI_GetDeviceInfo(self.__serial_no, ctypes.byref(self.device_info))

    def get_device_info(self):
        try:
            device_info = self.device_info
        except AttributeError:
            self.__query_device_info()
            device_info = self.device_info
        finally:
            return dict((field, getattr(device_info, field)) for field, _ 
                in device_info._fields_)

    def get_position(self, in_mm = False):
        '''
        Get current motor position.

        in_mm: bool
            if True, the value is returned on millimeter based on the steps per millimeter setting.
            Otherwise the encoder position is returned.
        
        '''
        encoder_pos = kdc.CC_GetPosition(self.__serial_no)
        if in_mm:
            return encoder_pos/self.steps_per_mm
        else:
            return encoder_pos


    def print_device_info(self):
        try:
            device_info = self.device_info
        except AttributeError:
            # print("AttributeError")
            self.__query_device_info()
            device_info = self.device_info
        finally:
            print("Description: ", device_info.description)
            print("Serial No: ", device_info.serialNo)
            print("Motor Type: ", device_info.motorType)
            print("USB PID: ", device_info.PID)
            print("Max Number of  Channels: ", device_info.maxChannels)

    # Communication
    def open(self):
        '''
        Open Communication to controller.

        If return value is 0 the connection was succesfully opened. Otherwise the return
        value corresponds to the C_DLL_ERRORCODES_page "Error Codes" .
        '''
        # c_short
        opened_return = kdc.CC_Open(self.__serial_no)
        # print(type(opened_return))
        if not opened_return == 0:
            print("Opening communication failed!") 
        return opened_return

    def close(self):
        '''
        Close communication to controller.
        '''
        kdc.CC_Close(self.__serial_no)

    def start_polling(self, polling_rate_ms=200):
        '''
        Starts the internal polling loop which continuously requests position and status.

        polling_rate_ms: int
            polling rate in milliseconds

        Return:
        bool:
            true if successful, false if not.
        '''
        return kdc.CC_StartPolling(self.__serial_no, ctypes.c_int(polling_rate_ms))
    def stop_polling(self):
        '''
        Stop the internal polling loop.
        '''
        kdc.CC_StopPolling(self.__serial_no)

    def get_polling_duration(self):
        return kdc.CC_PollingDuration(self.__serial_no)
    
    def home(self):
        pass


    # https://stackoverflow.com/questions/3774328/implementing-use-of-with-object-as-f-in-custom-class-in-python
    def __enter__(self):
        #ttysetattr etc goes here before opening and returning the file object
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        #Exception handling here
        self.close()

    


