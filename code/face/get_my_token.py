# coding = utf-8
import requests

"""获取百度ＡＰＩ的ｔｏｋｅｎ"""

# SET KEYS
APP_ID = '10391559'
API_KEY = 'ucFNqjUpUe7SMvsjuCiXWShW'
SECRET_KEY = 'i4sAqqHuxAC3bq43CL9c2LHzzngKMwx8'

# get_token
def get_token(API_KEY,SECRET_KEY):
    headers = {"Content-Type" : "application/json; charset=UTF-8"}
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(API_KEY,SECRET_KEY)
    r = requests.post(host,headers = headers,timeout = 10)
    return r.json()["access_token"]

def main():
    token = get_token(API_KEY,SECRET_KEY)
    with open('token.txt','w') as f:
        f.write(token)

if __name__ == "__main__":
    main()
