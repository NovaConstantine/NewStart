from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)

@app.route('/wx')
def getinput():
    signature=request.args.get('signature')
    timestamp=request.args.get('timestamp')
    nonce=request.args.get('nonce')
    echostr=request.args.get('echostr')
    token = "dingxianchao"
    list = [token, timestamp, nonce]
    list.sort()
    sha1 = hashlib.sha1()
    sha1.update(list[0].encode('utf-8'))
    sha1.update(list[1].encode('utf-8'))
    sha1.update(list[2].encode('utf-8'))
    hashcode = sha1.hexdigest()
    print ("handle/GET func: hashcode, signature, timestamp, nonce, echostr, token: ", hashcode, signature,timestamp,nonce,echostr)
    if hashcode == signature:
        return echostr
    else:
        return ""

if __name__ == '__main__':
    app.run(port='80')
