"""Hardware abstraction layer for Northwind drone systems."""

from typing import Dict, List, Optional

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

try:
    import gpsd
    GPS_AVAILABLE = True
except ImportError:
    GPS_AVAILABLE = False


class FlightControllerHAL:
    """Abstract hardware layer interface for GPS, IMU, motors, and distance sensors."""

    def read_gps(self) -> Dict[str, float]:
        """Read GPS data from a connected module.

        Returns:
            dict: {'latitude': float, 'longitude': float, 'altitude': float, 'fix_quality': int}
        """
        raise NotImplementedError("GPS hardware read must be implemented by a subclass")

    def read_imu(self) -> Dict[str, float]:
        """Read IMU data from a connected gyro/accelerometer.

        Returns:
            dict: {'accel_x': float, 'accel_y': float, 'accel_z': float,
                   'gyro_x': float, 'gyro_y': float, 'gyro_z': float,
                   'mag_x': float, 'mag_y': float, 'mag_z': float}
        """
        raise NotImplementedError("IMU hardware read must be implemented by a subclass")

    def set_motor_pwm(self, motor_id: int, pwm_value: int) -> None:
        """Set a motor ESC PWM output.

        Args:
            motor_id (int): Motor index (0-3 for quadcopter)
            pwm_value (int): PWM value, typically 1000-2000
        """
        raise NotImplementedError("Motor PWM output must be implemented by a subclass")

    def read_distance_sensor(self) -> Optional[float]:
        """Read a distance sensor such as ultrasonic, lidar, or rangefinder.

        Returns:
            float or None: Distance in meters, or None if unsupported
        """
        raise NotImplementedError("Distance sensor read must be implemented by a subclass")

    def read_ultrasonic(self) -> Optional[float]:
        """Read an ultrasonic rangefinder if available."""
        return self.read_distance_sensor()

    def read_lidar(self) -> Optional[float]:
        """Read lidar distance if available."""
        return self.read_distance_sensor()

    def arm_motors(self) -> None:
        """Perform any hardware-specific motor arming sequence."""
        raise NotImplementedError("Motor arming must be implemented by a subclass")

    def disarm_motors(self) -> None:
        """Perform any hardware-specific motor disarm sequence."""
        raise NotImplementedError("Motor disarming must be implemented by a subclass")


class SimulatedHAL(FlightControllerHAL):
    """Simple fallback HAL for development and unit testing.

    This class is not a replacement for real hardware, but it provides a
    consistent abstraction so the software stack remains hardware-ready.
    """

    def __init__(self):
        self._gps = {'latitude': 0.0, 'longitude': 0.0, 'altitude': 0.0, 'fix_quality': 1}
        self._imu = {
            'accel_x': 0.0,
            'accel_y': 0.0,
            'accel_z': -9.81,
            'gyro_x': 0.0,
            'gyro_y': 0.0,
            'gyro_z': 0.0,
            'mag_x': 0.0,
            'mag_y': 0.0,
            'mag_z': 0.0,
        }
        self._motor_pwm = [1000, 1000, 1000, 1000]
        self._distance = None

    def read_gps(self) -> Dict[str, float]:
        return dict(self._gps)

    def read_imu(self) -> Dict[str, float]:
        return dict(self._imu)

    def set_motor_pwm(self, motor_id: int, pwm_value: int) -> None:
        if motor_id < 0 or motor_id >= 4:
            raise ValueError('motor_id must be between 0 and 3')
        self._motor_pwm[motor_id] = pwm_value

    def read_distance_sensor(self) -> Optional[float]:
        return self._distance

    def arm_motors(self) -> None:
        self._motor_pwm = [1000, 1000, 1000, 1000]

    def disarm_motors(self) -> None:
        self._motor_pwm = [0, 0, 0, 0]

    def set_simulated_distance(self, distance: float) -> None:
        self._distance = distance

    def set_simulated_gps(self, latitude: float, longitude: float, altitude: float = 0.0) -> None:
        self._gps.update({'latitude': latitude, 'longitude': longitude, 'altitude': altitude})

    def set_simulated_imu(self, accel_x: float, accel_y: float, accel_z: float, gyro_x: float = 0.0, gyro_y: float = 0.0, gyro_z: float = 0.0) -> None:
        self._imu.update({
            'accel_x': accel_x,
            'accel_y': accel_y,
            'accel_z': accel_z,
            'gyro_x': gyro_x,
            'gyro_y': gyro_y,
            'gyro_z': gyro_z,
        })


class RaspberryPiHAL(FlightControllerHAL):
    """HAL implementation for Raspberry Pi with GPIO and GPS support."""

    def __init__(self, motor_pins: List[int] = [12, 13, 18, 19], gps_host: str = 'localhost', gps_port: int = 2947):
        if not GPIO_AVAILABLE:
            raise ImportError("RPi.GPIO is required for RaspberryPiHAL")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.motor_pins = motor_pins
        self.pwm_objects = []
        for pin in motor_pins:
            GPIO.setup(pin, GPIO.OUT)
            pwm = GPIO.PWM(pin, 400)  # 400 Hz for drone ESCs
            pwm.start(0)
            self.pwm_objects.append(pwm)
        self.gps_connected = False
        if GPS_AVAILABLE:
            try:
                gpsd.connect(host=gps_host, port=gps_port)
                self.gps_connected = True
            except Exception:
                pass

    def read_gps(self) -> Dict[str, float]:
        if self.gps_connected:
            try:
                packet = gpsd.get_current()
                return {
                    'latitude': packet.lat,
                    'longitude': packet.lon,
                    'altitude': packet.alt,
                    'fix_quality': 1 if packet.mode >= 2 else 0
                }
            except Exception:
                pass
        # Fallback to simulated
        return {'latitude': 0.0, 'longitude': 0.0, 'altitude': 0.0, 'fix_quality': 0}

    def read_imu(self) -> Dict[str, float]:
        # Placeholder for IMU, would need additional library like mpu6050
        return {
            'accel_x': 0.0,
            'accel_y': 0.0,
            'accel_z': -9.81,
            'gyro_x': 0.0,
            'gyro_y': 0.0,
            'gyro_z': 0.0,
            'mag_x': 0.0,
            'mag_y': 0.0,
            'mag_z': 0.0,
        }

    def set_motor_pwm(self, motor_id: int, pwm_value: int) -> None:
        if motor_id < 0 or motor_id >= len(self.pwm_objects):
            raise ValueError(f'motor_id must be between 0 and {len(self.pwm_objects)-1}')
        duty_cycle = (pwm_value - 1000) / 10.0  # Convert 1000-2000 to 0-100%
        self.pwm_objects[motor_id].ChangeDutyCycle(duty_cycle)

    def read_distance_sensor(self) -> Optional[float]:
        # Placeholder for ultrasonic sensor
        return None

    def arm_motors(self) -> None:
        for pwm in self.pwm_objects:
            pwm.ChangeDutyCycle(0)

    def disarm_motors(self) -> None:
        for pwm in self.pwm_objects:
            pwm.ChangeDutyCycle(0)

    def cleanup(self) -> None:
        for pwm in self.pwm_objects:
            pwm.stop()
        GPIO.cleanup()
