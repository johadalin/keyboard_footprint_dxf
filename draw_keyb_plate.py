from ezdxf.addons import r12writer

#with r12writer("quick_and_dirty_dxf_r12.dxf") as dxf:
#    dxf.add_line((0, 0), (17, 23))
#    dxf.add_circle((0, 0), radius=2)
#    dxf.add_arc((0, 0), radius=3, start=0, end=175)
#    dxf.add_solid([(0, 0), (1, 0), (0, 1), (1, 1)])
#    dxf.add_point((1.5, 1.5))


def draw_key_footprint(ox, oy, dxf):
    dxf.add_circle((0 + ox, 0 + oy), radius=2)
    dxf.add_circle((-5.08 + ox, 0 + oy), radius=0.85)
    dxf.add_circle((5.08 + ox, 0 + oy), radius=0.85)

    # Need to adjust these to fit where the pins are. or make them matching ovals
    dxf.add_circle((2.54 + ox, -5.08 + oy), radius=0.75)
    dxf.add_circle((-2.54 + ox, -3.81 + oy), radius=0.75)

with r12writer("test_footprint.dxf") as dxf:
    x_offset = 15.65
    y_offset = 15.85
    for x,y in [(0*x_offset,0*y_offset),(1*x_offset,0*y_offset),(2*x_offset,0*y_offset),
                (0*x_offset,1*y_offset),(1*x_offset,1*y_offset),(2*x_offset,1*y_offset),
                (0*x_offset,2*y_offset),(1*x_offset,2*y_offset),(2*x_offset,2*y_offset),
                ]:
        draw_key_footprint(x, y, dxf)

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

