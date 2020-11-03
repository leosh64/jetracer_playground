import threading
import copy
import math
import time

from icm20948 import ICM20948
from smbus import SMBus
from madgwick_py.madgwickahrs import MadgwickAHRS
from madgwick_py.quaternion import Quaternion


class ImuUpdater:
    """Asynchronously get IMU state and pass to filter
    """

    def __init__(self, init_state=Quaternion(1, 0, 0, 0), target_freq=30.0):
        """Initialize IMU bus connection, filter and threading.

        Initialize a bus connection to the ICM20948 IMU, a MadgwickAHRS
        filter for filtering noisy sensor data, and a deamon thread
        for background updating.

        Args:
            init_state (madgwick_py.quaternion, optional): Initial state of the filter. Defaults to Quaternion(1, 0, 0, 0).
            target_freq (float, optional): Target update frequency. Defaults to 30.0.
        """

        self.lock = threading.Lock()

        self.target_freq = target_freq

        self.imu = ICM20948(i2c_bus=SMBus(0))

        self.filter = MadgwickAHRS(
            sampleperiod=1.0 / target_freq, quaternion=init_state, beta=0.05,
        )

        thread = threading.Thread(target=self.__update, args=())
        thread.daemon = True
        thread.start()

    def __update(self):
        """Background update function.

        Asynchronously called in the background by a thread, this function
        obtains IMU data and passes it to the filter.
        """
        while True:
            start = time.time()

            x, y, z = self.imu.read_magnetometer_data()
            ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()

            magnetometer = [x, y, z]
            accelerometer = [ax, ay, az]
            gyroscope = [math.radians(gx), math.radians(gy), math.radians(gz)]

            with self.lock:
                self.filter.update(gyroscope, accelerometer, magnetometer)

            time.sleep(max(1.0 / self.target_freq - (time.time() - start), 0))

    def get_data(self):
        """Get filtered IMU data

        Returns:
            madgwick_py.quaternion: Filtered orientation quaternion
        """
        with self.lock:
            return copy.deepcopy(self.filter.quaternion)
