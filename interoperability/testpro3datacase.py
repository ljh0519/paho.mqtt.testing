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
    try:
        client0 = mqtt_client.Client(clientid.encode("utf-8"))
        fails = True
        # try:
        client0.connect(host=host, port=port, cleansession=True,username=username,password=apppassword) # should work
        print(wildtopics[0],topics[1])
        client0.subscribe([wildtopics[0]],[2])
        time.sleep(.1)
        client0.publish(topics[1],"test cliendid",2,retained=False)
        time.sleep(1)
        print(callback3.messages)
        assert len(callback3.messages) ==2
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


def build_user(self,number):
  for i in range(number):
    clientid1 = "deviceid%s"%(i) + "@" + "1wyp94"
    print(clientid1)
    aclient = "aclient%s"%(i)
    print("aclient is %s"%aclient)
    aclient = mqtt_client.Client(clientid1.encode("utf-8"))
    callback = "callback%s"%(i)
    print(callback)
    callback = Callbacks()
    aclient.registerCallback(callback)
    aclient.setUserName(username1, password1)


class Test(unittest.TestCase):
    global host, port, topics, wildtopics, nosubscribe_topics, clientid1, clientid2, authentication, username1,username2,usernames, password1,password2,error_cliendid,\
        length_clientid,length_topic,length64_fold,clientid3,password3,username3
    authentication = False

    # 1.测试地址沙箱环境
    # host = "mqtt-ejabberd-hsb.easemob.com"   #发送地址
    # port = 2883 #发送端口
    # username1,username2,username3 = b"mqtttest1",b"mqtttest2",b"mqtttest3"  #用户名称
    # password1 = b"$t$YWMtzP0sDKdAEeu14SMMp-gviPLBUj23REhmv2d9MJZsm8W1kvwQpbMR67NY5XfrXvBLAwMAAAF5Es8XPgBPGgDR9jOQyYerAtoFZ0sPW5Uf8UXkYmdcUBVtU1Ewu4N_qQ"  #用户密码，实际为与用户匹配的token
    # password2 = b"$t$YWMt1xc7aqdAEeucVx_UwbjRCfLBUj23REhmv2d9MJZsm8W6vmEgpbMR655ln0Nsooa_AwMAAAF5Es9ZcgBPGgCp3XBI7JwPhYo6JnKGwcFN067Cagq_PmGIWiotkNf99w"  #用户密码，实际为与用户匹配的token
    # password3 = b"$t$YWMthVu47Ki2Eeu2NCVIo1LZv_LBUj23REhmv2d9MJZsm8V_NJnAqLYR64KoB6bbHIoMAwMAAAF5HGBNrgBPGgCNi1NOhAjzH8EddXwove26U0vPAXM7ETR7DmOdCLvRwA"
    # clientid1 = "mqtttest1@1wyp94"  #开启鉴权后clientid格式为deviceid@appkeyappid deviceid任意取值，只要保证唯一。
    # clientid2 = "mqtttest2@1wyp94"
    # clientid3 = "mqtttest3@1wyp94"
    # appid = {"right_appid":"1wyp94","error_appid":"","noappid":"123"} #构建appid


    #本地
    host = "172.17.1.160"
    port = 1883
    username1,username2,username3 = b"mqtttest1",b"mqtttest2",b"mqtttest3"  #用户名称
    password1 = b"$t$YWMthT_bXKZ5Eeuek9H9tYvkYPLBUj23REhmv2d9MJZsm8W1kvwQpbMR67NY5XfrXvBLAwMAAAF5DbUWfgBPGgB0jT5heMPzU_TtZJqSmmESmC6PzksQSNOyZuEscqu2cg"  #用户密码，实际为与用户匹配的token
    password2 = b"$t$YWMti47_9qZ5EeutzZVjt1Y3N_LBUj23REhmv2d9MJZsm8W6vmEgpbMR655ln0Nsooa_AwMAAAF5DbU_1wBPGgAFHk3GBqhgusAPC74z-xslVDS9HSvCYYZfL0y6ZkIAdQ"
    password3 = b"$t$YWMthVu47Ki2Eeu2NCVIo1LZv_LBUj23REhmv2d9MJZsm8V_NJnAqLYR64KoB6bbHIoMAwMAAAF5HGBNrgBPGgCNi1NOhAjzH8EddXwove26U0vPAXM7ETR7DmOdCLvRwA"
    # clientid1 = "ckjaakjncalnla@1RK24W"
    # clientid2 = "ckjaakjncalnla1@1RK24W"
    clientid1 = "mqtttest1@1wyp94"
    clientid2 = "mqtttest2@1wyp94"
    clientid3 = "mqtttest3@1wyp94"
    appid = {"right_appid":"1wyp94","error_appid":"","noappid":"123"} #构建appid
    

    topics =  ("TopicA", "TopicA/B", "Topic/C", "TopicA/C", "/TopicA","TopicA/B/C","topicA/B/C/D/E/F/G/H/I","topic/a/b/c/d/e/f/g")
    wildtopics = ("TopicA/+", "+/C", "#", "/#", "/+", "+/+", "TopicA/#","+/#","topicA/B/C/D/E/F/G/H/I","topic/a/b/c/d/e/f/g")
    nosubscribe_topics = ("test/nosubscribe",)
    length_topic = "1234567890123456789012345678901234567890123456789012345678901234"
    length64_fold = "a/b/c/d/e/f/g/f/h/i/gk/l/m/n/o/p/q/r/s/t/u/v/w/x/y/z/1/2/3/4/5/6"

    length_clientid = "123456789012345678901234567890123456789012345678901234567@" + appid["right_appid"]
    deviceid = {"right_deviceid":"testdeviceid1","error_deviceid":""}    #构建deviceid
    error_cliendid = {"error_format_one":deviceid["right_deviceid"] + "#" + appid["right_appid"],\
        "no_appid":deviceid["right_deviceid"],\
        "error_format_two":deviceid["right_deviceid"]  + appid["right_appid"],\
        "no_key":deviceid["right_deviceid"] + "@" + appid["noappid"],\
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

      cclient = mqtt_client.Client(clientid3.encode("utf-8"))
      cclient.registerCallback(callback3)
      cclient.setUserName(username3, password3)


    
    def setUp(self):
        callback.clear()
        callback2.clear()
    
    def tearDown(self):
        cleanup()


    """
      1.测试多个连接
    """
    def test_duoge_connect(self):
        print("Basic test starting")
        succeeded = True
        number = 10
        try:
            for i in range(number):
              clientid1 = "deviceid%s"%(i) + "@" + "1wyp94"
              print(clientid1)
              print("aclient is %s"%aclient)
              ac = mqtt_client.Client(clientid1.encode("utf-8"))
              callback = "callback%s"%(i)
              print(callback)
              ac.registerCallback(callback)
              ac.setUserName(username1, password1)
              print("succee")
              ac.connect(host=host, port=port)
            # build_user(self, number)
            # print("build end")
            # for i in range(number):
            #   ac = "aclient%s"%i
            #   print(ac)
            #   ac.connect(host=host, port=port)
            #   print("connect succeed")
            time.sleep(10)
            # aclient.disconnect()
        except:
            succeeded = False
        self.assertEqual(succeeded, True)
        return succeeded



    """
      1.测试订阅后取消订阅
    """
    def test_subscribe_and_unsubscribe(self):
        print("Basic test starting")
        print(topics)
        number = len(topics)
        aclient.connect(host=host, port=port)
        
        aclient.subscribe([topics[0]], [2])
        time.sleep(10)
        aclient.unsubscribe(topics[0])
        time.sleep(10)
        succeeded = True
        # try:
        #     aclient.connect(host=host, port=port)
        #     bclient.connect(host=host,port=port,cleansession=True)
        #     for i in range(number):
        #       print(i)
        #       aclient.subscribe([topics[i]], [2])
        #       bclient.subscribe([topics[i]], [2])
        #       time.sleep(.1)
        #     print("sub end")
        #     time.sleep(10)
        #     for i in range(number):
        #       aclient.unsubscribe(topics[i])
        #       bclient.unsubscribe(topics[i])
        #     # aclient.disconnect()
        #     print("unsub end")
        #     time.sleep(10)
        # except:
        #     traceback.print_exc()
        #     succeeded = False
        self.assertEqual(succeeded, True)
        return succeeded



    """
      1.测试mqtt只进行tcp连接(session小于连接数)
    """
    def test_session_less_than_connect(self):
        print("Basic test starting")
        succeeded = True
        try:
            aclient = mqtt_client.Client(clientid1.encode("utf-8"))
            aclient.registerCallback(callback)
            username1 = "errorusername"
            aclient.setUserName(username1, password1)
            aclient.connect(host=host, port=port,cleansession=True)
            print("connect succeeded")
        except:
            # traceback.print_exc()
            succeeded = False
        time.sleep(10)
        self.assertEqual(succeeded, True)



    """
      1.测试登陆成功后，订阅topic
    """
    def test_login_sub(self):
      print(topics,len(topics),len(wildtopics))
      connack = aclient.connect(host=host,port=port,cleansession=True)
      connack = bclient.connect(host=host,port=port,cleansession=True)
      connack = cclient.connect(host=host,port=port,cleansession=True)
      succeeded = True
      print("Basic test starting")
      succeeded = True
      try:
        for i in range(len(topics)):
          print("sub is %d"%i)
          aclient.subscribe([topics[i]], [2])
          bclient.subscribe([topics[i]], [2])
          cclient.subscribe([topics[i]], [2])
          time.sleep(.1)
        time.sleep(20)
      except:
        succeeded = False
      self.assertEqual(succeeded, True)
      return succeeded


    """
      1.测试登陆成功后，订阅topic
    """
    def test_login_sub_pub(self):
      print(topics,len(topics),len(wildtopics))
      connack = aclient.connect(host=host,port=port,cleansession=True)
      connack = bclient.connect(host=host,port=port,cleansession=True)
      succeeded = True
      print("Basic test starting")
      succeeded = True
      number = len(topics)
      try:
        for i in range(number):
          aclient.subscribe([topics[i]], [2])
          bclient.subscribe([topics[i]], [2])
          time.sleep(.1)
        time.sleep(10)
        for i in range(number):
          aclient.publish(topics[i],b"tset aclient %d qos0"%(i),0)
          aclient.publish(topics[i],b"tset aclient %d qos1"%(i),1)
          aclient.publish(topics[i],b"tset aclient %d qos2"%(i),2)
          time.sleep(.1)
        time.sleep(10)
      except:
        succeeded = False
      print("Basic test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded

    """
      1.测试登陆成功后，订阅topic
    """
    def test_login_sub_unsub(self):
      print(topics,len(topics),len(wildtopics))
      connack = aclient.connect(host=host,port=port,cleansession=True)
      connack = bclient.connect(host=host,port=port,cleansession=False)
      succeeded = True
      time.sleep(10)
      print("Basic test starting")
      succeeded = True
      # number = len(topics)
      # try:
        # for i in range(number):
        #   print("sub is %d"%i)
        #   aclient.subscribe([topics[i]], [2])
        #   bclient.subscribe([topics[i]], [2])
        #   time.sleep(.1)
        # time.sleep(5)
      #   for i in range(number):
      #     print("unsub is %s"%i)
      #     aclient.unsubscribe([topics[i]])
      #     bclient.unsubscribe([topics[i]])
      #     time.sleep(.1)
      #   time.sleep(5)
      # except:
      #   succeeded = False
      # print("Basic test", "succeeded" if succeeded else "failed")
      # self.assertEqual(succeeded, True)
      # return succeeded


      """
      """
    def test_login_sub_unsub_1(self):
      print(topics,len(topics),len(wildtopics))
      connack = aclient.connect(host=host,port=port,cleansession=True)
      connack = bclient.connect(host=host,port=port,cleansession=False)
      succeeded = True
      print("Basic test starting")
      succeeded = True
      number = len(topics)
      try:
        for i in range(number):
          print("sub is %d"%i)
          aclient.subscribe([topics[i]], [2])
          bclient.subscribe([topics[i]], [2])
          time.sleep(.1)
        time.sleep(5)
        
        print("重复订阅")
        for i in range(number):
          print("sub is %d"%i)
          aclient.subscribe([topics[i]], [2])
          bclient.subscribe([topics[i]], [2])
          time.sleep(.1)
        time.sleep(10)


        for i in range(number):
          print("unsub is %s"%i)
          aclient.unsubscribe([topics[i]])
          bclient.unsubscribe([topics[i]])
          time.sleep(.1)
        print("重复取消订阅")
        for i in range(number):
          print("unsub is %s"%i)
          aclient.unsubscribe([topics[i]])
          bclient.unsubscribe([topics[i]])
          time.sleep(.1)
        time.sleep(10)
      except:
        succeeded = False
      print("Basic test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded


    """
      1.测试session大于连接数
    """
    def test_session_than_sub(self):
      print(topics,len(topics),len(wildtopics))
      connack = aclient.connect(host=host,port=port,cleansession=False)
      connack = bclient.connect(host=host,port=port,cleansession=False)
      succeeded = True
      print("Basic test starting")
      succeeded = True
      try:
        for i in range(len(topics)):
          print(i)
          aclient.subscribe([topics[i]], [2])
          bclient.subscribe([topics[i]], [2])
          time.sleep(.1)
      except:
        succeeded = False

      print("Basic test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded

    """
      1.测试没有连接数只有session数
    """
    def test_noconect_session(self):
      print("test subnum max starting")
      print(topics,len(topics),len(wildtopics))
      connack = aclient.connect(host=host,port=port,cleansession=False)
      # aclient.subscribe([topics[0]], [2])
      connack = bclient.connect(host=host,port=port,cleansession=False)
      succeeded = True
      try:
        for i in range(len(topics)):
          print(i)
          aclient.subscribe([topics[i]], [2])
          bclient.subscribe([topics[i]], [2])
          time.sleep(.1)
      except:
        succeeded = False
      time.sleep(10)
      self.assertEqual(succeeded,True)
    

    """
      1.测试session数量等于连接数量
    """
    def test_session_equal_connect(self):
      print("test subnum max starting")
      print(topics,len(topics),len(wildtopics))
      connack = aclient.connect(host=host,port=port,cleansession=True)
      # aclient.subscribe([topics[0]], [2])
      connack = bclient.connect(host=host,port=port,cleansession=True)
      succeeded = True
      try:
        for i in range(len(topics)):
          print(i)
          aclient.subscribe([topics[i]], [2])
          bclient.subscribe([topics[i]], [2])
          time.sleep(.1)
      except:
        succeeded = False
      time.sleep(10)
      self.assertEqual(succeeded,True)


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
 
    # for i in range(iterations):
    #     unittest.main()
    #创建测试集
    suite = unittest.TestSuite()
    suite.addTest(Test("test_cleansession_false"))
    # suite.addTest(Test("test_seventh_topic_format"))
    # suite.addTest(Test("test_will_message_qos_one"))
    # suite.addTest(Test("test_zero_length_clientid"))
    # suite.addTest(Test("test_online_retained_messages"))
    # suite.addTest(Test("test_nosub_reatin_message"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

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
