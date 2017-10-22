# -*- coding: utf-8 -*-
# @Author: libing
# @Date:   2017-10-23 00:02:11
# @Last Modified by:   libing
# @Last Modified time: 2017-10-23 01:08:29
import time
from flask import Flask,request
import hashlib
import xml.etree.ElementTree as ET

app = Flask(__name__)

def talks_robot(info = '你叫什么名字'):
    api_url = 'http://www.tuling123.com/openapi/api'
    apikey = 'e916ce4d9c9adf6419d7b2fa381c78ba'
    data = {'key':apikey,'userid':'123','info': info}
    req = requests.post(api_url, data=data).text
    replys = json.loads(req)['text']
    return replys

@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'icrush'  
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return echostr
    else:
        xml_recv = ET.fromstring(request.data)
        ToUserName = xml_recv.find("ToUserName").text
        FromUserName = xml_recv.find("FromUserName").text
        Content = talks_robot(xml_recv.find("Content").text)
        reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = reply % (FromUserName, ToUserName,str(int(time.time())), Content)
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=80)