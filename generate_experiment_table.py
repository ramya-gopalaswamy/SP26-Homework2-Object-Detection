#!/usr/bin/env python3
"""
Generate a comparison table (markdown and CSV) for experiments stored in runs/detect/*
Specifically extracts: experiment name, epochs, img size, final mAP50, final mAP50-95
Usage: python generate_experiment_table.py
Outputs: prints markdown table and writes `experiment_table.md` and `experiment_table.csv` in the repo root.
"""
import csv
import os
import sys
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
RUNS_DIR = os.path.join(ROOT, 'runs', 'detect')

# Map desired display names to run folder names
EXPERIMENT_MAP = {
    'Baseline': 'baseline',
    'Epochs50': 'epochs50',
    'Img800': 'img800',
    'Final': 'final_combined',
}


def read_args_yaml(path):
    # Simple parser: look for lines 'epochs:' and 'imgsz:' and return ints if present
    epochs = ''
    imgsz = ''
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('epochs:'):
                    parts = line.split(':', 1)
                    epochs = parts[1].strip()
                if line.startswith('imgsz:'):
                    parts = line.split(':', 1)
                    imgsz = parts[1].strip()
    except FileNotFoundError:
        pass
    return epochs, imgsz


def read_results_csv(path):
    # Read CSV and return final values for metrics/ mAP columns
    if not os.path.exists(path):
        return '', ''
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        if len(rows) < 2:
            return '', ''
        header = rows[0]
        # find indices for metrics columns
        def idx(colname):
            try:
                return header.index(colname)
            except ValueError:
                return None
        mAP50_idx = idx('metrics/mAP50(B)')
        mAP5095_idx = idx('metrics/mAP50-95(B)')
        # find last non-empty metric row (iterate from bottom)
        for r in reversed(rows[1:]):
            if (mAP50_idx is not None and mAP50_idx < len(r) and r[mAP50_idx] != '') or \
               (mAP5095_idx is not None and mAP5095_idx < len(r) and r[mAP5095_idx] != ''):
                mAP50 = r[mAP50_idx] if (mAP50_idx is not None and mAP50_idx < len(r)) else ''
                mAP5095 = r[mAP5095_idx] if (mAP5095_idx is not None and mAP5095_idx < len(r)) else ''
                return mAP50, mAP5095
    return '', ''


def main():
    rows = []
    for display_name, folder in EXPERIMENT_MAP.items():
        folder_path = os.path.join(RUNS_DIR, folder)
        args_path = os.path.join(folder_path, 'args.yaml')
        results_path = os.path.join(folder_path, 'results.csv')
        epochs, imgsz = read_args_yaml(args_path)
        mAP50, mAP5095 = read_results_csv(results_path)
        # Normalize numbers
        epochs = epochs or ''
        imgsz = imgsz or ''
        mAP50 = mAP50 or ''
        mAP5095 = mAP5095 or ''
        rows.append((display_name, epochs, imgsz, mAP50, mAP5095))

    # Write markdown
    md_lines = []
    md_lines.append('| Experiment | Epochs | Img Size | mAP50 | mAP50-95 |')
    md_lines.append('|---|---:|---:|---:|---:|')
    for r in rows:
        md_lines.append(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |')
    md = '\n'.join(md_lines) + '\n'

    md_path = os.path.join(ROOT, 'experiment_table.md')
    with open(md_path, 'w') as f:
        f.write(md)

    # Write CSV
    csv_path = os.path.join(ROOT, 'experiment_table.csv')
    with open(csv_path, 'w', newline='') as cf:
        w = csv.writer(cf)
        w.writerow(['Experiment', 'Epochs', 'ImgSize', 'mAP50', 'mAP50-95'])
        for r in rows:
            w.writerow(r)

    print('Wrote', md_path)
    print('\nMarkdown table:\n')
    print(md)


if __name__ == '__main__':
    main()
