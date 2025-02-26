# import io
# import base64
# import json
# import cv2
# import numpy as np
# from ultralytics import YOLO
# # from PIL import Image
# # import yaml

# # Initialize your model
# def init_context(context):
#     context.logger.info('Initializing YOLOv8 pose estimation model...  0%')
#     model = YOLO('fish_pose_v5k14.pt')  # Load the YOLOv8 pose estimation model (adjust model path as necessary)
#     context.user_data.model_handler = model
#     context.logger.info('YOLOv8 pose estimation model initialized...100%')
# # Inference endpoint
# # def handler(context, event):
# #     context.logger.info('Running pose estimation on input image using YOLOv8 model')
# #     # Decode the input image from base64
# #     data = event.body
# #     context.logger.info(f'data : {data}')
# #     image_buffer = io.BytesIO(base64.b64decode(data['image']))
# #     threshold = data.get('threshold', 0.55)
# #     image = Image.open(image_buffer).convert("RGB")

# #     # image = cv2.imdecode(np.frombuffer(image_buffer.getvalue(), np.uint8), cv2.IMREAD_COLOR)

# #     # Perform inference using the YOLOv8 model
# #     # results = context.user_data.model_handler(image)
# #     # result = results[0]
# #     # context.logger.info(f"results: {results}")

# #     # Extract bounding boxes, keypoints, confidences, and class labels
# #     # boxes = result.boxes.data[:, :4]  # Extract the bounding boxes
# #     # keypoints = result.keypoints.data[:, :, :2]  # Extract the keypoints (x, y coordinates)
# #     # confs = result.boxes.conf         # Extract the confidence scores for each person detected
# #     # clss = result.boxes.cls           # Extract the class indices (typically 'person')
# #     # class_names = result.names        # Class names dictionary

# #     # detections = []
# #     # threshold = 0.1  # Confidence threshold for filtering detections
# #     # context.logger.info(f'keypoints: {keypoints.tolist()}')
# #     # context.logger.info(f'boxes: {boxes}')
# #     # context.logger.info(f'confidence score: {confs}')
# #     # context.logger.info(f'class: {clss}')

# #     # for box, keypoint_set, conf, cls in zip(boxes, keypoints, confs, clss):
# #     #     label = class_names[int(cls)]
# #     #     if conf >= threshold:
# #     #         keypoints_list = keypoint_set.tolist()  # Convert keypoints to list format
# #     #         # Format detection result as a dictionary
# #     #         # one_d_points = [coordinate for sublist in keypoints_list for pair in sublist for coordinate in pair]
# #     #         detections.append({
# #     #             'confidence': str(float(conf)),
# #     #             'label': label,
# #     #             'points': keypoints_list,
# #     #             'type': 'points',  # Indicate that this is a pose estimation
# #     #         })
# #     # Extract bounding boxes, keypoints, confidences, and class labels
# #     # boxes = result.boxes.data[:, :4]  # Extract the bounding boxes
# #     # keypoints = result.keypoints.data[:, :, :2]  # Extract the keypoints (x, y coordinates)
# #     # confs = result.boxes.conf         # Extract the confidence scores for each person detected
# #     # clss = result.boxes.cls           # Extract the class indices (typically 'person')
# #     # class_names = result.names        # Class names dictionary
# #     # detections = []
# #     # one_d_points = [coordinate.item() for sublist in keypoints for pair in sublist for coordinate in pair]
# #     # threshold = 0.1  # Confidence threshold for filtering detections

# #     results = []
# #     image = cv2.imdecode(np.frombuffer(image_buffer.getvalue(), np.uint8), cv2.IMREAD_COLOR)

# #     # Perform inference using the YOLOv8 model
# #     pred_instance = context.user_data.model_handler(image)
# #     context.logger.info(f" pred_instance : {pred_instance}")
# #     # pred_instances = next(context.user_data.inferencer(np.array(image)[...,::-1]))["predictions"][0]
# #     for pred_instance in pred_instance:
# #         keypoints = pred_instance["keypoints"]
# #         keypoint_scores = pred_instance["keypoint_scores"]
# #         for label in context.user_data.labels:
# #             # if label['name'] != 'fish':
# #             #     continue
# #             skeleton = {
# #                 "confidence": str(pred_instance["bbox_score"]),
# #                 "label": 'fish',
# #                 "type": "skeleton",
# #                 "elements": [{
# #                     "label": element['name'],
# #                     "type": "points",
# #                     "outside": 0 if threshold < keypoint_scores[element["id"]] else 1,
# #                     "points": [
# #                         float(keypoints[element["id"]][0]),
# #                         float(keypoints[element["id"]][1])
# #                     ],
# #                     "confidence": str(keypoint_scores[element["id"]]),
# #                 } for element in label["sublabels"]],
# #             }

# #             if not all([element['outside'] for element in skeleton["elements"]]):
# #                 results.append(skeleton)

# #     # Return the detection results as a JSON response
# #     return context.Response(body=json.dumps(results), headers={}, content_type="application/json", status_code=200)


# def handler(context, event):
#     context.logger.info('Running pose estimation on input image using YOLOv8 model')

#     # Decode the input image from base64
#     data = event.body
#     image_buffer = io.BytesIO(base64.b64decode(data['image']))
#     image = cv2.imdecode(np.frombuffer(image_buffer.getvalue(), np.uint8), cv2.IMREAD_COLOR)

#     # Perform inference using the YOLOv8 model
#     results = context.user_data.model_handler(image)
#     result = results[0]

#     # Extract bounding boxes, keypoints, confidences, and class labels
#     boxes = result.boxes.data[:, :4]  # Extract the bounding boxes
#     keypoints = result.keypoints.data[:, :, :2]  # Extract the keypoints (x, y coordinates)
#     confs = result.boxes.conf         # Extract the confidence scores for each person detected
#     clss = result.boxes.cls           # Extract the class indices (typically 'person')
#     class_names = result.names        # Class names dictionary

#     detections = []
#     threshold = 0.1  # Confidence threshold for filtering detections

#     for box, keypoint_set, conf, cls in zip(boxes, keypoints, confs, clss):
#         label = class_names[int(cls)]
#         if conf >= threshold:
#             keypoints_list = keypoint_set.tolist()  # Convert keypoints to list format
#             # Format detection result as a dictionary
#             detections.append({
#                 'confidence': str(float(conf)),
#                 'label': label,
#                 'points': box.tolist(),
#                 'keypoints': keypoints_list,
#                 'type': 'pose',  # Indicate that this is a pose estimation
#             })

#     # Return the detection results as a JSON response
#     return context.Response(body=json.dumps(detections), headers={},
#                             content_type='application/json', status_code=200)


import io
import base64
import json
import cv2
import numpy as np
from ultralytics import YOLO

# Initialize your model
def init_context(context):
    context.logger.info('Initializing YOLOv8 pose estimation model...  0%')
    model = YOLO('fish_pose_v6k14.pt')  # Load the YOLOv8 pose estimation model (adjust model path as necessary)
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
