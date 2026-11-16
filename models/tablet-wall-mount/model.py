"""Wall mount for Samsung Galaxy Tab A11, landscape, USB-C port on the right.

Two parts: `plate` (screws to the wall, holds the tablet in a rim) and `cover` (front frame,
held by 4 split press-fit pins, no fasteners). Cable goes through a slot in the plate and out
a channel on the back. Remove the tablet by prying the cover off.
Concept after "Samsung Galaxy Tab A11 Wall Mount" by Maakloods (Printables 1501242, CC BY-NC-SA 4.0).
Orientation: rotate the tablet so the USB-C port is on the right; the power/volume buttons end up on top.
"""
from math import hypot, sqrt

from build123d import Align, Box, Cone, Cylinder, Pos, RegularPolygon, Rot, extrude

# --- parameters (mm) ---
tab_w, tab_h, tab_t = 211.0, 124.7, 8.0  # Tab A11, landscape
clr = 0.4          # clearance per side
rim_t = 2.5        # rim wall thickness
plate_t = 5.0      # back plate thickness
cover_t = 3.0      # front cover thickness
lip = 6.0          # how much of the screen bezel the cover overlaps
m = 16.0           # margin from the tablet pocket to the outer edge (screws, cable slot)
btn_x0, btn_x1 = 15.0, 65.0  # button zone on the top edge, measured from the left tablet edge - VERIFY
rcam_x, rcam_top, rcam_d = 19.5, 15.45, 16.0  # rear camera hole (from the reference plate): from the left tablet edge, from the top edge, diameter
cam_len = 26.0      # front camera cutout in the left lip, centered on the left edge - VERIFY
btn_depth = 3.0     # cover strip kept past the tablet's top edge; the cutout opens from there to the outer edge
port_off = 0.0     # USB-C offset from the center of the right edge (+ up) - VERIFY
port_gap = 22.0    # rim opening height for the plug
groove_w, groove_d = 7.0, 3.0  # cable channel on the back
slot_w = 9.0
hex_r, hex_rib, hex_edge = 13.0, 3.0, 5.0  # lightening hex cutouts: cell radius, rib width, border kept around the pocket
hex_r_side, hex_rib_side = 4.5, 2.5  # smaller hexes for the strip right of the tablet
wall_screw, wall_head = 4.2, 8.6  # countersunk wall screws
hole_d, hole_depth, boss_d = 4.2, 8.0, 10.0  # pin sockets in the plate bosses
pin_d, pin_l, pin_slit = 4.4, 7.0, 1.0       # cover pins; tune pin_d for a snug fit

# --- derived ---
inner_w, inner_h = tab_w + 2 * clr, tab_h + 2 * clr
rim_h = tab_t + 2 * clr
PW, PH = inner_w + 2 * m, inner_h + 2 * m
right = m + inner_w                # x of the pocket's right edge
top = m + inner_h                  # y of the pocket's top edge
port_y = m + inner_h / 2 + port_off
corners = [(8, 8), (PW - 8, 8), (8, PH - 8), (PW - 8, PH - 8)]

MIN = (Align.MIN, Align.MIN, Align.MIN)
CEN = (Align.CENTER, Align.CENTER, Align.MIN)


def box(x0, y0, z0, x1, y1, z1):
    return Pos(x0, y0, z0) * Box(x1 - x0, y1 - y0, z1 - z0, align=MIN)


# --- plate (z=0 is the wall side, print as-is) ---
plate = box(0, 0, 0, PW, PH, plate_t)
plate += box(m - rim_t, m - rim_t, plate_t, right + rim_t, top + rim_t, plate_t + rim_h) \
    - box(m, m, plate_t - 1, right, top, plate_t + rim_h + 1)       # rim around the tablet
for x, y in corners:
    plate += Pos(x, y, plate_t) * Cylinder(boss_d / 2, rim_h, align=CEN)   # cover pin bosses
    plate -= Pos(x, y, plate_t + rim_h - hole_depth) * Cylinder(hole_d / 2, hole_depth + 1, align=CEN)
plate -= box(right - 1, port_y - port_gap / 2, plate_t, right + rim_t + 1, port_y + port_gap / 2, plate_t + rim_h + 1)  # plug opening
plate -= box(m + btn_x0, top - 1, plate_t, m + btn_x1, top + rim_t + 1, plate_t + rim_h + 1)  # button access
slot_x = right + rim_t + 2 + slot_w / 2
rcam_cx, rcam_cy = m + clr + rcam_x, top - clr - rcam_top
plate -= box(slot_x - slot_w / 2, port_y - slot_w / 2, -1, slot_x + slot_w / 2, port_y + slot_w / 2, plate_t + 1)
plate -= box(slot_x, port_y - groove_w / 2, -1, PW + 1, port_y + groove_w / 2, groove_d)
for fx in (0.25, 0.75):
    for y in (8, PH - 8):
        p = Pos(PW * fx, y, 0)
        plate -= p * Cylinder(wall_screw / 2, plate_t, align=CEN)
        plate -= p * Pos(0, 0, plate_t - (wall_head - wall_screw) / 2) * Cone(wall_screw / 2, wall_head / 2, (wall_head - wall_screw) / 2, align=CEN)

# lightening: hex grids through the plate
def hex_fill(x0, x1, y0, y1, r, rib):
    global plate
    pitch, apo, col, cx = sqrt(3) * r + rib, sqrt(3) / 2 * r, 0, x0 + r
    while cx + r <= x1:
        cy = y0 + apo + (pitch / 2 if col % 2 else 0)
        while cy + apo <= y1:
            if hypot(cx - rcam_cx, cy - rcam_cy) >= rcam_d / 2 + r + rib:   # keep clear of the camera hole
                plate -= Pos(cx, cy, -1) * extrude(RegularPolygon(r, 6), plate_t + 2)
            cy += pitch
        cx += pitch * sqrt(3) / 2
        col += 1


plate -= Pos(rcam_cx, rcam_cy, -1) * Cylinder(rcam_d / 2, plate_t + 2, align=CEN)   # rear camera
hex_fill(m + hex_edge, right - hex_edge, m + hex_edge, top - hex_edge, hex_r, hex_rib)  # under the tablet
sx0, sx1 = right + rim_t + 1.5, PW - 1.5                  # strip to the right of the tablet
sy = slot_w / 2 + groove_w / 2 + 2                        # keep clear of the cable slot/channel
hex_fill(sx0, sx1, 8 + boss_d / 2 + 3, port_y - sy, hex_r_side, hex_rib_side)   # below the cable
hex_fill(sx0, sx1, port_y + sy, PH - 8 - boss_d / 2 - 3, hex_r_side, hex_rib_side)  # above the cable

# --- cover (built outer face up, then flipped: outer face on the bed, pins up) ---
cover = box(0, 0, 0, PW, PH, cover_t)
cover -= box(m + lip, m + lip, -1, right - lip, top - lip, cover_t + 1)                   # screen window
cover -= box(m + btn_x0, top + btn_depth, -1, m + btn_x1, PH + 1, cover_t + 1)                    # button access
cover -= box(m, m + inner_h / 2 - cam_len / 2, -1, m + lip + 1, m + inner_h / 2 + cam_len / 2, cover_t + 1)  # front camera
for x, y in corners:   # split pins on the underside
    cover += Pos(x, y, -pin_l) * Cylinder(pin_d / 2, pin_l, align=CEN) \
        - box(x - pin_d, y - pin_slit / 2, -pin_l - 1, x + pin_d, y + pin_slit / 2, -1.5)
cover = Pos(0, PH, cover_t) * Rot(180, 0, 0) * cover

parts = {"plate": plate, "cover": cover}
