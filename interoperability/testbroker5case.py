"""
*******************************************************************
  Copyright (c) 2013, 2018 IBM Corp.

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

import mqtt.clients.V5 as mqtt_client, time, logging, socket, sys, getopt, traceback,random
# import mqtt.clients.V311 as mqtt_client_v311
# import testbroker3case as broker3callback
import mqtt.formats.MQTTV5 as MQTTV5

class Callbacks(mqtt_client.Callback):

  # global host, port, topics, wildtopics, nosubscribe_topics, clientid1, clientid2, authentication, username1,username2,usernames, password1,password2,error_cliendid,\
  #   length_clientid,length_topic,length64_fold
  # # authentication = False


  # # # 1.测试地址沙箱环境
  # host = "mqtt-ejabberd-hsb.easemob.com"   #发送地址
  # port = 2883 #发送端口
  # username1,username2 = b"mqtttest1",b"mqtttest2"  #用户名称
  # password1 = b"$t$YWMtzP0sDKdAEeu14SMMp-gviPLBUj23REhmv2d9MJZsm8W1kvwQpbMR67NY5XfrXvBLAwMAAAF5Es8XPgBPGgDR9jOQyYerAtoFZ0sPW5Uf8UXkYmdcUBVtU1Ewu4N_qQ"  #用户密码，实际为与用户匹配的token
  # password2 = b"$t$YWMt1xc7aqdAEeucVx_UwbjRCfLBUj23REhmv2d9MJZsm8W6vmEgpbMR655ln0Nsooa_AwMAAAF5Es9ZcgBPGgCp3XBI7JwPhYo6JnKGwcFN067Cagq_PmGIWiotkNf99w"  #用户密码，实际为与用户匹配的token
  # clientid1 = "mqtttest1@1wyp94"  #开启鉴权后clientid格式为deviceid@appkeyappid deviceid任意取值，只要保证唯一。
  # clientid2 = "mqtttest2@1wyp94"
  # appid = {"right_appid":"1wyp94","error_appid":"","noappid":"123"} #构建appid


  #本地
  # host = "172.17.1.160"
  # port = 1883
  # username1,username2 = b"mqtttest1",b"mqtttest2"  #用户名称
  # password1 = b"$t$YWMthT_bXKZ5Eeuek9H9tYvkYPLBUj23REhmv2d9MJZsm8W1kvwQpbMR67NY5XfrXvBLAwMAAAF5DbUWfgBPGgB0jT5heMPzU_TtZJqSmmESmC6PzksQSNOyZuEscqu2cg"  #用户密码，实际为与用户匹配的token
  # password2 = b"$t$YWMti47_9qZ5EeutzZVjt1Y3N_LBUj23REhmv2d9MJZsm8W6vmEgpbMR655ln0Nsooa_AwMAAAF5DbU_1wBPGgAFHk3GBqhgusAPC74z-xslVDS9HSvCYYZfL0y6ZkIAdQ"
  # clientid1 = "ckjaakjncalnla@1RK24W"
  # clientid2 = "ckjaakjncalnla1@1RK24W"
  # appid = {"right_appid":"1RK24W","error_appid":"","noappid":"123"} #构建appid


  # topics =  ("TopicA", "TopicA/B", "Topic/C", "TopicA/C", "/TopicA","TopicA/B/C","topicA/B/C/D/E/F/G/H/I","topic/a/b/c/d/e/f/g")
  # wildtopics = ("TopicA/+", "+/C", "#", "/#", "/+", "+/+", "TopicA/#","+/#","topicA/B/C/D/E/F/G/H/I","topic/a/b/c/d/e/f/g")
  # nosubscribe_topics = ("test/nosubscribe",)
  # length_topic = "1234567890123456789012345678901234567890123456789012345678901234"
  # length64_fold = "a/b/c/d/e/f/g/f/h/i/gk/l/m/n/o/p/q/r/s/t/u/v/w/x/y/z/1/2/3/4/5/6"

  # length_clientid = "123456789012345678901234567890123456789012345678901234567@" + appid["right_appid"]
  # deviceid = {"right_deviceid":"testdeviceid1","error_deviceid":""}    #构建deviceid
  # error_cliendid = {"error_format_one":deviceid["right_deviceid"] + "#" + appid["right_appid"],\
  #   "no_appid":deviceid["right_deviceid"],\
  #   "error_format_two":deviceid["right_deviceid"]  + appid["right_appid"],\
  #   "no_key":deviceid["right_deviceid"] + "@" + appid["noappid"],\
  #   "overlength_clientid":"123456789012345678901234567890123456789012345678901234567@1RK24W123456789012345678901234567890123456789012345678901234567@" + appid["right_appid"]}

  def __init__(self):
    self.messages = []
    self.messagedicts = []
    self.publisheds = []
    self.subscribeds = []
    self.unsubscribeds = []
    self.disconnects = []

  def __str__(self):
     return str(self.messages) + str(self.messagedicts) + str(self.publisheds) + \
        str(self.subscribeds) + str(self.unsubscribeds) + str(self.disconnects)

  def clear(self):
    self.__init__()

  def disconnected(self, reasoncode, properties):
    logging.info("disconnected %s %s", str(reasoncode), str(properties))
    self.disconnects.append({"reasonCode" : reasoncode, "properties" : properties})

  def connectionLost(self, cause):
    logging.info("connectionLost %s" % str(cause))

  def publishArrived(self, topicName, payload, qos, retained, msgid, properties=None):
    logging.info("publishArrived %s %s %d %s %d %s", topicName, payload, qos, retained, msgid, str(properties))
    self.messages.append((topicName, payload, qos, retained, msgid, properties))
    self.messagedicts.append({"topicname" : topicName, "payload" : payload,
        "qos" : qos, "retained" : retained, "msgid" : msgid, "properties" : properties})
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

def cleanRetained():
  callback = Callbacks()
  curclient = mqtt_client.Client(clientid1.encode("utf-8"))
  curclient.registerCallback(callback)
  curclient.setUserName(username1, password1)
  curclient.connect(host=host, port=port, cleanstart=True)
  curclient.subscribe(["#"], [MQTTV5.SubscribeOptions(0)])
  time.sleep(2) # wait for all retained messages to arrive
  for message in callback.messages:
    logging.info("deleting retained message for topic", message[0])
    curclient.publish(message[0], b"", 0, retained=True)
  curclient.disconnect()
  time.sleep(.1)


def topictest(self,sub_index=None,pub_index=None,message=None):
    #不同种类的topic测试
    callback.clear()
    callback2.clear()
    #用户B连接
    bclient.connect(host=host, port=port, cleanstart=True)
    print(wildtopics[sub_index],topics[pub_index])
    print("userb sub")
    bclient.subscribe([wildtopics[sub_index]], [MQTTV5.SubscribeOptions(2)])
    time.sleep(1) # wait for all retained messages, hopefully
    print("userb pub")
    bclient.publish(topics[pub_index], message, 1, retained=False)
    time.sleep(2)
    #用户a连接
    aclient.connect(host=host, port=port, cleanstart=True)
    print("usera pub")
    aclient.publish(topics[pub_index], message, 1, retained=False)
    time.sleep(5)
    aclient.disconnect()
    time.sleep(1)
    bclient.disconnect()
    print("用户B收到的消息 %s"%callback2.messages)
    return callback2.messages


def qostest(self,sub_qos=None,pub_qos=None,message=None):
  callback.clear()
  callback2.clear()
  #用户B连接
  print("用户B连接")
  bclient.connect(host=host, port=port, cleanstart=True)
  print(wildtopics[6],topics[1])
  bclient.subscribe([wildtopics[6]], [MQTTV5.SubscribeOptions(sub_qos)])
  time.sleep(1)
  bclient.publish(topics[1], message, pub_qos, retained=False)
  time.sleep(2)
  #用户a连接
  print("用户A连接")
  aclient.connect(host=host, port=port, cleanstart=True)
  aclient.publish(topics[1], message, pub_qos, retained=False)
  time.sleep(1)
  bclient.disconnect()
  time.sleep(1)
  aclient.disconnect()
  print(callback2.messages)
  return callback2.messages



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


def assert_topic_result(self,callbackmessage,*params):
  print("Start:判断topic格式是否正确")
  succeeded = True
  for i in range(len(callbackmessage)):
      for num in range(len(params)):
          print("num,i %d %d"%(num,i))
          if callbackmessage[i][0] == params[num]:
              print(callbackmessage[i][0],params[num])
          else:
              succeeded = False
  print("END:判断topic格式 %s"%"succeeded" if succeeded else "is False")
  return succeeded


def cleanup():
  # clean all client state
  print("clean up starting")
  clientids = (clientid1, clientid2)

  # for clientid in clientids:
  curclient = mqtt_client.Client(clientid1.encode("utf-8"))
  curclient.setUserName(username1, password1)
  curclient.connect(host=host, port=port, cleanstart=True)
  time.sleep(.1)
  curclient.disconnect()
  time.sleep(.1)

  curclient = mqtt_client.Client(clientid2.encode("utf-8"))
  curclient.setUserName(username2, password2)
  curclient.connect(host=host, port=port, cleanstart=True)
  time.sleep(.1)
  curclient.disconnect()
  time.sleep(.1)

  # clean retained messages
  cleanRetained()
  print("clean up finished")

def usage():
  logging.info(
"""
 -h: --hostname= hostname or ip address of server to run tests against
 -p: --port= port number of server to run tests against
 -z: --zero_length_clientid run zero length clientid test
 -d: --dollar_topics run $ topics test
 -s: --subscribe_failure run subscribe failure test
 -n: --nosubscribe_topic_filter= topic filter name for which subscriptions aren't allowed

""")

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
      setData()
      global callback, callback2, aclient, bclient,cclient,dclient,callback3,callback4
      # cleanup()

      callback = Callbacks()
      callback2 = Callbacks()
      callback3 = Callbacks()
      # callback4 = broker3callback.Callbacks

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

      # dclient = mqtt_client_v311.Client(clientid2.encode("utf-8"))
      # dclient.registerCallback(callback2)
      # dclient.setUserName(username2, password2)


    def setUp(self):
      callback.clear()
      callback2.clear()

    def tearDown(self):
        cleanup()




    def test_basic(self):
      aclient.connect(host=host, port=port)
      aclient.disconnect()

      rc = aclient.connect(host=host, port=port)
      print("rc")
      print(rc)
      self.assertEqual(rc.reasonCode.getName(), "Success")
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      aclient.publish(topics[0], b"qos 0")
      aclient.publish(topics[0], b"qos 1", 1)
      aclient.publish(topics[0], b"qos 2", 2)
      time.sleep(2)
      aclient.disconnect()
      print("判断收到消息条数")
      self.assertEqual(len(callback.messages), 3)

      with self.assertRaises(Exception):
        aclient.connect(host=host, port=port)
        aclient.connect(host=host, port=port, newsocket=False) # should fail - second connect on socket

      with self.assertRaises(Exception):
        aclient.connect(host=host, port=port, protocolName="hj") # should fail - wrong protocol name


    """
        1.测试连续订阅不同topic
    """
    def test_subscription_continuous(self):
        print("test subnum max starting")
        print(topics,len(topics),len(wildtopics))
        connack = aclient.connect(host=host,port=port)
        connack = bclient.connect(host=host,port=port)
        succeeded = True
        try:
            for i in range(len(topics)):
                print(i)
                aclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
                bclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
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
                aclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
                bclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
                time.sleep(.2)
            for num in range(len(topics)):
                print(num)
                aclient.unsubscribe([topics[num]])
                bclient.unsubscribe([topics[num]])
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
        connack = aclient.connect(host=host,port=port,cleanstart=True)
        connack = bclient.connect(host=host,port=port,cleanstart=True)
        succeeded = True
        try:
            for i in range(len(topics)):
                print(i)
                aclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
                bclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
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
        1.验证用户名称（username）与密码不一致（token）
    """
    def test_login_username_and_paw_donot_math(self):
        print("test_login_username_and_paw_donot_math starting")
        succeeded = False

        try:
            print("username = ", username1)
            print("password = ", password2)
            connect = aclient.connect(host=host,port=port,username=username1,password=password2)
            print("login succeed")
        except:
            traceback.print_exc()
            succeeded = True
        print("test_login_username_and_paw_donot_math starting ""succeeded" if succeeded else "failed")
        assert succeeded == True


    """
      1.测试遗嘱消息
    """
    def test_retained_message(self):
      qos0topic="fromb/qos 0"
      qos1topic="fromb/qos 1"
      qos2topic="fromb/qos2"
      wildcardtopic="fromb/+"

      publish_properties = MQTTV5.Properties(MQTTV5.PacketTypes.PUBLISH)
      publish_properties.UserProperty = ("a", "2")
      publish_properties.UserProperty = ("c", "3")

      # retained messages
      callback.clear()
      aclient.connect(host=host, port=port, cleanstart=True)
      aclient.publish(topics[1], b"qos 0", 0, retained=True, properties=publish_properties)
      aclient.publish(topics[2], b"qos 1", 1, retained=True, properties=publish_properties)
      aclient.publish(topics[3], b"qos 2", 2, retained=True, properties=publish_properties)
      time.sleep(1)
      aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2)])
      time.sleep(1)
      aclient.disconnect()

      self.assertEqual(len(callback.messages), 3)
      userprops = callback.messages[0][5].UserProperty
      self.assertTrue(userprops in [[("a", "2"), ("c", "3")],[("c", "3"), ("a", "2")]], userprops)
      userprops = callback.messages[1][5].UserProperty
      self.assertTrue(userprops in [[("a", "2"), ("c", "3")],[("c", "3"), ("a", "2")]], userprops)
      userprops = callback.messages[2][5].UserProperty
      self.assertTrue(userprops in [[("a", "2"), ("c", "3")],[("c", "3"), ("a", "2")]], userprops)
      qoss = [callback.messages[i][2] for i in range(3)]
      self.assertTrue(1 in qoss and 2 in qoss and 0 in qoss, qoss)

      cleanRetained()

    def test_will_message(self):
      # will messages
      callback.clear()
      callback2.clear()
      self.assertEqual(len(callback2.messages), 0, callback2.messages)

      will_properties = MQTTV5.Properties(MQTTV5.PacketTypes.WILLMESSAGE)
      will_properties.WillDelayInterval = 0 # this is the default anyway
      will_properties.UserProperty = ("a", "2")
      will_properties.UserProperty = ("c", "3")

      aclient.connect(host=host, port=port, cleanstart=True, willFlag=True,
          willTopic=topics[2], willMessage=b"will message", keepalive=2,
          willProperties=will_properties)
      bclient.connect(host=host, port=port, cleanstart=False)
      bclient.subscribe([topics[2]], [MQTTV5.SubscribeOptions(2)])
      self.waitfor(callback2.subscribeds, 1, 3)
      # keep alive timeout ought to be triggered so the will message is received
      self.waitfor(callback2.messages, 1, 10)
      bclient.disconnect()
      self.assertEqual(len(callback2.messages), 1, callback2.messages)  # should have the will message
      props = callback2.messages[0][5]
      self.assertEqual(props.UserProperty, [("a", "2"), ("c", "3")])

    # 0 length clientid
    def test_zero_length_clientid(self):
      pass
      logging.info("Zero length clientid test starting")
      succeeded = True
      try:
        client0 = mqtt_client.Client("")
        client0.setUserName(username1, password1)
        fails = False
        try:
          client0.connect(host=host, port=port, cleanstart=False) # should be rejected
        except:
          fails = True
        assert fails == True
        client0.disconnect()
        fails = False
        try:
          client0.connect(host=host, port=port, cleanstart=True) # should work
        except:
          fails = True
        assert fails == True
        client0.disconnect()
      except:
        traceback.print_exc()
        succeeded = False
      logging.info("Zero length clientid test %s", "succeeded" if succeeded else "failed")
      assert succeeded ==True
      return succeeded


    """
      测试离线消息
        1.默认设置session保留时长99999
        2.用户A登陆成功后，订阅topic，断开连接
        3.用户B登陆分别想topic发送消息，断开连接
        4.用户A再次登陆，会收到离线消息
    """
    def test_offline_message_queueing(self):
      # message queueing for offline clients
      callback.clear()
      callback2.clear()

      connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)
      connect_properties.SessionExpiryInterval = 99999
      aclient.connect(host=host, port=port, cleanstart=False, properties=connect_properties)
      print("sub is %s"%wildtopics[5])
      aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2)])
      aclient.disconnect()

      print("pub is %s %s %s"%(topics[1],topics[2],topics[3]))
      bclient.connect(host=host, port=port, cleanstart=True)
      bclient.publish(topics[1], b"qos 0", 0)
      bclient.publish(topics[2], b"qos 1", 1)
      bclient.publish(topics[3], b"qos 2", 2)
      time.sleep(2)
      bclient.disconnect()

      aclient.connect(host=host, port=port, cleanstart=False)
      time.sleep(5)
      aclient.disconnect()

      print("callback.messages is %s"%callback.messages)
      self.assertTrue(len(callback.messages) in [2, 3], len(callback.messages))
      logging.info("This server %s queueing QoS 0 messages for offline clients" % \
            ("is" if len(callback.messages) == 3 else "is not"))

    """
      测试一个用户订阅不同topic，但匹配结果是相同
        1.用户A订阅topic：TopicA/# TopicA/+
        2.用户B向topic：TopicA/C发送消息
        3.用户A应该收到1条或者两条消息（取决于服务器是否将消息合并）
    """
    def test_overlapping_subscriptions(self):
      # overlapping subscriptions. When there is more than one matching subscription for the same client for a topic,
      # the server may send back one message with the highest QoS of any matching subscription, or one message for
      # each subscription with a matching QoS.
      callback.clear()
      callback2.clear()
      aclient.connect(host=host, port=port)
      print("sub is %s %s"%(wildtopics[6], wildtopics[0]))
      print("pub is %s"%(topics[3]))
      aclient.subscribe([wildtopics[6], wildtopics[0]], [MQTTV5.SubscribeOptions(2), MQTTV5.SubscribeOptions(1)])
      aclient.publish(topics[3], b"overlapping topic filters", 2)
      time.sleep(1)
      print("callback.messages length is %d"%(len(callback.messages)))
      self.assertTrue(len(callback.messages) in [1, 2], callback.messages)
      if len(callback.messages) == 1:
        logging.info("This server is publishing one message for all matching overlapping subscriptions, not one for each.")
        self.assertEqual(callback.messages[0][2], 2, callback.messages[0][2])
      else:
        logging.info("This server is publishing one message per each matching overlapping subscription.")
        self.assertTrue((callback.messages[0][2] == 2 and callback.messages[1][2] == 1) or \
                 (callback.messages[0][2] == 1 and callback.messages[1][2] == 2), callback.messages)
      aclient.disconnect()

    """
      测试keetlive。keeplive*1.5，超过这个时间，服务端自动断开连接，发送遗嘱消息
    """
    def test_keepalive_one(self):
      # keepalive processing.  We should be kicked off by the server if we don't send or receive any data, and don't send
      # any pings either.
      logging.info("Keepalive test starting")
      succeeded = True
      try:
        callback2.clear()
        aclient.connect(host=host, port=port, cleanstart=True, keepalive=5, willFlag=True,
              willTopic=topics[4], willMessage=b"keepalive expiry")
        bclient.connect(host=host, port=port, cleanstart=True, keepalive=0)
        bclient.subscribe([topics[4]], [MQTTV5.SubscribeOptions(2)])
        time.sleep(15)
        bclient.disconnect()
        assert len(callback2.messages) == 1, "length should be 1: %s" % callback2.messages # should have the will message
      except:
        traceback.print_exc()
        succeeded = False
      logging.info("Keepalive test %s", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded

    """
      测试keetlive。keeplive*1.5，未超过这个时间，服务端不会自动断开连接，不会发送遗嘱消息
    """
    def test_keepalive_two(self):
      # keepalive processing.  We should be kicked off by the server if we don't send or receive any data, and don't send
      # any pings either.
      logging.info("Keepalive test starting")
      succeeded = True
      try:
        callback2.clear()
        aclient.connect(host=host, port=port, cleanstart=True, keepalive=5, willFlag=True,
              willTopic=topics[4], willMessage=b"keepalive expiry")
        bclient.connect(host=host, port=port, cleanstart=True, keepalive=0)
        bclient.subscribe([topics[4]], [MQTTV5.SubscribeOptions(2)])
        time.sleep(7) #设置keeolive*1.5以内时间
        bclient.disconnect()
        assert len(callback2.messages) == 0, "length should be 1: %s" % callback2.messages # should have the will message
      except:
        traceback.print_exc()
        succeeded = False
      logging.info("Keepalive test %s", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded



    def test_redelivery_on_reconnect(self):
      # redelivery on reconnect. When a QoS 1 or 2 exchange has not been completed, the server should retry the
      # appropriate MQTT packets
      logging.info("Redelivery on reconnect test starting")
      succeeded = True
      try:
        callback.clear()
        callback2.clear()
        connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)
        connect_properties.SessionExpiryInterval = 99999
        bclient.connect(host=host, port=port, cleanstart=False, properties=connect_properties)
        print("sub is %s "%wildtopics[6])
        bclient.subscribe([wildtopics[6]], [MQTTV5.SubscribeOptions(2)])
        bclient.pause() # stops responding to incoming publishes
        print("pub is %s %s"%(topics[1],topics[3]))
        bclient.publish(topics[1], b"", 1, retained=False)
        bclient.publish(topics[3], b"", 2, retained=False)
        time.sleep(1)
        bclient.disconnect()
        assert len(callback2.messages) == 0, "length should be 0: %s" % callback2.messages
        bclient.resume()
        bclient.connect(host=host, port=port, cleanstart=False, properties=connect_properties)
        time.sleep(3)
        assert len(callback2.messages) == 2, "length should be 2: %s" % callback2.messages
        bclient.disconnect()
      except:
        traceback.print_exc()
        succeeded = False
      logging.info("Redelivery on reconnect test %s", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded

    def test_subscribe_failure(self):
      # Subscribe failure.  A new feature of MQTT 3.1.1 is the ability to send back negative reponses to subscribe
      # requests.  One way of doing this is to subscribe to a topic which is not allowed to be subscribed to.
      logging.info("Subscribe failure test starting")
      succeeded = True
      try:
        callback.clear()
        aclient.connect(host=host, port=port)
        aclient.subscribe(['$share/A'], [MQTTV5.SubscribeOptions(2)])
        time.sleep(1)
        # subscribeds is a list of (msgid, [qos])
        print("callback.subscribeds = ", callback.subscribeds)
        assert callback.subscribeds[0][1][0].value == 0x9E, "return code should be 0x9E %s" % callback.subscribeds
      except:
        traceback.print_exc()
        succeeded = False
      logging.info("Subscribe failure test %s", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded



    """
        1.测试topic格式已$开头，例：$TopicA
    """
    def test_topics_starting_with_dollar(self):
      # $ topics. The specification says that a topic filter which starts with a wildcard does not match topic names that
      # begin with a $.  Publishing to a topic which starts with a $ may not be allowed on some servers (which is entirely valid),
      # so this test will not work and should be omitted in that case.
      logging.info("$ topics test starting")
      succeeded = True
      try:
        callback2.clear()
        bclient.connect(host=host, port=port, cleanstart=True, keepalive=0)
        bclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2)])
        time.sleep(1) # wait for all retained messages, hopefully
        callback2.clear()
        bclient.publish("$"+topics[1], b"", 1, retained=False)
        time.sleep(.2)
        assert len(callback2.messages) == 0, callback2.messages
        # bclient.disconnect()
      except:
        traceback.print_exc()
        succeeded = False
      logging.info("$ topics test %s", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded


    """
      测试取消订阅
    """
    def test_unsubscribe(self):
      callback2.clear()
      bclient.connect(host=host, port=port, cleanstart=True)
      bclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      bclient.subscribe([topics[1]], [MQTTV5.SubscribeOptions(2)])
      bclient.subscribe([topics[2]], [MQTTV5.SubscribeOptions(2)])
      time.sleep(1) # wait for any retained messages, hopefully
      # Unsubscribe from one topic
      bclient.unsubscribe([topics[0]])
      callback2.clear() # if there were any retained messsages

      aclient.connect(host=host, port=port, cleanstart=True)
      aclient.publish(topics[0], b"topic 0 - unsubscribed", 1, retained=False)
      aclient.publish(topics[1], b"topic 1", 1, retained=False)
      aclient.publish(topics[2], b"topic 2", 1, retained=False)
      time.sleep(2)

      bclient.disconnect()
      aclient.disconnect()
      print("callback2.messages is %s"%callback2.messages)
      self.assertEqual(len(callback2.messages), 2, callback2.messages)




    """
      测试session保留时长
    """
    def test_session_expiry(self):
      # no session expiry property == never expire

      connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)

      connect_properties.SessionExpiryInterval = 0
      connack = aclient.connect(host=host, port=port, cleanstart=True, properties=connect_properties)
      self.assertEqual(connack.reasonCode.getName(), "Success")
      # self.assertEqual(connack.sessionPresent, False) #自己取消
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      aclient.disconnect()

      # session should immediately expire
      connack = aclient.connect(host=host, port=port, cleanstart=False, properties=connect_properties)
      self.assertEqual(connack.reasonCode.getName(), "Success")
      # self.assertEqual(connack.sessionPresent, False) #自己取消
      aclient.disconnect()

      connect_properties.SessionExpiryInterval = 5
      connack = aclient.connect(host=host, port=port, cleanstart=True, properties=connect_properties)
      self.assertEqual(connack.reasonCode.getName(), "Success")
      # self.assertEqual(connack.sessionPresent, False)   #自己取消
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      aclient.disconnect()

      time.sleep(2)
      # session should still exist
      connack = aclient.connect(host=host, port=port, cleanstart=False, properties=connect_properties)
      self.assertEqual(connack.reasonCode.getName(), "Success")
      # self.assertEqual(connack.sessionPresent, True)  #自己取消
      aclient.disconnect()

      time.sleep(6)
      # session should not exist
      connack = aclient.connect(host=host, port=port, cleanstart=False, properties=connect_properties)
      self.assertEqual(connack.reasonCode.getName(), "Success")
      # self.assertEqual(connack.sessionPresent, False) #自己取消
      aclient.disconnect()

      connect_properties.SessionExpiryInterval = 1
      connack = aclient.connect(host=host, port=port, cleanstart=True, properties=connect_properties)
      self.assertEqual(connack.reasonCode.getName(), "Success")
      # self.assertEqual(connack.sessionPresent, False) #自己取消
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      disconnect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.DISCONNECT)
      disconnect_properties.SessionExpiryInterval = 5
      aclient.disconnect(properties = disconnect_properties)

      time.sleep(3)
      # session should still exist
      connack = aclient.connect(host=host, port=port, cleanstart=False, properties=connect_properties)
      self.assertEqual(connack.reasonCode.getName(), "Success")
      # self.assertEqual(connack.sessionPresent, True)  #自己取消
      disconnect_properties.SessionExpiryInterval = 0
      aclient.disconnect(properties = disconnect_properties)

      # session should immediately expire
      connack = aclient.connect(host=host, port=port, cleanstart=False, properties=connect_properties)
      self.assertEqual(connack.reasonCode.getName(), "Success")
      # self.assertEqual(connack.sessionPresent, False) #自己取消
      aclient.disconnect()

    def test_user_properties(self):
      callback.clear()
      succeeded = True
      aclient.connect(host=host, port=port, cleanstart=True)
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      publish_properties = MQTTV5.Properties(MQTTV5.PacketTypes.PUBLISH)
      publish_properties.UserProperty = ("a", "2")
      publish_properties.UserProperty = ("c", "3")
      aclient.publish(topics[0], b"", 0, retained=False, properties=publish_properties)
      aclient.publish(topics[0], b"", 1, retained=False, properties=publish_properties)
      aclient.publish(topics[0], b"", 2, retained=False, properties=publish_properties)
      while len(callback.messages) < 3:
        time.sleep(.1)
      aclient.disconnect()
      self.assertEqual(len(callback.messages), 3, callback.messages)
      try:
        for i in range(len(callback.messages)):
          print("callback.messages[%d] is %s"%(i,callback.messages[i][5]))
          if  callback.messages[i][0] == topics[0]:
            print(callback.messages[i][0])
          else:
            succeeded = False
      except:
        succeeded = False
      assert succeeded == True
      userprops = callback.messages[0][5].UserProperty
      self.assertTrue(userprops in [[("a", "2"), ("c", "3")],[("c", "3"), ("a", "2")]], userprops)
      userprops = callback.messages[1][5].UserProperty
      self.assertTrue(userprops in [[("a", "2"), ("c", "3")],[("c", "3"), ("a", "2")]], userprops)
      userprops = callback.messages[2][5].UserProperty
      self.assertTrue(userprops in [[("a", "2"), ("c", "3")],[("c", "3"), ("a", "2")]], userprops)
      qoss = [callback.messages[i][2] for i in range(3)]
      self.assertTrue(1 in qoss and 2 in qoss and 0 in qoss, qoss)


    """
      测试messages的格式
        1.用户A设置一个ContentType，并发送消息
        2.用户A查看消息，消息返回体中存在属性：ContentType
    """
    def test_payload_format(self):
      callback.clear()
      aclient.connect(host=host, port=port, cleanstart=True)
      print("sub is %s"%(topics[0]))
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      publish_properties = MQTTV5.Properties(MQTTV5.PacketTypes.PUBLISH)
      publish_properties.PayloadFormatIndicator = 1
      publish_properties.ContentType = "My name"
      print("pub is %s"%(topics[0]))
      aclient.publish(topics[0], b"", 0, retained=False, properties=publish_properties)
      aclient.publish(topics[0], b"", 1, retained=False, properties=publish_properties)
      aclient.publish(topics[0], b"", 2, retained=False, properties=publish_properties)
      while len(callback.messages) < 3:
        time.sleep(.1)
      aclient.disconnect()


      print("callback.messages = %s"%callback.messages)
      self.assertEqual(len(callback.messages), 3, callback.messages)
      props = callback.messages[0][5]
      self.assertEqual(props.ContentType, "My name", props.ContentType)
      self.assertEqual(props.PayloadFormatIndicator, 1, props.PayloadFormatIndicator)
      props = callback.messages[1][5]
      self.assertEqual(props.ContentType, "My name", props.ContentType)
      self.assertEqual(props.PayloadFormatIndicator, 1, props.PayloadFormatIndicator)
      props = callback.messages[2][5]
      self.assertEqual(props.ContentType, "My name", props.ContentType)
      self.assertEqual(props.PayloadFormatIndicator, 1, props.PayloadFormatIndicator)
      qoss = [callback.messages[i][2] for i in range(3)]
      self.assertTrue(1 in qoss and 2 in qoss and 0 in qoss, qoss)


    """
      PUBLISH数据在Server的最长等待时间。超过这个时间，这个数据不能被publish到匹配topic的subscriber
    """
    def test_publication_expiry(self):
      callback.clear()
      callback2.clear()
      connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)
      connect_properties.SessionExpiryInterval = 99999
      bclient.connect(host=host, port=port, cleanstart=False, properties=connect_properties)
      print("sub is %s"%topics[0])
      bclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      disconnect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.DISCONNECT)
      disconnect_properties.SessionExpiryInterval = 999999999
      bclient.disconnect(properties = disconnect_properties)

      aclient.connect(host=host, port=port, cleanstart=True)
      publish_properties = MQTTV5.Properties(MQTTV5.PacketTypes.PUBLISH)
      publish_properties.MessageExpiryInterval = 1
      print("pub is %s"%topics[0])
      aclient.publish(topics[0], b"qos 1 - expire", 1, retained=False, properties=publish_properties)
      aclient.publish(topics[0], b"qos 2 - expire", 2, retained=False, properties=publish_properties)
      publish_properties.MessageExpiryInterval = 6
      aclient.publish(topics[0], b"qos 1 - don't expire", 1, retained=False, properties=publish_properties)
      aclient.publish(topics[0], b"qos 2 - don't expire", 2, retained=False, properties=publish_properties)

      time.sleep(3)
      print("user B is login")
      bclient.connect(host=host, port=port, cleanstart=False)
      self.waitfor(callback2.messages, 1, 3)
      time.sleep(1)
      print("callback2.messages is %s"%callback2.messages)
      self.assertEqual(len(callback2.messages), 2, callback2.messages)
      self.assertTrue(callback2.messages[0][5].MessageExpiryInterval < 6,
                             callback2.messages[0][5].MessageExpiryInterval)
      self.assertTrue(callback2.messages[1][5].MessageExpiryInterval < 6,
                                   callback2.messages[1][5].MessageExpiryInterval)
      self.assertTrue((callback2.messages[0][1] == b"qos 2 - don't expire" and callback2.messages[1][1] == b"qos 1 - don't expire") or \
        (callback2.messages[0][1] == b"qos 1 - don't expire" and callback2.messages[1][1] == b"qos 2 - don't expire") )
      aclient.disconnect()

    def waitfor(self, queue, depth, limit):
      total = 0
      while len(queue) < depth and total < limit:
        interval = .5
        total += interval
        time.sleep(interval)

    def test_subscribe_noLocal(self):
      callback.clear()
      callback2.clear()

      # noLocal
      aclient.connect(host=host, port=port, cleanstart=True)
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2, noLocal=True)])
      self.waitfor(callback.subscribeds, 1, 3)

      bclient.connect(host=host, port=port, cleanstart=True)
      bclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2, noLocal=True)])
      self.waitfor(callback.subscribeds, 1, 3)

      aclient.publish(topics[0], b"noLocal test", 1, retained=False)
      self.waitfor(callback2.messages, 1, 3)
      time.sleep(1)

      self.assertEqual(callback.messages, [], callback.messages)
      self.assertEqual(len(callback.messages), 0, callback.messages)
      self.assertEqual(len(callback2.messages), 1, callback2.messages)
      aclient.disconnect()
      bclient.disconnect()

      callback.clear()
      callback2.clear()


    def test_subscribe_retainAsPublished(self):
      # retainAsPublished
      aclient.connect(host=host, port=port, cleanstart=True)
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2, retainAsPublished=True)])
      self.waitfor(callback.subscribeds, 1, 3)
      aclient.publish(topics[0], b"retain as published false", 1, retained=False)
      aclient.publish(topics[0], b"retain as published true", 1, retained=True)

      self.waitfor(callback.messages, 2, 3)
      time.sleep(1)

      print("retainAsPublished result")
      self.assertEqual(len(callback.messages), 2, callback.messages)
      aclient.disconnect()
      self.assertEqual(callback.messages[0][3], False)
      self.assertEqual(callback.messages[1][3], True)


    """
      测试A发布retained=True消息，A用户订阅topic，收到最新topic的retained=True消息
    """
    def test_subscribe_retainHandling(self):
      # retainHandling
      callback.clear()
      aclient.connect(host=host, port=port, cleanstart=True)
      print("pub is %s %s %s"%(topics[1],topics[2],topics[3]))
      aclient.publish(topics[1], b"qos 00", 0, retained=True)
      aclient.publish(topics[2], b"qos 10", 1, retained=True)
      aclient.publish(topics[3], b"qos 20", 2, retained=True)
      time.sleep(1)
      print("sub is %s"%wildtopics[5])
      aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2, retainHandling=1)])
      # aclient.subscribe(["Topic/+"], [MQTTV5.SubscribeOptions(2, retainHandling=1)])
      time.sleep(3)
      print("callback.messages is %s"%callback.messages)
      self.assertEqual(len(callback.messages), 3)
      qoss = [callback.messages[i][2] for i in range(3)]
      self.assertTrue(1 in qoss and 2 in qoss and 0 in qoss, qoss)
      callback.clear()      
      aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2, retainHandling=1)])
      # aclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(2, retainHandling=1)])
      time.sleep(1)
      self.assertEqual(len(callback.messages), 0)
      aclient.disconnect()


      callback.clear()
      aclient.connect(host=host, port=port, cleanstart=True)
      aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2, retainHandling=2)])
      # aclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(2, retainHandling=2)])
      time.sleep(1)
      self.assertEqual(len(callback.messages), 0)
      aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2, retainHandling=2)])
      # aclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(2, retainHandling=2)])
      time.sleep(1)
      self.assertEqual(len(callback.messages), 0)
      aclient.disconnect()


      callback.clear()
      aclient.connect(host=host, port=port, cleanstart=True)
      time.sleep(1)
      aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2, retainHandling=0)])
      # aclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(2, retainHandling=0)])
      time.sleep(1)
      self.assertEqual(len(callback.messages), 3)
      qoss = [callback.messages[i][2] for i in range(3)]
      self.assertTrue(1 in qoss and 2 in qoss and 0 in qoss, qoss)
      callback.clear()
      aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2, retainHandling=0)])
      # aclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(2, retainHandling=0)])
      time.sleep(1)
      self.assertEqual(len(callback.messages), 3)
      qoss = [callback.messages[i][2] for i in range(3)]
      self.assertTrue(1 in qoss and 2 in qoss and 0 in qoss, qoss)
      aclient.disconnect()

      cleanRetained()


    """
      测试A发布retained=True消息，B用户订阅topic，收到最新topic的retained=True消息
      TODO: 有争议：如果订阅了A/B（retainHandling=1），再次订阅#（retainHandling=1），是否应该不再发送retain消息？
    """
    def test_subscribe_retainHandling_three(self):
      # retainHandling
      callback.clear()
      callback2.clear()
      aclient.connect(host=host, port=port, cleanstart=True)
      bclient.connect(host=host, port=port, cleanstart=True)
      print("pub is %s %s %s"%(topics[1],topics[2],topics[3]))
      aclient.publish(topics[1], b"qos 0", 0, retained=True)
      aclient.publish(topics[2], b"qos 1", 1, retained=True)
      aclient.publish(topics[3], b"qos 2", 2, retained=True)
      time.sleep(1)
      print("sub is %s"%wildtopics[5])
      # bclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2, retainHandling=1)])
      bclient.subscribe(["Topic/+"], [MQTTV5.SubscribeOptions(2, retainHandling=1)])
      bclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(2, retainHandling=1)])
      time.sleep(3)
      print("callback2.messages is %s"%callback2.messages)
      self.assertEqual(len(callback2.messages), 3)
      qoss = [callback2.messages[i][2] for i in range(3)]
      self.assertTrue(1 in qoss and 2 in qoss and 0 in qoss, qoss)
      callback2.clear()
      # bclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2, retainHandling=1)])
      bclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(2, retainHandling=1)])
      time.sleep(1)
      self.assertEqual(len(callback2.messages), 0, len(callback2.messages))
      bclient.disconnect()

      callback.clear()
      callback2.clear()
      bclient.connect(host=host, port=port, cleanstart=True)
      bclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2, retainHandling=2)])
      # aclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(2, retainHandling=2)])
      time.sleep(1)
      self.assertEqual(len(callback2.messages), 0)
      bclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2, retainHandling=2)])
      # aclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(2, retainHandling=2)])
      time.sleep(1)
      self.assertEqual(len(callback2.messages), 0)
      bclient.disconnect()



      """
          现在有3个retain消息
      """
      time.sleep(1)
      callback.clear()
      callback2.clear()
      bclient.connect(host=host, port=port, cleanstart=True)
      time.sleep(1)
      bclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2, retainHandling=0)])
      # aclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(2, retainHandling=0)])
      time.sleep(1)
      self.assertEqual(len(callback2.messages), 3)
      qoss = [callback2.messages[i][2] for i in range(3)]
      self.assertTrue(1 in qoss and 2 in qoss and 0 in qoss, qoss)
      aclient.disconnect()
      bclient.disconnect()

      cleanRetained()


    def test_subscribe_retainHandling_one(self):
      # retainHandling
      callback.clear()
      time.sleep(1)
      aclient.connect(host=host, port=port, cleanstart=True)
      aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2)])
      aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(1, retainHandling=1)])
      # aclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(2, retainHandling=1)])
      # aclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(1, retainHandling=1)])
      print("pub is %s %s %s"%(topics[1],topics[2],topics[3]))
      aclient.publish(topics[1], b"qos 0", 0, retained=True)
      aclient.publish(topics[2], b"qos 1", 1, retained=True)
      aclient.publish(topics[3], b"qos 2", 2, retained=True)
      time.sleep(1)
      print("sub is %s"%wildtopics[5])
      
      time.sleep(1)
      print("callback.message is %s"%callback.messages)
      self.assertEqual(len(callback.messages), 3)
      qoss = [callback.messages[i][2] for i in range(2)]  #qos质量取最小值
      self.assertTrue(1 in qoss and  0 in qoss, qoss)
      callback.clear()
      # aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2, retainHandling=1)])
      # time.sleep(1)
      # self.assertEqual(len(callback.messages), 0)
      aclient.disconnect()


    def test_subscribe_retainHandling_two(self):
      # retainHandling
      callback.clear()
      aclient.connect(host=host, port=port, cleanstart=True)
      aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2, retainHandling=1)])
      # aclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(2, retainHandling=1)])
      print("unsub")
      aclient.unsubscribe([wildtopics[5]])
      # aclient.unsubscribe(["TopicA/+"])
      time.sleep(1)
      print("pub is %s %s %s"%(topics[1],topics[2],topics[3]))
      aclient.publish(topics[1], b"qos 0", 0, retained=True)
      aclient.publish(topics[2], b"qos 1", 1, retained=True)
      aclient.publish(topics[3], b"qos 2", 2, retained=True)
      callback.clear()
      time.sleep(1)
      print("sub is %s"%wildtopics[5])
      aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(1, retainHandling=1)])
      # aclient.subscribe(["TopicA/+"], [MQTTV5.SubscribeOptions(1, retainHandling=1)])
      time.sleep(1)
      print(callback.messages)
      self.assertEqual(len(callback.messages), 3, callback.messages)
      callback.clear()

    """
      测试retainAsPublished=False
        客户端直接依靠消息中的 RETAIN 标识来区分这是一个正常的转发消息还是一个保留消息，而不是去判断消息是否是自己订阅后收到的第一个消息（转发消息甚至可能会先于保留消息被发送，视不同 Broker 的具体实现而定）。

    """
    def test_subscribe_retainAsPublished_one(self):
      callback.clear()
      callback2.clear()

      # retainAsPublished
      print("start")
      aclient.connect(host=host, port=port, cleanstart=True)
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2, retainAsPublished=False)])
      self.waitfor(callback.subscribeds, 1, 3)
      
      callback.clear()
      callback2.clear()

      aclient.publish(topics[0], b"retain as published false", 1, retained=False)
      aclient.publish(topics[0], b"retain as published true", 1, retained=True)

      self.waitfor(callback.messages, 2, 3)
      time.sleep(1)

      print("retainAsPublished result")
      self.assertEqual(len(callback.messages), 2, callback.messages)
      aclient.disconnect()
      self.assertEqual(callback.messages[0][3], False)
      self.assertEqual(callback.messages[1][3], False)
      print("end")
      cleanRetained()


    """
      测试retainAsPublished=True时，其他用户再订阅，查看收到messages中retained消息为true
    """

    def test_subscribe_retainAsPublished_two(self):
      callback.clear()
      callback2.clear()

      # retainAsPublished

      bclient.connect(host=host, port=port, cleanstart=True)
      bclient.publish(topics[0], b"retain as published false", 1, retained=False)
      bclient.publish(topics[0], b"retain as published true", 1, retained=True)
      aclient.connect(host=host, port=port, cleanstart=True)
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2, retainAsPublished=True)])
      self.waitfor(callback.subscribeds, 1, 3)

      self.waitfor(callback.messages, 2, 3)
      time.sleep(1)

      print("retainAsPublished result")
      self.assertEqual(len(callback.messages), 1, callback.messages)
      aclient.disconnect()
      self.assertEqual(callback.messages[0][3], True)
      self.assertEqual(callback.messages[0][1], b"retain as published true")

      cleanRetained()


    """
      测试retainAsPublished=False时，其他用户再订阅，查看收到messages中retained消息为true
    """
    def test_subscribe_retainAsPublished_three(self):
      callback.clear()
      callback2.clear()

      # retainAsPublished

      bclient.connect(host=host, port=port, cleanstart=True)
      bclient.publish(topics[0], b"retain as published false", 1, retained=False)
      bclient.publish(topics[0], b"retain as published true", 1, retained=True)
      aclient.connect(host=host, port=port, cleanstart=True)
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2, retainAsPublished=False)])

      time.sleep(5)

      print("retainAsPublished result")
      print("callback.messages is %s"%callback.messages)
      self.assertEqual(len(callback.messages), 1, callback.messages)
      aclient.disconnect()
      self.assertEqual(callback.messages[0][3], True)
      self.assertEqual(callback.messages[0][1], b"retain as published true")

      cleanRetained()


    def test_assigned_clientid(self):
      noidclient = mqtt_client.Client("")
      noidclient.setUserName(username1, password1)
      succeeded = False
      try:
        print("login")
        connack = noidclient.connect(host=host, port=port, cleanstart=True)
        # print("login end")
        # noidclient.disconnect()
        # logging.info("Assigned client identifier %s" % connack.properties.AssignedClientIdentifier)
        # self.assertTrue(connack.properties.AssignedClientIdentifier != "")
      except:
        # traceback.print_exc()
        succeeded = True
      print("The clientid must exist and not be empty")
      assert succeeded == True


    """
        测试修改已订阅topic中的qos质量
    """
    def test_topic_qos_revise_0(self):
        connack = aclient.connect(host=host,port=port,cleanstart=True)
        connack = bclient.connect(host=host,port=port,cleanstart=True)
        succeeded = True
        try:
            print(wildtopics[0])
            aclient.subscribe([wildtopics[0]],[MQTTV5.SubscribeOptions(0)])
            time.sleep(1)
            print("修改已订阅topic的qos")
            aclient.subscribe([wildtopics[0]],[MQTTV5.SubscribeOptions(1)])
            print("publish messages")
            time.sleep(1)
            bclient.publish(topics[1], b"qos =1",2,retained=False)
            time.sleep(2)
            print("callback.messages is %s"%callback.messages)
            assert len(callback.messages) == 1
            assert callback.messages[0][2] == 1
        except:
            succeeded = False
        self.assertEqual(succeeded,True)

    def test_topic_qos_revise_1(self):
        connack = aclient.connect(host=host,port=port,cleanstart=True)
        connack = bclient.connect(host=host,port=port,cleanstart=True)
        succeeded = True
        try:
            print(wildtopics[0])
            aclient.subscribe([wildtopics[0]],[MQTTV5.SubscribeOptions(1)])
            time.sleep(1)
            print("修改已订阅topic的qos")
            aclient.subscribe([wildtopics[0]],[MQTTV5.SubscribeOptions(2)])
            print("publish messages")
            time.sleep(1)
            bclient.publish(topics[1], b"qos =1",2,retained=False)
            time.sleep(2)
            print("callback.messages is %s"%callback.messages)
            assert len(callback.messages) == 1
            assert callback.messages[0][2] == 2
        except:
            succeeded = False
        self.assertEqual(succeeded,True)

    def test_topic_qos_revise_2(self):

        connack = aclient.connect(host=host,port=port,cleanstart=True)
        connack = bclient.connect(host=host,port=port,cleanstart=True)
        succeeded = True
        try:
            print(wildtopics[0])
            aclient.subscribe([wildtopics[0]],[MQTTV5.SubscribeOptions(0)])
            time.sleep(1)
            print("修改已订阅topic的qos")
            aclient.subscribe([wildtopics[0]],[MQTTV5.SubscribeOptions(2)])
            print("publish messages")
            time.sleep(1)
            bclient.publish(topics[1], b"qos =1",2,retained=False)
            time.sleep(2)
            print("callback.messages is %s"%callback.messages)
            assert len(callback.messages) == 1
            assert callback.messages[0][2] == 2
        except:
            succeeded = False
        self.assertEqual(succeeded,True)


    """
      测试订阅标识符
        1.客户端订阅主题 a/+ 并指定订阅标识符为 2，订阅主题a/b 并指定订阅标识符为3
        2。主题为 a/b 的 PUBLISH 报文将会携带两个不同的订阅标识符，一个消息将触发两个不同的消息处理程序。
    """
    def test_subscribe_identifiers_one(self):
      callback.clear()
      callback2.clear()

      bclient.connect(host=host, port=port, cleanstart=True)
      sub_properties = MQTTV5.Properties(MQTTV5.PacketTypes.SUBSCRIBE)
      sub_properties.SubscriptionIdentifier = 2
      bclient.subscribe([topics[1]], [MQTTV5.SubscribeOptions(1)], properties=sub_properties)

      sub_properties.clear()
      sub_properties.SubscriptionIdentifier = 3
      print("sub is %s"%(topics[0]+"/+"))
      bclient.subscribe([topics[0]+"/+"], [MQTTV5.SubscribeOptions(0)], properties=sub_properties)
      print("pub is %s"%topics[0])
      bclient.publish(topics[1], b"sub identifier test", 1, retained=False)

      self.waitfor(callback2.messages, 1, 3)
      print("callback2.messages is %s"%callback2.messages)
      self.assertEqual(len(callback2.messages), 2, callback2.messages)
      # expected_subsids = set([2, 3])
      expected_subsids = [2, 3]
      print("expected_subsids is %s"%expected_subsids)
      print("received_subsids1 is %s"%callback2.messages[0][5].SubscriptionIdentifier)
      print("received_subsids2 is %s"%callback2.messages[1][5].SubscriptionIdentifier)
      received_subsids1 = set(callback2.messages[0][5].SubscriptionIdentifier)
      received_subsids2 = set(callback2.messages[1][5].SubscriptionIdentifier)
      print("判断主题为 a/b 的 PUBLISH 报文将会携带两个不相同的订阅标识符")
      self.assertEquals(received_subsids1.issubset(expected_subsids), True) 
      self.assertEquals(received_subsids2.issubset(expected_subsids), True)   
      # self.assertEquals(received_subsids1, 2)
      # self.assertEqual(received_subsids2, 3)
      bclient.disconnect()

      callback.clear()
      callback2.clear()





    """
      测试订阅标识符
        1.客户端订阅主题 a/# 并指定订阅标识符为 1，订阅主题a/b 并指定订阅标识符为 2。
        2.主题为 a/b 的 PUBLISH 报文将会携带两个不同的订阅标识符，一个消息将触发两个不同的消息处理程序。
    """
    def test_subscribe_identifiers_two(self):
      callback.clear()
      callback2.clear()

      aclient.connect(host=host, port=port, cleanstart=True)
      sub_properties = MQTTV5.Properties(MQTTV5.PacketTypes.SUBSCRIBE)
      sub_properties.SubscriptionIdentifier = 456789
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)], properties=sub_properties)
      self.waitfor(callback.subscribeds, 1, 3)

      bclient.connect(host=host, port=port, cleanstart=True)
      sub_properties = MQTTV5.Properties(MQTTV5.PacketTypes.SUBSCRIBE)
      sub_properties.SubscriptionIdentifier = 2
      bclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)], properties=sub_properties)

      sub_properties.clear()
      sub_properties.SubscriptionIdentifier = 3
      print("sub is %s"%(topics[0]+"/#"))
      bclient.subscribe([topics[0]+"/#"], [MQTTV5.SubscribeOptions(2)], properties=sub_properties)
      print("pub is %s"%topics[0])
      bclient.publish(topics[0], b"sub identifier test", 1, retained=False)

      self.waitfor(callback.messages, 1, 3)
      print("callback.messages is %s"%callback.messages)
      self.assertEqual(len(callback.messages), 1, callback.messages)
      print("判断订阅标识符")
      self.assertEqual(callback.messages[0][5].SubscriptionIdentifier[0], 456789, callback.messages[0][5].SubscriptionIdentifier)
      aclient.disconnect()

      self.waitfor(callback2.messages, 1, 3)
      print("callback2.messages is %s"%callback2.messages)
      self.assertEqual(len(callback2.messages), 2, callback2.messages)
      expected_subsids = [2, 3]
      print("expected_subsids is %s"%expected_subsids)
      print("callback2.messages[0][5].SubscriptionIdentifier = ", callback2.messages[0][5].SubscriptionIdentifier)
      print("callback2.messages[1][5].SubscriptionIdentifier = ", callback2.messages[1][5].SubscriptionIdentifier)
      received_subsids = set(callback2.messages[0][5].SubscriptionIdentifier)
      print(received_subsids)
      self.assertEqual(received_subsids.issubset(expected_subsids), True)
      bclient.disconnect()

      callback.clear()
      callback2.clear()


      
    """
      测试nolocal=true时，服务端将不会向你转发你自己发布的消息。
    """
    def test_request_response(self):
      callback.clear()
      callback2.clear()

      aclient.connect(host=host, port=port, cleanstart=True)
      bclient.connect(host=host, port=port, cleanstart=True)
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2, noLocal=True)])
      self.waitfor(callback.subscribeds, 1, 3)

      bclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2, noLocal=True)])
      self.waitfor(callback.subscribeds, 1, 3)

      publish_properties = MQTTV5.Properties(MQTTV5.PacketTypes.PUBLISH)
      print("ResponseTopic is %s "%topics[0])
      publish_properties.ResponseTopic = topics[0]
      publish_properties.CorrelationData = b"334"
      # client a is the requester
      aclient.publish(topics[0], b"request", 1, properties=publish_properties)

      # client b is the responder
      self.waitfor(callback2.messages, 1, 3)
      print("callback2.messages is %s"%callback2.messages)
      print("callback.messages is %s"%callback.messages)
      self.assertEqual(len(callback.messages), 0,callback.messages)
      self.assertEqual(len(callback2.messages), 1, callback2.messages)

      self.assertEqual(len(callback2.messages), 1, callback2.messages)
      self.assertEqual(callback2.messages[0][5].ResponseTopic, topics[0],
                       callback2.messages[0][5])
      self.assertEqual(callback2.messages[0][5].CorrelationData, b"334",
                       callback2.messages[0][5])

      bclient.publish(callback2.messages[0][5].ResponseTopic, b"response", 1,
                      properties=callback2.messages[0][5])

      # client a gets the response
      self.waitfor(callback.messages, 1, 3)
      print("callback.messages is %s "%callback.messages)
      self.assertEqual(len(callback.messages), 1, callback.messages)

      aclient.disconnect()
      bclient.disconnect()

      callback.clear()
      callback2.clear()

    """
      1.测试客户端设置的topic alias。
        当前PUBLISH消息的topic为0，那么接受方需要解析 Topic Alias 中的值，用该值去查找对应的topic
        当前PUBLISH消息的topic长度不为0，那么接受方需要解析 Topic Alias 中的值，并且 将topic和该值进行映射。
    """
    def test_client_topic_alias_0(self):
      callback.clear()

      # no server side topic aliases allowed
      connack = aclient.connect(host=host, port=port, cleanstart=True)

      publish_properties = MQTTV5.Properties(MQTTV5.PacketTypes.PUBLISH)
      publish_properties.TopicAlias = 0 # topic alias 0 not allowed
      print("pub messages is:topic alias 0 ")
      print("pub is %s"%topics[0])
      aclient.publish(topics[0], "topic alias 0", 1, properties=publish_properties)

      # should get back a disconnect with Topic alias invalid
      print("callback.disconnects is %s"%(callback.disconnects))
      self.waitfor(callback.disconnects, 1, 2)
      print("callback.disconnects is %s"%(callback.disconnects))
      self.assertEqual(len(callback.disconnects), 1, callback.disconnects)
      #print("disconnect", str(callback.disconnects[0]["reasonCode"]))
      #self.assertEqual(callback.disconnects, 1, callback.disconnects)

      connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)
      connect_properties.TopicAliasMaximum = 0 # server topic aliases not allowed
      connect_properties.SessionExpiryInterval = 99999
      connack = aclient.connect(host=host, port=port, cleanstart=True,
                                           properties=connect_properties)
      print('!!!!!!!!!')
      print(connack)
      clientTopicAliasMaximum = 0

      if hasattr(connack.properties, "TopicAliasMaximum"):
        clientTopicAliasMaximum = connack.properties.TopicAliasMaximum

      if clientTopicAliasMaximum == 0:
        print(clientTopicAliasMaximum)
        aclient.disconnect()
        return

      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      self.waitfor(callback.subscribeds, 1, 3)

    """
      1.服务端默认topic alias个数为0，设置topic alias个数为1，设置topic alias
    """
    def test_client_topic_alias_1(self):
      #设置connect属性，topic alias 个数
      connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)
      connect_properties.TopicAliasMaximum = 1
      connack = aclient.connect(host=host, port=port, cleanstart=True,properties=connect_properties)
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      self.waitfor(callback.subscribeds, 1, 3)

      #设置publish属性，topic alias
      publish_properties = MQTTV5.Properties(MQTTV5.PacketTypes.PUBLISH)
      publish_properties.TopicAlias = 1
      
      print("当前PUBLISH消息的topic长度不为0，那么接受方需要解析 Topic Alias 中的值，并且 将topic和该值进行映射。")
      aclient.publish(topics[0], b"topic alias 1", 1, properties=publish_properties)
      self.waitfor(callback.messages, 1, 3)
      print("第一次publish")
      print(callback.messages)
      self.assertEqual(len(callback.messages), 1, callback.messages)
      print("前PUBLISH消息的topic为0，那么接受方需要解析 Topic Alias 中的值，用该值去查找对应的topic")
      aclient.publish("", b"topic alias 2", 1, properties=publish_properties)
      self.waitfor(callback.messages, 2, 3)
      print("第二次publish")
      print(callback.messages)
      self.assertEqual(len(callback.messages), 2, callback.messages)
      print("判断topic与订阅的topic一致")
      succeeded = True
      for i in range(len(callback.messages)):
        self.assertEqual(callback.messages[i][0],topics[0])
      assert succeeded == True
      aclient.disconnect() # should get rid of the topic aliases but not subscriptions

      # check aliases have been deleted
      callback.clear()
      aclient.connect(host=host, port=port, cleanstart=False)
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])

      aclient.publish(topics[0], b"topic alias 3", 1)
      self.waitfor(callback.messages, 1, 3)
      self.assertEqual(len(callback.messages), 1, callback.messages)

      publish_properties = MQTTV5.Properties(MQTTV5.PacketTypes.PUBLISH)
      publish_properties.TopicAlias = 1
      aclient.publish("", b"topic alias 4", 1, properties=publish_properties)

      # should get back a disconnect with Topic alias invalid
      self.waitfor(callback.disconnects, 1, 2)
      print("callback.disconnects is %s"%callback.disconnects)
      self.assertEqual(len(callback.disconnects), 1, callback.disconnects)
      #print("disconnect", str(callback.disconnects[0]["reasonCode"]))
      #self.assertEqual(callback.disconnects, 1, callback.disconnects)


    """
      1.服务端默认topic alias个数为0，设置topic alias个数为1，设置topic alias
    """
    def test_client_topic_alias_2(self):
      succeeded = False
      #设置connect属性，topic alias 个数
      connack = aclient.connect(host=host, port=port, cleanstart=True)
      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      self.waitfor(callback.subscribeds, 1, 3)

      #设置publish属性，topic alias
      publish_properties = MQTTV5.Properties(MQTTV5.PacketTypes.PUBLISH)
      publish_properties.TopicAlias = 1
      
      try:
        print("当前PUBLISH消息的topic长度不为0，那么接受方需要解析 Topic Alias 中的值，并且 将topic和该值进行映射。")
        aclient.publish(topics[0], b"topic alias 1", 1, properties=publish_properties)
        self.waitfor(callback.messages, 1, 3)
        print("第一次publish")
        print(callback.messages)
        self.assertEqual(len(callback.messages), 1, callback.messages)
      except:
        succeeded = True
      
      assert succeeded == True
      print("服务端设置topic alias默认个数为0，未设置个数时，无法设置topic %s"%"succeeded" if succeeded else "is fasle")


      # print("前PUBLISH消息的topic为0，那么接受方需要解析 Topic Alias 中的值，用该值去查找对应的topic")
      # aclient.publish("", b"topic alias 2", 1, properties=publish_properties)
      # self.waitfor(callback.messages, 2, 3)
      # print("第二次publish")
      # print(callback.messages)
      # self.assertEqual(len(callback.messages), 1, callback.messages)
      # print("判断topic与订阅的topic一致")
      # succeeded = True
      # for i in range(len(callback.messages)):
      #   self.assertEqual(callback.messages[i][0],topics[0])
      # assert callback.messages[0][1] == b"topic alias 1"
      # assert succeeded == True
      # time.sleep(2)
      # aclient.disconnect()  #目前aclient.disconnect()存在问题。


    """
      测试下行消息时，
      服务端为客户端设置的主题别名topic alias,
      目前服务端没有自主设置主题别名的能力
    """
    def test_server_topic_alias(self):
      pass
      callback.clear()

      serverTopicAliasMaximum = 1 # server topic alias allowed
      connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)
      connect_properties.TopicAliasMaximum = serverTopicAliasMaximum
      connack = aclient.connect(host=host, port=port, cleanstart=True,
                                       properties=connect_properties)
      clientTopicAliasMaximum = 0
      if hasattr(connack.properties, "TopicAliasMaximum"):
        clientTopicAliasMaximum = connack.properties.TopicAliasMaximum

      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      self.waitfor(callback.subscribeds, 1, 3)

      for qos in range(3):
         aclient.publish(topics[0], b"topic alias 1", qos)
      self.waitfor(callback.messages, 3, 3)
      self.assertEqual(len(callback.messages), 3, callback.messages)
      print("callback.messages is %s "%callback.messages)
      aclient.disconnect()

      # first message should set the topic alias
      print("callback.messagedicts is %s"%callback.messagedicts)
      self.assertTrue(hasattr(callback.messagedicts[0]["properties"], "TopicAlias"), callback.messagedicts[0]["properties"])
      topicalias = callback.messagedicts[0]["properties"].TopicAlias

      print("server topic alias is %s"%topicalias)
      self.assertTrue(topicalias > 0)
      self.assertEqual(callback.messagedicts[0]["topicname"], topics[0])

      self.assertEqual(callback.messagedicts[1]["properties"].TopicAlias, topicalias)
      self.assertEqual(callback.messagedicts[1]["topicname"], "")

      self.assertEqual(callback.messagedicts[2]["properties"].TopicAlias, topicalias)
      self.assertEqual(callback.messagedicts[1]["topicname"], "")

      callback.clear()

      serverTopicAliasMaximum = 0 # no server topic alias allowed
      connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)
      connect_properties.TopicAliasMaximum = serverTopicAliasMaximum # default is 0
      connack = aclient.connect(host=host, port=port, cleanstart=True,
                                       properties=connect_properties)
      clientTopicAliasMaximum = 0
      if hasattr(connack.properties, "TopicAliasMaximum"):
        clientTopicAliasMaximum = connack.properties.TopicAliasMaximum

      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      self.waitfor(callback.subscribeds, 1, 3)

      for qos in range(3):
         aclient.publish(topics[0], b"topic alias 1", qos)
      self.waitfor(callback.messages, 3, 3)
      self.assertEqual(len(callback.messages), 3, callback.messages)
      aclient.disconnect()

      # No topic aliases
      self.assertFalse(hasattr(callback.messagedicts[0]["properties"], "TopicAlias"), callback.messagedicts[0]["properties"])
      self.assertFalse(hasattr(callback.messagedicts[1]["properties"], "TopicAlias"), callback.messagedicts[1]["properties"])
      self.assertFalse(hasattr(callback.messagedicts[2]["properties"], "TopicAlias"), callback.messagedicts[2]["properties"])

      callback.clear()

      serverTopicAliasMaximum = 0 # no server topic alias allowed
      connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)
      connect_properties.TopicAliasMaximum = serverTopicAliasMaximum # default is 0
      connack = aclient.connect(host=host, port=port, cleanstart=True,
                                       properties=connect_properties)
      clientTopicAliasMaximum = 0
      if hasattr(connack.properties, "TopicAliasMaximum"):
        clientTopicAliasMaximum = connack.properties.TopicAliasMaximum

      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      self.waitfor(callback.subscribeds, 1, 3)

      for qos in range(3):
         aclient.publish(topics[0], b"topic alias 1", qos)
      self.waitfor(callback.messages, 3, 3)
      self.assertEqual(len(callback.messages), 3, callback.messages)
      aclient.disconnect()

      # No topic aliases
      self.assertFalse(hasattr(callback.messagedicts[0]["properties"], "TopicAlias"), callback.messagedicts[0]["properties"])
      self.assertFalse(hasattr(callback.messagedicts[1]["properties"], "TopicAlias"), callback.messagedicts[1]["properties"])
      self.assertFalse(hasattr(callback.messagedicts[2]["properties"], "TopicAlias"), callback.messagedicts[2]["properties"])



    """
      测试发送message最大字节数
        1.对端如果发现将发送的包大于该大小，就默默丢弃，不关闭连接
        2.自己收到超过自己通告的Maximum Packet Size需要关闭连接
        #目前appconfig和脚本中设置messages最大字节数取两个中嘴小值（目前appconfig中设置了65535）
    """
    def test_maximum_packet_size_server(self):
      callback.clear()

      # 1. server max packet size
      connack = aclient.connect(host=host, port=port, cleanstart=True)
      serverMaximumPacketSize = 2**28-1 #2**28-1=268435456-1=268435455
      if hasattr(connack.properties, "MaximumPacketSize"):
        serverMaximumPacketSize = connack.properties.MaximumPacketSize

      print("serverMaximumPacketSize length is %s"%(serverMaximumPacketSize))
      if serverMaximumPacketSize < 65535:
        print("serverMaximumPacketSize length is %s"%(serverMaximumPacketSize))
        # publish bigger packet than server can accept
        payload = b"."*serverMaximumPacketSize
        aclient.publish(topics[0], payload, 0)
        # should get back a disconnect with packet size too big
        self.waitfor(callback.disconnects, 1, 2)
        self.assertEqual(len(callback.disconnects), 1, callback.disconnects)
        print(callback.disconnects[0]["reasonCode"])
        self.assertEqual(str(callback.disconnects[0]["reasonCode"]),
          "Packet too large", str(callback.disconnects[0]["reasonCode"]))
      else:
        aclient.disconnect()
    
    """
      测试client发送错误信息时server主动断开连接时，服务端是否发送disconnect消息
    """
    def test_server_disconnected_reasoncode(self):
      aclient.setUserName(username1, password2)
      succeeded = False
      try:
        aclient.connect(host=host,port=port,cleanstart=True)

        publish_properties = MQTTV5.Properties(MQTTV5.PacketTypes.PUBLISH)
        publish_properties.TopicAlias = 0 # topic alias 0 not allowed
        print("pub messages is:topic alias 0 ")
        print("pub is %s"%topics[0])
        aclient.publish(topics[0], "topic alias 0", 1, properties=publish_properties)
        self.waitfor(callback.disconnects, 1, 2)
      except:
        succeeded = True
      assert(succeeded,True)
      print(callback.disconnects)
      self.assertEqual(len(callback.disconnects), 1)


    """
      测试发送message最大字节数
        1.自己收到超过自己通告的Maximum Packet Size需要关闭连接
        #目前appconfig和脚本中设置messages最大字节数取两个中嘴小值（目前appconfig中设置了65535）
    """
    def test_maximum_packet_size_client(self):
      print("设置最大字节数为64")
      # 1. client max packet size
      maximumPacketSize = 64 # max packet size we want to receive（maximumPacketSize 表示单个MQTT控制报文的大小，如果不携带表示不限制）
      connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)
      connect_properties.MaximumPacketSize = maximumPacketSize
      connack = aclient.connect(host=host, port=port, cleanstart=True,
                                             properties=connect_properties)
      # serverMaximumPacketSize = 2**28-1
      # if hasattr(connack.properties, "MaximumPacketSize"):
      #   serverMaximumPacketSize = connack.properties.MaximumPacketSize

      aclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      self.waitfor(callback.subscribeds, 1, 3)

      # send a small enough packet, should get this one back
      payload = b"."*(int(maximumPacketSize/2)) #maximumPacketSize 表示单个MQTT控制报文的大小，如果不携带表示不限制
      aclient.publish(topics[0], payload, 0)
      self.waitfor(callback.messages, 1, 3)
      self.assertEqual(len(callback.messages), 1, callback.messages)

      # send a packet too big to receive
      payload = b"."*maximumPacketSize #maximumPacketSize 表示单个MQTT控制报文的大小，如果不携带表示不限制
      aclient.publish(topics[0], payload, 1)
      self.waitfor(callback.messages, 2, 3)
      print(len(callback.messages))
      self.assertEqual(len(callback.messages), 1, callback.messages)

      # aclient.disconnect()  #自己取消


    def test_server_keep_alive(self):
      callback.clear()

      connack = aclient.connect(host=host, port=port, keepalive=120, cleanstart=True)
      self.assertTrue(hasattr(connack.properties, "ServerKeepAlive"))
      self.assertEqual(connack.properties.ServerKeepAlive, 120)

      aclient.disconnect()



    """
      1.测试下行流控
    """
    def test_flow_control1(self):
      pass
      testcallback = Callbacks()
      # no callback means no background thread, to control receiving
      testclient = mqtt_client.Client(clientid1.encode("utf-8"))
      testclient.setUserName(username1, password1)

      # set receive maximum - the number of concurrent QoS 1 and 2 messages
      clientReceiveMaximum = 2 # set to low number so we can test
      connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)
      connect_properties.ReceiveMaximum = clientReceiveMaximum
      connect_properties.SessionExpiryInterval = 0  #server和client则不会保存session信息。
      connack = testclient.connect(host=host, port=port, cleanstart=True,
                   properties=connect_properties)

      # serverReceiveMaximum = 2**16-1 # the default
      print("connack.properties = ", connack.properties)
      # if hasattr(connack.properties, "ReceiveMaximum"):
      #   serverReceiveMaximum = connack.properties.ReceiveMaximum

      receiver = testclient.getReceiver()

      testclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)])
      receiver.receive(testcallback)
      self.waitfor(testcallback.subscribeds, 1, 3)

      pubs = 0
      for i in range(1, clientReceiveMaximum + 2):
        testclient.publish(topics[0], "message %d" % i, 1)
        pubs += 1

      # get two publishes
      acks = 0
      while True:
        response1 = MQTTV5.unpackPacket(MQTTV5.getPacket(testclient.sock))
        if response1.fh.PacketType == MQTTV5.PacketTypes.PUBLISH:
          break
        self.assertEqual(response1.fh.PacketType, MQTTV5.PacketTypes.PUBACK)
        acks += 1
        del receiver.outMsgs[response1.packetIdentifier]
      self.assertEqual(response1.fh.PacketType, MQTTV5.PacketTypes.PUBLISH)
      self.assertEqual(response1.fh.QoS, 1, response1.fh.QoS)

      while True:
        response2 = MQTTV5.unpackPacket(MQTTV5.getPacket(testclient.sock))
        if response2.fh.PacketType == MQTTV5.PacketTypes.PUBLISH:
          break
        self.assertEqual(response2.fh.PacketType, MQTTV5.PacketTypes.PUBACK)
        acks += 1
        del receiver.outMsgs[response2.packetIdentifier]
      self.assertEqual(response2.fh.PacketType, MQTTV5.PacketTypes.PUBLISH)
      self.assertEqual(response2.fh.QoS, 1, response1.fh.QoS)

      while acks < pubs:
        ack = MQTTV5.unpackPacket(MQTTV5.getPacket(testclient.sock))
        self.assertEqual(ack.fh.PacketType, MQTTV5.PacketTypes.PUBACK)
        acks += 1
        del receiver.outMsgs[ack.packetIdentifier]

      with self.assertRaises(socket.timeout):
        # this should time out because we haven't acknowledged the first one
        response3 = MQTTV5.unpackPacket(MQTTV5.getPacket(testclient.sock))

      # ack the first one
      puback = MQTTV5.Pubacks()
      puback.packetIdentifier = response1.packetIdentifier
      testclient.sock.send(puback.pack())

      # now get the next packet
      response3 = MQTTV5.unpackPacket(MQTTV5.getPacket(testclient.sock))
      self.assertEqual(response3.fh.PacketType, MQTTV5.PacketTypes.PUBLISH)
      self.assertEqual(response3.fh.QoS, 1, response1.fh.QoS)

      # ack the second one
      puback.packetIdentifier = response2.packetIdentifier
      testclient.sock.send(puback.pack())

      # ack the third one
      puback.packetIdentifier = response3.packetIdentifier
      testclient.sock.send(puback.pack())

      testclient.disconnect()

    """
      1.测试上行流控
    """
    def test_flow_control2(self):
      pass
      testcallback = Callbacks()
      # no callback means no background thread, to control receiving
      testclient = mqtt_client.Client(clientid1.encode("utf-8"))

      # get receive maximum - the number of concurrent QoS 1 and 2 messages
      connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)
      connect_properties.SessionExpiryInterval = 0
      testclient.setUserName(username1, password1)
      connack = testclient.connect(host=host, port=port, cleanstart=True)

      # serverReceiveMaximum = 2**16-1 # the default
      serverReceiveMaximum = 5
      print("connack.properties = ", connack.properties)
      if hasattr(connack.properties, "ReceiveMaximum"):
        serverReceiveMaximum = connack.properties.ReceiveMaximum

      receiver = testclient.getReceiver()

      # send number of messages to exceed receive maximum
      qos = 1
      pubs = 0
      for i in range(1, serverReceiveMaximum + 2):
        testclient.publish(topics[0], "message %d" % i, qos)
        pubs += 1
        time.sleep(.1)

      # should get disconnected...
      while testcallback.disconnects == []:
        receiver.receive(testcallback)
      self.waitfor(testcallback.disconnects, 1, 1)
      self.assertEqual(len(testcallback.disconnects), 1, len(testcallback.disconnects))
      self.assertEqual(testcallback.disconnects[0]["reasonCode"].value, 147,
                       testcallback.disconnects[0]["reasonCode"].value)

    def test_will_delay(self):
      """
      the will message should be received earlier than the session expiry

      """
      callback.clear()
      callback2.clear()

      will_properties = MQTTV5.Properties(MQTTV5.PacketTypes.WILLMESSAGE)
      connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)

      # set the will delay and session expiry to the same value -
      # then both should occur at the same time
      will_properties.WillDelayInterval = 3 # in seconds
      connect_properties.SessionExpiryInterval = 10

      connack = aclient.connect(host=host, port=port, cleanstart=True, properties=connect_properties,
        willProperties=will_properties, willFlag=True, willTopic=topics[0], willMessage=b"test_will_delay will message")
      self.assertEqual(connack.reasonCode.getName(), "Success")
      # self.assertEqual(connack.sessionPresent, False) #自己取消

      connack = bclient.connect(host=host, port=port, cleanstart=True)
      bclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)]) # subscribe to will message topic
      self.waitfor(callback2.subscribeds, 1, 3)

      # terminate client a and wait for the will message
      start = time.time()
      aclient.terminate()
      while callback2.messages == []:
        time.sleep(.1)
      duration = time.time() - start
      #print(duration)
      self.assertAlmostEqual(duration, 4, delta=1)
      self.assertEqual(callback2.messages[0][0], topics[0])
      self.assertEqual(callback2.messages[0][1], b"test_will_delay will message")

      aclient.disconnect()
      bclient.disconnect()

      callback.clear()
      callback2.clear()

      # if session expiry is less than will delay then session expiry is used
      will_properties.WillDelayInterval = 5 # in seconds
      connect_properties.SessionExpiryInterval = 0

      connack = aclient.connect(host=host, port=port, cleanstart=True, properties=connect_properties,
        willProperties=will_properties, willFlag=True, willTopic=topics[0], willMessage=b"test_will_delay will message")
      self.assertEqual(connack.reasonCode.getName(), "Success")
      # self.assertEqual(connack.sessionPresent, False) #自己取消

      connack = bclient.connect(host=host, port=port, cleanstart=True)
      bclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)]) # subscribe to will message topic
      self.waitfor(callback2.subscribeds, 1, 3)

      # terminate client a and wait for the will message
      aclient.terminate()
      start = time.time()
      while callback2.messages == []:
        time.sleep(.1)
      duration = time.time() - start
      #print(duration)
      self.assertAlmostEqual(duration, 1, delta=1)
      self.assertEqual(callback2.messages[0][0], topics[0])
      self.assertEqual(callback2.messages[0][1], b"test_will_delay will message")

      aclient.disconnect()
      bclient.disconnect()

      callback.clear()
      callback2.clear()

            # if session expiry is less than will delay then session expiry is used
      will_properties.WillDelayInterval = 5 # in seconds
      connect_properties.SessionExpiryInterval = 2

      connack = aclient.connect(host=host, port=port, cleanstart=True, properties=connect_properties,
        willProperties=will_properties, willFlag=True, willTopic=topics[0], willMessage=b"test_will_delay will message")
      self.assertEqual(connack.reasonCode.getName(), "Success")
      # self.assertEqual(connack.sessionPresent, False) #自己取消

      connack = bclient.connect(host=host, port=port, cleanstart=True)
      bclient.subscribe([topics[0]], [MQTTV5.SubscribeOptions(2)]) # subscribe to will message topic
      self.waitfor(callback2.subscribeds, 1, 3)

      # terminate client a and wait for the will message
      aclient.terminate()
      start = time.time()
      while callback2.messages == []:
        time.sleep(.1)
      duration = time.time() - start
      #print(duration)
      self.assertAlmostEqual(duration, 3, delta=1)
      self.assertEqual(callback2.messages[0][0], topics[0])
      self.assertEqual(callback2.messages[0][1], b"test_will_delay will message")

      aclient.disconnect()
      bclient.disconnect()

      callback.clear()
      callback2.clear()

    """
        测试服务端是否支持共享订阅
    """
    def test_shared_subscriptions(self):
      pass
      callback.clear()
      callback2.clear()
      shared_sub_topic = '$share/sharename/' + topic_prefix + 'x'
      shared_pub_topic = topic_prefix + 'x'

      connack = aclient.connect(host=host, port=port, cleanstart=True)
      self.assertEqual(connack.reasonCode.getName(), "Success")
      # self.assertEqual(connack.sessionPresent, False) #自己取消
      aclient.subscribe([shared_sub_topic, topics[0]], [MQTTV5.SubscribeOptions(2)]*2) 
      self.waitfor(callback.subscribeds, 1, 3)

      connack = bclient.connect(host=host, port=port, cleanstart=True)
      self.assertEqual(connack.reasonCode.getName(), "Success")
      # self.assertEqual(connack.sessionPresent, False) #自己取消
      bclient.subscribe([shared_sub_topic, topics[0]], [MQTTV5.SubscribeOptions(2)]*2) 
      self.waitfor(callback2.subscribeds, 1, 3)

      callback.clear()
      callback2.clear()

      count = 1
      for i in range(count):
        bclient.publish(topics[0], "message "+str(i), 0)
      j = 0
      while len(callback.messages) + len(callback2.messages) < 2*count and j < 20:
        time.sleep(.1)
        j += 1
      time.sleep(1)
      self.assertEqual(len(callback.messages), count)
      self.assertEqual(len(callback2.messages), count)

      callback.clear()
      callback2.clear()

      for i in range(count):
        bclient.publish(shared_pub_topic, "message "+str(i), 0)
      j = 0
      while len(callback.messages) + len(callback2.messages) < count and j < 20:
        time.sleep(.1)
        j += 1
      time.sleep(1)
      # Each message should only be received once
      self.assertEqual(len(callback.messages) + len(callback2.messages), count)

      aclient.disconnect()
      bclient.disconnect()

      
    """
        1.测试服务质量为零
    """
    def test_messages_qos_zero(self):
        print("QoS is minimized test starting")
        message = b"sub_qos = 0,pub_qos=0"
        sub_qos = 0
        succeeded = True
        result =[]
        try:
            result = qostest(self,sub_qos=sub_qos,pub_qos=0,message=message)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][2],sub_qos,result[0][2])
            self.assertEqual(result[1][2],sub_qos,result[0][2])
        except:
            succeeded = False
        topic_result = assert_topic_result(self,result,topics[1])
        self.assertTrue(topic_result)
        self.assertTrue(succeeded)
        message = b"sub_qos = 0,pub_qos=1"
        try:
            result1 = qostest(self,sub_qos=0,pub_qos=1,message=message)
            self.assertEqual(len(result1), 2)
            self.assertEqual(result1[0][2],sub_qos,result1[0][2])
            self.assertEqual(result1[1][2],sub_qos,result1[0][2])
        except:
            succeeded = False
        topic_result = assert_topic_result(self,result1,topics[1])
        self.assertTrue(topic_result)
        self.assertTrue(succeeded)
        message = b"sub_qos = 0,pub_qos=2"
        try:
            result2 = qostest(self,sub_qos=0,pub_qos=2,message=message)
            self.assertEqual(len(result2), 2)
            self.assertEqual(result2[0][2],sub_qos,result2[0][2])
            self.assertEqual(result2[1][2],sub_qos,result2[0][2])
        except:
            succeeded = False
        topic_result = assert_topic_result(self,result1,topics[1])
        self.assertTrue(topic_result)
        self.assertTrue(succeeded)
        print("QoS minimum test was ","succeeded" if succeeded else "falsed")
        
    
    """
        1.测试服务质量为1
    """
    def test_messages_qos_one(self):
        print("QoS is minimized test starting")
        message = b"QoS is minimized "
        sub_qos = 1
        result = []
        succeeded = True
        print("qos =0")
        try:
            result = qostest(self,sub_qos=sub_qos,pub_qos=0,message=message)
            print(len(result))
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][2],0,result[0][2])
            self.assertEqual(result[1][2],0,result[0][2])
        except:
            succeeded = False
        topic_result = assert_topic_result(self,result,topics[1])
        self.assertTrue(topic_result)
        self.assertTrue(succeeded)
        print("qos =1")
        succeeded = True
        try:
            result1 = qostest(self,sub_qos=sub_qos,pub_qos=1,message=message)
            self.assertEqual(len(result1), 2)
            self.assertEqual(result1[0][2],sub_qos,result1[0][2])
            self.assertEqual(result1[1][2],sub_qos,result1[0][2])
        except:
            succeeded = False
        topic_result = assert_topic_result(self,result1,topics[1])
        self.assertTrue(topic_result)
        self.assertTrue(succeeded)
        print("qos =2")
        succeeded = True
        try:
            result2 = qostest(self,sub_qos=sub_qos,pub_qos=2,message=message)
            self.assertEqual(len(result2), 2)
            self.assertEqual(result2[0][2],sub_qos,result2[0][2])
            self.assertEqual(result2[1][2],sub_qos,result2[0][2])
        except:
            succeeded = False
        topic_result = assert_topic_result(self,result2,topics[1])
        self.assertTrue(topic_result)
        self.assertTrue(succeeded)
        print("QoS minimum test was ","succeeded" if succeeded else "falsed")

            
            
    #测试服务质量为2
    def test_messages_qos_two(self):
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
        topic_result = assert_topic_result(self,result,topics[1])
        self.assertTrue(topic_result)
        self.assertTrue(succeeded)
        try:
            result1 = qostest(self,sub_qos=sub_qos,pub_qos=1,message=message)
            self.assertEqual(len(result1), 2)
            self.assertEqual(result1[0][2],1,result1[0][2])
            self.assertEqual(result1[1][2],1,result1[0][2])
        except:
            succeeded = False
        topic_result = assert_topic_result(self,result1,topics[1])
        self.assertTrue(topic_result)
        self.assertTrue(succeeded)
        try:
            result2 = qostest(self,sub_qos=sub_qos,pub_qos=2,message=message)
            self.assertEqual(len(result2), 2)
            self.assertEqual(result2[0][2],2,result2[0][2])
            self.assertEqual(result2[1][2],2,result2[0][2])
        except:
            succeeded = False
        topic_result = assert_topic_result(self,result2,topics[1])
        self.assertTrue(topic_result)
        self.assertTrue(succeeded)  
        print("QoS minimum test was ","succeeded" if succeeded else "falsed")
 

    """
      测试mqtt v3.x与v5.x互通"
    """
    # def test_v3_v5(self):
        # print("测试mqtt v3.x与v5.x互通")
        # print(" Start：测试场景一:v3.x订阅topic，v5.x发布消息")
        # succeeded =True
        # callback.clear()
        # callback4.clear(self)
        # try:
        #     connectA = aclient.connect(host=host,port=port,cleanstart=True)
        #     connectB = dclient.connect(host=host,port=port,cleanstart=True)
        #     print("用户A订阅的topic：%s"%wildtopics[0])
        #     aclient.subscribe([wildtopics[0]],[MQTTV5.SubscribeOptions(1)])
        #     print("用户B发布消息topic：%s"%topics[1])
        #     for i in range(3):
        #         print("i = %d"%i)
        #         dclient.publish(topics[1],b"test V3.x and V5.x interoperability num=%d"%i,i)
        #         time.sleep(1)    
        # except:
        #     print("测试v3.x与v5.x互通出现错误")
        #     succeeded = False
        # print("用户A获取的消息内容长度%d %s"%(len(callback.messages),callback.messages))
        # assert len(callback.messages) == 3
        # print("判断用户A收到的消息，topic格式与期望一致")
        # topic_result = assert_topic_result(self,callback.messages,topics[1])
        # assert topic_result == True
        # self.assertEqual(callback.messages[0][1] == 0,"用户B收到的消息质量为%d"%callback.messages[0][1])
        # self.assertEqual(callback.messages[0][1] == 1,"用户B收到的消息质量为%d"%callback.messages[0][1])
        # self.assertEqual(callback.messages[0][1] == 1,"用户B收到的消息质量为%d"%callback.messages[0][1])
        # assert succeeded ==True
        # aclient.disconnect()
        # dclient.disconnect()
        # print(" End：测试场景一:v3.x订阅topic，v5.x发布消息 %s"%"succeeded" if succeeded else "is False")


        # succeeded = True
        # print(" Start：测试场景二:v5.x订阅topic，v3.x发布消息")
        # try:
        #     connectA = aclient.connect(host=host,port=port,cleanstart=True)
        #     connectB = dclient.connect(host=host,port=port,cleanstart=True)
        #     print("用户B订阅的topic：%s"%wildtopics[0])
        #     dclient.subscribe([wildtopics[0]],[1])
        #     print("用户A发布消息topic：%s"%topics[1])
        #     for i in range(3):
        #         aclient.publish(topics[1],b"est V3.x and V5.x interoperability", i,retained=False)
        #         time.sleep(1)
        # except:
        #     print("测试v3.x与v5.x互通出现错误")
        #     succeeded = False
        # print("callback4.messages is %s"%callback4.messages)
        # assert len(callback4.messages) == 3
        # print("判断用户B收到的消息，topic格式与期望一致")
        # topic_result = assert_topic_result(self,callback.messages,topics[1])
        # assert topic_result == True
        # self.assertEqual(callback.messages[0][1] == 0,"用户B收到的消息质量为%d"%callback.messages[0][1])
        # self.assertEqual(callback.messages[0][1] == 1,"用户B收到的消息质量为%d"%callback.messages[0][1])
        # self.assertEqual(callback.messages[0][1] == 2,"用户B收到的消息质量为%d"%callback.messages[0][1])
        # assert succeeded ==True
        # aclient.disconnect()
        # dclient.disconnect()
        # print(" End：测试场景一:v5.x订阅topic，v3.x发布消息 %s"%"succeeded" if succeeded else "is False")



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
            print(wildtopics[7],topics[1])
            self.assertEqual(len(callbackresult), 2,"callbackresult is %s"%(callbackresult))
            self.assertEqual(callbackresult[0][1],message)
            self.assertEqual(callbackresult[1][1],message)
        except:
            traceback.print_exc()
            succeeded = False
        assert succeeded ==True
        succeeded =True
        try:
            callbackresult = topictest(self,sub_index=7,pub_index=5,message=message)
            print(wildtopics[7],topics[5])
            self.assertEqual(len(callbackresult), 2,"callbackresult is $s"%(callbackresult))
            self.assertEqual(callbackresult[0][1],message)
            self.assertEqual(callbackresult[1][1],message)
        except:
            traceback.print_exc()
            succeeded = False
        print("callback2.messages is %s"%callback2.messages)
        print("topics format +/#  test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    
    #验证topic格式为+/+匹配规则
    def test_topic_format_fifth(self):
        print("test topic:+/+ starting")
        succeeded = True
        try:
            callback.clear()
            connack = aclient.connect(host=host, port=port, cleanstart=True)
            print(wildtopics[5])
            aclient.subscribe([wildtopics[5]], [MQTTV5.SubscribeOptions(2)])
            connack = bclient.connect(host=host, port=port, cleanstart=True)
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
            connect = aclient.connect(host=host,port=port,cleanstart=True)
            print(topics[6])
            print("user sub")
            aclient.subscribe([topics[6]],[2])
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
            connect = bclient.connect(host=host,port=port,cleanstart=True)
            print(topics[6])
            print("user pub")
            bclient.publish(topics[6],b'abc',2,retained=False)
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
            callbackresult = topictest(self,sub_index=9,pub_index=7,message=message)
            self.assertEqual(len(callbackresult), 2,"callbackresult is %s"%(callbackresult))
            self.assertEqual(callbackresult[0][1],message)
            self.assertEqual(callbackresult[1][1],message)
            self.assertEqual(callbackresult[0][0],topics[7])
            self.assertEqual(callbackresult[1][0],wildtopics[9])
        except:
            traceback.print_exc()
            succeeded = False
        print("topics format topic/a/b/c/d/e/f/g  test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded




def setData():
  global topics, wildtopics, nosubscribe_topics, host, port,clientid1,clientid2,clientid3,host,port,password1,password2,username1,username2,username3,appid,server
  #沙箱地址
  host = "mqtt-ejabberd-hsb.easemob.com"   #发送地址
  port = 2883 #发送端口

  #EMQ地址
  # host = "broker.emqx.io"
  # port = 1883

  # # 本地地址
  # host = "172.17.1.160"
  # port = 1883
  # topics =  ("TopicA", "TopicA/B", "Topic/C", "TopicA/C", "/TopicA")
  # wildtopics = ("TopicA/+", "+/C", "#", "/#", "/+", "+/+", "TopicA/#")
  # nosubscribe_topics = ("test/nosubscribe",)


  clientid1 = "mqtttest1@1wyp94"  #开启鉴权后clientid格式为deviceid@appkeyappid deviceid任意取值，只要保证唯一。
  clientid2 = "mqtttest2@1wyp94"
  clientid3 = "mqtttest3@1wyp94"
  appid = {"right_appid":"1wyp94","error_appid":"123","noappid":""} #构建appid
  server = 5.0
  username1,username2,username3 = b"mqtttest1",b"mqtttest2",b"mqtttest3"  #用户名称
  password1 = b"$t$YWMtmkljBq41Eeu39Qv1-LC0RfLBUj23REhmv2d9MJZsm8W1kvwQpbMR67NY5XfrXvBLAwMAAAF5QGXBIQBPGgDJJHzH_o8JNe8OnCH7DOZHrKQU05cDi1qZLKDIhcWn9w"  #用户密码，实际为与用户匹配的token
  password2 = b"$t$YWMtq6E8qq41EeuYmM-_R3av2fLBUj23REhmv2d9MJZsm8W6vmEgpbMR655ln0Nsooa_AwMAAAF5QGYyygBPGgAx8nXG_XiJ4gzEWSL0VjTmr07KfvmGOT2NgXSL9jsZvA"  #用户密码，实际为与用户匹配的token
  password2 = b"$t$YWMtq6E8qq41EeuYmM-_R3av2fLBUj23REhmv2d9MJZsm8W6vmEgpbMR655ln0Nsooa_AwMAAAF5QGYyygBPGgAx8nXG_XiJ4gzEWSL0VjTmr07KfvmGOT2NgXSL9jsZvA"  #用户密码，实际为与用户匹配的token
  topics =  ("TopicA", "TopicA/B", "Topic/C", "TopicA/C", "/TopicA","TopicA/B/C","topicA/B/C/D/E/F/G/H/I","topic/a/b/c/d/e/f/g")
  wildtopics = ("TopicA/+", "+/C", "#", "/#", "/+", "+/+", "TopicA/#","+/#","topicA/B/C/D/E/F/G/H/I","topic/a/b/c/d/e/f/g")
  nosubscribe_topics = ("test/nosubscribe",)
  length_topic = "1234567890123456789012345678901234567890123456789012345678901234"
  length64_fold = "a/b/c/d/e/f/g/f/h/i/gk/l/m/n/o/p/q/r/s/t/u/v/w/x/y/z/1/2/3/4/5/6"
  length_clientid = "123456789012345678901234567890123456789012345678901234567@" + appid["right_appid"]
  deviceid = {"right_deviceid":"testdeviceid1","error_deviceid":""}    #构建deviceid
  error_cliendid = {"error_format_one":deviceid["right_deviceid"] + "#" + appid["right_appid"],\
      "error_appid":deviceid["right_deviceid"] + "@",\
      "error_format_two":deviceid["right_deviceid"]  + appid["right_appid"],\
      "appid_empty":deviceid["right_deviceid"] + "@" + appid["noappid"],\
      "overlength_clientid":"123456789012345678901234567890123456789012345678901234567@1RK24W123456789012345678901234567890123456789012345678901234567@" + appid["right_appid"]}



if __name__ == "__main__":
  try:
    opts, args = getopt.gnu_getopt(sys.argv[1:], "h:p:vzdsn:",
      ["help", "hostname=", "port=", "iterations="])
  except getopt.GetoptError as err:
    logging.info(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

  iterations = 1

  global topics, wildtopics, nosubscribe_topics, host, topic_prefix
  topic_prefix = "client_test5/"
  topics = [topic_prefix+topic for topic in ["TopicA", "TopicA/B", "Topic/C", "TopicA/C", "/TopicA"]]
  wildtopics = [topic_prefix+topic for topic in ["TopicA/+", "+/C", "#", "/#", "/+", "+/+", "TopicA/#"]]
  print(wildtopics)
  nosubscribe_topics = ("test/nosubscribe",)
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
      sys.argv.remove("-p") if "-p" in sys.argv else sys.argv.remove("--port")
      sys.argv.remove(a)
    elif o in ("--iterations"):
      iterations = int(a)

  root = logging.getLogger()
  root.setLevel(logging.ERROR)

  logging.info("hostname %s port %d", host, port)
  print("argv", sys.argv)
  for i in range(iterations):
    unittest.main()
