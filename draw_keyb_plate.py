from ezdxf.addons import r12writer

def draw_cable_footprint_matrix(ox, oy, x_offset, y_offset, num_rows, num_cols, dxf):
    channel_width = 1
    # Draw horizontal rectangles for row wires
    for row_counter in range(num_rows):
        draw_rectangle(-2.54, (row_counter * y_offset) - 5.08 - channel_width/2, (num_cols - 1) * x_offset, channel_width, dxf)

    # Draw vertical rectangles for column wires
    for col_counter in range(num_cols):
        draw_rectangle((col_counter * x_offset) + 3.54 - channel_width/2, -2.60, channel_width, (num_rows - 1) * y_offset, dxf)

def draw_key_footprint(ox, oy, dxf):
    dxf.add_circle((0 + ox, 0 + oy), radius=2)
    dxf.add_circle((-5.08 + ox, 0 + oy), radius=0.85)
    dxf.add_circle((5.08 + ox, 0 + oy), radius=0.85)

    # Need to adjust these to fit where the pins are. or make them matching ovals
    dxf.add_circle((2.54 + ox, -5.08 + oy), radius=0.75)
    dxf.add_circle((-3.54 + ox, -2.60 + oy), radius=0.75)

    # Add wider circle around pads for engraving
    dxf.add_circle((2.54 + ox, -5.08 + oy), radius=1.25)
    dxf.add_circle((-3.54 + ox, -2.60 + oy), radius=1.25)



def draw_rectangle(ox, oy, x, y, dxf):
    dxf.add_line((ox,oy),(ox,oy+y))
    dxf.add_line((ox,oy+y),(ox+x,oy+y))
    dxf.add_line((ox+x,oy+y),(ox+x,oy))
    dxf.add_line((ox+x,oy),(ox,oy))



def draw_matrix():
    with r12writer("test_footprint.dxf") as dxf:
        x_offset = 15.65
        y_offset = 15.85
        for x,y in [(0*x_offset,0*y_offset),(1*x_offset,0*y_offset),(2*x_offset,0*y_offset),
                    (0*x_offset,1*y_offset),(1*x_offset,1*y_offset),(2*x_offset,1*y_offset),
                    (0*x_offset,2*y_offset),(1*x_offset,2*y_offset),(2*x_offset,2*y_offset),
                    ]:
            draw_key_footprint(x, y, dxf)
        draw_rectangle(-x_offset/2,-y_offset/2,x_offset*3, y_offset*3,dxf)

        # draw_cable_footprint_matrix(-x_offset/2, -y_offset/2, x_offset, y_offset, 3, 3, dxf)

def draw_single():
    with r12writer("test_footprint.dxf") as dxf:
        x_offset = 15.65
        y_offset = 15.85
        draw_key_footprint(x_offset/2, y_offset/2, dxf)
        draw_rectangle(0, 0, x_offset, y_offset, dxf)


draw_single()
#draw_matrix()


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

