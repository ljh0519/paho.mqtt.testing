# coding=UTF-8

import mqtt.clients.V311 as mqtt_client, time, logging, socket, sys, getopt, traceback
import threading


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


# # # #timeout 2 seconds
class Dispacher(threading.Thread):
    def __init__(self,fun):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.result = None
        self.error = None
        self.fun = fun
        
        self.start()
    def run(self):
        try:
            self.result =self.fun()
        except:
            self.error = sys.exc_info()


def test_basic1():
    host = "172.17.1.160"
    port = 1883

    username1 = b"test-ljh"
    password1 = b"YWMt5641htfoEeuzjKErDIFCPugrzF8zZk2Wp8GS3pF-orBzFBswjHIR66up95didFMbAwMAAAF6Ua9qawBPGgC00Ao3kcePo7PbyWuuTTdzfJupSABf_DJeu6wxF86nQw"
    clientid1 = "test-ljh1@1PGUGY"

    callback = Callbacks()


    #aclient = mqtt_client.Client(b"\xEF\xBB\xBF" + "myclientid".encode("utf-8"))
    aclient = mqtt_client.Client(clientid1.encode("utf-8"))
    aclient.registerCallback(callback)
    aclient.setUserName(username1, password1)

    print("Basic test starting")
    succeeded = True
    try:
        aclient.connect(host=host, port=port)
        aclient.disconnect()
        time.sleep(3)
    except:
        traceback.print_exc()
        succeeded = False
    return succeeded

def test_time_fun():
    start = time.time()
    detection = Dispacher(test_basic1)
    detection.join(2)

    if detection.isAlive():
        return "TimeOutError"
    elif detection.error():
        return detection.error[1]
    end = time.time()
    print("test_time_fun success! : ", end - start)
    time_result = detection.result
    return time_result



if __name__ == "__main__":
    test_time_fun()