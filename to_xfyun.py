# -*- coding: UTF-8 -*-
import urllib2
import time
import urllib
import json
import hashlib
import base64
from pydub import AudioSegment
from pydub.utils import make_chunks

def sound_recognize():
    '''
    myaudio = AudioSegment.from_file("E:/work/CNLP/resource/test2.wav" , "wav")
    chunk_length_ms = 1000 # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec

    #Convert chunks to raw audio data which you can then feed to HTTP stream
    for i, chunk in enumerate(chunks):
        raw_audio_data = chunk.raw_data
    '''
    f = open("E:/work/CNLP/resource/test.wav", 'rb')
    file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = urllib.urlencode({'audio': base64_audio})

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = 'd3cff9f77f2a2d79898cfa153df15a3a'
    param = {"engine_type": "sms16k", "aue": "raw"}
    
    x_appid = '5b7fbe72'
    x_param = base64.b64encode(json.dumps(param).replace(' ', ''))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key + str(x_time) + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib2.Request(url, body, x_header)
    result = urllib2.urlopen(req)
    result = result.read()
    print result
    d1 = json.loads(result)
    print(d1['data'])

if (
         __name__ == "__main__"):
    sound_recognize()
