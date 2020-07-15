# Bindings for Thorlabs KCube Solenoid DLL
# Implemented with Kinesis Version 1.14.23.16838

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

lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.Solenoid.dll")

# enum MOT_MotorTypes
MOT_NotMotor = c_int(0)
MOT_DCMotor = c_int(1)
MOT_StepperMotor = c_int(2)
MOT_BrushlessMotor = c_int(3)
MOT_CustomMotor = c_int(100)
MOT_MotorTypes = c_int

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

TLI_BuildDeviceList = bind(lib, "TLI_BuildDeviceList", None, c_short)
TLI_GetDeviceListSize = bind(lib, "TLI_GetDeviceListSize", None, c_short)
# TLI_GetDeviceList  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short  TLI_GetDeviceList(SAFEARRAY** stringsReceiver);
# TLI_GetDeviceListByType  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short  TLI_GetDeviceListByType(SAFEARRAY** stringsReceiver, int typeID);
# TLI_GetDeviceListByTypes  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short  TLI_GetDeviceListByTypes(SAFEARRAY** stringsReceiver, int * typeIDs, int length);
TLI_GetDeviceListExt = bind(lib, "TLI_GetDeviceListExt", [POINTER(c_char), c_dword], c_short)
TLI_GetDeviceListByTypeExt = bind(lib, "TLI_GetDeviceListByTypeExt", [POINTER(c_char), c_dword, c_int], c_short)
TLI_GetDeviceListByTypesExt = bind(lib, "TLI_GetDeviceListByTypesExt", [POINTER(c_char), c_dword, POINTER(c_int), c_int], c_short)
TLI_GetDeviceInfo = bind(lib, "TLI_GetDeviceInfo", [POINTER(c_char), POINTER(TLI_DeviceInfo)], c_short)

SC_Open = bind(lib, "SC_Open", [POINTER(c_char)], c_short)
SC_Close = bind(lib, "SC_Close", [POINTER(c_char)], None)
SC_CheckConnection = bind(lib, "SC_CheckConnection", [POINTER(c_char)], c_bool)
SC_Identify = bind(lib, "SC_Identify", [POINTER(c_char)], None)
SC_RequestLEDswitches = bind(lib, "SC_RequestLEDswitches", [POINTER(c_char)], c_short)
SC_GetLEDswitches = bind(lib, "SC_GetLEDswitches", [POINTER(c_char)], c_word)
SC_SetLEDswitches = bind(lib, "SC_SetLEDswitches", [POINTER(c_char), c_word], c_short)
# SC_GetHardwareInfo = bind(lib, "SC_GetHardwareInfo", [POINTER(c_char)], c_short)
# short SC_GetHardwareInfo(char const * serialNo, char * modelNo, DWORD sizeOfModelNo, WORD * type, WORD * numChannels, 
#												  char * notes, DWORD sizeOfNotes, DWORD * firmwareVersion, WORD * hardwareVersion, WORD * modificationState);
# short SC_GetHardwareInfoBlock(char const *serialNo, TLI_HardwareInformation *hardwareInfo)
# short SC_RequestHubBay(char const * serialNo);
# char SC_GetHubBay(char const * serialNo);
# 
# DWORD  SC_GetSoftwareVersion(char const * serialNo);
# bool  SC_LoadSettings(char const * serialNo);

# bool  SC_LoadNamedSettings(char const * serialNo, char const *settingsName);
# bool  SC_PersistSettings(char const * serialNo);
# void  SC_ClearMessageQueue(char const * serialNo);
# void  SC_RegisterMessageCallback(char const * serialNo, void (* functionPointer)());
# int  SC_MessageQueueSize(char const * serialNo);
# bool  SC_GetNextMessage(char const * serialNo, WORD * messageType, WORD * messageID, DWORD *messageData);
# bool  SC_WaitForMessage(char const * serialNo, WORD * messageType, WORD * messageID, DWORD *messageData);
# bool  SC_StartPolling(char const * serialNo, int milliseconds);
# long  SC_PollingDuration(char const * serialNo);
# void  SC_StopPolling(char const * serialNo);
# bool  SC_TimeSinceLastMsgReceived(char const * serialNo, __int64 &lastUpdateTimeMS );
# void  SC_EnableLastMsgTimer(char const * serialNo, bool enable, __int32 lastMsgTimeout );
# bool  SC_HasLastMsgTimerOverrun(char const * serialNo);
# short  SC_RequestSettings(char const * serialNo);
# short  SC_RequestStatus(char const * serialNo);
# short  SC_RequestStatusBits(char const * serialNo);
# DWORD  SC_GetStatusBits(char const * serialNo);
# short  SC_RequestOperatingMode(char const * serialNo);
# SC_OperatingModes  SC_GetOperatingMode(char const * serialNo);
# short  SC_SetOperatingMode(char const * serialNo, SC_OperatingModes mode);

# SC_SolenoidStates  SC_GetSolenoidState(char const * serialNo);

# short  SC_RequestOperatingState(char const * serialNo);

# SC_OperatingStates  SC_GetOperatingState(char const * serialNo);
# short  SC_SetOperatingState(char const * serialNo, SC_OperatingStates state);
# short  SC_RequestCycleParams(char const * serialNo);
# short  SC_GetCycleParams(char const * serialNo, unsigned int * onTime, unsigned int * offTime, unsigned int * numCycles);
# short  SC_SetCycleParams(char const * serialNo, unsigned int onTime, unsigned int offTime, unsigned int numCycles);
# short  SC_GetCycleParamsBlock(const char * serialNo, SC_CycleParameters *cycleParams);
# short  SC_SetCycleParamsBlock(const char * serialNo, SC_CycleParameters *cycleParams);
# short  SC_RequestMMIParams(char const * serialNo);
# short  SC_GetMMIParamsExt(char const * serialNo, __int16 *displayIntensity, __int16 *displayTimeout, __int16 *displayDimIntensity);
# short  SC_GetMMIParams(char const * serialNo, __int16 *displayIntensity);
# short  SC_SetMMIParamsExt(char const * serialNo, __int16 displayIntensity, __int16 displayTimeout, __int16 displayDimIntensity);
# short  SC_SetMMIParams(char const * serialNo, __int16 displayIntensity);
# short  SC_GetMMIParamsBlock(char const * serialNo, KSC_MMIParams *mmiParams);
# short  SC_SetMMIParamsBlock(char const * serialNo, KSC_MMIParams *mmiParams);
# short  SC_RequestTriggerConfigParams(char const * serialNo);
# short  SC_GetTriggerConfigParams(char const * serialNo, KSC_TriggerPortMode *trigger1Mode, KSC_TriggerPortPolarity *trigger1Polarity, KSC_TriggerPortMode *trigger2Mode, KSC_TriggerPortPolarity *trigger2Polarity);
# short  SC_SetTriggerConfigParams(char const * serialNo, KSC_TriggerPortMode trigger1Mode, KSC_TriggerPortPolarity trigger1Polarity, KSC_TriggerPortMode trigger2Mode, KSC_TriggerPortPolarity trigger2Polarity);
# short  SC_GetTriggerConfigParamsBlock(char const * serialNo, KSC_TriggerConfig *triggerConfigParams);
# short  SC_SetTriggerConfigParamsBlock(char const * serialNo, KSC_TriggerConfig *triggerConfigParams);
# short  SC_RequestDigitalOutputs(char const * serialNo);
# byte  SC_GetDigitalOutputs(char const * serialNo);
# short  SC_SetDigitalOutputs(char const * serialNo, byte outputsBits);


