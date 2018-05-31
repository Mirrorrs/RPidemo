# coding = utf-8
import requests

"""这个ｄｅｍｏ用于调用百度ＡＰＩ进行语音识别"""

ID = '10353129'
api_key = 'YjPlAAIIMF1a9FSC3AmI2gDp'
secret_key = 'afc5aba3e2f198cac19b793a522baa92'
token_url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(api_key,secret_key)
r = requests.post(token_url,timeout = 10)
token = r.json()['access_token']

# 读取文件
def get_wave(path):
    f = open(path,'rb')
    return f

# 调用ＡＰＩ
def use_cloud(path):
    headers = {"Content-Type": "audio/pcm;rate=8000"}
    sever_url = "http://vop.baidu.com/server_api?lan=zh&cuid={0}&token={1}".format("hansoma",token)
    req = requests.post(sever_url,headers = headers,data = get_wave(path))

    if req.json()['err_msg'] == 'success.':
        return req.json()['result'][0][:-1]
    else:
        print(req.json()['err_msg'])
        return ''

def main():

    print(use_cloud('sb.wav'))

if __name__ == '__main__':
    main()
