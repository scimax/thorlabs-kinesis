# thorlabs_kinesis

Python bindings for Thorlabs Kinesis DLLs. This project aims to map all C API
functions provided by Kinesis libraries to python. More information on
Kinesis Motion Control Software can be found on
[Thorlabs' Website](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control).

The version I'm using to map the libraries is **1.14.4.0 64 Bit**

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

At it's current stage this module only provides bindings. So, basic mapping of
C code provided with the Kinesis documentation should be enough to use the
module. **However** you have to make sure that DLLs are in the PATH. For that,
you can add the Kinesis folder to PATH, or add the Kinesis folder to your PATH variable via python before importing thorlabs_kinesis, e.g. for a default installation on Windows it could look like this:

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

