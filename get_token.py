import time
import requests
import encryption
import tools
from get_data import GetData
# 获取TOKEN接口类
class GetToken(GetData):
    def __init__(self):
        GetData.__init__(self)
        # url
        self.url = self.file['get_token_url']
        # 参数
        self.data = {
            "mlsUser": encryption.descrypt_3des(self.file['get_token_data']['mlsUser']),
            "mlsPwd": encryption.descrypt_3des(self.file['get_token_data']['mlsPwd'])
        }
        # 调用成功间隔时间
        self.success_ct = self.file['get_token_success_ct']
        # 调用失败间隔时间
        self.fail_ct = self.file['get_token_fail_ct']

    def run(self):
        # 半小时失效循环体
        while True:
            # 发送POST请求循环体
            while True:
                try:
                    result = requests.post(url=self.url,json=self.data,headers=self.headers)
                    # 返回200且有token参数返回
                    if result.status_code == 200 and self.parse(result)['data']:
                        tools.logger.info('请求token成功,%s'%(self.parse(result)['msg']))
                        break
                    else:
                        tools.logger.warning('请求token失败,重新请求,%s'%(self.parse(result)['msg']))
                except Exception as reason:
                    tools.logger.warning('请求token出现异常 %s'%reason)
                time.sleep(self.fail_ct)
            # 解析结果,存入配置文件中/全局变量/redis
            tools.token_str = self.parse(result)['data']
            # 半小时后密钥失效，重新获取
            time.sleep(self.success_ct)