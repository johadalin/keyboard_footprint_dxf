from ezdxf.addons import r12writer
x_offset = 15.75
y_offset = 15.95

class Hole:
    def __init__(self, x, y, radius, horizontal_wire=False, vertical_wire=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.horizontal_wire = horizontal_wire
        self.vertical_wire = vertical_wire

switch_holes = [
    Hole(0, 0, 2),
    Hole(-5.08, 0, 0.85),
    Hole(5.08, 0, 0.85),
    Hole(2.54, -5.08, 1.35, horizontal_wire=True),
    Hole(-3.54, -2.60, 1.35, vertical_wire=True),
    ]


def draw_cable_footprint_matrix(x_origin, y_origin, x_count, y_count, dxf, horizontal=False, vertical=False):
    channel_width = 1.2

    if horizontal:
        # Find the right hole to target
        horiz_holes = [hole for hole in switch_holes if hole.horizontal_wire==True]
        hole = horiz_holes[0]

        # Draw horizontal rectangles for row wires
        for y_counter in range(y_count):
            # find centre of line coords
            y = y_origin + (y_counter * y_offset) + y_offset/2 + hole.y
            y_start = y - channel_width/2
            y_end = y + channel_width/2
            x_start = x_origin + x_offset/2 + hole.x
            # Override to set channels up to edge
            x_start = x_origin
            x_end = x_origin + ((x_count-1) * x_offset) + x_offset/2 + hole.x

            draw_rectangle(x_start, y_start, (x_end - x_start), (y_end - y_start), dxf)

    if vertical:
        # Find the right hole to target
        vertical_holes = [hole for hole in switch_holes if hole.vertical_wire==True]
        hole = vertical_holes[0]

        # Draw vertical rectangles for column wires
        for x_counter in range(x_count):
            # find centre of line coords
            x = x_origin + (x_counter * x_offset) + x_offset/2 + hole.x
            x_start = x - channel_width/2
            x_end = x + channel_width/2
            y_start = y_origin + y_offset/2 + hole.y
            # Override to set channels up to edge
            y_start = y_origin
            y_end = y_origin + ((y_count-1) * y_offset) + y_offset/2 + hole.y

            draw_rectangle(x_start, y_start, (x_end - x_start), (y_end - y_start), dxf)


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

        # Draw base
        ox = x_count * x_offset + 5
        oy = y_count * y_offset + 5
        draw_matrix(x_count, y_count, ox, oy, dxf, base=True)


def draw_matrix(x_count, y_count, x_origin, y_origin, dxf, base=False):
        matrix = [[((x * x_offset) + x_origin, (y * y_offset) + y_origin) for x in range(x_count)] for y in range(y_count)]
        if not base:
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


#draw_single()
#draw_plates(15,15)
draw_plates(4, 3)

