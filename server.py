from geventwebsocket.handler import WebSocketHandler
from geventwebsocket import WebSocketError
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template
import numpy as np
import cv2
import base64
from PIL import Image

app = Flask(__name__)

#cam = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('webcam.html')


def base64_to_cv2_img(base64DataUri):
    encoded_data = base64DataUri.split(',')[1]
    img = cv2.imdecode(np.fromstring(encoded_data.decode('base64'), dtype=np.uint8),cv2.IMREAD_COLOR)
    return img

@app.route('/webcam')
def webcam():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            try:
                base64DataUri = ws.receive()
                img = base64_to_cv2_img(base64DataUri)
                _, img_encoded = cv2.imencode('.jpg', img)
                b64 = base64.encodestring(img_encoded)
                ws.send(b64)
            except WebSocketError:
                break




if __name__ == '__main__':
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()