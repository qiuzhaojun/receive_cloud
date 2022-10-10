import get_rfid,get_token,get_material
import threading

if __name__ == '__main__':

    # 实例化
    get_material = get_material.GetMaterial()
    get_rfid = get_rfid.GetRfid()
    get_token = get_token.GetToken()

    # 定义线程
    thread_material = threading.Thread(target=get_material.run,name='TsetThread1')
    thread_rfid = threading.Thread(target=get_rfid.run,name='TsetThread2')
    thread_token = threading.Thread(target=get_token.run,name='TsetThread3')

    #启动线程
    thread_token.start()
    thread_token.join(10)
    thread_material.start()
    thread_rfid.start()

    # 销毁线程

