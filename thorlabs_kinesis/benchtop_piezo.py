# Bindings for Thorlabs Benchtop Piezo BCP 303 (3 channel piezo controller)
# Implemented with Kinesis Version 1.14.23.16838
import thorlabs_kinesis as tk

from ctypes import (
    Structure,
    cdll,
    c_bool,
    c_short,
    c_int,
    c_uint,
    c_int16,
    c_int32,
    c_char,
    c_byte,
    c_long,
    c_float,
    c_double,  
    POINTER,
    CFUNCTYPE,
)

from thorlabs_kinesis._utils import (
    c_word,
    c_dword,
    bind
)

lib = cdll.LoadLibrary("Thorlabs.MotionControl.Benchtop.Piezo.dll")


# enum MOT_MotorTypes
MOT_NotMotor = c_int(0)
MOT_DCMotor = c_int(1)
MOT_StepperMotor = c_int(2)
MOT_BrushlessMotor = c_int(3)
MOT_CustomMotor = c_int(100)
MOT_MotorTypes = c_int

CTR_OpenLoop = c_int(1)
CTR_ClosedLoop = c_int(2)
CTR_OpenLoopSmoothed = c_int(3)
CTR_ClosedLoopSmoothed = c_int(4)
PZ_ControlModeTypes = c_int

Channel1 = c_int(1)
Channel2 = c_int(2)
Channel3 = c_int(3)
ChannelType = c_int


class TLI_DeviceInfo(Structure):
    _fields_ = [("typeID", c_dword),
                ("description", (65 * c_char)),
                ("serialNo", (9 * c_char)),
                ("PID", c_dword),
                ("isKnownType", c_bool),
                ("motorType", MOT_MotorTypes),
                ("isPiezoDevice", c_bool),
                ("isLaser", c_bool),
                ("isCustomType", c_bool),
                ("isRack", c_bool),
                ("maxChannels", c_short)]

class TLI_HardwareInformation(Structure):
    _fields_ = [("serialNumber", c_dword),
                ("modelNumber", (8 * c_char)),
                ("type", c_word),
                ("firmwareVersion", c_dword),
                ("notes", (48 * c_char)),
                ("deviceDependantData", (12 * c_byte)),
                ("hardwareVersion", c_word),
                ("modificationState", c_word),
                ("numChannels", c_short)]

PBC_CheckConnection = bind(lib, "PBC_CheckConnection", )



TLI_BuildDeviceList = bind(lib, "TLI_BuildDeviceList", None, c_short)
TLI_GetDeviceListSize = bind(lib, "TLI_GetDeviceListSize", None, c_short)
# TLI_GetDeviceList  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceList(SAFEARRAY** stringsReceiver);
# TLI_GetDeviceListByType  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceListByType(SAFEARRAY** stringsReceiver, int typeID);
# TLI_GetDeviceListByTypes  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceListByTypes(SAFEARRAY** stringsReceiver, int * typeIDs, int length);
TLI_GetDeviceListExt = bind(lib, "TLI_GetDeviceListExt", [POINTER(c_char), c_dword], c_short)
TLI_GetDeviceListByTypeExt = bind(lib, "TLI_GetDeviceListByTypeExt", [POINTER(c_char), c_dword, c_int], c_short)
TLI_GetDeviceListByTypesExt = bind(lib, "TLI_GetDeviceListByTypesExt", [POINTER(c_char), c_dword, POINTER(c_int), c_int], c_short)
TLI_GetDeviceInfo = bind(lib, "TLI_GetDeviceInfo", [POINTER(c_char), POINTER(TLI_DeviceInfo)], c_short)

# CC_CanHome = bind(lib, "CC_CanHome", [POINTER(c_char)], c_bool)
# CC_ClearMessageQueue = bind(lib, "CC_ClearMessageQueue", [POINTER(c_char)], None)
# CC_GetJogVelParams = bind(lib, "CC_GetJogVelParams", [POINTER(c_char),POINTER(c_int),POINTER(c_int)], c_short)
# CC_GetPosition  = bind(lib, "CC_GetPosition", [POINTER(c_char)], c_int)
# CC_Home = bind(lib, "CC_Home", [POINTER(c_char)], c_short)
# CC_MoveToPosition = bind(lib, "CC_MoveToPosition", [POINTER(c_char),c_int], c_short)



# set the position control mode
PBC_SetPositionControlMode = bind(lib, "PBC_SetPositionControlMode", [POINTER(c_char), c_short, PZ_ControlModeTypes], c_short)
# get position control mode
PBC_GetPositionControlMode = bind(lib, "PBC_GetPositionControlMode", [POINTER(c_char), c_short], PZ_ControlModeTypes)
# requests position control mode be read from the device for the device and channel
PBC_RequestPositionControlMode = bind(lib, "PBC_RequestPositionControlMode", [POINTER(c_char), c_short], c_bool)
# open the device for communication
PBC_Open = bind(lib, "PBC_Open", [POINTER(c_char)], c_short)
# tells the device its is being disconnected
PBC_Disconnect = bind(lib, "PBC_Disconnect", [POINTER(c_char)], c_short) 
# disconnects and closes the device
PBC_Close = bind(lib, "PBC_Close", [POINTER(c_char)], None)
# enable channel for computer control, power applied so it is in a fixed position
PBC_EnableChannel = bind(lib, "PBC_EnableChannel", [POINTER(c_char), c_short], c_short)
# disable channel so it can be moved by hand
PBC_DisableChannel = bind(lib, "PBC_DisableChannel", [POINTER(c_char), c_short], c_short)


# gets position if in closed loop mode (undefined otherwise)
PBC_GetPosition = bind(lib, "PBC_GetPosition", [POINTER(c_char), c_short], c_short)
# sets the position when in closed loop mode, returns an error code
PBC_SetPosition = bind(lib, "PBC_SetPosition", [POINTER(c_char), c_short, c_short], c_short)
# sends a command to the device to make it identify itself (which channel)
PBC_Identify = bind(lib, "PBC_Identify", [POINTER(c_char), c_short], None)
# verifies that the specified channel is valid
PBC_IsChannelValid = bind(lib, "PBC_IsChannelValid", [POINTER(c_char), c_short], c_bool)

# resets all parameters to power-up values
PBC_ResetParameters = bind(lib, "PBC_ResetParameters", [POINTER(c_char), c_short], c_short)
# sets the voltage output to zero and defines the ensuing actuator position as zero
PBC_SetZero = bind(lib, "PBC_SetZero", [POINTER(c_char), c_short], c_short)
# clears the device message queue
PBC_ClearMessageQueue = bind(lib, "PBC_ClearMessageQueue")

# starts internal polling loop which continuously requests position and status
PBC_StartPolling = bind(lib, "PBC_StartPolling", [POINTER(c_char), c_short, c_int], c_bool)
# stops internal polling loop
PBC_StopPolling = bind(lib, "PBC_StopPolling", [POINTER(c_char), c_short], None)
# gets polling duration
PBC_PollingDuration = bind(lib, "PBC_PollingDuration", [POINTER(c_char), c_short], c_long)

# CC_WaitForMessage = bind(lib, "CC_WaitForMessage", [POINTER(c_char),POINTER(c_word),POINTER(c_word),POINTER(c_dword)], None)
# CC_RequestPosition = bind(lib, "CC_RequestPosition", [POINTER(c_char)], None)