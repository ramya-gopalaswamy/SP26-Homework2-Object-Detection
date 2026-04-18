#!/usr/bin/env python3
import csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

CSV='experiment_table.csv'
OUT='runs/plots/experiment_map_for_user.png'
if not os.path.exists(CSV):
    raise SystemExit('CSV not found')
names=[]; m50=[]; m5095=[]
with open(CSV,newline='') as f:
    r=csv.DictReader(f)
    for row in r:
        names.append(row['Experiment'])
        m50.append(float(row['mAP50']))
        m5095.append(float(row['mAP50-95']))
print('Experiments:', names)
if not os.path.exists('runs/plots'):
    os.makedirs('runs/plots')
fig,ax=plt.subplots(figsize=(max(10,len(names)*1.0),6))
x=range(len(names))
width=0.35
ax.bar([i-width/2 for i in x], m50, width, label='mAP50')
ax.bar([i+width/2 for i in x], m5095, width, label='mAP50-95')
ax.set_xticks(x)
ax.set_xticklabels(names, rotation=40, ha='right')
ax.set_ylim(0,1.0)
ax.legend(loc='upper left')
plt.tight_layout()
plt.savefig(OUT, dpi=200)
print('Wrote', OUT)
