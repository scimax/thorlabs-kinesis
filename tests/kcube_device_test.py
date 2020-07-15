import sys
import os

os.environ['PATH'] = r"C:\Program Files\Thorlabs\Kinesis" + os.pathsep + os.environ['PATH']
sys.path.append(r"..\thorlabs-kinesis")

from thorlabs_kinesis.kcube_dc_device import kcube

if __name__ == "__main__":
    controller = kcube("270001")
    print(controller.get_device_info())