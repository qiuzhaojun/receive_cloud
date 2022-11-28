import get_rfid,get_token,get_material,get_mToken,get_produce,get_ct,get_NG,get_DefectTop5,get_DeviceTest
import threading

if __name__ == '__main__':

    # 实例化
    get_material = get_material.GetMaterial()
    get_rfid = get_rfid.GetRfid()
    get_token = get_token.GetToken()
    get_mToken = get_mToken.GetMToken()
    get_produce = get_produce.GetProduce()
    get_ct = get_ct.GetCT()
    get_NG = get_NG.Get_NG()
    get_DefectTop5 = get_DefectTop5.Get_DefectTop5()
    get_DeviceTest = get_DeviceTest.Get_DeviceTest()

    # 定义线程
    thread_material = threading.Thread(target=get_material.run,name='MaterialThread')  #获取物料
    thread_rfid = threading.Thread(target=get_rfid.run,name='RfidThread')  # 获取rfid
    thread_token = threading.Thread(target=get_token.run,name='TokenThread') # 获取物料token
    thread_mToken = threading.Thread(target=get_mToken.run,name='MTokenThread')
    thread_produce = threading.Thread(target=get_produce.run,name='ProduceThread')  # 获取produce
    thread_ct = threading.Thread(target=get_ct.run,name='CTThread')  # 获取节拍时间
    thread_NG = threading.Thread(target=get_NG.run,name='NGThread')  # 获取一次装配不良率
    thread_top5 = threading.Thread(target=get_DefectTop5.run,name='TOP5Thread')  # 获取一次装配不良率
    thread_DeviceTest = threading.Thread(target=get_DeviceTest.run,name='DeviceTestThread')  # 获取一次装配不良率

    #启动线程
    thread_token.start()
    thread_mToken.start()

    thread_token.join(10)
    thread_mToken.join(10)

    thread_material.start()
    thread_rfid.start()
    thread_produce.start()
    thread_ct.start()
    thread_NG.start()
    thread_top5.start()
    thread_DeviceTest.start()

    # 销毁线程

