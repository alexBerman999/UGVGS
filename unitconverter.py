import math

"""
    A unit converter utility
"""
class Converter():
    def __init__(self, orig = None):
        self.origin = orig

    """
        Set origin for the cartesian coordinate system that
        will be used to convert latitude and longitude to metric units.
        All metric coordinates will be expressed as distances in meters from
        this point.
    """
    def set_orig(self, orig):
        self.origin = orig

    """
        Converts degrees latitude to meters. This conversion finds the east/west
        distance in meters between the supplied point and origin.
    """
    def degreesLatToMeters(self, degrees):
        latR = math.radians(self.origin[0])
        return (degrees - self.origin[0]) * (111132.954 - (559.822 * math.cos(2 * latR)) +	(1.175 * math.cos(4 * latR)) - (0.0023 * math.cos(6 * latR)))

    """
        Converts degrees longitude to meters. This conversion finds the
        north/south distance in meters between the supplied point and origin.
    """
    def degreesLongToMeters(self, degrees):
        latR = math.radians(self.origin[0])
        return (degrees - self.origin[1]) * (111132.954 * math.cos(latR))
    
    """
        Converts meters to degrees latitude. This conversion finds the point
        meters to the east/west of the origin.
    """
    def metersToDegreesLat(self, meters):
	    latR = math.radians(self.origin[0])
	    return (meters / (111132.954 - (559.822 * math.cos(2 * latR)) + (1.175 * math.cos(4 * latR)) - (0.0023 * math.cos(6 * latR)))) + self.origin[0]
    
    """
        Converts meters to degrees longitude. This conversion finds the point
        meters to the north/south of the origin.
    """
    def metersToDegreesLong(self, meters):
        latR = math.radians(self.origin[0])
        return (meters / (111132.954 * math.cos(latR))) + self.origin[1]

    """
        Converts feet to meters by multiplying by 0.3048.
    """
    def feetToMeters(self, feet):
        return feet * 0.3048

    """
        Converts meters to feet by dividing by 0.3048.
    """
    def metersToFeet(self, meters):
        return meters / 0.3048
    
    """
        Converts meters per second to miles per hour by multiplying by 2.23694.
    """
    def metersPerSecondToMPH(self, metersPerSecond):
        return metersPerSecond * 2.23694
    
    """
        Converts miles per hour to meters per second by dividing by 2.23694.
    """ 
    def mPHToMetersPerSecond(self, mph):
        return mph / 2.23694
    
    
    """
        Converts meters per second to knots by multiplying by 1.94384.
    """
    def metersPerSecondToKnots(self, metersPerSecond):
        return metersPerSecond * 1.94384
    
    """
        Converts knots to meters per second by dividing by 1.94384.
    """
    def knotsToMetersPerSecond(self, knots):
        return knots / 1.94384

