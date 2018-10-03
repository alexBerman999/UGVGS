from dronekit import connect, VehicleMode

class mav_interface:
    def __init__(self, connection_string):
        print("\nConnecting to vehicle on: %s" % connection_string)
        self.vehicle = connect(connection_string, wait_ready=True)
        self.vehicle.wait_ready('autopilot_version')

    def get_gps_loc(self):
        return [self.vehicle.location.global_frame.lat, self.vehicle.location.global_frame.lon]
    def get_heading(self):
        return self.vehicle.heading
    def get_altitude(self):
        return self.vehicle.location.global_relative_frame.alt
    def get_speed(self):
        return self.vehicle.groundspeed
    def get_battery_status(self):
        return self.vehicle.battery
