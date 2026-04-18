# 2D Object Detection Training Optimization (YOLOv8)

## 📌 Overview

This project focuses on improving the training process of a 2D object detection model using YOLOv8. The objective is to evaluate how different training strategies affect detection performance and identify configurations that improve accuracy.

Experiments were conducted using the COCO128 dataset, along with a custom annotated dataset to further enhance performance. See SP26 Homework2 Object Detection.docx for detailed analysis

---

## 🧠 Approach

The project follows a structured experimental pipeline:

1. Train a baseline YOLOv8 model
2. Apply controlled training strategy modifications
3. Evaluate performance using COCO-style metrics
4. Compare results across experiments
5. Analyze improvements and optimization strategies

---

## ⚙️ Baseline Setup

- Model: YOLOv8n (pretrained)
- Dataset: COCO128
- Epochs: 30
- Image Size: 640
- Optimizer: Default (SGD-based)

---

## 🚀 Training Strategy Improvements

### 1. Increased Training Duration
- Epochs: 30 → 50

### 2. Increased Image Resolution
- Image Size: 640 → 800

### 3. Combined Strategy
- Epochs = 50, Image Size = 800

### 4. Custom Annotated Dataset
- Added ~60 manually labeled images

### 5. Optimizer Modification (AdamW - Untuned)
- Resulted in performance degradation

### 6. Advanced Optimization (AdamW + Cosine + Warmup)
- Achieved best performance

---

## 📊 Results

| Experiment | Epochs | Img Size | Optimizer | mAP@0.5 | mAP@0.5:0.95 |
|-----------|-------:|---------:|-----------|--------:|-------------:|
| Baseline | 30 | 640 | Default | 0.795 | 0.622 |
| Epochs50 | 50 | 640 | Default | 0.841 | 0.660 |
| Img800 | 30 | 800 | Default | 0.820 | 0.636 |
| Final | 50 | 800 | Default | 0.852 | 0.674 |
| Combined_custom | 50 | 800 | Default | 0.874 | 0.699 |
| AdamW_test | 50 | 800 | AdamW | 0.598 | 0.404 |
| AdamW_cosine | 50 | 800 | AdamW + Cosine | **0.907** | **0.725** |

---

## 📈 Key Findings

- Increasing epochs provided the largest improvement
- Higher image resolution improved localization accuracy
- Combining strategies yielded better results
- Custom data improved generalization
- AdamW alone degraded performance
- Properly tuned AdamW achieved the best results

---

## 🧪 How to Run

### Baseline Training
```
yolo detect train model=yolov8n.pt data=coco128.yaml epochs=30 imgsz=640 name=baseline
```

### Improved Training
```
yolo detect train model=yolov8n.pt data=coco128.yaml epochs=50 imgsz=800 name=final
```

### Advanced Optimization
```
python train_improved.py --model yolov8n.pt --data coco128.yaml --epochs 50 --imgsz 800 --batch 16 --lr 0.001 --name adamw_cosine
```

---

## 📂 Project Structure

```
Object_Detection_hw2/
├── datasets/
│   └── coco128/
├── runs/
│   └── detect/
├── custom_data/
│   ├── images/
│   ├── labels/
├── train_improved.py
├── README.md
└── report.docx
```

---

## 🏁 Conclusion

Training optimization significantly improves object detection performance. Combining multiple strategies and properly tuning advanced optimization techniques leads to the best results.

---

## 👩‍💻 Author

Ramya G
