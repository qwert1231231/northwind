"""Sensor fusion for GPS and IMU in Hoveryn."""

from typing import Dict, Tuple


class SensorFusion:
    """Combine GPS and IMU data into a stable position estimate."""

    def __init__(self):
        self.position = (0.0, 0.0)
        self.altitude = 0.0
        self.velocity = (0.0, 0.0)
        self.last_timestamp = None

    def estimate_position(self, gps_data: Dict[str, float], imu_data: Dict[str, float], dt: float = 0.02) -> Dict[str, float]:
        """Estimate current position and altitude with a complementary filter.

        Args:
            gps_data: GPS readings with latitude, longitude, altitude
            imu_data: IMU readings with accel and gyro values
            dt: Time delta in seconds

        Returns:
            dict: Estimated state including latitude, longitude, altitude, speed
        """
        gps_lat = gps_data.get('latitude', self.position[0])
        gps_lon = gps_data.get('longitude', self.position[1])
        gps_alt = gps_data.get('altitude', self.altitude)

        accel_x = imu_data.get('accel_x', 0.0)
        accel_y = imu_data.get('accel_y', 0.0)

        vx = self.velocity[0] + accel_x * dt
        vy = self.velocity[1] + accel_y * dt

        alpha = 0.8
        fused_lat = alpha * self.position[0] + (1 - alpha) * gps_lat
        fused_lon = alpha * self.position[1] + (1 - alpha) * gps_lon
        fused_alt = alpha * self.altitude + (1 - alpha) * gps_alt

        self.position = (fused_lat, fused_lon)
        self.altitude = fused_alt
        self.velocity = (vx, vy)

        return {
            'latitude': self.position[0],
            'longitude': self.position[1],
            'altitude': self.altitude,
            'velocity_x': vx,
            'velocity_y': vy,
        }

    def estimate_heading(self, imu_data: Dict[str, float]) -> float:
        """Estimate heading from IMU gyroscope data."""
        gyro_z = imu_data.get('gyro_z', 0.0)
        return gyro_z

    def get_position(self) -> Tuple[float, float]:
        return self.position

    def get_altitude(self) -> float:
        return self.altitude
