from ezdxf.addons import r12writer
import math

def draw_magnet_circles(centre_x, centre_y, fidget_radius, magnet_count, dxf):
    magnet_radius = 6
    spacing_ratio = 0.67
    magnet_distance = fidget_radius * spacing_ratio

    # Add outer circle
    dxf.add_circle((centre_x, centre_y), radius=fidget_radius)
    # centre circle
    dxf.add_circle((centre_x, centre_y), radius=magnet_radius)

    # radial circles
    for i in range(magnet_count):
        theta = i * 360/magnet_count
        theta = i * ((math.pi*2) / magnet_count)

        x = (magnet_distance * math.cos(theta)) + centre_x
        y = (magnet_distance * math.sin(theta)) + centre_y
        print(f"i {i}, x: {x}, y: {y} - theta {theta}")
        dxf.add_circle((x, y), radius=magnet_radius)


def draw_fidget(magnet_count, radius):
    with r12writer("fidget_circles.dxf") as dxf:
        offset = radius + 5
        print(f"Drawing circles. r{radius}, magnet count {magnet_count}")
        draw_magnet_circles(0, 0, radius, magnet_count, dxf)
        draw_magnet_circles(0, radius + offset, radius, magnet_count, dxf)
        dxf.add_circle((0, 2*(radius + offset)), radius=radius)
        dxf.add_circle((0, 3*(radius + offset)), radius=radius)

        #dxf.add_circle((radius + offset, 0), radius=radius)
        #dxf.add_circle((radius + offset, radius + offset), radius=radius)
        #draw_magnet_circles(radius + offset, 0, radius, magnet_count, dxf)
        #draw_magnet_circles(radius + offset, radius + offset, radius, magnet_count, dxf)

draw_fidget(6, 50)

with r12writer("testfidget.dxf") as f:
    draw_magnet_circles(0, 0, 50, 6, f)


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

