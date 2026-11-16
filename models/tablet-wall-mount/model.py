"""Wall mount for Samsung Galaxy Tab A11 (landscape, USB-C port on the right, cable routed behind the plate).

Print back-side down (z=0 is the bed). The tablet slides in from the top and lifts straight out.
"""
from build123d import Align, Cone, Cylinder, Box, Pos

# --- parameters (mm) ---
tab_w, tab_h, tab_t = 211.0, 124.7, 8.0  # Tab A11, landscape
clr = 0.5          # clearance per side
wall = 3.0         # side/bottom wall
plate = 6.0        # back plate thickness
lip = 7.0          # how much of the screen bezel is covered
lip_t = 2.5        # lip thickness
grab = 30.0        # how far the tablet sticks out the top (grip + free access to power/volume buttons)
bay_w = 24.0       # cable area to the right of the tablet
port_off = 0.0     # USB-C offset from the center of the short side (+ up) - VERIFY
port_gap = 22.0    # height of the plug opening
groove_w, groove_d = 7.0, 4.0  # cable channel on the back
screw_d, head_d = 4.2, 8.6

# --- derived ---
inner_w = tab_w + 2 * clr
depth = tab_t + 2 * clr
total_w = 2 * wall + inner_w + bay_w
total_h = wall + tab_h - grab
total_z = plate + depth + lip_t
port_y = wall + tab_h / 2 + port_off
slot_x = 2 * wall + inner_w + bay_w / 2

MIN = (Align.MIN, Align.MIN, Align.MIN)
CEN = (Align.CENTER, Align.CENTER, Align.MIN)


def box(x0, y0, z0, x1, y1, z1):
    return Pos(x0, y0, z0) * Box(x1 - x0, y1 - y0, z1 - z0, align=MIN)


part = box(0, 0, 0, total_w, total_h, plate)                       # back plate
part += box(0, 0, plate, 2 * wall + inner_w, total_h, total_z)     # frame
part -= box(wall, wall, plate, wall + inner_w, total_h + 1, plate + depth)          # pocket, open at the top
part -= box(wall + lip, wall + lip, plate, wall + inner_w - lip, total_h + 1, total_z + 1)  # window
# plug opening through the right wall + slot through the plate to the channel on the back
part -= box(wall + inner_w - 1, port_y - port_gap / 2, plate, total_w, port_y + port_gap / 2, total_z + 1)
part -= box(slot_x - 5, port_y - 4, -1, slot_x + 5, port_y + 4, plate + 1)
part -= box(slot_x, port_y - groove_w / 2, -1, total_w + 1, port_y + groove_w / 2, groove_d)
# 4 countersunk screws (reachable from the front with the tablet removed)
for fx in (0.25, 0.75):
    for fy in (0.25, 0.75):
        p = Pos(wall + inner_w * fx, total_h * fy, 0)
        part -= p * Cylinder(screw_d / 2, plate, align=CEN)
        part -= p * Pos(0, 0, plate - head_d / 2 + screw_d / 2) * Cone(screw_d / 2, head_d / 2, head_d / 2 - screw_d / 2, align=CEN)
