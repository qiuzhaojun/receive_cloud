import get_rfid,get_token,get_material,get_mToken,get_produce
import threading

if __name__ == '__main__':

    # 实例化
    get_material = get_material.GetMaterial()
    get_rfid = get_rfid.GetRfid()
    get_token = get_token.GetToken()
    get_mToken = get_mToken.GetMToken()
    get_produce = get_produce.GetProduce()

    # 定义线程
    thread_material = threading.Thread(target=get_material.run,name='MaterialThread')  #获取物料
    thread_rfid = threading.Thread(target=get_rfid.run,name='RfidThread')  # 获取rfid
    thread_token = threading.Thread(target=get_token.run,name='TokenThread') # 获取物料token
    thread_mToken = threading.Thread(target=get_mToken.run,name='MTokenThread')
    thread_produce = threading.Thread(target=get_produce.run,name='ProduceThread')  # 获取produce

    #启动线程
    # thread_token.start()
    # thread_token.join(10)
    # thread_material.start()
    # thread_rfid.start()
    thread_mToken.start()
    thread_mToken.join(10)
    thread_produce.start()

    # 销毁线程

