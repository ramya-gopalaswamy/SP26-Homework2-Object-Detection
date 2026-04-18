#!/usr/bin/env python3
"""
Train with AdamW + cosine LR + warmup based on your best run settings.
Usage examples (from repo root):

# dry-run (prints command):
python3 train_improved.py --dry-run

# run training (will execute Ultralytics training command):
python3 train_improved.py --model yolov8n.pt --data coco128.yaml --epochs 50 --imgsz 800 --batch 16 --lr 0.001 --name adamw_cosine --device 0

This script requires the Ultralytics package (pip install ultralytics) and a GPU for reasonable speed.
"""
import argparse
import os
import shlex
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--model', default='yolov8n.pt')
parser.add_argument('--data', default='coco128.yaml')
parser.add_argument('--epochs', type=int, default=50)
parser.add_argument('--imgsz', type=int, default=800)
parser.add_argument('--batch', type=int, default=16)
parser.add_argument('--lr', type=float, default=0.001)
parser.add_argument('--name', default='adamw_cosine')
parser.add_argument('--device', default='0', help='CUDA device id or cpu')
parser.add_argument('--project', default='runs/detect', help='project output dir')
parser.add_argument('--dry-run', action='store_true', help='print command but do not execute')
args = parser.parse_args()

# find ultralytics CLI executable next to the Python interpreter, fallback to module invocation
venv_bin_dir = os.path.dirname(sys.executable)
ultralytics_cli = os.path.join(venv_bin_dir, 'ultralytics')
if not os.path.exists(ultralytics_cli):
    # try platform-specific script name (Windows) or fallback to module
    ultralytics_cli = None
    # use module invocation as fallback

if ultralytics_cli:
    cmd = (
        f"{shlex.quote(ultralytics_cli)} train model={shlex.quote(args.model)}"
        f" data={shlex.quote(args.data)}"
        f" epochs={args.epochs} imgsz={args.imgsz} batch={args.batch}"
        f" optimizer=AdamW lr0={args.lr} cos_lr=true warmup_epochs=3"
        f" amp=true pretrained=true"
        f" name={shlex.quote(args.name)} project={shlex.quote(args.project)} device={shlex.quote(args.device)}"
    )
else:
    # fallback to module invocation
    cmd = (
        f"{shlex.quote(sys.executable)} -m ultralytics.train model={shlex.quote(args.model)}"
        f" data={shlex.quote(args.data)}"
        f" epochs={args.epochs} imgsz={args.imgsz} batch={args.batch}"
        f" optimizer=AdamW lr0={args.lr} cos_lr=true warmup_epochs=3"
        f" amp=true pretrained=true"
        f" name={shlex.quote(args.name)} project={shlex.quote(args.project)} device={shlex.quote(args.device)}"
    )

print('Training command:')
print(cmd)

if args.dry_run:
    print('\nDry run - not executing')
else:
    print('\nStarting training...')
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print('Training command failed with exit code', e.returncode)
        print('Command stderr/stdout above — common cause: ultralytics not installed in this Python interpreter.')
        raise