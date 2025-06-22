import logging
from ultralytics import YOLO
from typing import List

# Set ultralytics logging level to WARNING to suppress inference output
logging.getLogger("ultralytics").setLevel(logging.WARNING)

# Load YOLO model (recommended to execute once during module load)
yolo_model = YOLO("yolov8n.pt")

def returntype(image_path: str) -> List[str]:
    """
    Use YOLO model to detect object types in the given image.

    Args:
        image_path (str): Path to the image file

    Returns:
        list[str]: List of detected object class names
    """
    results = yolo_model(image_path)
    if not results or not results[0].boxes:
        return []

    detected_labels = list(set([
        yolo_model.names[int(cls)]
        for cls in results[0].boxes.cls
    ]))
    return detected_labels
