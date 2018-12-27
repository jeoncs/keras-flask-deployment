#-*- coding: utf-8 -*-

# for downloading model from S3
import boto3

# for image processing
from PIL import Image
import numpy as np
import io

# os level processing
import os

# for reading json file from category_code.json
import json

# for loading keras model
from tensorflow.python.keras.metrics import top_k_categorical_accuracy
from tensorflow.python.keras.models import load_model

# for run_server function
from gevent.pywsgi import WSGIServer


def read_json(path):
    with open(path) as file:
        cat_code = json.loads(file.read())
    return cat_code

def dl_from_s3(s3_path, model_path):
    # parse s3_path input
    s3_path = s3_path.replace("s3://", "").split("/")
    bucket = s3_path.pop(0)
    key = "/".join(s3_path)

    # instantiate s3 client
    s3_client = boto3.client(
        's3',
        region_name='ap-northeast-2'
        )

    local_dir = os.path.dirname(model_path)
    if not os.path.exists(local_dir):
        print('local path does not exist, creating directory')
        os.makedirs(local_dir)

    print('downloading from {} to {}'.format(os.path.join(bucket,key), model_path))
    s3_client.download_file(bucket, key, model_path)
    print('download completed')

def load_model_global(path, framework):
    assert os.path.exists(path), "model does not exist"

    def top_3_accuracy(true, pred):
        return top_k_categorical_accuracy(true, pred, 3)

    print("model loading")
    if framework == "keras":
        model = load_model(path, custom_objects={'top_3_accuracy':top_3_accuracy})
    elif framework == "pytorch":
        model
    print("model loaded")
    return model

def prepare_image(img):
    # convert to handle png file format
    img = Image.open(io.BytesIO(img)).convert(mode='RGB')
    img = img.resize((224,224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def parse_result(pred, cat_code):
    pred_classes = np.argsort(pred[0])[-3:][::-1]
    pred_probs = np.sort(pred[0])[-3:][::-1]
    result = [(cat_code[str(pred_classes[i])],pred_probs[i]) for i in range(3)]
    return result

def run_server(app, port):
    print(("* Starting Flask server..."
        "please wait until server has fully started"))
    http_server = WSGIServer(('', port), app)
    print('Flask server listening on port {}'.format(port))
    http_server.serve_forever()
