import time
import requests
import encryption
import tools
from get_data import GetData

# 获取TOKEN接口类
class GetMToken(GetData):
    def __init__(self):
        GetData.__init__(self)
        # url
        self.url = self.file['get_mToken_url']
        # 参数
        self.data = {
            "User": encryption.descrypt_3des(self.file['get_mToken_data']['User']),
            "Pwd": encryption.descrypt_3des(self.file['get_mToken_data']['Pwd'])
        }
        # 调用成功间隔时间
        self.success_ct = self.file['get_mToken_success_ct']
        # 调用失败间隔时间
        self.fail_ct = self.file['get_mToken_fail_ct']

    def run(self):
        # 半小时失效循环体
        while True:
            # 发送POST请求循环体
            while True:
                try:
                    result = requests.post(url=self.url,json=self.data,headers=self.headers)
                    # 返回200且有token参数返回
                    if result.status_code == 200 and self.parse(result)['Data']:
                        tools.logger.info('请求mToken成功,%s'%(self.parse(result)['Message']))
                        break
                    else:
                        tools.logger.warning('请求mToken失败,重新请求,%s'%(self.parse(result)['Message']))
                except Exception as reason:
                    tools.logger.warning('请求mToken出现异常 %s'%reason)
                time.sleep(self.fail_ct)
            # 解析结果,存入配置文件中/全局变量/redis,因为是bearer模式，所以需要进行拼接
            tools.mToken_str = 'Bearer ' + self.parse(result)['Data']['Token']
            # 半小时后密钥失效，重新获取
            time.sleep(self.success_ct)