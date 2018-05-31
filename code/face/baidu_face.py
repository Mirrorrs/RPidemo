# coding = utf-8
import requests,base64,os

"""对调用百度ＡＰＩ的封装
具体说明见https://cloud.baidu.com/product/face"""

token = open('/home/pi/files/IoT/face/token.txt').read()

#　人脸注册
#　return string
def regi_myface(path,uid,group_id):
    url = "https://aip.baidubce.com/rest/2.0/face/v2/faceset/user/add"
    sever_url = url + '?access_token=' + token
    f = open(path,'rb')
    img = base64.b64encode(f.read())
    hds = {'Content-Type' : 'application/x-www-form-urlencoded'}
    data = {
            'uid' : uid,
            'user_info' : 'register for 118',
            'group_id' : group_id,
            'image' : img,
            'action_type' : 'raplace',#replace则替换该uid下的所有图片
            }
    r = requests.post(sever_url,headers = hds,data = data)
    results = r.json()
    if 'error_msg' not in results:
        return 'Registration success.'
    else:
        return results['error_msg']

#　人脸数据更新
#　return string
def update_myface(path,uid):
    url = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/user/update'
    server_url = url + '?access_token=' + token
    f = open(path,'rb')
    img = base64.b64encode(f.read())
    hds = {'Content-Type' : 'application/x-www-form-urlencoded'}
    data = {
            'uid' : uid,
            'user_info' : 'update data for 118',
            'group_id' : '118',
            'image' : img,
            }
    r = requests.post(server_url,headers = hds,data = data)
    results = r.json()
    if 'error_msg' not in results:
        return 'Update success.'
    else:
        return results['error_msg']



#　删除组内人脸数据
#　return string
def delete_myface(uid,group_id):
    url = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/group/deleteuser'
    server_url = url + '?access_token=' + token
    hds = {'Content-Type' : 'application/x-www-form-urlencoded'}
    data = {
            'uid' : uid,
            'group_id' : group_id,
            }
    r = requests.post(server_url,headers = hds,data = data)
    results = r.json()
    if 'error_msg' not in results:
        return 'Delete success.'
    else:
        return results['error_msg']

#　查看某uid详细信息
#　return dic
def check_uid(uid,group_id):
    url = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/user/get'
    server_url = url + '?access_token=' + token
    hds = {'Content-Type' : 'application/x-www-form-urlencoded'}
    data = {
            'uid' : uid,
            'group_id' : group_id,
            }
    r = requests.post(server_url,headers = hds,data = data)
    results = r.json()
    if 'result' in results:
        return results['result']
    else:
        return None

#　查看已有组
#　return list
def check_my_groups():
    url = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/group/getlist'
    server_url = url + '?access_token=' + token
    hds = {'Content-Type' : 'application/x-www-form-urlencoded'}
    r = requests.post(server_url,headers = hds)
    results = r.json()
    if 'result' in results:
        return results['result']

#　查看组内用户
#　return list
def check_uids_in_group(group_id):
    url = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/group/getusers'
    server_url = url + '?access_token=' + token
    hds = {'Content-Type' : 'application/x-www-form-urlencoded'}
    data = {
            'group_id' : str(group_id),
            }
    r = requests.post(server_url,headers = hds,data = data)
    results = r.json()
    if 'result' in results:
        return results['result']
    else:
        return results

#　人脸识别
#　return dic
def iden_myface(path):
    url = "https://aip.baidubce.com/rest/2.0/face/v2/identify"
    sever_url = url + '?access_token=' + token
    f = open(path,'rb')
    img = base64.b64encode(f.read())
    hds = {'Content-Type' : 'application/x-www-form-urlencoded'}
    data = {
            'group_id' : 'gaozi',
            'image' : img,
            'ext_fields' : 'faceliveness',
            }
    r = requests.post(sever_url,headers = hds,data = data)
    results = r.json()
    result_dic = {}
    if 'result' in results:
        result_dic['uid'] = str(results['result'][0]['uid'])
        result_dic['group_id'] = str(results['result'][0]['group_id'])
        result_dic['score'] = str(results['result'][0]['scores'][0])
        result_dic['faceliveness'] = str(results['ext_info']['faceliveness'])
        return result_dic
    else:
        return None

#　人脸认证
#　return list
def vrf_myface(path,uid,group_id):
    url = 'https://aip.baidubce.com/rest/2.0/face/v2/verify'
    server_url = url + '?access_token=' + token
    f = open(path,'rb')
    img = base64.b64encode(f.read())
    hds = {'Content-Type' : 'application/x-www-form-urlencoded'}
    data = {
            'uid' : uid,
            'image' : img,
            'group_id' : group_id,
            'ext_fields' : 'faceliveness',
            }
    r = requests.post(server_url,headers = hds,data = data)
    results = r.json()
    result_dic = {}
    if 'result' in results:
        result_dic['scores'] = str(results['result'])
        result_dic['faceliveness'] = str(results['ext_info']['faceliveness'])
        return result_dic
    else:
        return None

#　树莓派拍摄照片
def take_a_photo(path):
    path = '/home/pi/files/IoT/face/storage/test.jpg'
    command = 'raspistill -t 500 -o ' + path + ' -q 5'
    os.system(path)



if __name__ == '__main__':
    #regi_img = '/home/pi/files/IoT/face/sample/mty.jpg'
    test_img = '/home/pi/files/IoT/face/storage/test.jpg'
    
    #print(check_my_groups())
    #print(regi_myface(regi_img,'mty','118'))
    #print(check_uids_in_group('118'))
    #print(delete_myface('hansoma','118'))
    print(iden_myface(test_img))
    #print(vrf_myface(test_img,'mty','118'))
