#!/usr/bin/env python3
"""
Demo script for Northwind Drone Library
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import northwind

def main():
    print("Northwind Drone Library Demo")
    print("=" * 30)

    # Navigation demo
    print("\n1. Navigation:")
    northwind.set_target_coordinate(37.7749, -122.4194)  # San Francisco
    route = northwind.plan_flight_path((0.0, 0.0), (37.7749, -122.4194))
    position = northwind.refresh_position()

    # Obstacle handling demo
    print("\n2. Obstacle Handling:")
    obstacle_detected = northwind.scan_for_obstacle({'distance': 5.0})
    if obstacle_detected:
        northwind.execute_avoidance('left')
        northwind.reroute_path()

    # Stability demo
    print("\n3. Stability:")
    northwind.correct_gps_drift((0.001, -0.002))
    northwind.adjust_altitude({'speed': 20, 'direction': 'N'})
    northwind.engage_hover_hold()

    # Mission control demo
    print("\n4. Mission Control:")
    northwind.start_mission()
    northwind.pause_mission()
    northwind.return_home()

    # Short mission API demo
    print("\n7. Short mission API:")
    drone = northwind.Drone()
    drone.fly([(0.0, 0.0), (37.7749, -122.4194)])
    drone.home()

    # Decision logic demo
    print("\n5. Decision Logic:")
    action = northwind.choose_action('obstacle_detected')
    next_move = northwind.predict_next_move()

    # Data logging demo
    print("\n6. Data Logging:")
    northwind.log_flight_data()
    northwind.export_data()
    northwind.send_to_cloud()

    print("\nDemo completed!")

if __name__ == "__main__":
    main()