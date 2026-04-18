#!/usr/bin/env python3
"""
Read `experiment_table.csv` and create a grouped bar chart for mAP50 and mAP50-95.
Saves image to `runs/plots/experiment_map.png`.
"""
import csv
import os
import math
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(ROOT, 'experiment_table.csv')
OUT_DIR = os.path.join(ROOT, 'runs', 'plots')
OUT_PATH = os.path.join(OUT_DIR, 'experiment_map.png')

if not os.path.exists(CSV_PATH):
    raise SystemExit(f'CSV file not found: {CSV_PATH}')

names = []
mAP50 = []
mAP5095 = []

with open(CSV_PATH, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        names.append(row['Experiment'])
        try:
            mAP50.append(float(row['mAP50']))
        except Exception:
            mAP50.append(float('nan'))
        try:
            mAP5095.append(float(row['mAP50-95']))
        except Exception:
            mAP5095.append(float('nan'))

# debug: print experiments loaded
print('Loaded experiments from CSV:', names)

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

x = list(range(len(names)))
width = 0.35

# Cap figure width so we don't create extremely large images that viewers can't open
max_fig_width = 24  # inches
fig_width = max(10, min(max_fig_width, len(names) * 1.1))
fig_height = 6
fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.bar([i - width/2 for i in x], mAP50, width, label='mAP50', color='#2b8cbe')
ax.bar([i + width/2 for i in x], mAP5095, width, label='mAP50-95', color='#f03b20')

ax.set_xticks(x)
# compute rotation and bottom margin based on label length and count
max_label_len = max((len(n) for n in names), default=0)
if len(names) > 12 or max_label_len > 18:
    rotation = 60
    ha = 'right'
else:
    rotation = 35
    ha = 'right'
ax.set_xticklabels(names, rotation=rotation, ha=ha)
ax.set_ylabel('mAP')
ax.set_ylim(0, 1.0)
ax.set_title('Experiment mAP50 and mAP50-95')
# place legend inside plot to avoid cutting off bars on the right
ax.legend(loc='upper right', frameon=False)

# annotate values
for i, (a, b) in enumerate(zip(mAP50, mAP5095)):
    if not math.isnan(a):
        ax.text(i - width/2, a + 0.01, f'{a:.3f}', ha='center', va='bottom', fontsize=8)
    if not math.isnan(b):
        ax.text(i + width/2, b + 0.01, f'{b:.3f}', ha='center', va='bottom', fontsize=8)

# dynamic bottom margin so long labels don't get cut off
bottom_margin = 0.28 + min(0.25, 0.01 * max_label_len) + (0.015 * max(0, len(names) - 8))
# relax right margin so bars aren't clipped
plt.subplots_adjust(bottom=bottom_margin, right=0.95)

# Ensure layout fits
fig.tight_layout()
# Avoid bbox_inches='tight' which can expand the image to include out-of-bounds artists
# Use a conservative DPI so image dimensions stay reasonable for viewers
save_dpi = 150
print('Plotting experiments:', names)
print('Saving to', OUT_PATH, 'with dpi', save_dpi)
plt.savefig(OUT_PATH, dpi=save_dpi, bbox_inches='tight', pad_inches=0.12)
print('Wrote', OUT_PATH)
