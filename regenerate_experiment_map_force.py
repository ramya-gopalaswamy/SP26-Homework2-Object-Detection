#!/usr/bin/env python3
import csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

CSV='experiment_table.csv'
OUT='runs/plots/experiment_map_with_adamw_test_explicit.png'
if not os.path.exists(CSV):
    raise SystemExit('CSV not found')

names=[]; m50=[]; m5095=[]
with open(CSV,newline='') as f:
    r=csv.DictReader(f)
    for row in r:
        names.append(row['Experiment'])
        try:
            m50.append(float(row['mAP50']))
        except:
            m50.append(float('nan'))
        try:
            m5095.append(float(row['mAP50-95']))
        except:
            m5095.append(float('nan'))

print('Read experiments:', names)

if not os.path.exists('runs/plots'):
    os.makedirs('runs/plots')

fig,ax=plt.subplots(figsize=(max(10,len(names)*1.0),6))
idx = list(range(len(names)))
width=0.35
ax.bar([i-width/2 for i in idx], m50, width, label='mAP50', color='#2b8cbe')
ax.bar([i+width/2 for i in idx], m5095, width, label='mAP50-95', color='#f03b20')
ax.set_xticks(idx)
ax.set_xticklabels(names, rotation=40, ha='right')
ax.set_ylim(0,1.0)
ax.set_ylabel('mAP')
ax.set_title('Experiment mAP50 and mAP50-95')
ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5))
plt.tight_layout(rect=(0,0,0.85,1))
plt.savefig(OUT, dpi=200)
print('Wrote', OUT)
