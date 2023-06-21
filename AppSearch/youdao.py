# -*- coding: utf-8 -*-
import json
import sys
import uuid
import requests
import hashlib
import time
# from imp import reload
from importlib import reload
import time
import csv

reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '20f7b3cdb0aa3b4e'
APP_SECRET = 'joWJc2yEHLm499XQGtgxOA4BykBfzHew'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(q):
    if q == '' or q == '\n' or q is None:
        return ''

    data = {}
    data['from'] = 'zh-CHS'
    data['to'] = 'en'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    data['vocabId'] = "您的用户词表ID"

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        print(1234)
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()

    else:
        result = json.loads(response.content.decode())
        # print(q, result)
        return result.get('translation')[0]


if __name__ == '__main__':
    # query = "待输入的文字"
    # answer = connect(query)
    # print(answer[0])
    file_in = open('/Users/wshuo/Desktop/data4KG/ckzz/applications.csv', encoding='utf-8')
    reader = csv.DictReader(file_in)
    count = 0
    for i in reader:
        print(i)
        count += 1
        if count == 10:
            break
