import os
from ultralytics import YOLO

def train_model():
    # 1. Load the existing model to fine-tune it
    model_type = "best.pt"
    print(f"[INFO] Initializing training with {model_type}...")
    
    model = YOLO(model_type)

    # 2. Train the model
    # data: path to your data.yaml
    # epochs: 100 is usually good for fine-tuning
    # imgsz: 640 is standard
    # batch: 8 to ensure it runs accurately without memory issues
    # device: 0 for GPU, 'cpu' if no GPU
    results = model.train(
        data="data.yaml",
        epochs=100,
        imgsz=640,
        batch=8,           # Lower batch size for stability
        patience=20,       # Early stopping if no improvement
        save=True,
        project="runs/train",
        name="varicose_model",
        exist_ok=True,
        pretrained=True,
        optimizer='AdamW', # Robust optimizer
        lr0=0.001,         # Lower initial learning rate for accurate fine-tuning
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
