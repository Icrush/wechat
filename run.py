# -*- coding: utf-8 -*-
# @Author: libing
# @Date:   2017-10-23 00:02:11
# @Last Modified by:   libing
# @Last Modified time: 2017-10-23 00:14:49
import time
from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET

app = Flask(__name__)
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
            return make_response(echostr)
    else:
        xml_recv = ET.fromstring(request.data)
        ToUserName = xml_recv.find("ToUserName").text
        FromUserName = xml_recv.find("FromUserName").text
        Content = xml_recv.find("Content").text
        reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(reply % (FromUserName, ToUserName,
                                          str(int(time.time())), Content))
        response.content_type = 'application/xml'
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=80)