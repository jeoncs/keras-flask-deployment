# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
from util import *
import time
import argparse


ACCESS_KEY = os.environ.get('S3_KEY')
SECRET_KEY = os.environ.get('S3_ACCESS_SECRET_KEY')

# parser
parser = argparse.ArgumentParser(description="Model performance demo on Flask")
parser.add_argument("--port", default=8080, help="port number to run the application", type=int)
parser.add_argument("--model_path", default='model/model.h5', help="path to model used in demo",  type=str)
parser.add_argument("--framework", default='keras', help="Keras or Pytorch", type=str)
parser.add_argument("--from_s3", help="download model from s3 and use the model if needed", type=str)
args = parser.parse_args()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = {}
    cat_code = read_json('category_code.json')
    if request.method == "POST":
        if 'file' not in request.files:
            print(u'파일 없음')

        else:
            print(u'파일 업로드')
            # read the image in PIL format
            image = request.files["file"].read()

            print(u'이미지 전처리')
            timer = time.time()
            # preprocess the image and prepare it for classification
            image = prepare_image(image)
            print(u'이미지 처리 시간 {}'.format(time.time() - timer))

            # classify the input image and then initialize the list
            # of predictions to return to the client
            print(u'추론 시작')
            timer = time.time()
            preds = model.predict(image)
            results = parse_result(preds, cat_code)
            print(u'추론 처리 시간 {}'.format(time.time() - timer))

            # loop over the results and add them to the list of
            # returned predictions
            data["predictions"] = []
            for (label, prob) in results:
                r = {"label": label, "probability": "{:.1f}".format(prob*100)}
                data["predictions"].append(r)

    # return the data dictionary as a JSON response
    return jsonify(data).data

if __name__ == "__main__":
    if args.from_s3:
        dl_from_s3(args.from_s3, args.model_path)

    model = load_model_global(args.model_path, args.framework)
    
    # run the server with the specified port
    run_server(app, args.port)

