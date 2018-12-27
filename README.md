# 케라스 모델을 Flask서버에 올리기


[![](https://img.shields.io/badge/python-2.7%2C%203.5%2B-green.svg)]()
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)

> 거의 모든 코드는 https://github.com/mtobeiyf/keras-flask-deploy-webapp 를 수정한 것 입니다.
------------------

## Changelog
 - aws s3에 저장된 모델을 불러 사용 가능
 - index.py 에 argparse 추가
  -- port: 포트지정 (default=8080)
  --model_path: 경로 모델에 있는 모델 사용(default=/tmp/model.h5)
  --framework: keras(케라스 모델 사용) / pytorch(pytorch 모델 사용) (default=keras)
  --from_s3: s3에 있는 모델을 로컬 파일로 저장 후 사용. default 저장경로 /tmp/model.h5
 - static/js/main.js 로직을 1개에서 3개의 카테고리가 나오게 변경
  
example usage:
 ```shell
 python index.py --port 8080 --from_s3 s3://your_bucket/path_to_model --model_path /tmp/keras/model.h5
 ```
 

------------------

## Docker Installation

Build the image

```shell
cd keras-flask-deploy-webapp
docker build -t keras_flask .
docker run -e MODEL_PATH=models/your_model.h5 -p 5000:5000
```

You can mount your model into the container.

```shell
docker run -e MODEL_PATH=/mnt/models/your_model.h5  -v volume-name:/mnt/models -p 5000:5000 keras_flask
```


## Local Installation

### Clone the repo
```shell
$ git clone https://github.com/JeonCS/keras-flask-deployment.git
```

### Install requirements

```shell
$ pip install -r requirements.txt
```

Make sure you have the following installed:
- tensorflow
- keras
- flask
- pillow
- h5py
- gevent
- boto3

### Run with Python

Python 2.7 or 3.5+ are supported and tested.

```shell
$ python index.py
```

------------------

## Customization

### Use your own model

Place your trained `.h5` file saved by `model.save()` under models directory.

Check the [commented code](https://github.com/mtobeiyf/keras-flask-deploy-webapp/blob/master/app.py#L25) in app.py.


### Use other pre-trained model

See [Keras applications](https://keras.io/applications/) for more available models such as DenseNet, MobilNet, NASNet, etc.

Check [this section](https://github.com/mtobeiyf/keras-flask-deploy-webapp/blob/master/app.py#L25) in app.py.

### UI Modification

Modify files in `templates` and `static` directory.

`index.html` for the UI and `main.js` for all the behaviors

## Deployment

To deploy it for public use, you need to have a public **linux server**.

### Run the app

Run the script and hide it in background with `tmux` or `screen`.
```
$ python app.py
```

You can also use gunicorn instead of gevent
```
$ gunicorn -b 127.0.0.1:5000 app:app
```

More deployment options, check [here](http://flask.pocoo.org/docs/0.12/deploying/wsgi-standalone/)

### Set up Nginx

To redirect the traffic to your local app.
Configure your Nginx `.conf` file.
```
server {
    listen  80;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
```

## More resources

Check Siraj's ["How to Deploy a Keras Model to Production"](https://youtu.be/f6Bf3gl4hWY) video. The corresponding [repo](https://github.com/llSourcell/how_to_deploy_a_keras_model_to_production).

[Building a simple Keras + deep learning REST API](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html)
