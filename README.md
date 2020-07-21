# thorlabs_kinesis

Python bindings for Thorlabs Kinesis DLLs. This project aims to map all C API
functions provided by Kinesis libraries to python. More information on
Kinesis Motion Control Software can be found on
[Thorlabs' Website](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control). Due to the limited access to the hardware the library bindings can only be tested for devices present.

The Kinesis library versions tested are
- **1.14.4.0 64 Bit** ()
- **1.14.23.16838 64-Bit** 

This project emerged as a need to use it with Thorlabs BSC201, BSC203, and LTS150.
So examples are tested with those controllers on Windows 7 with Python 3.6.

Binding methodology is inspired by
[PySDL2](https://github.com/marcusva/py-sdl2) project.

Code structure in the original DLLs is transferred 1-1, even though it could
have benefited from some refactoring. This makes easier to map examples given in
Thorlabs' documentation.


## Installation
Clone the repository or download the ZIP-packaged code and extract it, open the folder 'thorlabs-kinesis' in a terminal and install the package via
```
pip install .
```
If you use conda install `pip` in your desired environment first.

If you want to use the package without prior installation you can add it manually to the PYTHONPATH of each script via

```py
import sys
sys.path.append('path/to/thorlabs_kinesis')
```


## Using
The package consists of three parts. 
- The module `thorlabs_kinesis` provides the python based mapping of the API for selected devices. The naming of the modules follows the naming of the corresponding DLLs with lower case and underscore instead of dots. The prefix *MotionControl* is omitted. For example `Thorlabs.MotionControl.KCube.DCServo.dll` is mapped in `kcube_dcservo.py` 
- The script `generate_binding.py` takes the path to a header file for device for which the python bindings are not implemented yet. It generates the python code required for the binding to the shared DLL library.
- an object-oriented interface will be provided in `devices`. It relies on the bindings in `thorlabs_kinesis`.

In order to use the bindings you have to make sure **that DLLs are in the PATH**. For that,
you can add the Kinesis folder to your system-related PATH variable, or add the Kinesis folder to your PATH variable dynamically via python before importing thorlabs_kinesis, e.g. for a default installation on Windows it could look like this:

```py
import os
os.environ['PATH'] = r"C:\Program Files\Thorlabs\Kinesis" + os.pathsep + os.environ['PATH']
```
Change the path to Kinesis according to your installation path.

## Example
The devices available can be imported directly from the module as shown in the following example ([ex1_deviceinfo_bsc.py](../blob/master/examples/ex1_deviceinfo_bsc.py) from the example folder):
```py
from ctypes import (
    c_char_p,
    byref,
)

from thorlabs_kinesis import benchtop_stepper_motor as bsm

if bsm.TLI_BuildDeviceList() == 0:
    serial_no = c_char_p(bytes("00000000", "utf-8"))
    device_info = bsm.TLI_DeviceInfo()  # container for device info
    bsm.TLI_GetDeviceInfo(serial_no, byref(device_info))

    print("Description: ", device_info.description)
    print("Serial No: ", device_info.serialNo)
    print("Motor Type: ", device_info.motorType)
    print("USB PID: ", device_info.PID)
    print("Max Number of  Channels: ", device_info.maxChannels)
```

To run this code with your device change the serial number *00000000* in `serial_no` to the one matching your motor. If your device is not a stepper motor but, for instance, a DC Servo, replace the import with `from thorlabs_kinesis import kcube_dcservo as kdc`. Keep in mind that all`bsm` literals would have to be replaced with `kdc`.

# Contributors
This repository was first initiated by [ekarademir](https://github.com/ekarademir/). The following users also contributed
- [ando600](https://github.com/ando600) from [BYUCamachoLab](https://github.com/BYUCamachoLab)
- [Sequoia Ploeg](https://github.com/sequoiap) from [BYUCamachoLab](https://github.com/BYUCamachoLab)
- [mtsimmons715](https://github.com/mtsimmons715)
- [davotrey](https://github.com/davotrey)
