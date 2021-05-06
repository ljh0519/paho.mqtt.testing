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

      cclient = mqtt_client.Client(clientid3.encode("utf-8"))
      cclient.registerCallback(callback3)
      cclient.setUserName(username3, password3)

      # dclient = mqtt_client_v311.Client(clientid2.encode("utf-8"))
      # dclient.registerCallback(callback2)
      # dclient.setUserName(username2, password2)


    # def setUp(self):
    #   callback.clear()
    #   callback2.clear()

    # def tearDown(self):
    #     cleanup()



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
        #     bclient.connect(host=host,port=port,cleanstart=True)
        #     for i in range(number):
        #       print(i)
        #       aclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
        #       bclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
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
            aclient.connect(host=host, port=port,cleanstart=True)
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
      connack = aclient.connect(host=host,port=port,cleanstart=True)
      connack = bclient.connect(host=host,port=port,cleanstart=True)
      connack = cclient.connect(host=host,port=port,cleanstart=True)
      succeeded = True
      print("Basic test starting")
      succeeded = True
      try:
        for i in range(len(topics)):
          print("sub is %d"%i)
          aclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
          bclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
          cclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
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
      connack = aclient.connect(host=host,port=port,cleanstart=True)
      connack = bclient.connect(host=host,port=port,cleanstart=True)
      succeeded = True
      print("Basic test starting")
      succeeded = True
      number = len(topics)
      try:
        for i in range(number):
          aclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
          bclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
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
      callback2.clear()
      connect_properties = MQTTV5.Properties(MQTTV5.PacketTypes.CONNECT)
      connect_properties.SessionExpiryInterval = 1000
      connack = bclient.connect(host=host,port=port,cleanstart=True)
      bclient.disconnect()
      time.sleep(1)
      connack = aclient.connect(host=host,port=port,cleanstart=True,properties=connect_properties)
      connack = bclient.connect(host=host,port=port,cleanstart=False,properties=connect_properties)
      succeeded = True
      time.sleep(10)
      # print("Basic test starting")
      # succeeded = True
      # number = len(topics)
      # try:
      #   for i in range(number):
      #     print("sub is %d"%i)
      #     aclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
      #     bclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
      #     time.sleep(.1)
      #   time.sleep(10)
        # for i in range(number):
        #   print("unsub is %s"%i)
        #   aclient.unsubscribe([topics[i]])
        #   bclient.unsubscribe([topics[i]])
        #   time.sleep(.1)
        # time.sleep(10)
      # except:
      #   succeeded = False
      # print("Basic test", "succeeded" if succeeded else "failed")
      # self.assertEqual(succeeded, True)
      # return succeeded


      """
      """
    def test_login_sub_unsub_1(self):
      print(topics,len(topics),len(wildtopics))
      connack = aclient.connect(host=host,port=port,cleanstart=True)
      connack = bclient.connect(host=host,port=port,cleanstart=False)
      succeeded = True
      print("Basic test starting")
      succeeded = True
      number = len(topics)
      try:
        for i in range(number):
          print("sub is %d"%i)
          aclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
          bclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
          time.sleep(.1)
        time.sleep(5)
        
        print("重复订阅")
        for i in range(number):
          print("sub is %d"%i)
          aclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
          bclient.subscribe([topics[i]], [MQTTV5.SubscribeOptions(2)])
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



def setData():
  global topics, wildtopics, nosubscribe_topics, host, port,clientid1,clientid2,clientid3,host,port,password1,password2,password3,username1,username2,username3,appid,server
  #沙箱地址
  # host = "mqtt-ejabberd-hsb.easemob.com"   #发送地址
  # port = 2883 #发送端口

  #EMQ地址
  # host = "broker.emqx.io"
  # port = 1883

  # 本地地址
  host = "172.17.1.160"
  port = 1883
  # topics =  ("TopicA", "TopicA/B", "Topic/C", "TopicA/C", "/TopicA")
  # wildtopics = ("TopicA/+", "+/C", "#", "/#", "/+", "+/+", "TopicA/#")
  # nosubscribe_topics = ("test/nosubscribe",)
  clientid1 = "mqtttest1@1wyp94"  #开启鉴权后clientid格式为deviceid@appkeyappid deviceid任意取值，只要保证唯一。
  clientid2 = "mqtttest2@1wyp94"
  clientid3 = "mqtttest3@1wyp94"
  appid = {"right_appid":"1wyp94","error_appid":"123","noappid":""} #构建appid
  server = 5.0
  username1,username2,username3 = b"mqtttest1",b"mqtttest2",b"mqtttest3"  #用户名称
  password1 = b"$t$YWMtzP0sDKdAEeu14SMMp-gviPLBUj23REhmv2d9MJZsm8W1kvwQpbMR67NY5XfrXvBLAwMAAAF5Es8XPgBPGgDR9jOQyYerAtoFZ0sPW5Uf8UXkYmdcUBVtU1Ewu4N_qQ"  #用户密码，实际为与用户匹配的token
  password2 = b"$t$YWMt1xc7aqdAEeucVx_UwbjRCfLBUj23REhmv2d9MJZsm8W6vmEgpbMR655ln0Nsooa_AwMAAAF5Es9ZcgBPGgCp3XBI7JwPhYo6JnKGwcFN067Cagq_PmGIWiotkNf99w"  #用户密码，实际为与用户匹配的token
  password3 = b"$t$YWMtMubpQqlgEeuaW6tYyyxzoPLBUj23REhmv2d9MJZsm8V_NJnAqLYR64KoB6bbHIoMAwMAAAF5ILhN-ABPGgDWCb_idFTCLnpUCbJR5HBtZKS3skxat7x9mZUvY6hX_w"
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
