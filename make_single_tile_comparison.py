#!/usr/bin/env python3
"""
Extract the same single image tile from batch prediction collages and create a clean
side-by-side comparison (Baseline | Final) saved to runs/plots/qualitative_single.png.
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(ROOT, 'runs', 'detect', 'baseline', 'val_batch1_pred.jpg')
FINAL_PATH = os.path.join(ROOT, 'runs', 'detect', 'adamw_test', 'val_batch1_pred.jpg')
OUT_DIR = os.path.join(ROOT, 'runs', 'plots')
OUT_PATH = os.path.join(OUT_DIR, 'qualitative_single.png')

for p in (BASE_PATH, FINAL_PATH):
    if not os.path.exists(p):
        raise SystemExit(f'Missing file: {p}')
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

base = Image.open(BASE_PATH).convert('RGB')
final = Image.open(FINAL_PATH).convert('RGB')
if base.size != final.size:
    print('Warning: baseline and final images have different sizes; proceeding with baseline size')

w, h = base.size
candidates = [(1,1), (2,2), (3,3), (4,4), (5,5)]
selected = None

def tile_variance(im, rows, cols, r_idx, c_idx):
    tw = im.width // cols
    th = im.height // rows
    left = c_idx * tw
    upper = r_idx * th
    box = (left, upper, left+tw, upper+th)
    tile = im.crop(box)
    arr = np.array(tile.convert('L'), dtype=np.float32)
    return arr.var(), tile

# try to find a grid where center tile is not blank
for rows, cols in candidates:
    if w % cols != 0 or h % rows != 0:
        # allow non-exact division but compute tile size via floor
        pass
    r_idx = rows//2
    c_idx = cols//2
    var_b, tile_b = tile_variance(base, rows, cols, r_idx, c_idx)
    var_f, tile_f = tile_variance(final, rows, cols, r_idx, c_idx)
    # require both tiles to have some texture (variance threshold)
    if var_b > 200 and var_f > 200:
        selected = (rows, cols, r_idx, c_idx, tile_b, tile_f)
        break

# fallback: use whole image if no grid found
if selected is None:
    print('No grid detected; using full images for comparison')
    tile_b = base
    tile_f = final
else:
    rows, cols, r_idx, c_idx, tile_b, tile_f = selected
    print(f'Selected grid {rows}x{cols}, tile ({r_idx},{c_idx})')

# Resize tiles to reasonable height
max_h = 800
tile_b = tile_b if tile_b.height <= max_h else tile_b.resize((int(tile_b.width*max_h/tile_b.height), max_h), Image.LANCZOS)
tile_f = tile_f if tile_f.height <= max_h else tile_f.resize((int(tile_f.width*max_h/tile_f.height), max_h), Image.LANCZOS)

padding = 30
caption_area = 100
width = tile_b.width + tile_f.width + padding * 3
height = max(tile_b.height, tile_f.height) + caption_area + padding * 2

canvas = Image.new('RGB', (width, height), color=(255,255,255))
# paste images
x1 = padding
y1 = padding
canvas.paste(tile_b, (x1, y1))
canvas.paste(tile_f, (x1 + tile_b.width + padding, y1))

# draw titles
draw = ImageDraw.Draw(canvas)
try:
    font_title = ImageFont.truetype('/Library/Fonts/Arial.ttf', 22)
    font_caption = ImageFont.truetype('/Library/Fonts/Arial.ttf', 16)
except Exception:
    font_title = ImageFont.load_default()
    font_caption = ImageFont.load_default()

draw.text((x1, 8), 'Baseline (runs/detect/baseline)', fill=(0,0,0), font=font_title)
draw.text((x1 + tile_b.width + padding, 8), 'Final (AdamW) (runs/detect/adamw_test)', fill=(0,0,0), font=font_title)

caption = 'Baseline: missed detections and lower confidence.  Final (AdamW): more objects detected, tighter boxes, higher confidence.'
# wrap caption
words = caption.split()
lines = []
line = ''
for w in words:
    test = (line + ' ' + w).strip()
    bbox = draw.textbbox((0,0), test, font=font_caption)
    if bbox[2]-bbox[0] <= width - 2*padding:
        line = test
    else:
        lines.append(line)
        line = w
if line:
    lines.append(line)

cap_y = y1 + max(tile_b.height, tile_f.height) + 12
for i, ln in enumerate(lines[:3]):
    draw.text((padding, cap_y + i*20), ln, fill=(50,50,50), font=font_caption)

canvas.save(OUT_PATH, dpi=(150,150))
print('Wrote', OUT_PATH)
