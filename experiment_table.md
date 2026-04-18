| Experiment | Epochs | Img Size | mAP50 | mAP50-95 | Precision | Recall |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 30 | 640 | 0.795 | 0.622 | 0.833 | 0.706 |
| Epochs50 | 50 | 640 | 0.841 | 0.660 | 0.8829 | 0.7654 |
| Img800 | 30 | 800 | 0.820 | 0.636 | 0.8066 | 0.7463 |
| Final (50,800) | 50 | 800 | 0.852 | 0.674 | 0.8476 | 0.7777 |
| Combined_custom | 50 | 800 | 0.874 | 0.699 | 0.8948 | 0.7886 |
| AdamW (adamw_cosine) | 50 | 800 | 0.907 | 0.725 | 0.8769 | 0.8375 |

Notes:
- mAP and metrics taken from each run's `results.csv` final epoch.
- `AdamW` row corresponds to `runs/detect/adamw_cosine` (final epoch values).
