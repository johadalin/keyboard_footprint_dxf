from ezdxf.addons import r12writer
import copy

# Thickness of lino is about 3.15mm, so recommended dimensions are:
# layer_one = 4mm mdf (for stiffness. Can be any material or thickness, 
#   but it helps if it has some rigidity, and is opaque so the etches 
#   lines show clearly. THe etches lines will face up, but will not contact
#   paer as the next layer of the acrylic will be on top.)
# layer_two = 2mm clear acrylic (clear so can see through to lines on layer one,
#   acylic so ink wipes clean)
# layer_two (just the central cutout (with circles for corners) = 1.5 mm acrylic.
# layer_three = 2mm clear acrylic (clear so can see through to lines on layer one, 
#   and also to etching lines on underside of itself - should be on the botton as
#   the paper will be on the top side and should be smooth in case the barran rubs it,
#   acylic so ink wipes clean)
#
# This should mean that (ignoring the base), the lino (3mm) will sit on the 
# cutout (1.5mm), to a total height of 4.5mm,
# and the top two layers of the frame (ignoring the base) will add up to 4mm. 
# So the lino should sit 'proud' by 0.5mm.


MM_IN_AN_INCH = 2.54
def inches_to_mm(inches):
    mm = inches*25.4
    return mm


FILE_NAME = "4_inch_printing_frame.dxf"
# Intended lino size (err on the large size - lino must fit in this)
# Note to self - might be fine because  laser cut has width
LINO_WIDTH = inches_to_mm(4)
LINO_HEIGHT = inches_to_mm(4)
# Extra space around lino (the width of the white border)
PAPER_BORDER = inches_to_mm(1)
# Extra gap on top of the paper border, to allow for slightly bigger paper sizes,
# or just a bit of leeway in the frame
EXTRA_SPACE_AROUND_PAPER = inches_to_mm(1)
# Whether to draw the concentric rectangles (spaced 1/8 inch apart) on layer one
# and three
# These help with placement of the paper.
DRAW_ETCHED_PLACEMENT_RECTANGLES = True


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def copy_and_add_additional_offset(self, additional_offset: 'Point'):
        return Point(self.x + additional_offset.x, self.y + additional_offset.y)
    
    def to_tuple(self):
        return (self.x, self.y)


class Circle:
    def __init__(self, radius, offset: Point):
        self.radius = radius
        self.centre_offset = offset
    
    def __repr__(self):
        return f"Circle(radius: {self.radius}, centre: {self.centre_offset})"
    
    def draw_dxf(self, dxf):
        dxf.add_circle(self.centre_offset.to_tuple(), radius=self.radius)
    
    def copy_and_add_additional_offset(self, additional_offset: 'Point'):
        return Circle(radius=self.radius, offset=self.centre_offset.copy_and_add_additional_offset(additional_offset))
    
    def max_x(self):
        return self.centre_offset.x + self.radius

        
class RectangleDimensions:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def __repr__(self):
        return f"({self.width} x {self.height})"

class Rectangle():
    #  Given the height and width of the rectangle, and the offset of the bottom left corner
    def __init__(self, rectangle_dimensions: RectangleDimensions, offset: Point):
        self.offset = offset      
        self.rectangle_dimensions = rectangle_dimensions
        self.corners = self.find_corners()

    def __repr__(self):
        return f"Rectangle({self.rectangle_dimensions}, offset: {self.offset}, corners: {self.corners})"
    
    def find_corners(self):
        corner_one= self.offset
        corner_two = Point(self.offset.x, (self.offset.y + self.rectangle_dimensions.height))
        corner_three = Point((self.offset.x + self.rectangle_dimensions.width), (self.offset.y + self.rectangle_dimensions.height))
        corner_four = Point((self.offset.x + self.rectangle_dimensions.width), self.offset.y)
        return [corner_one, corner_two, corner_three, corner_four]

    def draw_dxf(self, dxf):
        dxf.add_line(self.corners[0].to_tuple(), self.corners[1].to_tuple())
        dxf.add_line(self.corners[1].to_tuple(), self.corners[2].to_tuple())
        dxf.add_line(self.corners[2].to_tuple(), self.corners[3].to_tuple())
        dxf.add_line(self.corners[3].to_tuple(), self.corners[0].to_tuple())# back to origin

    def max_x(self):
        x_values = []
        for corner in self.corners:
            x_values.append(corner.x)
        return max(x_values)
    
    def copy_and_add_additional_offset(self, additional_offset: Point):
        return Rectangle(self.rectangle_dimensions, self.offset.copy_and_add_additional_offset(additional_offset))

class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
    
    def __repr__(self):
            return f"Line({self.start} to {self.end})"

    def draw_dxf(self, dxf):
        dxf.add_line(self.start.to_tuple(), self.end.to_tuple())
    
    def max_x(self):
        return max(self.start.x, self.end.x)
    
    def copy_and_add_additional_offset(self, additional_offset: Point):
        return Line(self.start.copy_and_add_additional_offset(additional_offset),
             self.end.copy_and_add_additional_offset(additional_offset))


# The real world objects that define the size I can make the frame
class RealWorldObjects:
    def __init__(self, lino_width, lino_height,
                 paper_border=inches_to_mm(0.5),
                 registration_pin_width=inches_to_mm(1.125),
                 registration_pin_height=inches_to_mm(2.125)):
        # The rectangle that represents the piece of lino I'll be printing from
        self.lino = RectangleDimensions(width=lino_width, height=lino_height)

        # The rectangle that represents the paper I'll be printing onto.
        # It is determined by the size of the lino print to go in it, and the 
        # size of the border I want around the print
        _paper_width = self.lino.width + (2* paper_border)
        _paper_height = self.lino.height + (2* paper_border)
        self.paper = RectangleDimensions(width=_paper_width, height=_paper_height)

        # The rectangle that represents the ternes registrations pins   
        self.registration_pin = RectangleDimensions(width=registration_pin_width, height=registration_pin_height)


def create_layers_for_printing_without_offset_between_layers(
        real_world_objects: RealWorldObjects,
        extra_space_around_paper=inches_to_mm(1),
        circle_radius_for_cutout_corner_circles=inches_to_mm(1/16),
        extra_vertical_leeway_around_hinge_layer_three=inches_to_mm(1/8),
        extra_leeway_around_cutout_layer_three=inches_to_mm(1/8),
        hinge_size=inches_to_mm(1),
        draw_etched_placement_rectangles = True
        ):

    _base_rectangle = Rectangle(
        RectangleDimensions(
            # Extra space around paper is *2 as it's on both sides
            width=real_world_objects.paper.width + (2*extra_space_around_paper),
            height=(
                real_world_objects.paper.height + 
                (2*extra_space_around_paper) + 
                # Want to be able to place the pin on the movable top piece (or the stationary section),                         
                # # with a bit of extra leeway given for the laser cut lines
                ((real_world_objects.registration_pin.height + extra_vertical_leeway_around_hinge_layer_three + hinge_size))
            )   
        ),
        # The baselayer (layer one) is just the total size, so no offset needed
        Point(0,0)
    )

    # Layer one is the background layer - the total size of the frame
    _layer_one = [copy.deepcopy(_base_rectangle)]

    # The layer to contain the lino - also has a cutout to fit the lino (with little circles on the corners for better fit)
    _layer_two_base = copy.deepcopy(_base_rectangle)
    _layer_two_cutout = Rectangle(
        RectangleDimensions(
            width=real_world_objects.lino.width,
            height=real_world_objects.lino.height
        ),
        Point(
            x=(_layer_two_base.rectangle_dimensions.width-real_world_objects.lino.width)/2,
            # Same as x offset so the cutout is the same dstance from the sides as it is
            # from the edge of the frame furthest from the hinge
            y=(_layer_two_base.rectangle_dimensions.width-real_world_objects.lino.width)/2
        )
    )
    # _layer_two_circles_on_cutout_corners
    _layer_two_cutout_corner_circles = []
    for corner in _layer_two_cutout.corners:
        _layer_two_cutout_corner_circles.append(Circle(radius=circle_radius_for_cutout_corner_circles, offset=corner))
    _layer_two = [
        _layer_two_base,
        _layer_two_cutout
        ] + _layer_two_cutout_corner_circles

    # The thrid and top layer with a hinge - where the paper goes. 
    # Same outside shape, with an only very slightly larger cutout around the lino
    # (just to keep it from interfering), and a line cut near the top to let it fold.
    _layer_three_base = copy.deepcopy(_base_rectangle)
    # Slightly larger cutout
    _layer_three_cutout = Rectangle(
        RectangleDimensions(
            width= _layer_two_cutout.rectangle_dimensions.width + extra_leeway_around_cutout_layer_three,
            height= _layer_two_cutout.rectangle_dimensions.height + extra_leeway_around_cutout_layer_three
        ),
        Point (
            x=_layer_two_cutout.offset.x - (extra_leeway_around_cutout_layer_three/2),
            y=_layer_two_cutout.offset.y - (extra_leeway_around_cutout_layer_three/2)
        )
    )
    _hinge_line_y_value = _base_rectangle.rectangle_dimensions.height - hinge_size
    _layer_three_hinge_line = Line(
            start=Point(x=0, y=_hinge_line_y_value),
            end= Point(x=_base_rectangle.rectangle_dimensions.width, y= _hinge_line_y_value)
        )
    _layer_three = [
        _layer_three_base,
        _layer_three_cutout,
        _layer_three_hinge_line
    ]

    if draw_etched_placement_rectangles:
        # Measure the size of the etch lines as how much bigger than the cutout in layer three 
        # (for the lino) they are.
        # Use layer three cutout instead of layer two because it's bigger, it's where we'll be 
        # etching some of the rectangles (as well as layer 1), and we want to not run off the
        # edge of the surface
        amount_wider_than_cutout = inches_to_mm(2/8)*2 # Both sides
        # How much bigger to make each etched rectangle than the last
        increments_to_width = inches_to_mm(2/8)*2 # Both sides
        # Minimum distance between biggest etched line and outside edge
        buffer_around_outside_edge = inches_to_mm(1/8) # Each side
        _layer_two_etched_lines =[]
        while (amount_wider_than_cutout + _layer_three_cutout.rectangle_dimensions.width) <= (_base_rectangle.rectangle_dimensions.width - 2*buffer_around_outside_edge):
            etch_lines_width = amount_wider_than_cutout + _layer_three_cutout.rectangle_dimensions.width
            etch_lines_height = amount_wider_than_cutout + _layer_three_cutout.rectangle_dimensions.height
            etch_lines_x_offset = _layer_three_cutout.offset.x - amount_wider_than_cutout/2
            etch_lines_y_offset = _layer_three_cutout.offset.y - amount_wider_than_cutout/2
            
            _layer_two_etched_lines.append(Rectangle(
                RectangleDimensions(width=etch_lines_width, height=etch_lines_height),
                Point(etch_lines_x_offset, etch_lines_y_offset)
            ))
            amount_wider_than_cutout = amount_wider_than_cutout + increments_to_width
        _layer_one.extend(_layer_two_etched_lines)
        _layer_three.extend(_layer_two_etched_lines)

    return [_layer_one, _layer_two, _layer_three]



def main():
    # Most commonly changed variables - change these in the constants up top.
    file_name = FILE_NAME
    real_world_objects = RealWorldObjects(
        lino_width = LINO_WIDTH,
        lino_height = LINO_HEIGHT,
        paper_border = PAPER_BORDER)
    extra_space_around_paper= EXTRA_SPACE_AROUND_PAPER
    
    # Other things which can be tweaked
    tiny_extra_offset_between_layers = inches_to_mm(1/4)    

    printing_frame_split_by_layers= create_layers_for_printing_without_offset_between_layers(
        real_world_objects,
        extra_space_around_paper,
        circle_radius_for_cutout_corner_circles=inches_to_mm(1/16),
        extra_vertical_leeway_around_hinge_layer_three=inches_to_mm(1/8),
        extra_leeway_around_cutout_layer_three=inches_to_mm(1/8),
        hinge_size=inches_to_mm(1),
        draw_etched_placement_rectangles=DRAW_ETCHED_PLACEMENT_RECTANGLES)

    # Add an offset for each layer, and flatten the list of shapes (previously split up by layers) into a list
    printing_frame=[]
    for layer_number, layer in enumerate(printing_frame_split_by_layers):
        # Calculate this layer's offset
        if layer_number == 0:
            x_offset = 0
        else:
            previous_layer = printing_frame_split_by_layers[layer_number-1]
            # Note that this is assuming nothing in the current layer goes to the left of 0. @@@
            max_x_of_everything_in_previous_layer = [shape.max_x() for shape in previous_layer]
            max_width_previous_layer = max(max_x_of_everything_in_previous_layer)
            x_offset = (max_width_previous_layer + tiny_extra_offset_between_layers) * layer_number
        # Add a tiny bit extra so layers don't overlap
        offset = Point(x=x_offset, y= 0)

        # Create a flat list of shapes (not split into layers, with each shape offset by the appropriate amount for its layer)
        for shape in layer:
            printing_frame.append(shape.copy_and_add_additional_offset(offset))
    # Iterate through the list of shapes, writing them to file
    with r12writer(file_name) as dxf:
        for shape in printing_frame:
            shape.draw_dxf(dxf)


main()
