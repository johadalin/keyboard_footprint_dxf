from ezdxf.addons import r12writer
import copy
# TODO:
# add circles to layer two cutout

CM_IN_AN_INCH = 2.54
def inches_to_cm(inches):
    cm = inches*2.54
    return cm


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
    #  Given the height and width of the rectangle, and the offfset of the bottom left corner
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
    def __init__(self, lino_width_inches, lino_height_inches,
                 paper_border_inches=0.5):
        # The rectangle that represents the piece of lino I'll be printing from
        self.lino = RectangleDimensions(width=inches_to_cm(lino_width_inches), height=inches_to_cm(lino_height_inches))

        # The rectangle that represents the paper I'll be printing onto.
        # It is determined by the size of the lino print to go in it, and the 
        # size of the border I want around the print
        _paper_width = self.lino.width + (2* inches_to_cm(paper_border_inches))
        _paper_height = self.lino.height + (2* inches_to_cm(paper_border_inches))
        self.paper = RectangleDimensions(width=_paper_width, height=_paper_height)

        # The rectangle that represents the ternes registrations pins   
        self.registration_pin = RectangleDimensions(width=inches_to_cm(1.125), height=inches_to_cm(2.125))


def create_layers_for_printing_without_offset_between_layers(
        real_world_objects: RealWorldObjects,
        extra_space_around_paper_inches=2,
        circle_radius=inches_to_cm(1/16)):
    _extra_space_around_paper=inches_to_cm(extra_space_around_paper_inches)

    _extra_vertical_leeway_around_hinge_layer_three=inches_to_cm(1/8)
    _extra_leeway_around_cutout_layer_three=inches_to_cm(1/8)

    _base_rectangle = Rectangle(
        RectangleDimensions(
            # Extra space around paper is *2 as it's on both sides
            width=real_world_objects.paper.width + (2*_extra_space_around_paper),
            height=(
                real_world_objects.paper.height + 
                (2*_extra_space_around_paper) + 
                # Want to be able to place the pin on the movable top piece (or the stationary section),                         
                # # with a bit of extra leeway given for the laser cut lines
                (2*(real_world_objects.registration_pin.height + _extra_vertical_leeway_around_hinge_layer_three))
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
        _layer_two_cutout_corner_circles.append(Circle(radius=circle_radius, offset=corner))
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
            width= _layer_two_cutout.rectangle_dimensions.width + _extra_leeway_around_cutout_layer_three,
            height= _layer_two_cutout.rectangle_dimensions.height + _extra_leeway_around_cutout_layer_three
        ),
        Point (
            x=_layer_two_cutout.offset.x - (_extra_leeway_around_cutout_layer_three/2),
            y=_layer_two_cutout.offset.y - (_extra_leeway_around_cutout_layer_three/2)
        )
    )
    _layer_three_hinge_line = Line(
            start=Point(x=0,
                        y=(_base_rectangle.rectangle_dimensions.height - (real_world_objects.registration_pin.height + _extra_vertical_leeway_around_hinge_layer_three))),
            end= Point(x=_base_rectangle.rectangle_dimensions.width,
                        y= (_base_rectangle.rectangle_dimensions.height - (real_world_objects.registration_pin.height + _extra_vertical_leeway_around_hinge_layer_three)))
        )
    _layer_three = [
        _layer_three_base,
        _layer_three_cutout,
        _layer_three_hinge_line
    ]
    return [_layer_one, _layer_two, _layer_three]



def main():
    # @@@ Change any of the numbers here
    real_world_objects = RealWorldObjects(
        lino_width_inches=2,
        lino_height_inches=2,
        paper_border_inches=0.5)
    circle_radius = inches_to_cm(1/16) 
    tiny_extra_offset = inches_to_cm(1/4)
    extra_space_around_paper_inches=2
    file_name = "test_printing_frame.dxf"
    printing_frame_split_by_layers= create_layers_for_printing_without_offset_between_layers(real_world_objects, extra_space_around_paper_inches, circle_radius)
    
    # Add an offset for each layer, and flatten the list of shapes (previously split up by layers) into a list
    printing_frame=[]
    for layer_number, layer in enumerate(printing_frame_split_by_layers):
        # Calculate this layer's offset
        if layer_number == 0:
            x_offset = 0
        else:
            previous_layer = printing_frame_split_by_layers[layer_number-1]
            # Note that this is assuming nothing in the current layer goes to the left of 0.
            max_x_of_everything_in_previous_layer = [shape.max_x() for shape in previous_layer]
            max_width_previous_layer = max(max_x_of_everything_in_previous_layer)
            x_offset = (max_width_previous_layer + tiny_extra_offset) * layer_number
        # Add a tiny bit extra so layers don't overlap
        offset = Point(x=x_offset, y= 0)

        # Create a flat list of shapes (not split into layers, with each shape offset by the appropriate amount for its layer)
        for shape in layer:
            printing_frame.append(shape.copy_and_add_additional_offset(offset))
            print(shape)
    # Iterate through the list of shapes, writing them to file
    with r12writer(file_name) as dxf:
        for shape in printing_frame:
            shape.draw_dxf(dxf)


main()
