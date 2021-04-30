"""
*******************************************************************
  Copyright (c) 2013, 2017 IBM Corp.

  All rights reserved. This program and the accompanying materials
  are made available under the terms of the Eclipse Public License v1.0
  and Eclipse Distribution License v1.0 which accompany this distribution.

  The Eclipse Public License is available at
     http://www.eclipse.org/legal/epl-v10.html
  and the Eclipse Distribution License is available at
    http://www.eclipse.org/org/documents/edl-v10.php.

  Contributors:
     Ian Craggs - initial implementation and/or documentation
*******************************************************************
"""

import unittest
import random

import mqtt.clients.V311 as mqtt_client, time, logging, socket, sys, getopt, traceback

class Callbacks(mqtt_client.Callback):

  def __init__(self):
    self.messages = []
    self.publisheds = []
    self.subscribeds = []
    self.unsubscribeds = []

  def clear(self):
    self.__init__()

  def connectionLost(self, cause):
    logging.info("connectionLost %s", str(cause))

  def publishArrived(self, topicName, payload, qos, retained, msgid):
    logging.info("publishArrived %s %s %d %d %d", topicName, payload, qos, retained, msgid)
    self.messages.append((topicName, payload, qos, retained, msgid))
    return True

  def published(self, msgid):
    logging.info("published %d", msgid)
    self.publisheds.append(msgid)

  def subscribed(self, msgid, data):
    logging.info("subscribed %d", msgid)
    self.subscribeds.append((msgid, data))

  def unsubscribed(self, msgid):
    logging.info("unsubscribed %d", msgid)
    self.unsubscribeds.append(msgid)

def cleanup():
    # clean all client state
    print("clean up starting")
    print(clientid1,clientid2)
    clientids = (clientid1, clientid2)
    
    for clientid in clientids:
        curclient = mqtt_client.Client(clientid.encode("utf-8"))
        curclient.setUserName(username1, password1)
        curclient.connect(host=host, port=port, cleansession=True)
        time.sleep(.1)
        curclient.disconnect()
        time.sleep(.1)

    # clean retained messages
    callback = Callbacks()
    curclient = mqtt_client.Client(clientid1.encode("utf-8"))
    curclient.registerCallback(callback)
    curclient.setUserName(username1, password1)
    curclient.connect(host=host, port=port, cleansession=True)
    curclient.subscribe(["#"], [0])
    time.sleep(2) # wait for all retained messages to arrive
    for message in callback.messages:
        if message[3]: # retained flag
            print("deleting retained message for topic", message[0])
            curclient.publish(message[0], b"", 0, retained=True)
    curclient.disconnect()
    time.sleep(.1)
    print("clean up finished")
    
    
def topictest(self,sub_index=None,pub_index=None,message=None):
    #不同种类的topic测试
    callback.clear()
    callback2.clear()
    #用户B连接
    bclient.connect(host=host, port=port, cleansession=True)
    print("userb sub")
    bclient.subscribe([wildtopics[sub_index]], [2])
    time.sleep(1) # wait for all retained messages, hopefully
    #callback2.clear()
    print("userb pub")
    bclient.publish(topics[pub_index], message, 1, retained=False)
    time.sleep(2)
    #用户a连接
    aclient.connect(host=host, port=port, cleansession=True)
    print("usera pub")
    aclient.publish(topics[pub_index], message, 1, retained=False)
    time.sleep(1)
    aclient.disconnect()
    time.sleep(1)
    bclient.disconnect()
    print(callback2.messages)
    return callback2.messages

def qostest(self,sub_qos=None,pub_qos=None,message=None):
    callback.clear()
    callback2.clear()
    #用户B连接
    bclient.connect(host=host, port=port, cleansession=True)
    print(wildtopics[6],topics[1])
    bclient.subscribe([wildtopics[6]], [sub_qos])
    time.sleep(1)
#     callback2.clear()
    bclient.publish(topics[1], message, pub_qos, retained=False)
    time.sleep(2)
    #用户a连接
    aclient.connect(host=host, port=port, cleansession=True)
    aclient.publish(topics[1], message, pub_qos, retained=False)
    time.sleep(1)
    bclient.disconnect()
    time.sleep(1)
    aclient.disconnect()
    print(callback2.messages)
    return callback2.messages
def will_message_qos(self,willQos=None,subQos=None):
    succeeded = True
    callback2.clear()
    assert len(callback2.messages) == 0, callback2.messages
    connack = aclient.connect(host=host, port=port, cleansession=True, willFlag=True,
      willTopic=topics[2], willMessage=b"test will message qos zero", keepalive=2,willQoS=willQos)
    # #assert connack.flags == 0x00 # Session present
    print(topics[2])
    connack = bclient.connect(host=host, port=port, cleansession=False)
    bclient.subscribe([topics[2]], [subQos])
    time.sleep(.1)
    print("usera shutdown")
    aclient.terminate()
    time.sleep(5)
    # bclient.disconnect()
    print(callback2.messages)
    return callback2.messages


def test_will_message_qos_zero(self):
      # will messages
      print("Will message test starting")
      succeeded = True
      callback2.clear()
      assert len(callback2.messages) == 0, callback2.messages
      try:
        connack = aclient.connect(host=host, port=port, cleansession=True, willFlag=True,
          willTopic=topics[2], willMessage=b"client not disconnected", keepalive=2,willQoS=0)
        # #assert connack.flags == 0x00 # Session present
        connack = bclient.connect(host=host, port=port, cleansession=False)
        bclient.subscribe([topics[2]], [0])
        time.sleep(.1)
        aclient.terminate()
        time.sleep(5)
        bclient.disconnect()
        print(callback2.messages)
        assert len(callback2.messages) == 1, callback2.messages  # should have the will message
        self.assertEqual(callback2.messages[0][1],b"client not disconnected")
      except:
        traceback.print_exc()
        succeeded = False
      print("Will message test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded


def clientidtest(self,clientid,username,apppassword):
    print("clientid test starting")
    succeeded = True
    callback4 = Callbacks()
    try:
        client0 = mqtt_client.Client(clientid.encode("utf-8"))
        client0.registerCallback(callback4)
        client0.setUserName(username, apppassword)
        # try:
        client0.connect(host=host, port=port, cleansession=True) # should work
        print(wildtopics[0],topics[1])
        client0.subscribe([wildtopics[0]],[2])
        time.sleep(.1)
        client0.publish(topics[1],b"test cliendid",2,retained=False)
        time.sleep(1)
        print(callback4.messages)
        assert len(callback4.messages) ==1
        # except:
        #     fails = False
        # self.assertEqual(fails, True)
        # fails = True
        # try:
        #     client0.connect(host=host, port=port, cleansession=True,username=username,password=apppassword) # should work
        # except:
        #     fails = False
        # self.assertEqual(fails, True)
        client0.disconnect()
    except:
        traceback.print_exc()
        succeeded = False
    print("error appkey clientid test", "succeeded" if succeeded else "failed")
    return succeeded


def usage():
  print(
"""
 -h: --hostname= hostname or ip address of server to run tests against
 -p: --port= port number of server to run tests against
 -z: --zero_length_clientid run zero length clientid test
 -d: --dollar_topics run $ topics test
 -s: --subscribe_failure run subscribe failure test
 -n: --nosubscribe_topic_filter= topic filter name for which subscriptions aren't allowed

""")

def generate_random_str(randomlength=None):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

class Test(unittest.TestCase):
    global host, port, topics, wildtopics, nosubscribe_topics, clientid1, clientid2, authentication, username1,username2,usernames, password1,password2,error_cliendid,\
        length_clientid,length_topic,length64_fold
    authentication = False

    # 1.测试地址沙箱环境
    host = "mqtt-ejabberd-hsb.easemob.com"   #发送地址
    port = 2883 #发送端口
    username1,username2 = b"mqtttest1",b"mqtttest2"  #用户名称
    password1 = b"$t$YWMtzP0sDKdAEeu14SMMp-gviPLBUj23REhmv2d9MJZsm8W1kvwQpbMR67NY5XfrXvBLAwMAAAF5Es8XPgBPGgDR9jOQyYerAtoFZ0sPW5Uf8UXkYmdcUBVtU1Ewu4N_qQ"  #用户密码，实际为与用户匹配的token
    password2 = b"$t$YWMt1xc7aqdAEeucVx_UwbjRCfLBUj23REhmv2d9MJZsm8W6vmEgpbMR655ln0Nsooa_AwMAAAF5Es9ZcgBPGgCp3XBI7JwPhYo6JnKGwcFN067Cagq_PmGIWiotkNf99w"  #用户密码，实际为与用户匹配的token
    clientid1 = "mqtttest1@1wyp94"  #开启鉴权后clientid格式为deviceid@appkeyappid deviceid任意取值，只要保证唯一。
    clientid2 = "mqtttest2@1wyp94"
    appid = {"right_appid":"1wyp94","error_appid":"123","noappid":""} #构建appid


    #本地
    # host = "172.17.1.160"
    # port = 1883
    # username1,username2 = b"mqtttest1",b"mqtttest2"  #用户名称
    # password1 = b"$t$YWMthT_bXKZ5Eeuek9H9tYvkYPLBUj23REhmv2d9MJZsm8W1kvwQpbMR67NY5XfrXvBLAwMAAAF5DbUWfgBPGgB0jT5heMPzU_TtZJqSmmESmC6PzksQSNOyZuEscqu2cg"  #用户密码，实际为与用户匹配的token
    # password2 = b"$t$YWMti47_9qZ5EeutzZVjt1Y3N_LBUj23REhmv2d9MJZsm8W6vmEgpbMR655ln0Nsooa_AwMAAAF5DbU_1wBPGgAFHk3GBqhgusAPC74z-xslVDS9HSvCYYZfL0y6ZkIAdQ"
    # clientid1 = "ckjaakjncalnla@1RK24W"
    # clientid2 = "ckjaakjncalnla1@1RK24W"
    # appid = {"right_appid":"1RK24W","error_appid":"123","noappid":""} #构建appid
    

    topics =  ("TopicA", "TopicA/B", "Topic/C", "TopicA/C", "/TopicA","TopicA/B/C","topicA/B/C/D/E/F/G/H/I","topic/a/b/c/d/e/f/g")
    wildtopics = ("TopicA/+", "+/C", "#", "/#", "/+", "+/+", "TopicA/#","+/#","topicA/B/C/D/E/F/G/H/I","topic/a/b/c/d/e/f/g")
    nosubscribe_topics = ("test/nosubscribe",)
    length_topic = "1234567890123456789012345678901234567890123456789012345678901234"
    length64_fold = "a/b/c/d/e/f/g/f/h/i/gk/l/m/n/o/p/q/r/s/t/u/v/w/x/y/z/1/2/3/4/5/6"
    length_clientid = "123456789012345678901234567890123456789012345678901234567@" + appid["right_appid"]
    deviceid = {"right_deviceid":"testdeviceid1","error_deviceid":""}    #构建deviceid
    error_cliendid = {"error_format_one":deviceid["right_deviceid"] + "#" + appid["right_appid"],\
        "no_appid":deviceid["right_deviceid"] + "@",\
        "error_format_two":deviceid["right_deviceid"]  + appid["right_appid"],\
        "appid_empty":deviceid["right_deviceid"] + "@" + appid["noappid"],\
        "overlength_clientid":"123456789012345678901234567890123456789012345678901234567@1RK24W123456789012345678901234567890123456789012345678901234567@" + appid["right_appid"]}
    
    @classmethod
    def setUpClass(cls):
      global callback, callback2, callback3,aclient, bclient,cclient
    #   cleanup()

      callback = Callbacks()
      callback2 = Callbacks()
      callback3 = Callbacks()


      #aclient = mqtt_client.Client(b"\xEF\xBB\xBF" + "myclientid".encode("utf-8"))
      aclient = mqtt_client.Client(clientid1.encode("utf-8"))
      aclient.registerCallback(callback)
      aclient.setUserName(username1, password1)

      bclient = mqtt_client.Client(clientid2.encode("utf-8"))
      bclient.registerCallback(callback2)
      bclient.setUserName(username2, password2)

      cclient = mqtt_client.Client(clientid1.encode("utf-8"))
      cclient.registerCallback(callback3)
      cclient.setUserName(username1, password1)
    
    def setUp(self):
        callback.clear()
        callback2.clear()
    
    def tearDown(self):
        cleanup()

    """
        1.基础测试
    """
    def test_basic(self):
        print("Basic test starting")
        succeeded = True
        try:
            aclient.connect(host=host, port=port)
            aclient.disconnect()

            connack = aclient.connect(host=host, port=port)
            # #assert connack.flags == 0x00 # Session present
            aclient.subscribe([topics[0]], [2])
            aclient.publish(topics[0], b"qos 0")
            aclient.publish(topics[0], b"qos 1", 1)
            aclient.publish(topics[0], b"qos 2", 2)
            time.sleep(2)
            aclient.disconnect()
            print(callback.messages)
            self.assertEqual(len(callback.messages), 3)
        except:
            traceback.print_exc()
            succeeded = False

        print("Basic test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded




    """
        1.测试连续订阅不同topic
    """
    def test_subscription_continuous(self):
        print("test subnum max starting")
        print(print(topics),len(topics),len(wildtopics))
        connack = aclient.connect(host=host,port=port)
        connack = bclient.connect(host=host,port=port)
        succeeded = True
        try:
            for i in range(len(topics)):
                print(i)
                aclient.subscribe([topics[i]], [2])
                bclient.subscribe([topics[i]], [2])
                time.sleep(0.1)
        except:
            succeeded = False
        time.sleep(5)
        self.assertEqual(succeeded,True)


    """
        1.测试连续订阅取消订阅（可以验证console中最大订阅topic）
    """
    def test_subcription_unsubcription_continuous(self):
        print("test continuous subscription unsubscription starting")
        print(print(topics),len(topics),len(wildtopics))
        connack = aclient.connect(host=host,port=port)
        connack = bclient.connect(host=host,port=port)
        succeeded = True
        try:
            for i in range(len(topics)):
                print(i)
                aclient.subscribe([topics[i]], [2])
                bclient.subscribe([topics[i]], [2])
                time.sleep(.2)
        except:
            succeeded = False
        self.assertEqual(succeeded,True)

    
    """
        1.测试连续向不同topic发送消息
    """
    def test_sending_messages_continuously(self):
        print("test subnum max starting")
        print(print(topics),len(topics),len(wildtopics))
        connack = aclient.connect(host=host,port=port)
        connack = bclient.connect(host=host,port=port)
        succeeded = True
        try:
            for i in range(len(topics)):
                print(i)
                aclient.subscribe([topics[i]], [2])
                bclient.subscribe([topics[i]], [2])
                time.sleep(.2)
        except:
            succeeded = False
        # f = generate_random_str(10)
        print("send messages")
        succeeded = True
        number = 10
        try:
            # f = generate_random_str(10)
            for num in range(number):
                for i in range(len(topics)):
                    print(num,i)
                    print("first")
                    aclient.publish(topics[i],b"publish topic: qos0",0, retained=False)
                    print("sencode")
                    aclient.publish(topics[i],b"publish topic qos1", 1, retained=False)
                    print("third")
                    aclient.publish(topics[i],b"publish topic qos2", 2, retained=False)
                    time.sleep(1)
        except:
            succeeded = False
        print(len(callback.messages))
        print(len(callback.messages))
        assert len(callback.messages) == number*3*len(topics)
        assert len(callback2.messages) == number*3*len(topics)
        self.assertEqual(succeeded,True)





    """
        1.测试发送内容字符串长度
    """
    def test_send_message_length(self):
        print("Basic test starting")
        succeeded = True
        number = 65535
        f = generate_random_str(number) #随机构建一个指定字符串
        message = bytes(f, encoding='utf-8')    #将字符串转化为bytes
        time.sleep(1)
        # print(message)
        try:
            print("登陆")
            connack = aclient.connect(host=host, port=port)
            # #assert connack.flags == 0x00 # Session present
            print("sub")
            aclient.subscribe([topics[0]], [2])
            # aclient.publish(topics[0], message, 0)
            aclient.publish(topics[0], message, 1)
            time.sleep(.1)
            aclient.publish(topics[0], message, 2)
            time.sleep(2)
            aclient.disconnect()
            # print(callback.messages)
            print("断言")
            print(len(callback.messages))
            self.assertEqual(len(callback.messages), 2)
            self.assertEqual(len(callback.messages[0][1]),number)
            self.assertEqual(len(callback.messages[1][1]),number)
        except:
            traceback.print_exc()
            succeeded = False

        print("Basic test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded




    """
        1.验证用户名称（username）与密码不一致（token）
    """
    def test_login_username_and_paw_donot_math(self):
        print("test_login_username_and_paw_donot_math starting")
        succeeded = False

        try:
            connect = aclient.connect(host=host,port=port,username=username1,password=password2)
            print("login succeed")
        
        except:
            traceback.print_exc()
            succeeded = True
        print("test_login_username_and_paw_donot_math starting %s""succeeded" if succeeded else "failed")
        assert succeeded == True




    """
        1.验证用户名称（username、password）与appid不匹配
    """
    def test_login_username_and_appid_donot_math(self):
        print("test_login_username_and_appid_donot_math starting")
        succeeded = False
        try:
            aclient0 = mqtt_client.Client(clientid2.encode("utf-8"))
            connect = aclient0.connect(host=host,port=port)
            print("login succeed")
        
        except:
            traceback.print_exc()
            succeeded = True
        print("test_login_username_and_appid_donot_math starting %s""succeeded" if succeeded else "failed")
        assert succeeded == True




    """
        1。默认是session保存时长为1800分钟，为了方便测试可以找研发修改session默认时长（此case设置默认时长为120s）
    """
    def test_session_defaults_120s(self):
        print("The test session defaults to 120s")
        succeeded = True
        try:
            connect =  aclient.connect(host=host,port=port,cleansession=False)
            print(wildtopics[0],topics[1])
            aclient.subscribe([wildtopics[0]],[2])
            aclient.disconnect()
            localtime_start = time.asctime( time.localtime(time.time()) )
            print(localtime_start)
            time.sleep(115)
            localtime_end = time.asctime(time.localtime(time.time()))
            print(localtime_end)
            connect =  aclient.connect(host=host,port=port,cleansession=False)
            time.sleep(.1)
            aclient.publish(topics[1],b"test session",1,retained=False)
            time.sleep(1)
            aclient.disconnect()
            print(callback.messages)
            assert (len(callback.messages)) ==1
            self.assertEqual(callback.messages[0][1],b"test session")

        except:
            traceback.print_exc()
            succeeded = False
        print("The test session defaults to 120s %s""succeeded" if succeeded else "failed")
        assert succeeded == True




    """
        1.默认是session保存时长为1800分钟，为了方便测试可以找研发修改session默认时长（此case设置默认时长为120s）
    """
    def test_session_defaults_130s(self):
        print("The test session defaults to 120s")
        succeeded = False
        try:
            connect =  aclient.connect(host=host,port=port,cleansession=False)
            print(wildtopics[0],topics[1])
            aclient.subscribe(wildtopics[0],[2])
            aclient.disconnect()
            time.sleep(125)
            connect =  aclient.connect(host=host,port=port,cleansession=False)
            time.sleep(.1)
            aclient.publish(topics[1],b"test session",1,retained=False)
            print(callback.message)
            assert (len(callback.message)) ==0
            self.assertEqual(callback.message[0][1],b"test session")
        except:
            traceback.print_exc()
            succeeded = True
        print("The test session defaults to 120s %s""succeeded" if succeeded else "failed")
        self.assertTrue(succeeded)




    def test_cleansession_false(self):
      print("cleansession false test starting")
      global aclient
      succeeded = True
      try:
        callback.clear()
        callback2.clear()
        connack = aclient.connect(host=host, port=port,cleansession=False)
        aclient.subscribe([topics[1]], [2])
        time.sleep(1)
        print(callback.subscribeds)
        # aclient.disconnect()
        aclient.terminate()
        print("user A shutdown")
        time.sleep(2)
        connack = aclient.connect(host=host, port=port,cleansession=False)
        print(callback.subscribeds)
        time.sleep(2)
        connack = bclient.connect(host=host, port=port,cleansession=True)
        bclient.publish(topics[1], b"qos1", 1, retained=False)
        time.sleep(1)
        # aclient.disconnect()
        # bclient.disconnect()
        aclient.terminate()
        bclient.terminate
        print("user A and b shutdown")
        print(callback.messages)
        self.assertEqual(len(callback.messages), 1)
        self.assertEqual(callback.messages[0][1], b"qos1")
      except:
        traceback.print_exc()
        succeeded = False
        
      print("Cleansession false test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded
    

    """
        1.测试服务质量为零
    """
    def test_qos_zero(self):
        print("QoS is minimized test starting")
        message = b"QoS is minimized "
        sub_qos = 0
        succeeded = True
        try:
            result = qostest(self,sub_qos=sub_qos,pub_qos=0,message=message)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][2],sub_qos,result[0][2])
            self.assertEqual(result[1][2],sub_qos,result[0][2])
        except:
            succeeded = False
        self.assertTrue(succeeded)
        try:
            result1 = qostest(self,sub_qos=0,pub_qos=1,message=message)
            self.assertEqual(len(result1), 2)
            self.assertEqual(result1[0][2],sub_qos,result1[0][2])
            self.assertEqual(result1[1][2],sub_qos,result1[0][2])
        except:
            succeeded = False
        self.assertTrue(succeeded)
        try:
            result2 = qostest(self,sub_qos=0,pub_qos=2,message=message)
            self.assertEqual(len(result2), 2)
            self.assertEqual(result2[0][2],sub_qos,result2[0][2])
            self.assertEqual(result2[1][2],sub_qos,result2[0][2])
        except:
            succeeded = False
        print("QoS minimum test was ","succeeded" if succeeded else "falsed")
        self.assertTrue(succeeded)
    
    """
        1.测试服务质量为1
    """
    def test_qos_one(self):
        print("QoS is minimized test starting")
        message = b"QoS is minimized "
        sub_qos = 1
        result = []
        succeeded = True
        try:
            result = qostest(self,sub_qos=sub_qos,pub_qos=0,message=message)
            print(len(result))
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][2],0,result[0][2])
            self.assertEqual(result[1][2],0,result[0][2])
        except:
            succeeded = False
        self.assertTrue(succeeded)
        try:
            result1 = qostest(self,sub_qos=sub_qos,pub_qos=1,message=message)
            self.assertEqual(len(result1), 2)
            self.assertEqual(result1[0][2],sub_qos,result1[0][2])
            self.assertEqual(result1[1][2],sub_qos,result1[0][2])
        except:
            succeeded = False
        self.assertTrue(succeeded)
        try:
            result2 = qostest(self,sub_qos=sub_qos,pub_qos=2,message=message)
            self.assertEqual(len(result2), 2)
            self.assertEqual(result2[0][2],sub_qos,result2[0][2])
            self.assertEqual(result2[1][2],sub_qos,result2[0][2])
        except:
            succeeded = False
        print("QoS minimum test was ","succeeded" if succeeded else "falsed")
        self.assertTrue(succeeded)
            
            
    #测试服务质量为2
    def test_qos_two(self):
        print("QoS is minimized test starting")
        message = b"QoS is minimized "
        sub_qos = 2
        result = []
        succeeded = True
        try:
            result = qostest(self,sub_qos=sub_qos,pub_qos=0,message=message)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][2],0,result[0][2])
            self.assertEqual(result[1][2],0,result[0][2])
        except:
            succeeded = False
        self.assertTrue(succeeded)
        try:
            result1 = qostest(self,sub_qos=sub_qos,pub_qos=1,message=message)
            self.assertEqual(len(result1), 2)
            self.assertEqual(result1[0][2],1,result1[0][2])
            self.assertEqual(result1[1][2],1,result1[0][2])
        except:
            succeeded = False
        self.assertTrue(succeeded)
        try:
            result2 = qostest(self,sub_qos=sub_qos,pub_qos=2,message=message)
            self.assertEqual(len(result2), 2)
            self.assertEqual(result2[0][2],2,result2[0][2])
            self.assertEqual(result2[1][2],2,result2[0][2])
        except:
            succeeded = False
        print("QoS minimum test was ","succeeded" if succeeded else "falsed")
        self.assertTrue(succeeded)        
        


    """
        1.验证newsocket为false时，再次连接会连接失败
        
    """
    def test_newsocket_false(self):
        print("the test newcocket is false starting")
        succeeded = True
        try:
            aclient.connect(host=host, port=port)
            aclient.connect(host=host, port=port, newsocket=False) # should fail - second connect on socket
        except Exception as exc:
            succeeded = False
        print("the newcocket test","succeeded" if succeeded else "failed")
        self.assertFalse(succeeded)
    

    """
        1.用户A使用错误的端口名称连接——连接失败
    """
    def test_wrong_protocol_name(self):
        print("the test wrong protocol name starting")
        succeeded = True
        try:
            aclient.connect(host=host, port=port, protocolName="hj") # should fail - wrong protocol name
            succeeded = False
        except Exception as exc:
            pass # exception expected
        print("Wrong protocol name test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    
    """
        1.用户A先订阅topic（+/+）
        2.用户A再向三个topic（"TopicA/B", "Topic/C", "TopicA/C"）发送三条retained=true，qos分别为1、2、3的消息——用户应该收到三条消息
    """
    def test_sub_before_pubretainedmessages(self):
        print("Retained message test starting")
        succeeded = False
        try:
            # retained messages
            callback.clear()
            connack = aclient.connect(host=host, port=port, cleansession=True)
            # #assert connack.flags == 0x00 # Session present
            aclient.subscribe([wildtopics[5]], [2])
            time.sleep(1)
            aclient.publish(topics[1], b"qos 0", 0, retained=True)
            aclient.publish(topics[2], b"qos 1", 1, retained=True)
            aclient.publish(topics[3], b"qos 2", 2, retained=True)
            time.sleep(1)
            aclient.disconnect()
            print(callback.messages)
            print(callback.messages[0][1])
            assert len(callback.messages) == 3
            #目前排序是按照topic命名排序
            for index in range(len(callback.messages)):
                if callback.messages[index][1] == b"qos 0":
                    print(callback.messages[index][1])
                elif callback.messages[index][1] == b"qos 1":
                    print(callback.messages[index][1])
                elif callback.messages[index][1] == b"qos 2":
                    print(callback.messages[index][1])
                else:
                    print("There is no match")
                    succeeded = False

            # clear retained messages
            callback.clear()
            connack = aclient.connect(host=host, port=port, cleansession=True)
            #assert connack.flags == 0x00 # Session present
            aclient.publish(topics[1], b"", 0, retained=True)
            aclient.publish(topics[2], b"", 1, retained=True)
            aclient.publish(topics[3], b"", 2, retained=True)
            time.sleep(1) # wait for QoS 2 exchange to be completed
            aclient.subscribe([wildtopics[5]], [2])
            time.sleep(1)
            aclient.disconnect()

            assert len(callback.messages) == 0, "callback messages is %s" % callback.messages
            succeeded = True
        except:
            traceback.print_exc()
        print("Retained message test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    
    """
        1.用户A先向topic（"TopicA/B", "Topic/C", "TopicA/C"）发送三条retained=true，qos分别为0、1、2消息
        2.用户A在订阅通配topic（+/+）——用户A应该收到三条消息
    """
    def test_online_retained_messages(self):
        print("Retained message test starting")
        succeeded = False
        try:
            # retained messages
            callback.clear()
            connack = aclient.connect(host=host, port=port, cleansession=True)
#             #assert connack.flags == 0x00 # Session present
            print(topics[1],topics[2],topics[3],wildtopics[5])
            aclient.publish(topics[1], b"qos 0", 0, retained=True)
            aclient.publish(topics[2], b"qos 1", 1, retained=True)
            aclient.publish(topics[3], b"qos 2", 2, retained=True)
            time.sleep(5)
            aclient.subscribe([wildtopics[5]], [2])
            time.sleep(1)
            aclient.disconnect()
            print(callback.messages)
            print(callback.messages[0][1])
            assert len(callback.messages) == 3
            #目前排序是按照topic命名排序
            for index in range(len(callback.messages)):
                if callback.messages[index][1] == b"qos 0":
                    print(callback.messages[index][1])
                elif callback.messages[index][1] == b"qos 1":
                    print(callback.messages[index][1])
                elif callback.messages[index][1] == b"qos 2":
                    print(callback.messages[index][1])
                else:
                    print("There is no match")
                    succeeded = False
            # self.assertEqual(callback.messages[0][1],b"qos 0")
            # self.assertEqual(callback.messages[1][1],b"qos 1")
            # self.assertEqual(callback.messages[2][1],b"qos 2")

            # clear retained messages
            callback.clear()
            connack = aclient.connect(host=host, port=port, cleansession=True)
            # #assert connack.flags == 0x00 # Session present
            aclient.publish(topics[1], b"", 0, retained=True)
            aclient.publish(topics[2], b"", 1, retained=True)
            aclient.publish(topics[3], b"", 2, retained=True)
            time.sleep(5) # wait for QoS 2 exchange to be completed
            aclient.subscribe([wildtopics[5]], [2])
            time.sleep(1)
            aclient.disconnect()

            assert len(callback.messages) == 0, "callback messages is %s" % callback.messages
            succeeded = True
        except:
            traceback.print_exc()
        print("Retained message test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    """
        1.用户A在线向一个topic发送三条，retained=true，qos分别为0、1、2的消息
        2.用户B连接登陆成功后，订阅此topic后——应该收到1条最新的消息
    """
    def test_offline_reatin_message(self):
        print("offline reatin message test starting")
        succeeded = False
        try:
            callback.clear()
            callback2.clear()
            connack = aclient.connect(host=host, port=port, cleansession=True)
            # #assert connack.flags == 0x00 # Session present
            aclient.publish(topics[1], b"qos 0", 0, retained=True)
            aclient.publish(topics[1], b"qos 1", 1, retained=True)
            aclient.publish(topics[1], b"qos 2", 2, retained=True)
            time.sleep(5)
            connack = bclient.connect(host=host, port=port, cleansession=True)
            bclient.subscribe([topics[1]], [2])
            time.sleep(1)
            print(callback2.messages)
            assert len(callback2.messages) == 1
            self.assertEqual(callback2.messages[0][1], b"qos 2")
            succeeded = True
        except:
            traceback.print_exc()
        print("offline reatin message test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    
    """
        1.用户A向topic发送retained=True，qos分别为0、1、2消息
        2.用户B连接登陆成功后，未订阅步骤1中的tiopic，则不会收到消息
    """
    def test_nosub_reatin_message(self):
        print("nosub reatin message test starting")
        succeeded = False
        try:
            # retained messages
            callback.clear()
            callback2.clear()
            connack = aclient.connect(host=host, port=port, cleansession=True)
            #assert connack.flags == 0x00 # Session present
            print(topics[1])
            aclient.publish(topics[1], b"qos 0", 0, retained=True)
            aclient.publish(topics[1], b"qos 1", 1, retained=True)
            aclient.publish(topics[1], b"qos 2", 2, retained=True)
            time.sleep(5)
#             aclient.disconnect()
#             time.sleep(1)
            connack = bclient.connect(host=host, port=port, cleansession=True)
            print(topics[2])
            bclient.subscribe([topics[2]], [2])
            time.sleep(1)
            print(callback2.messages)
            assert len(callback2.messages) == 0
            succeeded = True
        except:
            traceback.print_exc()
        print("nosub reatin message test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    
    def test_pub_reatin_message_before_sub(self):
        print("nosub reatin message test starting")
        succeeded = False
        try:
            # retained messages
            callback.clear()
            callback2.clear()
            connack = aclient.connect(host=host, port=port, cleansession=True)
#             #assert connack.flags == 0x00 # Session present
            aclient.publish(topics[1], b"qos 0", 0, retained=True)
            aclient.publish(topics[1], b"qos 1", 1, retained=True)
            aclient.publish(topics[1], b"qos 2", 2, retained=True)
            time.sleep(5)
#             aclient.disconnect()
#             time.sleep(1)
            connack = bclient.connect(host=host, port=port, cleansession=True)
            bclient.subscribe([topics[1]], [2])
            time.sleep(1)
            print(callback2.messages)
            assert len(callback2.messages) == 1
            self.assertEqual(callback2.messages[0][1], b"qos 2")
            succeeded = True
        except:
            traceback.print_exc()
        print("nosub reatin message test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    
    def test_reatin_true_false_message(self):
        print("reatin is true and false message test starting")
        succeeded = False
        try:
            # retained messages
            callback.clear()
            callback2.clear()
            connack = bclient.connect(host=host, port=port, cleansession=True)
            bclient.subscribe([topics[1]], [2])
            
            connack = aclient.connect(host=host, port=port, cleansession=True)
#             #assert connack.flags == 0x00 # Session present
            aclient.publish(topics[1], b"qos 0", 0, retained=True)
#             aclient.publish(topics[2], b"qos 1", 1, retained=True)
            aclient.publish(topics[1], b"qos 1", 1, retained=False)
            aclient.publish(topics[1], b"qos 2", 2, retained=True)
#             aclient.publish(topics[1], b"", 2, retained=True)
            time.sleep(1)
            aclient.disconnect()
            time.sleep(1)
            bclient.disconnect()
            print(callback2.messages)
            print(len(callback2.messages))
            assert len(callback2.messages) == 3
            self.assertEqual(callback2.messages[0][1], b"qos 0")
            self.assertEqual(callback2.messages[1][1], b"qos 1")
            self.assertEqual(callback2.messages[2][1], b"qos 2")
            succeeded = True
        except:
            traceback.print_exc()
        print("reatin is true and false message test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    

    """
        1.测试遗嘱消息
    """
    def test_will_message(self):
      # will messages
      print("Will message test starting")
      succeeded = True
      callback2.clear()
      assert len(callback2.messages) == 0, callback2.messages
      try:
        connack = aclient.connect(host=host, port=port, cleansession=True, willFlag=True,
          willTopic=topics[2], willMessage=b"client not disconnected", keepalive=2)
        # #assert connack.flags == 0x00 # Session present
        connack = bclient.connect(host=host, port=port, cleansession=False)
        bclient.subscribe([topics[2]], [2])
        time.sleep(.1)
        print("usera shutdown")
        aclient.terminate()
        time.sleep(5)
        # bclient.disconnect()
        bclient.terminate()
        print("user B shutdown")
  
        print(callback2.messages)
        assert len(callback2.messages) == 1, callback2.messages  # should have the will message
        self.assertEqual(callback2.messages[0][1],b"client not disconnected")
      except:
        traceback.print_exc()
        succeeded = False
      print("Will message test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded



    """
    1.未订阅遗嘱topic不会收到消息
    """
    def test_nosub_will_message(self):
        print("nosub will message test starting")
        succeeded = True
        callback2.clear()
        assert len(callback2.messages) == 0, callback2.messages
        try:
            connack = aclient.connect(host=host, port=port, cleansession=True, willFlag=True,
              willTopic=topics[2], willMessage=b"client not disconnected", keepalive=2)
            # #assert connack.flags == 0x00 # Session present
            connack = bclient.connect(host=host, port=port, cleansession=False)
            bclient.subscribe([topics[3]], [2])
            time.sleep(.1)
            aclient.terminate()
            time.sleep(5)
            bclient.disconnect()
            print(callback2.messages)
            assert len(callback2.messages) == 0, callback2.messages  # should have the will message
#             self.assertEqual(callback2.messages[0][1],b"client not disconnected")
        except:
            traceback.print_exc()
            succeeded = False
        print("nosub will message test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    """
        1.修改遗嘱消息
    """
    def test_will_message_revise(self):
        print("revise will message test starting")
        succeeded = True
        callback2.clear()
        assert len(callback2.messages) == 0, callback2.messages
        try:
            connack = aclient.connect(host=host, port=port, cleansession=False, willFlag=True,
              willTopic=topics[2], willMessage=b"will message",willQoS=2)
            connack = bclient.connect(host=host, port=port, cleansession=False)
            bclient.subscribe([topics[2]], [2])
            time.sleep(1)
            callback3.clear()
            print("new user login")
            connack = cclient.connect(host=host, port=port, cleansession=False,willFlag=True,
              willTopic=topics[2], willMessage=b" new will messages")
            print("usera login succeeded")
            cclient.terminate()
            print("user c shutdown")
            time.sleep(5)
            print(callback3.messages)
            print(callback2.messages)
            print(callback.messages)
            assert len(callback2.messages) == 1, callback2.messages  # should have the will message
            self.assertEqual(callback2.messages[0][1],b" new will messages")
        except:
            traceback.print_exc()
            succeeded = False
        print("revise will message test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    

    """
        1.测试遗嘱消息服务质量为零与订阅此topic，服务质量取最小值
    """
    def test_will_message_qos_zero(self):
        # will messages
        print("Will message qos0 test starting")
        willQos=0
        succeeded = True
        try:
            result = will_message_qos(self,willQos=willQos,subQos=0)
            assert len(result) == 1
            self.assertEqual(result[0][2],0)
        except:
            traceback.print_exc()
            succeeded = False
        succeeded = True
        try:
            result = will_message_qos(self,willQos=willQos,subQos=1)
            assert len(result) == 1
            self.assertEqual(result[0][2],0)
        except:
            traceback.print_exc()
            succeeded = False
        succeeded = True
        try:
            result = will_message_qos(self,willQos=willQos,subQos=2)
            assert len(result) == 1
            self.assertEqual(result[0][2],0)
        except:
            traceback.print_exc()
            succeeded = False
        print("Will message qos0 test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)




    """   
        1。测试遗嘱消息服务质量为1与订阅此topic，服务质量取最小值
    """
    def test_will_message_qos_one(self):
        print("Will message qos1 test starting")
        willQos=1
        succeeded = True
        try:
            result = will_message_qos(self,willQos=willQos,subQos=0)
            assert len(result) == 1
            self.assertEqual(result[0][2],0)
        except:
            traceback.print_exc()
            succeeded = False
        print("subqos =1")
        succeeded= True
        try:
            result = will_message_qos(self,willQos=willQos,subQos=1)
            assert len(result) == 1
            self.assertEqual(result[0][2],willQos)
        except:
            traceback.print_exc()
            succeeded = False

        print("subqos =2")
        succeeded= True
        try:
            result = will_message_qos(self,willQos=willQos,subQos=2)
            assert len(result) == 1
            self.assertEqual(result[0][2],willQos)
        except:
            traceback.print_exc()
            succeeded = False
        print("Will message qos1 test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
    
    """
        1.测试遗嘱消息服务质量为2与订阅此topic，服务质量取最小值
    """
    def test_will_message_qos_two(self):
        # will messages
        print("Will message qos2 test starting")
        willQos=2
        succeeded = True
        try:
            result = will_message_qos(self,willQos=willQos,subQos=0)
            assert len(result) == 1
            self.assertEqual(result[0][2],0)
        except:
            traceback.print_exc()
            succeeded = False
        succeeded = True
        try:
            result = will_message_qos(self,willQos=willQos,subQos=1)
            assert len(result) == 1
            self.assertEqual(result[0][2],1)
        except:
            traceback.print_exc()
            succeeded = False
        succeeded = True
        try:
            result = will_message_qos(self,willQos=willQos,subQos=2)
            assert len(result) == 1
            self.assertEqual(result[0][2],willQos)
        except:
            traceback.print_exc()
            succeeded = False
        print("Will message qos2 test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return callback2.messages
  
    """
        1.使用错误的cliendid格式，例如：deviceid#id
    """
    @unittest.skipIf(authentication == True,"not run")
    def test_clientid_error_format_one(self):
        print("error cliendid format \"eviceid#id\"test starting")
        clientid = error_cliendid["error_format_one"]
        print(clientid,username1,password1)
        succeeded = clientidtest(self,clientid,username1,password1)
        self.assertEqual(succeeded, True)
        print("error cliendid format  test %s"%("succeeded") if succeeded else "is not")



    """
        1.使用错误的cliendid格式正确的deviceid和appid的，未有连接符号@，例如：deviceid1wyp94
    """
    @unittest.skipIf(authentication == True,"not run")
    def test_clientid_error_format_two(self):
        print("error cliendid format \'deviceidid\'test starting")
        clientid = error_cliendid["error_format_two"]
        password = password1
        print(clientid,username1,password)
        succeeded = clientidtest(self,clientid,username1,password)
        self.assertEqual(succeeded, False)
        print("error cliendid format  test %s"%("succeeded") if succeeded else "is not")



        
    """
        1.clientid中使用appid为空,例如：devicesid@
    """
    @unittest.skipIf(authentication == True,"Not Run")
    def test_cliendid_contains_no_appid(self):
        print("cliendid contains no appid test starting")
        clientid = error_cliendid["appid_empty"]
        username = username1
        password = password1
        print(clientid,username,password)
        succeeded = clientidtest(self,clientid,username,password)
        self.assertEqual(succeeded, False)
        print("cliendid contains no appid test starting")



    
    """
        1.测试clientid最大字节为64位
    """
    def test_clientid_length_64(self):
        print("Starting:ClientId has a maximum length of 64")
        succeeded = True
        try:
            print("length clientid %d"%(len(length_clientid)))
            client0 = mqtt_client.Client(length_clientid.encode("utf-8"))
            client0.registerCallback(callback)
            client0.setUserName(username1, password1)
            connect = bclient.connect(host=host,port=port,cleansession=True)
            print(wildtopics[0],topics[1])
            bclient.subscribe([wildtopics[0]],[2])
            connect = client0.connect(host=host,port=port,cleansession=True)
            client0.publish(topics[1],b"test",1,retained=False)
            time.sleep(.1)
            print(len(callback2.messages))
            assert len(callback2.messages) == 1
            self.assertEqual(callback2.messages[0][1],b"test")
        except:
            traceback.print_exc()
            succeeded = False
        print("ClientId has a maximum length of 64 is %s""succeed"if succeeded else "failed")
        assert succeeded == True



    """
        1.测试cliendid最大字节超过64位
    """
    def test_clientid_length_65(self):
        print("Starting:ClientId has a maximum length of 65")
        succeeded = False
        try:
            client0 = mqtt_client.Client(error_cliendid["overlength_clientid"].encode("utf-8"))
            client0.setUserName(username1,password1)
            connect = client0.connect(host=host,port=port,cleansession=True)
        except:
            traceback.print_exc()
            succeeded = True
        print("ClientId has a maximum length of 65 is %s""succeeded"if succeeded else "failed")
        self.assertEqual(succeeded,True)



    """
        1.测试设备使用相同的clientid登陆，先登陆的用户被挤掉(先使用客户端使用)
    """
    def test_clientid_same_login(self):
        print("clientid same test starting")
        succeeded = True
        try:
            connect = aclient.connect(host=host, port=port, cleansession=False) # 用户A登陆
            print(wildtopics[0],topics[1])
            aclient.subscribe([wildtopics[0]],[2])
            time.sleep(.1)
            connect = cclient.connect(host=host, port=port, cleansession=False)  #使用相同的clientid再次登陆
            cclient.publish(topics[1],b"test clientid same connect",2,retained=False)
            time.sleep(.1)
            print(callback.messages)
            print(callback3.messages)
            assert len(callback3.messages) == 1
        except:
            traceback.print_exc()
            succeeded = False
        print("error appkey clientid test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded

        
    """
        1.测试clientid长度为0
    """
    def test_clientid_zero_length(self):
        print("Zero length clientid test starting")
        succeeded = True
        try:
            client0 = mqtt_client.Client("")
            fails = False
            try:
                client0.connect(host=host, port=port, cleansession=False) # should be rejected        
            except:
                fails = True
            print(fails)
            self.assertEqual(fails, True)
            try:
                client0.connect(host=host, port=port, cleansession=True) # should work(目前环信clientid为空字符串时，连接会被拒)
            except:
                fails = True
            self.assertEqual(fails, True)
            client0.disconnect()
        except:
            traceback.print_exc()
            succeeded = False
        print("Zero length clientid test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded,True)
        return succeeded


    """
        1.测试离线消息
    """
    def test_offline_message_queueing(self):
        succeeded = True
        try:
            # message queueing for offline clients
            callback.clear()
            #用户A登陆
            connack = aclient.connect(host=host, port=port, cleansession=False)
            #用户A订阅一个topic
            aclient.subscribe([wildtopics[5]], [2])
            #用户B断开连接
            aclient.disconnect()
            #用户B登陆
            connack = bclient.connect(host=host, port=port, cleansession=True)
            #assert connack.flags == 0x00 # Session present
            #用户B分别向"TopicA/B", "Topic/C", "TopicA/C"发送qos0、1、2消息
            bclient.publish(topics[1], b"qos 0", 0)
            bclient.publish(topics[2], b"qos 1", 1)
            bclient.publish(topics[3], b"qos 2", 2)
            time.sleep(2)
            bclient.disconnect()
            #用户A再次登陆
            connack = aclient.connect(host=host, port=port, cleansession=False)
            # assert connack.flags == 0x01 # Session present
            time.sleep(2)
            # aclient.disconnect()
            aclient.terminate()
            print("user A shutdown")
            #判断用户A收到离线消息（0的消息不会收到）
            print(callback.messages)
            assert len(callback.messages) in [2, 3], callback.messages
            for index in range(len(callback.messages)):
                if callback.messages[index][1] == b"qos 1":
                    print(callback.messages[index][1])
                elif callback.messages[index][1] == b"qos 2":
                    print(callback.messages[index][1])
                else:
                    print("the test fail")
                    succeeded = False
            # self.assertEqual(callback.messages[0][1],b"qos 1")
            # self.assertEqual(callback.messages[1][1],b"qos 2")
            print("This server %s queueing QoS 0 messages for offline clients" % \
                ("is" if len(callback.messages) == 3 else "is not"))
        except:
            traceback.print_exc()
            succeeded = False
        print("Offline message queueing test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded


    """
        1.测试消息最大长度为50字节（官网规定最大字节是65535，为了测试，目前嘉豪给设置的最大字节是50）
    """
    def test_send_message_length_50(self):
        print("Staring：The maximum length of offline messages is 50")
        succeeded =  True
        number = 50
        f = generate_random_str(number) #随机构建一个指定字符串
        message = bytes(f, encoding='utf-8')    #将字符串转化为bytes
        time.sleep(2)
        # message = b"12345678901234567890123456789012345678901234567890"
        try:
            connect = aclient.connect(host=host,port=port)
            print(wildtopics[0],topics[1])
            aclient.subscribe([wildtopics[0]],[2])
            time.sleep(.1)
            connect = bclient.connect(host=host,port=port)
            bclient.publish(topics[1],message,2,retained=False)
            time.sleep(2)
            print(callback.messages)
            self.assertEqual(len(callback.messages),1)
            aclient.disconnect
            bclient.disconnect
        except:
            traceback.print_exc()
            succeeded = False
        print(len(callback.messages))
        print("The maximum length of messages is 50 ""success" if succeeded else "failed" )
        self.assertEqual(succeeded,True)


    """
        1.发送消息字节书超过50个，此条消息被丢弃(appconfig默认配置是65535)
    """
    def test_send_message_length_65536(self):
        print("Staring：The maximum length of offline messages is 50")   
        succeeded =  True     
        number = 65536
        f = generate_random_str(number) #随机构建一个指定字符串
        message = bytes(f, encoding='utf-8')    #将字符串转化为bytes
        time.sleep(1)
        try:
            connect = aclient.connect(host=host,port=port,cleansession=False)
            print(wildtopics[0],topics[1])
            aclient.subscribe([wildtopics[0]],[2])
            time.sleep(.1)
            connect = bclient.connect(host=host,port=port,cleansession=True)
            bclient.publish(topics[1],message,2,retained=False)
            time.sleep(2)
            print(callback.messages)
            assert len(callback.messages) == 0
            aclient.disconnect
            bclient.disconnect
        except:
            traceback.print_exc()
            succeeded = False
        print(len(callback.messages))
        print("The maximum length of messages is 50 ""success" if succeeded else "failed" )
        self.assertEqual(succeeded,True)


    """
        1.离线消息最大条数为100条
    """
    def test_offline_message_number_ten(self):
        print("Staring：The maximum number of offline messages is 100")
        number = 50
        succeeded =  True
        try:
            connect = aclient.connect(host=host,port=port,cleansession=False)
            print(wildtopics[0],topics[1])
            aclient.subscribe([wildtopics[0]],[2])
            time.sleep(.1)
            aclient.disconnect
            time.sleep(5)
            connect = bclient.connect(host=host,port=port,cleansession=True)
            for index in range(number):
                bclient.publish(topics[1],b'message %d'%(index),2,retained=False)
            time.sleep(2)
            for num in range(number):
                bclient.publish(topics[1],b'message retained=true %d'%(num),1,retained=True)
            time.sleep(2)
            connect = aclient.connect(host=host,port=port,cleansession=False)
            time.sleep(5)
            print(callback.messages)
            aclient.disconnect()
            bclient.disconnect()
        except:
            traceback.print_exc()
            succeeded = False
        print("the offline message number is %d"%(len(callback.messages)))
        assert len(callback.messages) == number*2
        print("The maximum number of offline messages is 100 ""success" if succeeded else "failed" )
        self.assertEqual(succeeded,True)




    """
        1.离线消息超过100条后，只保留100+1条，删除最老的数据
    """
    def test_offline_message_number_eleven(self):
        print("Staring：The maximum number of offline messages is 100")
        succeeded =  True
        number = 51
        try:
            connect = aclient.connect(host=host,port=port,cleansession=False)
            print(wildtopics[0],topics[1])
            aclient.subscribe([wildtopics[0]],[1])
            time.sleep(.1)
            print("waiting for disconnect")
            aclient.disconnect()
            print("disconnect succeeded")
            time.sleep(5)   #等待断开连接
            connect = bclient.connect(host=host,port=port,cleansession=True)
            for index in range(number):
                bclient.publish(topics[1],b'test offline message qos2 num is %d'%(index),2,retained=False)
            for num in range(number):
                bclient.publish(topics[1],b'test offline message qos1 num is %d'%(num),1,retained=False)
            time.sleep(2)
            connect = aclient.connect(host=host,port=port,cleansession=False)
            time.sleep(5)
            print(callback.messages)
            aclient.terminate()
            bclient.terminate()
            time.sleep(1)
            # aclient.disconnect()
            # bclient.disconnect()
        except:
            traceback.print_exc()
            succeeded = False
        print(len(callback.messages))
        assert len(callback.messages) == number*2-1 #目前离线消息callback.messages中应该10+1，10为离线消息数，1为最后一次发送消息一直在尝试发送。
        print("The maximum number of offline messages is 100 ""success" if succeeded else "failed" )
        self.assertEqual(succeeded,True)



    """
        1.测试订阅topic qos=0时，离线消息数量应该为零
    """
    def test_offline_message_qos0_zero(self):
        print("Staring：The maximum number of offline messages is zero")
        succeeded =  True
        try:
            connect = aclient.connect(host=host,port=port,cleansession=False)
            print(wildtopics[0],topics[1])
            aclient.subscribe([wildtopics[0]],[0])
            time.sleep(.1)
            aclient.disconnect()
            time.sleep(5)   #等待断开连接
            connect = bclient.connect(host=host,port=port,cleansession=True)
            for index in range(1,6):
                bclient.publish(topics[1],b'test offline message qos2 num is %d'%(index),2,retained=False)
            for index in range(1,6):
                bclient.publish(topics[1],b'test offline message qos1 num is %d'%(index),1,retained=False)
            time.sleep(2)
            connect = aclient.connect(host=host,port=port,cleansession=False)
            time.sleep(5)
            print(callback.messages)
            aclient.disconnect()
            bclient.disconnect()
        except:
            traceback.print_exc()
            succeeded = False
        print(len(callback.messages))
        assert len(callback.messages) == 0 #当订阅或者发布topic中存在qod=0，那么是不会存在离线消息
        print("The maximum number of offline messages is zero ""success" if succeeded else "failed" )
        self.assertEqual(succeeded,True)



    """
        1.测试重复订阅
    """
    def test_overlapping_subscriptions(self):
        # overlapping subscriptions. When there is more than one matching subscription for the same client for a topic,
        # the server may send back one message with the highest QoS of any matching subscription, or one message for
        # each subscription with a matching QoS.
        print("Overlapping subscriptions test starting")
        succeeded = True
        try:
            callback.clear()
            callback2.clear()
            aclient.connect(host=host, port=port)
            #注释wildtopics[6]=="TopicA/#",wildtopics[0]="TopicA/+"
            print(wildtopics[6], wildtopics[0])
            aclient.subscribe([wildtopics[6], wildtopics[0]], [2, 1])
            #注释topics[3]="TopicA/C"
            aclient.publish(topics[3], b"overlapping topic filters", 2)
            time.sleep(1)
            print(callback.messages)
            assert len(callback.messages) in [1, 2]
            #打印出callback.messages
            if len(callback.messages) == 1:
              print("This server is publishing one message for all matching overlapping subscriptions, not one for each.")
              assert callback.messages[0][2] == 2
              self.assertCountEqual(callback.messages[0][1], b"overlapping topic filters")
            else:
              print("This server is publishing one message per each matching overlapping subscription.")
              assert (callback.messages[0][2] == 2 and callback.messages[1][2] == 1) or \
                     (callback.messages[0][2] == 1 and callback.messages[1][2] == 2), callback.messages
              self.assertCountEqual(callback.messages[0][1], b"overlapping topic filters")
              self.assertCountEqual(callback.messages[1][1], b"overlapping topic filters")
              aclient.disconnect()
        except:
            traceback.print_exc()
            succeeded = False
        print("Overlapping subscriptions test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded




    def test_keepalive(self):
      # keep_alive processing.  We should be kicked off by the server if we don't send or receive any data, and don't send
      # any pings either.
      print("Keep_alive test starting")
      succeeded = True
      try:
        callback2.clear()
        aclient.connect(host=host, port=port, cleansession=True, keepalive=5, willFlag=True,
              willTopic=topics[4], willMessage=b'keepalive_expiry')
        bclient.connect(host=host, port=port, cleansession=True, keepalive=0)
        #注释topics[4]=TopicA/C
        bclient.subscribe([topics[4]], [2])
        time.sleep(15)
        bclient.disconnect()
        print(callback2.messages)
        self.assertEqual(callback2.messages[0][1], b"keepalive_expiry")
        assert len(callback2.messages) == 1, "length should be 1: %s" % callback2.messages # should have the will message
      except:
        traceback.print_exc()
        succeeded = False
      print("Keepalive test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded


    def test_redelivery_on_reconnect(self):
      # redelivery on reconnect. When a QoS 1 or 2 exchange has not been completed, the server should retry the
      # appropriate MQTT packets
      print("Redelivery on reconnect test starting")
      succeeded = True
      try:
        callback.clear()
        callback2.clear()
        bclient.connect(host=host, port=port, cleansession=False)
        bclient.subscribe([wildtopics[6]], [2])
        bclient.pause() # stops responding to incoming publishes
        bclient.publish(topics[1], b"", 1, retained=False)  #注释topics[1]=TopicA/B,
        bclient.publish(topics[3], b"", 2, retained=False)  #注释topics[3]="TopicA/C"
        time.sleep(1)
        bclient.disconnect()
        assert len(callback2.messages) == 0, "length should be 0: %s" % callback2.messages
        bclient.resume()
        bclient.connect(host=host, port=port, cleansession=False)
        time.sleep(3)
        print(callback2.messages)
        assert len(callback2.messages) == 2
        self.assertEqual(callback2.messages[0][1], b"")
        self.assertEqual(callback2.messages[1][1], b"")
        bclient.disconnect()
      except:
        traceback.print_exc()
        succeeded = False
      print("Redelivery on reconnect test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded



    def test_topic_format_nosubscribe_end(self):
      # Subscribe failure.  A new feature of MQTT 3.1.1 is the ability to send back negative reponses to subscribe
      # requests.  One way of doing this is to subscribe to a topic which is not allowed to be subscribed to.
      #中文：此case主要验证了可以订阅/发布已nosubscribe结尾的topic
      print("nosubscribe end test starting")
      succeeded = True
      try:
        callback.clear()
        aclient.connect(host=host, port=port)
        aclient.subscribe([nosubscribe_topics[0]], [2])     #订阅已nosubscribe结尾的topic
        time.sleep(.2)
        # subscribeds is a list of (msgid, [qos])
        print(callback.subscribeds)
        #assert callback.subscribeds[0][1][0] == 0x80, "return code should be 0x80 %s" % callback.subscribeds
        self.assertCountEqual(callback.subscribeds[0][1], [2])
        #aclient.publish(wildtopics[0],b"Test the topic has nosubscribe end",2)
        aclient.publish(nosubscribe_topics[0], b"overlapping topic filters", 2)
        time.sleep(.2)
        assert len(callback.messages) == 1,"callback messages length is %d"%(len(callback.messages))
        aclient.disconnect()
      except:
        traceback.print_exc()
        succeeded = False
      print("Nosubscribe end test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded

    
    
    """
        1.验证通配符#，sub：TopicA/#,pub:TopicA/B
    """
    def test_topic_format_first(self):
        print("topic/# topics test starting")
        succeeded = True
        message=b"test topic/#"
        callbackresult = []
        try:
            callbackresult = topictest(self,sub_index=6,pub_index=1, message=message)
            assert len(callbackresult) == 2
            self.assertEqual(callbackresult[0][1],message,callbackresult[0][1])
            self.assertEqual(callbackresult[1][1],message,callbackresult[0][1])
        except:
            traceback.print_exc()
            succeeded = False
        try:
            callbackresult = topictest(self,sub_index=6,pub_index=5, message=message)
            assert len(callbackresult) == 2
            self.assertEqual(callbackresult[0][1],message,callbackresult[0][1])
            self.assertEqual(callbackresult[1][1],message,callbackresult[0][1])
        except:
            traceback.print_exc()
            succeeded = False
        print(callbackresult)
        print("topic/# topics test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    



    """
        1.验证topic通配符+,sub:"TopicA/+",pub:"TopicA/B"
    """
    def test_topic_format_second(self):
        print("topics:topics/+ test starting")
        succeeded = True
        message=b"test topic:topic/#"
        callbackresult = []
        try:
            callbackresult = topictest(self,sub_index=0,pub_index=1,message=message)
            assert len(callbackresult) == 2,"callback length is %s"%(len(callback))
            self.assertEqual(callbackresult[0][1], message,callbackresult[0][1])
            self.assertEqual(callbackresult[1][1],message,callbackresult[0][1])
        except:
            traceback.print_exc()
            succeeded = False
        try:
            callbackresult = topictest(self,sub_index=0,pub_index=5,message=message)
#             self.assertEqual(callback[0][1], message,callback[0][1])
            assert len(callbackresult) == 0,print("层级不同无法接收到消息"+callbackresult)
        except:
            traceback.print_exc()
            succeeded = False
        print(callbackresult)
        print("topics:topics/+ test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    #验证topic通配符
    def test_topic_format_third(self):
        print("topics format +/# test starting")
        succeeded = True
        message=b"test topic:+/#"
        callbackresult = []
        try:
            callbackresult = topictest(self,sub_index=0,pub_index=1,message=message)
            assert len(callbackresult) == 2,"callback length is %s"%(len(callback))
            self.assertEqual(callbackresult[0][1], message,callbackresult[0][1])
            self.assertEqual(callbackresult[1][1],message,callbackresult[0][1])
        except:
            traceback.print_exc()
            succeeded = False
        try:
            callbackresult = topictest(self,sub_index=0,pub_index=5,message=message)
            #self.assertEqual(callback[0][1], message,callback[0][1])
            assert len(callbackresult) == 0,print("层级不同无法接收到消息"+callbackresult)
        except:
            traceback.print_exc()
            succeeded = False
        print(callbackresult)
        print("topics format +/# test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded

    #验证topic通配符格式为+/#
    #@unittest.skip("由于目前使用EMQ的客户端测试，pub消息太多，导致卡死。目前不测试，需要修改case")
    def test_topic_format_hourth(self):
        print("topics format +/# test starting")
        succeeded = True
        message=b"test topic:+/#"
        callbackresult = []
        try:
            callbackresult = topictest(self,sub_index=7,pub_index=1,message=message)
            self.assertEqual(len(callbackresult), 2,"callbackresult is %s"%(callbackresult))
            self.assertEqual(callbackresult[0][1],message)
            self.assertEqual(callbackresult[1][1],message)
        except:
            traceback.print_exc()
            succeeded = False
        try:
            callbackresult = topictest(self,sub_index=7,pub_index=5,message=message)
            self.assertEqual(len(callbackresult), 2,"callbackresult is $s"%(callbackresult))
            self.assertEqual(callbackresult[0][1],message)
            self.assertEqual(callbackresult[1][1],message)
        except:
            traceback.print_exc()
            succeeded = False
        print(callback)
        print("topics format +/#  test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    
    #验证topic格式为+/+匹配规则
    def test_topic_format_fifth(self):
        print("test topic:+/+ starting")
        succeeded = True
        try:
            callback.clear()
            connack = aclient.connect(host=host, port=port, cleansession=True)
            print(wildtopics[5])
            aclient.subscribe([wildtopics[5]], [2])
            connack = bclient.connect(host=host, port=port, cleansession=True)
            # #assert connack.flags == 0x00 # Session present
            print(topics[1],topics[2],topics[3])
            bclient.publish(topics[1], b"qos 0", 0)
            bclient.publish(topics[2], b"qos 1", 1)
            bclient.publish(topics[3], b"qos 2", 2)
            time.sleep(2)
            print(callback.messages)
            assert len(callback.messages) == 3
            self.assertEqual(callback.messages[0][1],b"qos 0")
            self.assertEqual(callback.messages[1][1],b"qos 1")
            self.assertEqual(callback.messages[2][1],b"qos 2")
            
            time.sleep(2)
            aclient.disconnect()
            bclient.disconnect()
        except:
            traceback.print_exc()
            succeeded = False
        print("test topic:+/+ ", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    #验证topic层级为9层（目前只限制最大字符，未限制层数）
    def test_topic_format_sixth(self):
        print("topics format topicA/B/C/D/E/F/G/H/I test starting")
        succeeded = True
        #订阅topic层级为9层
        try:
            connect = aclient.connect(host=host,port=port,cleansession=True)
            print(topics[-2])
            print("user sub")
            aclient.subscribe([topics[-2]],[2])
            print("assert result")
            print(len(callback.subscribeds))
            assert callback.subscribeds[1] == 0
            aclient.disconnect()
        except:
            succeeded =  False
        #发布消息topic层级为9层
        print("user pub")
        succeeded = True
        try:
            connect = bclient.connect(host=host,port=port,cleansession=True)
            print(topics[-2])
            print("user pub")
            bclient.publish(topics[-2],b'abc',2,retained=False)
            print("user pub succeeded")
            time.sleep(1)
            bclient.disconnect()
            print("user disconnect")
        except:
            succeeded =  False
        print("topics format topicA/B/C/D/E/F/G/H/I  test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    
    
    #验证topic层级为8层
    def test_topic_format_seventh(self):
        print("topics format topic/a/b/c/d/e/f/g test starting")
        succeeded = True
        message = b"test"
        #订阅和发布topic层级为8层
        try:
            callbackresult = topictest(self,sub_index=-1,pub_index=-1,message=message)
            print(topics[-1])
            print(wildtopics[-1])
            self.assertEqual(len(callbackresult), 2,"callbackresult is %s"%(callbackresult))
            self.assertEqual(callbackresult[0][1],message)
            self.assertEqual(callbackresult[1][1],message)
            self.assertEqual(callbackresult[0][0],topics[-1])
            self.assertEqual(callbackresult[1][0],wildtopics[-1])
        except:
            traceback.print_exc()
            succeeded = False
        print("topics format topic/a/b/c/d/e/f/g  test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded


    """
        1.验证topic中字符串长度大于64时，订阅和发布失败
    """
    def test_topic_format_length65(self):
        special_topic = "12345678901234567890123456789012345678901234567890123456789012345"
        print("topic length is %d"%(len(special_topic)))
        print("topics format %s test starting"%(special_topic))   #由于目前使用EMQ的客户端测试，pub消息太多，导致卡死。目前不测试
        succeeded = False
        #订阅topic超过64位，不会订阅阅成功
        try:
            connect = aclient.connect(host=host,port=port,cleansession=True)
            aclient.subscrible([special_topic],[2])
            # assert len(callback.subscribeds) == 0
            
        except:
            succeeded =  True
        #发布消息topic超过64位，不会发布成功
        try:
            connect = bclient.connect(host=host,port=port,cleansession=True)
            bclient.pubscrible([special_topic],[2])
            time.sleep(1)
            bclient.disconnect()
        except:
            succeeded =  True
        aclient.disconnect()
        assert len(callback.messages) == 0
        print("topics format %s  test"%(special_topic), "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    """
        1.验证topic通配符格式为#/#，订阅失败
    """
    def test_topic_format_ninth(self):
        special_topic = "#/#"
        print(len(special_topic))
        print("topics format %s test starting"%(special_topic))
        succeeded =  False 
        #订阅topic为#/#
        try:
            connect = aclient.connect(host=host,port=port,cleansession=True)
            aclient.subscrible([special_topic],[2])
            assert len(callback.subscribeds) == 0
            aclient.disconnect()
        except:
            succeeded =  True
        #发布消息topic为#/#
        try:
            connect = bclient.connect(host=host,port=port,cleansession=True)
            bclient.pubscrible([special_topic],[2])
            time.sleep(1)
            bclient.disconnect()
        except:
            succeeded =  True
        print("topics format %s  test"%(special_topic), "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    
    #验证topic通配符格式为#/+，订阅失败
    def test_topic_format_tenth(self):
        special_topic = "#/+"
        print(len(special_topic))
        print("topics format %s test starting"%(special_topic)) 
        #订阅topic为#/#
        succeeded =  False
        try:
            connect = aclient.connect(host=host,port=port,cleansession=True)
            aclient.subscrible([special_topic],[2])
            assert len(callback.subscribeds) == 0
            aclient.disconnect()
        except:
            succeeded =  True
        #发布消息topic为#/#
        try:
            connect = bclient.connect(host=host,port=port,cleansession=True)
            bclient.pubscrible([special_topic],[2])
            time.sleep(1)
            bclient.disconnect()
        except:
            succeeded =  True
        print("topics format %s  test"%(special_topic), "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    


    #订阅层级不相同的topic
    def test_topic_format_eleventh(self):
        print("The testing sub and pub topic levels are different  starting")
        succeeded = True
        message = b"The testing sub and pub topic levels are different"
        try:
            print("======")
            print(topics[2],wildtopics[-1])
            print("!!!!!!")
            result = topictest(self,sub_index=-1, pub_index=2, message=message)
            print(len(result))
            assert len(result) == 0
        except:
            succeeded = False
        print("The testing sub and pub topic levels are different test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
        


    #一个用户订阅了规则不同，但匹配结果相同的topic，此用户可以多条消息
    def test_topic_format_twelfth(self):
        print("The matching results are the same for different topic")
        succeeded = True
        message = b"The matching results are the same for different topic"
        try:
            connect =  aclient.connect(host=host,port=port)
            aclient.subscribe([wildtopics[0]],[2])
            time.sleep(1)
            print("sub topic "+wildtopics[0])
            aclient.subscribe([wildtopics[6]],[2])
            time.sleep(1)
            print("sub topic "+wildtopics[6])
            connect = bclient.connect(host=host,port=port)
            bclient.publish(topics[1],message,1,retained=False)
            print("pub topic "+topics[1])
            time.sleep(2)
            assert len(callback.messages) == 2
            print(callback.messages)
        except:
             succeeded = False
        aclient.disconnect()
        bclient.disconnect()
        print("The matching results are the same for different topic test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded


    """
        1.验证通配符#，sub：TopicA/#,pub:TopicA
    """
    def test_topic_format_thirteenth(self):
        print("sub：TopicA/#,pub:TopicA, topics test starting")
        succeeded = True
        message=b"test topic/#"
        callbackresult = []
        try:
            callbackresult = topictest(self,sub_index=6,pub_index=0, message=message)
            assert len(callbackresult) == 2
            self.assertEqual(callbackresult[0][1],message,callbackresult[0][1])
            self.assertEqual(callbackresult[1][1],message,callbackresult[0][1])
        except:
            traceback.print_exc()
            succeeded = False
        # try:
        #     callbackresult = topictest(self,sub_index=6,pub_index=5, message=message)
        #     assert len(callbackresult) == 2
        #     # self.assertEqual(callbackresult[0][1],message,callbackresult[0][1])
        #     # self.assertEqual(callbackresult[1][1],message,callbackresult[0][1])
        # except:
        #     traceback.print_exc()
        #     succeeded = False
        print(callbackresult)
        print("topic/# topics test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded

    """
        1.验证topic层级为8层,64位字符
    """
    def test_topic_format_length64_fold(self):
        print("topic length is %d"%(len(length64_fold)))
        print("topics format %s test starting"%(length64_fold))
        succeeded = True
        #appconfig中设置topic最大为64位，订阅topic成功
        print("test sub")
        try:
            connect = aclient.connect(host=host,port=port,cleansession=True)
            aclient.subscribe([length64_fold],[1])
            # print(callback.subscribeds)
            # assert len(callback.subscribeds) == 1
            # aclient.disconnect()
        except:
            succeeded =  False
        #appconfig中设置topic最大为64位，向topic发布消息成功
        print(succeeded)
        self.assertEqual(succeeded, True)
        print("test pub")
        try:
            connect = bclient.connect(host=host,port=port,cleansession=True)
            bclient.publish(length64_fold,b"test topic length is 64",2,retained=False)
            time.sleep(1)
            bclient.disconnect()
        except:
            succeeded =  False
        aclient.disconnect()
        assert len(callback.messages) == 1
        print("topics format %s  test"%(length64_fold), "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded


    """
        1.测试topic格式最大允许64位字符
    """
    def test_topic_format_length64(self):
        print("topic length is %d"%(len(length_topic)))
        print("topics format %s test starting"%(length_topic))
        succeeded = True
        #appconfig中设置topic最大为64位，订阅topic成功
        print("test sub")
        try:
            connect = aclient.connect(host=host,port=port,cleansession=True)
            aclient.subscribe([length_topic],[1])
            # print(callback.subscribeds)
            # assert len(callback.subscribeds) == 1
            # aclient.disconnect()
        except:
            succeeded =  False
        #appconfig中设置topic最大为64位，向topic发布消息成功
        print(succeeded)
        self.assertEqual(succeeded, True)
        print("test pub")
        try:
            connect = bclient.connect(host=host,port=port,cleansession=True)
            print("user B login succeed")
            bclient.publish(length_topic,b"test topic length is 64",2,retained=False)
            time.sleep(1)
            bclient.disconnect()
        except:
            succeeded =  False
        aclient.disconnect()
        assert len(callback.messages) == 1
        print("topics format %s  test"%(length_topic), "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded


    
    
    def test_topics_starting_with_dollar(self):
        # $ topics. The specification says that a topic filter which starts with a wildcard does not match topic names that
        # begin with a $.  Publishing to a topic which starts with a $ may not be allowed on some servers (which is entirely valid),
        # so this test will not work and should be omitted in that case.
        print("$ topics test starting")
        succeeded = True
        try:
            callback2.clear()
            bclient.connect(host=host, port=port, cleansession=True, keepalive=0)
            bclient.subscribe([wildtopics[5]], [2])
            time.sleep(1) # wait for all retained messages, hopefully
            callback2.clear()
            bclient.publish("$"+topics[1], b"", 1, retained=False)
            time.sleep(2)
            assert len(callback2.messages) == 0, callback2.messages
            # bclient.disconnect()
        except:
            traceback.print_exc()
            succeeded = False
        print("$ topics test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded


    """
        1.取消订阅topic，不会收到此topic发送消息
    """
    def test_topic_unsubscribe(self):
        print("Unsubscribe test starting")
        succeeded = True
        try:
            callback2.clear()
            bclient.connect(host=host, port=port, cleansession=True)
            bclient.subscribe([topics[0]], [2])
            bclient.subscribe([topics[1]], [2])
            bclient.subscribe([topics[2]], [2])
            time.sleep(1) # wait for all retained messages, hopefully
            # Unsubscribed from one topic
            bclient.unsubscribe([topics[0]])    #取消订阅topics[0]
    
            aclient.connect(host=host, port=port, cleansession=True)
            aclient.publish(topics[0], b"", 1, retained=False)
            aclient.publish(topics[1], b"", 1, retained=False)
            aclient.publish(topics[2], b"", 1, retained=False)
            time.sleep(2)
    
            bclient.disconnect()
            aclient.disconnect()
            print(callback2.messages)
            self.assertEqual(len(callback2.messages), 2, callback2.messages)
        except:
            traceback.print_exc()
            succeeded = False
        self.assertEqual(succeeded, True)
        print("unsubscribe tests", "succeeded" if succeeded else "failed")
        return 
    
    
    def test_repetition_sub(self):
        print("test repetition sub starting")
        succeeded = True
        try:
            callback2.clear()
            callback.clear()
            connack=bclient.connect(host=host, port=port)
            bclient.subscribe([topics[0]], [2])
            time.sleep(1)
            bclient.subscribe([topics[0]], [2])
            time.sleep(1) # wait for all retained messages, hopefully
            aclient.connect(host=host, port=port)
            aclient.publish(topics[0],b"test repetition sub starting", 1, retained=False)
            time.sleep(2)
            print(callback2.messages)
            self.assertEqual(len(callback2.messages), 1)
            self.assertEqual(callback2.messages[0][1], b"test repetition sub starting")
            bclient.disconnect()
        except:
            traceback.print_exc()
            succeeded = False
        self.assertEqual(succeeded, True)
        print("test repetition sub tests", "succeeded" if succeeded else "failed")
        return succeeded
    @unittest.skip("reason")
    def tset_1(self):
        print("Basic test starting")
        global aclient
        succeeded = True
        try:
            aclient.connect(host=host, port=port)
            aclient.disconnect()
    
            connack = aclient.connect(host=host, port=port)
            # #assert connack.flags == 0x00 # Session present
            aclient.subscribe([topics[0]], [2])
            aclient.publish(topics[0], b"qos 0")
            aclient.publish(topics[0], b"qos 1", 1)
            aclient.publish(topics[0], b"qos 2", 2)
            time.sleep(2)
            aclient.disconnect()
            print(callback.messages)
            self.assertEqual(len(callback.messages), 3)
        except:
            traceback.print_exc()
            succeeded = False
        
        print("Basic test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded

if __name__ == "__main__":
    try:
      opts, args = getopt.gnu_getopt(sys.argv[1:], "h:p:zdsn:",
        ["help", "hostname=", "port=", "iterations="])
    except getopt.GetoptError as err:
      print(err) # will print something like "option -a not recognized"
      usage()
      sys.exit(2)

    iterations = 1
    for o, a in opts:
      if o in ("--help"):
        usage()
        sys.exit()
      elif o in ("-n", "--nosubscribe_topic_filter"):
        nosubscribe_topic_filter = a
      elif o in ("-h", "--hostname"):
        host = a
      elif o in ("-p", "--port"):
        port = int(a)
      elif o in ("--iterations"):
        iterations = int(a)
      else:
        assert False, "unhandled option"

    root = logging.getLogger()
    root.setLevel(logging.ERROR)

    print("hostname", host, "port", port)
 
    for i in range(iterations):
        unittest.main()
    #创建测试集
    # suite = unittest.TestSuite()
    # suite.addTest(Test("test_cleansession_false"))
    # suite.addTest(Test("test_seventh_topic_format"))
    # suite.addTest(Test("test_will_message_qos_one"))
    # suite.addTest(Test("test_zero_length_clientid"))
    # suite.addTest(Test("test_online_retained_messages"))
    # suite.addTest(Test("test_nosub_reatin_message"))
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)

    #生成测试报告
#     suite = unittest.TestSuite()  #实例化
#     suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Test))
#     now = time.strftime("%Y-%m%d %H%M%S")
#     print(now)
#     report_path = "//Users//mac//easemob//auto_test//paho.mqtt.testing//interoperability//" + now + "report.html"
#     fp = open(report_path,"wb")
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=fp,
#         title=u"test report",
#         description=u"用例执行情况"
#         )
#     runner.run(suite)
#     fp.close()
