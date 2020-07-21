import sys
import os

os.environ['PATH'] = r"C:\Program Files\Thorlabs\Kinesis" + os.pathsep + os.environ['PATH']
sys.path.append(r"..\thorlabs-kinesis")

from thorlabs_kinesis.devices.kcube_dc import kcube_dc

if __name__ == "__main__":
    controller = kcube_dc("270001")
    print(controller.get_device_info())