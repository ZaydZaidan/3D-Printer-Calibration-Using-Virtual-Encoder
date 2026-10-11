import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

# 1. Setup Ukuran Kertas A4 dalam milimeter
a4_w, a4_h = 210, 297

# Membuat figure dengan rasio fisik A4 dan resolusi 600 DPI
fig = plt.figure(figsize=(a4_w / 25.4, a4_h / 25.4), dpi=600)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, a4_w)
ax.set_ylim(0, a4_h)
ax.axis('off')

# 2. Spesifikasi Grid Catur (Diperbesar agar memenuhi A4)
sq_size = 20 # Ukuran satu kotak diperbesar menjadi 20 mm (2 cm)
rows, cols = 8, 8
grid_w = cols * sq_size
grid_h = rows * sq_size

# Titik tengah kertas A4
cx, cy = a4_w / 2, a4_h / 2

# 3. Menggambar Margin Hitam
margin = 15 # Lebar margin hitam = 15 mm
marker_w = grid_w + 2 * margin
marker_h = grid_h + 2 * margin

ax.add_patch(Rectangle(
    (cx - marker_w/2, cy - marker_h/2), 
    marker_w, marker_h, 
    facecolor='black', edgecolor='none'
))

# 4. Menggambar Grid Catur 8x8
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

# 5. Menambahkan Lingkaran Penanda (Proporsional dengan kotak)
# Radius lingkaran = 1/4 dari ukuran kotak (berarti diameter = 1/2 ukuran kotak)
radius = sq_size / 4 

def get_center(r, c):
    return (start_x + c * sq_size + sq_size / 2, 
            start_y + r * sq_size + sq_size / 2)

# Lingkaran Origin (Baris 3, Kolom 4) 
ax.add_patch(Circle(get_center(3, 4), radius, facecolor='white', edgecolor='none'))

# Lingkaran Sumbu X (Baris 3, Kolom 6) 
ax.add_patch(Circle(get_center(3, 6), radius, facecolor='white', edgecolor='none'))

# Lingkaran Sumbu Y (Baris 4, Kolom 4) 
ax.add_patch(Circle(get_center(4, 4), radius, facecolor='black', edgecolor='none'))

# 6. Menyimpan Hasil
plt.savefig('chessboard_marker_A4_Large.pdf', format='pdf')
plt.savefig('chessboard_marker_A4_Large.png', format='png', dpi=600)

plt.close()
print("Berhasil membuat file chessboard_marker_A4_Large berukuran maksimal!")