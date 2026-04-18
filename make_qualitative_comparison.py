#!/usr/bin/env python3
"""
Create a side-by-side qualitative comparison image from two prediction images.
Saves to `runs/plots/qualitative_comparison.png`.
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(ROOT, 'runs', 'detect', 'baseline', 'val_batch1_pred.jpg')
FINAL = os.path.join(ROOT, 'runs', 'detect', 'adamw_test', 'val_batch1_pred.jpg')
OUT_DIR = os.path.join(ROOT, 'runs', 'plots')
OUT_PATH = os.path.join(OUT_DIR, 'qualitative_comparison.png')

if not os.path.exists(BASE):
    raise SystemExit(f'Baseline image not found: {BASE}')
if not os.path.exists(FINAL):
    raise SystemExit(f'Final image not found: {FINAL}')
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

# open images
im1 = Image.open(BASE).convert('RGB')
im2 = Image.open(FINAL).convert('RGB')

# resize so heights match (but keep not too large)
max_height = max(im1.height, im2.height)
# cap height to 800 px for portability
cap_height = min(max_height, 800)

def scale_to_height(im, h):
    if im.height == h:
        return im
    w = int(im.width * (h / im.height))
    return im.resize((w, h), Image.LANCZOS)

im1 = scale_to_height(im1, cap_height)
im2 = scale_to_height(im2, cap_height)

padding = 20
caption_area = 90
width = im1.width + im2.width + padding * 3
height = cap_height + caption_area + padding * 2

canvas = Image.new('RGB', (width, height), color=(255, 255, 255))

# paste images
x1 = padding
y1 = padding
canvas.paste(im1, (x1, y1))
x2 = x1 + im1.width + padding
canvas.paste(im2, (x2, y1))

# draw labels and captions
draw = ImageDraw.Draw(canvas)
# try to use a truetype font if available, else default
try:
    font_title = ImageFont.truetype('/Library/Fonts/Arial.ttf', 20)
    font_caption = ImageFont.truetype('/Library/Fonts/Arial.ttf', 16)
except Exception:
    font_title = ImageFont.load_default()
    font_caption = ImageFont.load_default()

# Titles above each image
title_y = 6
draw.text((x1, title_y), 'Baseline (runs/detect/baseline)', fill=(0, 0, 0), font=font_title)
draw.text((x2, title_y), 'Final (AdamW) (runs/detect/adamw_test)', fill=(0, 0, 0), font=font_title)

# Short caption below both images
caption_text = (
    'Baseline: missing objects, loose boxes, lower confidence    |    '
    'Final (AdamW): more objects detected, tighter boxes, higher confidence'
)
# wrap caption if too long
max_caption_width = width - padding * 2
lines = []
words = caption_text.split()
line = ''
for w in words:
    test = (line + ' ' + w).strip()
    # use draw.textbbox to measure width
    bbox = draw.textbbox((0,0), test, font=font_caption)
    tw = bbox[2] - bbox[0]
    if tw <= max_caption_width:
        line = test
    else:
        lines.append(line)
        line = w
if line:
    lines.append(line)

cap_x = padding
cap_y = y1 + cap_height + 12
for i, ln in enumerate(lines[:4]):
    draw.text((cap_x, cap_y + i * 18), ln, fill=(50, 50, 50), font=font_caption)

# draw vertical separator line between images
sep_x = x2 - padding // 2
draw.line([(sep_x, y1), (sep_x, y1 + cap_height)], fill=(200, 200, 200), width=2)

canvas.save(OUT_PATH, dpi=(150,150))
print('Wrote', OUT_PATH)
