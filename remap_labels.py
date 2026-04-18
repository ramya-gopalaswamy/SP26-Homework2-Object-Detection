#!/usr/bin/env python3
"""
Remap YOLO-format class ids in label .txt files according to a mapping.
Usage:
    python3 remap_labels.py --label-dir exported_dataset/labels

This will overwrite the label files in-place. Make a backup if needed.
"""
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--label-dir', type=str, default='exported_dataset/labels', help='Directory containing .txt label files')
args = parser.parse_args()

label_dir = args.label_dir

# mapping from old_class -> new_class
mapping = {
    0: 0,    # person
    1: 39,   # bottle
    2: 56,   # chair
    3: 63    # laptop
}

if not os.path.isdir(label_dir):
    print(f'Label directory not found: {label_dir}')
    raise SystemExit(1)

for file in os.listdir(label_dir):
    if file.endswith('.txt'):
        path = os.path.join(label_dir, file)

        with open(path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                continue

            old_class = int(parts[0])
            if old_class not in mapping:
                print(f'Warning: old class {old_class} not in mapping for file {file}; skipping line')
                continue

            new_class = mapping[old_class]
            parts[0] = str(new_class)
            new_lines.append(' '.join(parts))

        with open(path, 'w') as f:
            f.write('\n'.join(new_lines))

print('Remapping complete.')
