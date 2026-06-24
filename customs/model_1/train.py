from pathlib import Path
from ultralytics import YOLO

def train_model()-> None:
    root = Path(__file__).resolve().parent

    data_path = root / "data.yaml"
    model_path = root / 'models' / "yolo26n.pt"

    model = YOLO(str(model_path)) 

    # Train the model
    model.train(
        data=str(data_path),
        epochs=100,
        patience=20, # dừng sớm nếu không cải thiện
        imgsz=640,
        batch=16,
        device='0',  # Use GPU if available
        project=str(root / 'runs' / 'train'),
        name='yolo26n_custom_train',
        exist_ok=True,
        verbose=True,
        seed=42,
        workers=2  # Number of data loading workers
    )

    model.val(
        data=str(data_path), 
        split = 'test',
        project=str(root / 'runs' / 'val'),
        name = 'yolo26n_custom_val', 
        device='0',
        seed=42,
        workers=2)  # Evaluate the model after training


if __name__ == "__main__":
    train_model()