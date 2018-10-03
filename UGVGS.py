from tkinter import *
from unitconverter import Converter
from ugvutil import Mission_Param, Point, Polygon, UGV, read_lat_long, create_mission

"""
    UGVGS tkinter application
"""
class Application(Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()
        self.converter = Converter()
        self.mission = create_mission(self.converter, "file/border.txt", "file/wp.txt")
        self.ugv = UGV()
        self.create_widgets()
        self.draw_map()
        self.update_telem()

    def draw_map(self):
        self.draw_background("BLACK")

        if self.mission == None:
            return
        bounds = self.mission.bounding_rect()
        border, zoom_rat = self.graphical_consts(bounds, self.map)
        rel_orig = bounds[0]

        self.draw_poly(self.mission.bounds, rel_orig, zoom_rat, border, "RED")
        self.draw_circle(self.mission.drop_point, self.converter.feetToMeters(5), rel_orig, zoom_rat, border, "GREEN")
        self.draw_circle(self.mission.drop_point, self.converter.feetToMeters(25), rel_orig, zoom_rat, border, "YELLOW")
        self.draw_circle(self.mission.drop_point, self.converter.feetToMeters(75), rel_orig, zoom_rat, border, "ORANGE")
        self.draw_circle(self.mission.way_point, 5, rel_orig, zoom_rat, border, "BLUE")
        ugvloc = self.ugv.location
        ugvloc = Point(self.converter.degreesLongToMeters(ugvloc[1]), self.converter.degreesLatToMeters(ugvloc[0]))
        self.draw_circle(ugvloc, 5, rel_orig, zoom_rat, border, "PURPLE")
    
    """
        Updates mission telemetry including location, speed in mph, speed in
        knots, altitude, and heading all rounded to 5 digits
    """
    def update_telem(self):
        ugv_speed_mph = self.converter.metersPerSecondToMPH(self.ugv.speed)
        round_dig = 5
        r_loc = [round(self.ugv.location[0], round_dig), round(self.ugv.location[1], round_dig)]
        r_speed_mph = round(ugv_speed_mph, round_dig)
        r_speed_knt = round(self.converter.metersPerSecondToKnots(self.ugv.speed), round_dig)
        r_altitude = round(self.converter.metersToFeet(self.ugv.altitude), round_dig)
        r_heading = round(self.ugv.heading, round_dig)
        
        if self.ugv.connected:
            self.connection_label["text"] = "Connection: Active"
            self.connection_label["fg"] = "BLACK"
        else:
            self.connection_label["text"] = "Connection: Lost"
            self.connection_label["fg"] = "RED"
        self.location_label["text"] = "Location: " + str(r_loc)
        ugvloc = Point(self.converter.degreesLongToMeters(self.ugv.location[1]), self.converter.degreesLatToMeters(self.ugv.location[0]))
        if not self.mission.bounds.point_in_poly(ugvloc):
            self.location_label["fg"] = "RED"
        else:
            self.location_label["fg"] = "BLACK"
        
        self.speed_label_mph["text"] = "Speed: " + str(r_speed_mph) + " MPH" #But why tho?
        self.speed_label_knt["text"] = "Speed: " + str(r_speed_knt) + " Knots" #But why tho?
        if ugv_speed_mph >= 10:
            self.speed_label_mph["fg"] = "RED"
            self.speed_label_knt["fg"] = "RED"
        else:
            self.speed_label_mph["fg"] = "BLACK"
            self.speed_label_knt["fg"] = "BLACK"
        
        self.altitude_label["text"] = "Altitude: " + str(r_altitude) + " FT"
        
        self.heading_label["text"] = "Heading: " + str( r_heading) + " Degrees"
    
    """ 
        Creates GUI widgets. Produces an abort button and a canvas for the
        mission map.
    """
    def create_widgets(self):
        self.winfo_toplevel().title("UGV Ground Station")
        self["padx"] = 16
        self["pady"] = 16
        
        #Set Mission Parameters Button
        self.abort_button = Button(self)
        self.abort_button["text"] = "ABORT"
        self.abort_button["command"] = self.abort
        self.abort_button["bg"] = "RED"
        self.abort_button.pack(side = "top")
	
        #Telemetry
        self.telem_frame = Frame(self)
        self.telem_frame.pack(side = "right")

        #UGV Air Telemetry
        self.air_telem_frame = Frame(self.telem_frame)
        self.air_telem_frame["bd"] = 5
        self.air_telem_frame["relief"] = "ridge"
        self.air_telem_frame.pack(side = "top")

        self.air_telem_label = Label(self.air_telem_frame)
        self.air_telem_label.pack(side = "top")
        self.air_telem_label["text"] = "Air Telemetry"

        self.altitude_label = Label(self.air_telem_frame)
        self.altitude_label.pack(side = "top")
	
        
        #UGV Ground Telemetry
        self.ground_telem_frame = Frame(self.telem_frame)
        self.ground_telem_frame["bd"] = 5
        self.ground_telem_frame["relief"] = "ridge"
        self.ground_telem_frame.pack(side = "top")
        
        self.ground_telem_label = Label(self.ground_telem_frame)
        self.ground_telem_label.pack(side = "top")
        self.ground_telem_label["text"] = "Ground Telemetry"
        
        self.connection_label = Label(self.ground_telem_frame)
        self.connection_label.pack(side = "top")

        self.location_label = Label(self.ground_telem_frame)
        self.location_label.pack(side = "top")
        
        self.speed_label_mph = Label(self.ground_telem_frame)
        self.speed_label_mph.pack(side = "top")
        
        self.speed_label_knt = Label(self.ground_telem_frame)
        self.speed_label_knt.pack(side = "top")
        
        self.heading_label = Label(self.ground_telem_frame)
        self.heading_label.pack(side = "top")

        #Canvas
        self.canv_default_width = 300
        self.canv_default_height = 600
        self.map = Canvas(self, width = self.canv_default_width, height = self.canv_default_height)
        self.map.pack(side = "right")
        self.draw_background("BLACK")
    
    """
        Converts metric coordinates to the graphical coordinate system. P is the
        point whose coordinates are to be converted. top_left specifies the top
        left point of the graphical coordinate system (its origin). zoom_rat
        specifies the zoom of the graphics. border specifies the margin of the
        map elements from the edge of the canvas.
    """
    def conv_meters_graphics(self, p, top_left, zoom_rat, border):
        return [(p[0] - top_left[0]) * -zoom_rat + border, (p[1] - top_left[1]) * -zoom_rat + border]

    """
        Determines the graphical constants for a certain map. Let a be the
        returned array. a[0] is the border (margin offset from the edge of the
        canvas to the map elements). a[1] is the zoom ratio required to fit the
        map in the canvas with the specified border value.
    """
    def graphical_consts(self, bounds, map):
        width = abs(bounds[1][0] - bounds[0][0])
        height = abs(bounds[1][1] - bounds[0][1])
        top_left = bounds[0]
        c_w = self.canv_default_width
        c_h = self.canv_default_height
        border = c_w * 0.04 if c_w <= c_h else c_h * 0.04#how far in to draw map
        w_zoom_rat = (c_w - (border * 2)) / width
        h_zoom_rat = (c_h - (border * 2)) / height
        zoom_rat = w_zoom_rat if w_zoom_rat <= h_zoom_rat else h_zoom_rat
        return [border, zoom_rat]

    """
        Draws a polygon object. Consecutive vertices form the edges of the
        polygon. The rel_orig is the origin of the graphical coordinate system.
        The zoom_rat is the zoom ratio. The border determines the graphics
        offset from the edge of the canvas. The color determines the polygon's
        color.
    """
    def draw_poly(self, poly, rel_orig, zoom_rat, border, color):
        for i in range(1, len(poly.vertices) + 1):
            p = poly.vertices[i - 1]
            q = poly.vertices[i % (len(poly.vertices))]
            self.draw_line(p, q, rel_orig, zoom_rat, border, color)

    """
        Draws a line between two point objects. The rel_orig is the origin of
        the graphical coordinate system. The zoom_rat is the zoom ratio. The
        border determines the graphics offset from the edge of the canvas. 
        The color determines the line's color.
    """
    def draw_line(self, p, q, rel_orig, zoom_rat, border, color):
        p = self.conv_meters_graphics([p.x, p.y], rel_orig, zoom_rat, border)
        q = self.conv_meters_graphics([q.x, q.y], rel_orig, zoom_rat, border)
        self.map.create_line(p[0], p[1], q[0], q[1], fill = color)

    """
        Draws a circle of radius r around a point object. The rel_orig is the
        origin of the graphical coordinate system. The zoom_rat is the zoom
        ratio. The border determines the graphics offset from the edge of the
        canvas. The color determines the circle's color.
    """
    def draw_circle(self, p, radius, rel_orig, zoom_rat, border, color):
        p = self.conv_meters_graphics([p.x, p.y], rel_orig, zoom_rat, border)
        radius = radius
        self.map.create_oval(p[0] - radius, p[1] - radius, p[0] + radius, p[1] + radius, outline = color)

    """
        Fills the canvas with the specified color
    """
    def draw_background(self, color):
        self.map.create_rectangle(0, 0, self.canv_default_width, self.canv_default_height, fill = color)
    
    """
        Initiates abort procedure. Throttle is cut to zero.
    """
    def abort(self):
        self.ugv.abort()
    
root = Tk()
ugvgs = Application(master = root)
ugvgs.mainloop()
