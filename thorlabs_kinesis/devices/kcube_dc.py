
import ctypes
import time

from .. import kcube_dcservo as kdc

class kcube_dc:
    steps_per_mm = 34304    # class object
    velocity_scaling_to_mm_per_sec = 6e6/(2048 * 65536 *steps_per_mm)
    acc_scaling_to_mm_per_sec2 = (6e6/2048)**2 /(65536 *steps_per_mm)
    def __init__(self, serial_no):
        '''
        serial_no: str
            String representing the serial number of the device.
        '''
        self.serial_no = serial_no
        self.__serial_no = ctypes.c_char_p(bytes(serial_no, "utf-8"))
        # self.steps_per_mm = 34304
        self.__message_type = WORD()
        self.__message_id = WORD()
        self.__message_data = DWORD()

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
            raise ConnectionError("Opening communication to the device "+self.serial_no+\
                " failed. Is it connected?") 
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

    def clear_msg_queue(self):
        kdc.CC_ClearMessageQueue(self.__serial_no)
    def wait_for_msg(self):
        # kcdc.CC_WaitForMessage(serialno, byref(message_type), byref(message_id), byref(message_data))
        pass
    
    # Get move settings and moving
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
    def can_home(self):
        return kdc.CC_CanHome(self.__serial_no)
        # kcdc.CC_CanHome(serialno)
        # pass
    def home(self, wait = True):
        errorCode = kdc.CC_Home(self.__serial_no)
        if wait:

        else:
            return errorCode

    def get_jog_vel_params(self, in_mm_and_sec=False):
        '''
        in_mm_and_sec: bool
            if True, acceleration is returned in mm/sec^2 and velocity is returned as mm/sec.
            For details on the conversion, see page 36 of the Communication protocol.
            (https://www.thorlabs.com/Software/Motion%20Control/APT_Communications_Protocol.pdf)
        '''
        acceleration = ctypes.c_int()
        max_velocity = ctypes.c_int()
        if kdc.CC_RequestJogParams(self.__serial_no) == 0:
            err_code = kdc.CC_GetJogVelParams(self.__serial_no, ctypes.byref(acceleration), 
                ctypes.byref(max_velocity))
            if err_code != 0:
                raise Exception("'CC_GetJogVelParams' return a non-zero error code. Please refer "+\
                " to the API documentation. Error Code: "+str(errCode))
        if in_mm_and_sec:
            return acceleration*self.acc_scaling_to_mm_per_sec2,\
                max_velocity*self.velocity_scaling_to_mm_per_sec
        else:
            return acceleration, max_velocity
    def get_move_vel_params(self, in_mm_and_sec=False):
        '''
        in_mm_and_sec: bool
            if True, acceleration is returned in mm/sec^2 and velocity is returned as mm/sec.
            For details on the conversion, see page 36 of the Communication protocol.
            (https://www.thorlabs.com/Software/Motion%20Control/APT_Communications_Protocol.pdf)
        '''
        acceleration = ctypes.c_int()
        max_velocity = ctypes.c_int()
        if kdc.CC_RequestVelParams(self.__serial_no) == 0:
            err_code = kdc.CC_GetVelParams(self.__serial_no, ctypes.byref(acceleration), 
                ctypes.byref(max_velocity))
            if err_code != 0:
                raise Exception("'CC_GetVelParams' return a non-zero error code. Please refer "+\
                " to the API documentation. Error Code: "+str(errCode))
        if in_mm_and_sec:
            return acceleration*self.acc_scaling_to_mm_per_sec2,\
                max_velocity*self.velocity_scaling_to_mm_per_sec
        else:
            return acceleration, max_velocity

    def move_to_position(self, position_mm):
        #CC_MoveToPosition
        kdc.CC_MoveToPosition(self.__serial_no, position_mm)
        pass
    def move_relative(self, displacement)
        # TODO
        # CC_MoveRelative(char const * serialNo, int displacement);
        pass
    def move_jog(self):
        # TODO
        # CC_MoveJog(char const * serialNo, MOT_TravelDirection jogDirection);
        pass
    
    def set_jog_vel_params(self):
        # TODO
        print("NOT IMPLEMENTED YET!")
        return False
    def set_vel_params(self):
        # TODO
        print("NOT IMPLEMENTED YET!")
        return False

    # https://stackoverflow.com/questions/3774328/implementing-use-of-with-object-as-f-in-custom-class-in-python
    def __enter__(self):
        #ttysetattr etc goes here before opening and returning the file object
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        #Exception handling here
        self.close()

    


