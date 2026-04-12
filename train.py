import os
from ultralytics import YOLO

def train_model():
    # 1. Load a pretrained model (YOLOv8x is powerful for detection)
    # We use 'yolov8x.pt' as the base to get the best accuracy.
    model_type = "yolov8x.pt"
    print(f"[INFO] Initializing training with {model_type}...")
    
    model = YOLO(model_type)

    # 2. Train the model
    # data: path to your data.yaml
    # epochs: 100 is usually good for fine-tuning
    # imgsz: 640 is standard
    # batch: -1 auto-detects based on your GPU memory
    # device: 0 for GPU, 'cpu' if no GPU
    results = model.train(
        data="data.yaml",
        epochs=100,
        imgsz=640,
        batch=16,          # Adjust based on GPU memory (lower if out of memory)
        patience=20,       # Early stopping if no improvement
        save=True,
        device=0 if os.name == 'nt' else 'cpu', # Auto-detect GPU on Windows
        project="runs/train",
        name="varicose_model",
        exist_ok=True,
        pretrained=True,
        optimizer='AdamW', # Robust optimizer
        lr0=0.01,          # Initial learning rate
    )

    print("[OK] Training complete.")
    
    # 3. Export to best.pt in root for the app
    best_weights = os.path.join("runs", "train", "varicose_model", "weights", "best.pt")
    if os.path.exists(best_weights):
        import shutil
        shutil.copy(best_weights, "best.pt")
        print("[OK] Best weights copied to root as 'best.pt'")

if __name__ == "__main__":
    train_model()
