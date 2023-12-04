from ezdxf.addons import r12writer
import copy

# Measurements are in cm, unless stated as in inches

# x_offset = 15.75
# y_offset = 15.95

# class Hole:
#     def __init__(self, x, y, radius, horizontal_wire=False, vertical_wire=False):
#         self.x = x
#         self.y = y
#         self.radius = radius
#         self.horizontal_wire = horizontal_wire
#         self.vertical_wire = vertical_wire

# switch_holes = [
#     Hole(0, 0, 2),
#     Hole(-5.08, 0, 0.85),
#     Hole(5.08, 0, 0.85),
#     Hole(2.54, -5.08, 1.25, horizontal_wire=True),
#     Hole(-3.54, -2.60, 1.25, vertical_wire=True),
#     ]
CM_IN_AN_INCH = 2.54
def inches_to_cm(inches):
    cm = inches*2.54
    return cm


# The real world objects that define the size I can make the frame
class RealWorldObjects:
    # # The rectangle that represents the piece of lino I'll be printing from
    # class Lino(Rectangle):
    #     def __init__(self, width, height):
    #         super().__init__(width, height)
        
    # # The rectangle that represents the paper I'll be printing onto.
    # # It is determined by the size of the lino print to go in it, and the 
    # # size of the border I want around the print
    # class Paper(Rectangle):
    #     def __init__(self, lino_width, lino_height, paper_border):
    #         # The size of the paper is defined by the size of the lino,
    #         # and how much blank paper we want around it as a border
    #         width = lino_width + (2* paper_border)
    #         height = lino_height + (2* paper_border)
    #         super().__init(width, height)

    # # The rectangle that represents the ternes registrations pins
    # class RegistrationPin(Rectangle):
    #     def __init__(self):
    #         # Since these are bought, they don't change, so just use their measurements
    #         width = inches_to_cm(1.125)
    #         height = inches_to_cm(2.125)
    #         super().__init__(width, height)


    def __init__(self, lino_width_inches, lino_height_inches,
                 paper_border_inches=0.5):
        self.lino = dict(width=inches_to_cm(lino_width_inches), height=inches_to_cm(lino_height_inches))

        _paper_width = self.lino.width + (2* inches_to_cm(paper_border_inches))
        _paper_height = self.lino.height + (2* inches_to_cm(paper_border_inches))
        self.paper = dict(width=_paper_width, height=_paper_height)

        self.registration_pin = dict(width=inches_to_cm(1.125), height=inches_to_cm(2.125))

        # self.Lino(inches_to_cm(lino_width_inches), inches_to_cm(lino_height_inches))
        # self.paper = self.Paper(self.lino.max_height, self.lino.max_width, inches_to_cm(paper_border_inches))
        # self.registration_pin = self.RegistrationPin()


class Rectangle:
    def __init__(self, width, height, x_offset, y_offset):
        self.width = width
        self.height = height
        self.x_offset = x_offset
        self.y_offset = y_offset

class Line:
    def __init__(self, x_start_position,  y_start_position, x_end_position, y_end_position):

        

class PrintingFrame:
    def __init__(self, real_word_objects, extra_space_around_paper_inches=2):
        _extra_space_around_paper=inches_to_cm(extra_space_around_paper_inches)
        _extra_vertical_leeway_around_hinge=inches_to_cm(1/8)
        _extra_leeway_around_cutout_layer_three=inches_to_cm(1/8)

        # The baselayer (layer one) is just the total size, so no offset needed
        _layer_one_rectangle = self._find_layer_one_rectangle(
            real_word_objects, 
            _extra_space_around_paper, 
            _extra_vertical_leeway_around_hinge)
        self.layer_one = [_layer_one_rectangle]

        # The layer to contain the lino - same as the base layer, but with a hole the size of the lino
        _layer_two_cutout = Rectangle(
                width=real_word_objects.real_world_objects.lino['width'],
                height=real_word_objects.real_world_objects.lino['height'],
                x_offset=(_layer_one_rectangle.width-real_word_objects.real_world_objects.lino['width'])/2,
                # Same as x offset
                y_offset=(_layer_one_rectangle.width-real_word_objects.real_world_objects.lino['width'])/2
            )
        self.layer_two = [
            _layer_one_rectangle,
            _layer_two_cutout
        ]

        # The top layer with a hinge - where the paper goes. Same outside shape, with an only very slightly larger cutout around the lino
        # (just to keep it from interfering), and a line cut near the top to let it fold.
        _layer_three_cutout = copy.deepcopy(_layer_two_cutout)
        _layer_three_cutout.width += _extra_leeway_around_cutout_layer_three
        _layer_three_cutout.height += _extra_leeway_around_cutout_layer_three
        _layer_three_cutout.x_offset += (_extra_leeway_around_cutout_layer_three/2)
        _layer_three_cutout.y_offset += (_extra_leeway_around_cutout_layer_three/2)

        self.layer_three = [
            _layer_one_rectangle,
            _layer_three_cutout,
            Line(x_start_position=0,
                 y_start_position=(_layer_one_rectangle.height - (real_word_objects.registration_pin['height'] + _extra_vertical_leeway_around_hinges)),
                 x_end_position=_layer_one_rectangle.width,
                 # Same as start position
                 y_end_position=(_layer_one_rectangle.height - (real_word_objects.registration_pin['height'] + _extra_vertical_leeway_around_hinges))
            )
        ]

    def _find_layer_one_rectangle(real_world_objects, extra_space_around_paper, extra_vertical_leeway_around_hinge):
        width = real_world_objects.paper['width'] + (2*extra_space_around_paper)
        height = (
            real_world_objects.paper['height'] + 
            (2*extra_space_around_paper) + 
            # Want to be able to place the pin on the movable top piece (or the stationary section), 
            # with a bit of extra leeway given for the laser cut lines
            (2*(real_world_objects.registration_pin['height'] + extra_vertical_leeway_around_hinge))
        )
        return Rectangle(width=width, height=height, x_offset=0, y_offset=0)

    def draw(self):



def main():
    # @@@ Change any of the numbers here
    real_world_objects = RealWorldObjects(
        lino_width_inches=2,
        lino_height_inches=2,
        paper_border_inches=0.5)
    printing_frame=PrintingFrame(real_world_objects, extra_space_around_paper_inches=2)
    # @@@ Change the filename
    with r12writer("test_printing_frame.dxf") as dxf:
        printing_frame.draw()


def draw_key_footprint(ox, oy, dxf):
    # Move the origin to the centre of a footprint
    ox = ox + x_offset/2
    oy = oy + y_offset/2

    for hole in switch_holes:
        dxf.add_circle((ox + hole.x, oy + hole.y), radius=hole.radius)


def draw_rectangle(ox, oy, x, y, dxf):
    dxf.add_line((ox,oy),(ox,oy+y))
    dxf.add_line((ox,oy+y),(ox+x,oy+y))
    dxf.add_line((ox+x,oy+y),(ox+x,oy))
    dxf.add_line((ox+x,oy),(ox,oy))


def draw_plates(x_count, y_count):
    with r12writer("test_bigger_footprint.dxf") as dxf:
        # Draw basic plate
        draw_matrix(x_count, y_count, 0, 0, dxf)

        # Draw vertical wire plate
        ox = x_count * x_offset + 5
        oy = 0
        draw_matrix(x_count, y_count, ox, oy, dxf)
        draw_cable_footprint_matrix(ox, oy, x_count, y_count, dxf, vertical=True)

        # Draw horizontal wire plate
        ox = 0
        oy = y_count * y_offset + 5
        draw_matrix(x_count, y_count, ox, oy, dxf)
        draw_cable_footprint_matrix(ox, oy, x_count, y_count, dxf, horizontal=True)


def draw_matrix(x_count, y_count, x_origin, y_origin, dxf):
        matrix = [[((x * x_offset) + x_origin, (y * y_offset) + y_origin) for x in range(x_count)] for y in range(y_count)]
        for row in matrix:
            for x,y in row:
                draw_key_footprint(x, y, dxf)
        # draw_rectangle(-x_offset/2,-y_offset/2,x_offset*x_count, y_offset*y_count,dxf)
        draw_rectangle(x_origin, y_origin, x_offset*x_count, y_offset*y_count, dxf)


def draw_single():
    with r12writer("test_footprint2.dxf") as dxf:
        x_offset = 15.65
        y_offset = 15.85
        draw_key_footprint(x_offset/2, y_offset/2, dxf)
        draw_rectangle(0, 0, x_offset, y_offset, dxf)

def write_dxf(file_name):

def main():
    write_dxf()









  #(pad "" np_thru_hole circle (at 0 0) (size 3.9878 3.9878) (drill 3.9878) (layers *.Cu *.Mask))
  #(pad "" np_thru_hole circle (at -5.08 0) (size 1.7018 1.7018) (drill 1.7018) (layers *.Cu *.Mask))
  #(pad "" np_thru_hole circle (at 5.08 0) (size 1.7018 1.7018) (drill 1.7018) (layers *.Cu *.Mask))
  #(pad 1 thru_hole oval (at -3.255 -3.52 327.5) (size 2.5 4.75) (drill oval 1.5 3.75) (layers *.Cu *.Mask F.SilkS))
  #(pad 2 thru_hole oval (at 2.52 -4.79 356.1) (size 2.5 3.08) (drill oval 1.5 2.08) (layers *.Cu *.Mask F.SilkS))



  #(fp_line (start -6.35 -4.572) (end -6.35 -6.35) (layer F.SilkS) (width 0.381))
  #(fp_line (start -6.35 6.35) (end -6.35 4.572) (layer F.SilkS) (width 0.381))
  #(fp_line (start -4.572 6.35) (end -6.35 6.35) (layer F.SilkS) (width 0.381))
  #(fp_line (start 6.35 6.35) (end 4.572 6.35) (layer F.SilkS) (width 0.381))
  #(fp_line (start 6.35 4.572) (end 6.35 6.35) (layer F.SilkS) (width 0.381))
  #(fp_line (start 6.35 -6.35) (end 6.35 -4.572) (layer F.SilkS) (width 0.381))
  #(fp_line (start 4.572 -6.35) (end 6.35 -6.35) (layer F.SilkS) (width 0.381))
  #(fp_line (start -6.35 -6.35) (end -4.572 -6.35) (layer F.SilkS) (width 0.381))

