# CV/ImageRecognition.py

import logging
from ultralytics import YOLO
from typing import List

# 设置 ultralytics 的日志等级为 WARNING，避免输出模型推理过程
logging.getLogger("ultralytics").setLevel(logging.WARNING)
# 加载模型（建议放在模块加载时执行一次）
yolo_model = YOLO("yolov8n.pt")

def returntype(image_path: str) -> List[str]:
    """
    使用 YOLO 模型识别图像中包含的物体类型。
    参数:
        image_path (str): 图片文件路径
    返回:
        list[str]: 识别到的物体类别名称列表
    """
    results = yolo_model(image_path)
    if not results or not results[0].boxes:
        return []

    detected_labels = list(set([
        yolo_model.names[int(cls)]
        for cls in results[0].boxes.cls
    ]))
    return detected_labels
