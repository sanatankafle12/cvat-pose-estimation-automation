
import io
import base64
import json
import cv2
import numpy as np
from ultralytics import YOLO

# Initialize your model
def init_context(context):
    context.logger.info('Initializing YOLOv8 pose estimation model...  0%')
    model = YOLO('YOUR-MODEL-NAME')  # Load the YOLOv8 pose estimation model (adjust model path as necessary)
    context.user_data.model_handler = model
    context.logger.info('YOLOv8 pose estimation model initialized...100%')

# Inference endpoint
def handler(context, event):
    context.logger.info('Running pose estimation on input image using YOLOv8 model')

    # Decode the input image from base64
    data = event.body
    image_buffer = io.BytesIO(base64.b64decode(data['image']))
    image = cv2.imdecode(np.frombuffer(image_buffer.getvalue(), np.uint8), cv2.IMREAD_COLOR)

    # Perform inference using the YOLOv8 model
    results = context.user_data.model_handler(image)
    result = results[0]

    # Extract bounding boxes, keypoints, confidences, and class labels
    boxes = result.boxes.data[:, :4]  # Extract the bounding boxes
    keypoints = result.keypoints.data[:, :, :2]  # Extract the keypoints (x, y coordinates)
    confs = result.boxes.conf         # Extract the confidence scores for each person detected
    clss = result.boxes.cls           # Extract the class indices (typically 'person')
    class_names = result.names        # Class names dictionary

    detections = []
    threshold = 0.1  # Confidence threshold for filtering detections

    for box, keypoint_set, conf, cls in zip(boxes, keypoints, confs, clss):
        label = class_names[int(cls)]
        keypoints_list = keypoint_set.tolist()  # Convert keypoints to list format
        # Format detection result as a dictionary
    elements = []
    for index, key_points in enumerate(keypoints_list, start=1):
        elements.append({
            'confidence': '0.9',
            'label': str(index),
            # 'points': box.tolist(),
            # 'outside':0,
            "points": [
                    float(key_points[0]),
                    float(key_points[1])
                ],
            'type': 'points',  # Indicate that this is a pose estimation
        })
    skeleton = [{
        'confidence': '0.9',
        'label': class_names[int(cls)],
        'type': 'skeleton',
        'elements' : elements,
    }]
    context.logger.info(f"skeleton:{skeleton}")
    # Return the detection results as a JSON response
    return context.Response(body=json.dumps(skeleton), headers={}, content_type='application/json', status_code=200)
