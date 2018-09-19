"""
    Represents  mission parameters which include the mission bounds, drop point,
    and waypoint.
"""
class Mission_Param():
    def __init__(self, bnds, drp, wp):
        self.bounds = bnds
        self.drop_point = drp
        self.way_point = wp

    """
        Returns north west and south east points of bounding rectangle.
    """
    def bounding_rect(self):
        east = self.bounds.vertices[0].x
        west = self.bounds.vertices[0].x
        north = self.bounds.vertices[0].y
        south = self.bounds.vertices[0].y
        for point in self.bounds.vertices:
            #Assuming North-West semihemisphere
            if point.x > west:
                west = point.x
            if point.x < east:
                east = point.x
            if point.y > north:
                north = point.y
            if point.y < south:
                south = point.y
        return [[west, north], [east, south]]

"""
    Represents a point on a 2d plane.
"""
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

"""
    Represents a point on a 3d plane.
"""
class Point3D():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

"""
    Represents a polygon defined by its vertices. Consecutive vertices form the
    edges of the polygon.
"""
class Polygon():
    def __init__(self, points):
        self.vertices = points
    
    """
        Determines whether a point is within the polygon. This is determined by
        counting how many times a ray going away from a point intersects the
        edges of the polygon. An odd number of intersections means the point is
        within the polygon. An even number means the point is outside the
        polygon.
    """
    def point_in_poly(self, point):
        collisions = 0
        x,y = point.x, point.y
        xPrime = x + 10000
        yPrime = y + 10000
        for i in range(1, len(self.vertices) + 1):
            a = self.vertices[i - 1].x
            b = self.vertices[i - 1].y
            c = self.vertices[i % len(self.vertices)].x
            d = self.vertices[i % len(self.vertices)].y
            slope_orig = (yPrime - y) / (xPrime - x)
            if c == a:
                slope_edge = 1
            else:
                slope_edge = (d - b)/(c - a)
            if slope_orig != slope_edge:
                f = y - (slope_orig * x)
                g = b - (slope_edge * a)
                x_intersection = (g - f) / (slope_orig - slope_edge)
                y_intersection = (slope_orig * x_intersection) + f
                if x_intersection >= min(x, xPrime) and x_intersection <= max(x, xPrime):
                    if y_intersection >= min(y, yPrime) and y_intersection <= max(y, yPrime):
                        if x_intersection >= min(a, c) and x_intersection <= max(a, c):
                            if y_intersection >= min(b, d) and y_intersection <= max(b, d):
                                collisions = collisions + 1
        return collisions % 2 == 1

"""
    Represents an unmanned ground vehicle. Recieves information on location,
    speed, altitude, and heading
"""
class UGV():
    def __init__(self):
        self.connected = True
        self.location = [38.14600, -76.42640]
        self.speed = 5
        self.altitude = 50
        self.heading = 90
    
    """
        Updates UGV telemetry values
    """
    def update(self):
        #todo: stuff
        print("updating")
    
    """
        Sends an abort signal to the UGV
    """
    def abort(self):
        #todo: stuff
        print("aborting")
    

"""
    Reads a file containing latitude and longitude pairs seperated by whitespace
    and returns an array of Point objects in the order specified in the file.
"""
def read_lat_long(file, conv):
    f = open(file, "r")
    data = f.read()
    f.close()
    file_chunks = data.split()
    data_ll = []
    for i in range(0, len(file_chunks), 2):
        data_ll.append([float(file_chunks[i]),float(file_chunks[i + 1])])
    if conv.origin == None:
        conv.origin = data_ll[0]
    data_met = []
    for i in range(len(data_ll)):
        data_met.append([conv.degreesLongToMeters(data_ll[i][1]), conv.degreesLatToMeters(data_ll[i][0])])
    for i in range(len(data_met)):
        data_met[i] = Point(data_met[i][0], data_met[i][1])
    return data_met

"""
    Creates a mission to be drawn on the ground station map from a specified
    border and waypoint file. The border file is to be a list of the
    border's vertices in decimal degrees latitude and longitude. The
    waypoint file is to be the coordinates of the drop point and the
    destination waypoint in decimal degrees latitude and longitude.
"""
def create_mission(conv, border_file, wp_file):
    border = Polygon(read_lat_long(border_file, conv))
    wps = read_lat_long(wp_file, conv)
    return Mission_Param(border, wps[0], wps[1])
