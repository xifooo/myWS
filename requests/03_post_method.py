import requests as rs
import os

from flask import Flask, request


def dec(f):
    
    def inner(*args, **kwargs):
        print('')
        f(*args, **kwargs)
        print('')
    
    return inner


# post请求, 带参数
def post_value(url,data):
    resp = rs.post(url,data=data)
    print(resp.text)


# 上传图像
app = Flask(__name__)
@app.route("/")
def home():
    return 'This is home page'
@app.route("/upload", methods=['POST'])
def handleFileUpload():
    msg = 'failed to upload image'
    if 'image' in request.files:
        photo = request.files['image']
        if photo.filename != '':
            photo.save(os.path.join('.', photo.filename))
            msg = 'image uploaded successfully'
    return msg


if __name__ == '__main__':
    
    url = "https://httpbin.org/post"
    data = {'name': 'Peter'}
    
    app.run()
    flask_url = 'http://localhost:5000/upload'
    with open(os.path.join(os.getcwd(),'Birdie.png'), 'rb') as f:
        files = {'image': f}
        r = rs.post(url, files=files)
        print(r.text)
    