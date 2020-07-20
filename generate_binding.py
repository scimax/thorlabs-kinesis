# Desc: Helper script for generating the python bindings to the shared library
# Author: Max Kellermeier
# Date: 2020.07.18

import re
import ctypes
import os
import tempfile

reFuncPattern = re.compile(r"^\w+_API\W+((?:unsigned\W+)*\w+)\W+__cdecl\W+(\w+)\(([^)]*)\);")
# reFunc

ctypes.c_word = ctypes.c_ushort
ctypes.c_dword = ctypes.c_ulong

def type_dispatch(typeStr):
    typeStr = typeStr.strip().replace("__", "").replace("unsigned ", "u")
    # ctypes.wintypes
    return "c_"+typeStr.lower() if hasattr(ctypes,"c_"+typeStr.lower()) else typeStr

def cpp2py_function_binding_str(cpp_declaration):
    # Thanks to Chaoste for the great help with the regex
    # https://jsfiddle.net/Chaoste/htkebsx2/23/
    # https://regex101.com/r/ocIp9u/4

    # repeated subgroups are not supported
    # https://stackoverflow.com/questions/29020148/python-regex-subgroup-capturing
    # Using simpler regex: https://regex101.com/r/aWLXTx/5

    match = reFuncPattern.match(cpp_declaration)
    if match:
        matchgroups = match.groups()
        return_type = matchgroups[0].replace("unsigned ", "u")
        return_type = "c_" + return_type.lower() if return_type != "void" else "None"
        method_name = matchgroups[1]

        parameter_list_string = matchgroups[2].replace("void", "")
        parameter_types = [t.strip().split(" ") for t in parameter_list_string.split(",")]
        parameter_types = [single_param_list[0] if single_param_list[0] != "unsigned" else "u"+single_param_list[1] 
            for single_param_list in parameter_types]

        parameter_types =  ["c_"+t if hasattr(ctypes,"c_"+t) else t for t in parameter_types]
        # print(parameter_types)
        if parameter_types == [""]:
            return_parameter_str = "None"
        else:
            return_parameter_str = "["+", ".join(["POINTER("+t+")" for t in parameter_types]) + "]"
        # print("return_parameter_str:  ", return_parameter_str)
        return rf'{method_name} = bind(lib, "{method_name}", {return_parameter_str}, {return_type})'
    else:
        return cpp_declaration

def cpp2py_struct_binding_str(cpp_struct):
    '''
    cpp_struct: str
        multiline string containing the striped lines representing the struct declaration.
    '''
    typedef_str, member_block_str, name_str = re.split(r"[{}]", cpp_struct)
    struct_name = name_str.replace(";", "").strip()

    # matchLastLine = re.match(r"\}\W+(\w+);", cpp_struct[-1])
    # if matchLastLine:
    #     struct_name = matchLastLine[1]

    # # https://regex101.com/r/pFNsAo/1
    reStructMember = re.compile(r"(\w+)\W+(\w+)(\[[0-9]+\])*;(?:\W+)*\n")
    struct_member_matches = reStructMember.findall(member_block_str)
    struct_member_res_str = ["(\"" + m[1] + "\", " + type_dispatch(m[0]) + ")" 
        if m[2] =="" else 
        "(\"" + m[1] + "\", ("+ m[2][1:-1]+ " * " + type_dispatch(m[0]) + "))"
        for m in struct_member_matches]
    # print(",\n        ".join(struct_member_res_str))
    res_str = rf"class {struct_name}(Structure):" + "\n"
    res_str += "".join([" "]*4) + "_fields_ = ["
    res_str += ",\n        ".join(struct_member_res_str)
    res_str += "]\n"
    # print(res_str)
    return res_str

def cpp2py_enum_binding_str(cpp_enum):
    '''
    cpp_enum: str
        multiline string containing the striped lines representing the struct declaration.
    '''
    # if boolEnumDefLines and line.find("=") != -1:
    #             f_temp.write(line+"\n")
    typedef_str, member_block_str, name_str = re.split(r"[{}]", cpp_enum)
    try:
        underlying_type = typedef_str.split(":")[1].strip()
    except IndexError:
        underlying_type = "int"
    enum_name = name_str.replace(";", "").strip()
    underlying_type = type_dispatch(underlying_type)
    #https://regex101.com/r/FrdzBt/5
    reEnumerator = re.compile(r"^(\w+)\s*(?:=\s*(0?[xX]?[0-9a-fA-F]+))?[,\s]\s*(\/\/+)", flags=re.MULTILINE)
    py_enumerators_str = reEnumerator.sub(r"\1 = "+underlying_type+r"(\2) # ", member_block_str)
    py_enumerators_str = py_enumerators_str.replace(underlying_type + "()", "None")
    return py_enumerators_str + rf"{enum_name} = {underlying_type}"

if __name__ == "__main__":
    ## ToDos
    # 1. create a temp file
    # 2. open header file
    # 3. remove comment lines from header file while writing it to the temp file
    # 4. 

    ### Create Temp file
    f_temp = tempfile.NamedTemporaryFile(mode="w+", dir=".", delete=False)
    f_out_py = tempfile.NamedTemporaryFile(mode="w+", dir=".", delete=False)
    print("temp file for reading header file:", os.path.split(f_temp.name)[1])
    print("temp file for writing python code")

    pathToLib = r"C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.KCube.DCServo.h"

    with open(pathToLib, "r") as f_lib:
        bool_typedef_lines = False
        bool_funcdef_lines = False
        declaration_str = ""
        for line in f_lib:
            line = line.strip()
            
            if (not bool_funcdef_lines):
                if line.startswith("typedef"):
                    bool_typedef_lines = True
                if bool_typedef_lines:
                    declaration_str += line + "\n"
                # elif line.startswith("typedef enum"):
                #     boolEnumDefLines = True
                #     f_temp.write("# Enumerator "+ line.split(":")[0].split(" ")[-1]+"\n")
                if bool_typedef_lines and re.match(r"}(?:\W+)(\w+);", line):
                    bool_typedef_lines = False
                    if declaration_str.startswith("typedef enum"):
                        py_bind_str = cpp2py_enum_binding_str(declaration_str)
                    elif declaration_str.startswith("typedef struct"):
                        py_bind_str = cpp2py_struct_binding_str(declaration_str)
                    else:
                        py_bind_str = "\n"
                    declaration_str = "" # reset string
                    f_temp.write(py_bind_str+ "\n")

            if (not bool_typedef_lines):
                if line.startswith("KCUBEDCSERVO_API") or bool_funcdef_lines:
                    bool_funcdef_lines = True
                    declaration_str += line 
                if line.find(";") != -1:
                    f_temp.write(cpp2py_function_binding_str(declaration_str)+"\n")
                    declaration_str= ""
                    bool_funcdef_lines = False

    
    f_temp.seek(0)

    f_temp.close()
    if False:
        os.remove(f_temp.name)


    ### Test enum binding generation
    # input ='''	typedef enum MOT_TravelDirection : short
	# {
	# 	MOT_TravelDirectionUndefined,///<Undefined
	# 	MOT_Forwards = 0x01,///<Move in a Forward direction
	# 	MOT_Backwards = 0x02,///<Move in a Backward / Reverse direction
	# } MOT_TravelDirection;'''
    # input = "\n".join([l.strip() for l in input.split("\n")])
    # print(cpp2py_enum_binding_str(input))


    ### Test struct binding generation
    # input ='''	typedef struct TLI_DeviceInfo
	# {
	# 	/// <summary> The device Type ID, see \ref C_DEVICEID_page "Device serial numbers". </summary>
	# 	DWORD typeID;
	# 	/// <summary> The device description. </summary>
	# 	char description[65];
	# 	/// <summary> The device serial number. </summary>
	# 	char serialNo[16];
	# 	/// <summary> The USB PID number. </summary>
	# 	DWORD PID;

	# 	/// <summary> <c>true</c> if this object is a type known to the Motion Control software. </summary>
	# 	bool isKnownType;
	# 	/// <summary> The motor type (if a motor).
	# 	/// 		  <list type=table>
	# 	///				<item><term>MOT_NotMotor</term><term>0</term></item>
	# 	///				<item><term>MOT_DCMotor</term><term>1</term></item>
	# 	///				<item><term>MOT_StepperMotor</term><term>2</term></item>
	# 	///				<item><term>MOT_BrushlessMotor</term><term>3</term></item>
	# 	///				<item><term>MOT_CustomMotor</term><term>100</term></item>
	# 	/// 		  </list> </summary>
	# 	MOT_MotorTypes motorType;

	# 	/// <summary> <c>true</c> if the device is a piezo device. </summary>
	# 	bool isPiezoDevice;
	# 	/// <summary> <c>true</c> if the device is a laser. </summary>
	# 	bool isLaser;
	# 	/// <summary> <c>true</c> if the device is a custom type. </summary>
	# 	bool isCustomType;
	# 	/// <summary> <c>true</c> if the device is a rack. </summary>
	# 	bool isRack;
	# 	/// <summary> Defines the number of channels available in this device. </summary>
	# 	short maxChannels;
	# } TLI_DeviceInfo;'''
    # input = "\n".join([line.strip() for line in input.split("\n")])
    # # print(input)
    # print(cpp2py_struct_binding_str(input))

    ### Test function binding generation
    # input = "KCUBEDCSERVO_API short __cdecl TLI_GetDeviceInfo(char const *one, TLI_DeviceInfo * two, long const bliblub three);"
    # print(cpp2py_binding_str(input))
    # print(cpp2py_binding_str("KCUBEDCSERVO_API short __cdecl TLI_BuildDeviceList(void);"))

    # print(cpp2py_binding_str("KCUBEDCSERVO_API short __cdecl TLI_GetDeviceListSize();"))
    # print(cpp2py_function_binding_str(
    #     "KCUBEDCSERVO_API unsigned int __cdecl CC_GetHomingVelocity(char const * serialNo);"
    # ))

    # print(cpp2py_function_binding_str("KCUBEDCSERVO_API short __cdecl CC_SetJogStepSize(char const * serialNo, unsigned int stepSize);"))

    


