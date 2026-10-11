import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

# 1. Set up A4 paper size in millimeters
a4_w, a4_h = 210, 297

# Create the figure with A4 physical ratio and 600 DPI resolution
fig = plt.figure(figsize=(a4_w / 25.4, a4_h / 25.4), dpi=600)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, a4_w)
ax.set_ylim(0, a4_h)
ax.axis('off')

# 2. Chessboard Grid Specification (enlarged to fill A4)
sq_size = 20 # Each square enlarged to 20 mm (2 cm)
rows, cols = 8, 8
grid_w = cols * sq_size
grid_h = rows * sq_size

# Center point of the A4 paper
cx, cy = a4_w / 2, a4_h / 2

# 3. Draw the Black Margin
margin = 15 # Black margin width = 15 mm
marker_w = grid_w + 2 * margin
marker_h = grid_h + 2 * margin

ax.add_patch(Rectangle(
    (cx - marker_w/2, cy - marker_h/2), 
    marker_w, marker_h, 
    facecolor='black', edgecolor='none'
))

# 4. Draw the 8x8 Chessboard Grid
start_x = cx - grid_w / 2
start_y = cy - grid_h / 2

for r in range(rows):
    for c in range(cols):
        color = 'white' if (r + c) % 2 == 0 else 'black'
        ax.add_patch(Rectangle(
            (start_x + c * sq_size, start_y + r * sq_size), 
            sq_size, sq_size, 
            facecolor=color, edgecolor='none'
        ))

# 5. Add Marker Circles (proportional to the square)
# Circle radius = 1/4 of the square size (so diameter = 1/2 the square size)
radius = sq_size / 4 

def get_center(r, c):
    return (start_x + c * sq_size + sq_size / 2, 
            start_y + r * sq_size + sq_size / 2)

# Origin Circle (Row 3, Column 4) 
ax.add_patch(Circle(get_center(3, 4), radius, facecolor='white', edgecolor='none'))

# X-Axis Circle (Row 3, Column 6) 
ax.add_patch(Circle(get_center(3, 6), radius, facecolor='white', edgecolor='none'))

# Y-Axis Circle (Row 4, Column 4) 
ax.add_patch(Circle(get_center(4, 4), radius, facecolor='black', edgecolor='none'))

# 6. Save the Result
plt.savefig('chessboard_marker_A4_Large.pdf', format='pdf')
plt.savefig('chessboard_marker_A4_Large.png', format='png', dpi=600)

plt.close()
print("Successfully created the maximum-size chessboard_marker_A4_Large file!")