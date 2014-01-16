"""
*******************************************************************
  Copyright (c) 2013, 2014 IBM Corp.
 
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

import types, logging

from . import Topics, Subscriptions

from .Subscriptions import *

logger = logging.getLogger('MQTT broker')
 
class SubscriptionEngines:

   def __init__(self):
     self.__subscriptions = [] # list of subscriptions
     self.__retained = {}      # map of topics to retained msg+qos

     self.__dollar_subscriptions = []
     self.__dollar_retained = {}

   def reinitialize(self):
     self.__init__()

   def subscribe(self, aClientid, topic, qos):
     if type(topic) == type([]):
       rc = []
       count = 0
       for aTopic in topic:
         rc.append(self.__subscribe(aClientid, aTopic, qos[count]))
         count += 1
     else:
       rc = self.__subscribe(aClientid, topic, qos)
     return rc

   def __subscribe(self, aClientid, aTopic, aQos):
     "subscribe to one topic"
     rc = None
     assert Topics.isValidTopicName(aTopic)
     subscriptions = self.__subscriptions if aTopic[0] != "$" else self.__dollar_subscriptions
     resubscribed = False
     for s in subscriptions:
       if s.getClientid() == aClientid and s.getTopic() == aTopic:
         s.resubscribe(aQos)
         return s
     rc = Subscriptions(aClientid, aTopic, aQos)
     subscriptions.append(rc)
     return rc

   def unsubscribe(self, aClientid, aTopic):
     if type(aTopic) == type([]):
       for t in aTopic:
         self.__unsubscribe(aClientid, t)
     else:
       self.__unsubscribe(aClientid, aTopic)

   def __unsubscribe(self, aClientid, aTopic):
     "unsubscribe to one topic"
     subscriptions = self.__subscriptions if aTopic[0] != "$" else self.__dollar_subscriptions
     for s in subscriptions:
       if s.getClientid() == aClientid and s.getTopic() == aTopic:
         subscriptions.remove(s)
         break # once we've hit one, that's us done

   def clearSubscriptions(self, aClientid):
     for subscriptions in [self.__subscriptions, self.__dollar_subscriptions]:
       for s in subscriptions[:]:
         if s.getClientid() == aClientid:
           subscriptions.remove(s)

   def getSubscriptions(self, aTopic, aClientid=None):
     "return a list of subscriptions for this client"
     subscriptions = self.__subscriptions if aTopic[0] != "$" else self.__dollar_subscriptions
     if aClientid == None:
       rc = [sub for sub in subscriptions if Topics.topicMatches(sub.getTopic(), aTopic)]
     else:
       rc = [sub for sub in subscriptions if sub.getClientid() == aClientid and Topics.topicMatches(sub.getTopic(), aTopic)]
     return rc

   def qosOf(self, clientid, topic):
     # if there are overlapping subscriptions, choose maximum QoS
     chosen = None
     for sub in self.getSubscriptions(topic, clientid):
       if chosen == None:
         chosen = sub.getQoS()
       else:
         logger.info("[MQTT-3.3.5-1] Overlapping subscriptions max QoS")
         if sub.getQoS() > chosen:
           chosen = sub.getQoS()
       # Omit the following optimization because we want to check for condition [MQTT-3.3.5-1]
       #if chosen == 2:
       #  break
     return chosen

   def subscribers(self, aTopic):
     "list all clients subscribed to this (non-wildcard) topic"
     subscriptions = self.__subscriptions if aTopic[0] != "$" else self.__dollar_subscriptions
     result = []
     for s in subscriptions:
       if Topics.topicMatches(s.getTopic(), aTopic):
         if s.getClientid() not in result: # don't add a client id twice
             result.append(s.getClientid())
     return result

   def setRetained(self, aTopic, aMessage, aQoS):
     "set a retained message on a non-wildcard topic"
     retained = self.__retained if aTopic[0] != "$" else self.__dollar_retained
     if len(aMessage) == 0:
       if aTopic in retained.keys():
         logger.info("[MQTT-2.1.1-11] Deleting retained message")
         del retained[aTopic]
     else:
       retained[aTopic] = (aMessage, aQoS)

   def getRetained(self, aTopic):
     "returns (msg, QoS) for a topic"
     retained = self.__retained if aTopic[0] != "$" else self.__dollar_retained
     if aTopic in retained.keys():
       result = retained[aTopic]
     else:
       result = None
     return result

   def getRetainedTopics(self, aTopic):
     "returns a list of topics for which retained publications exist"
     retained = self.__retained if aTopic[0] != "$" else self.__dollar_retained
     return retained.keys()


def unit_tests():
  se = SubscriptionEngines()
  se.subscribe("Client1", ["topic1", "topic2"], [2, 1])
  assert se.subscribers("topic1") == ["Client1"]
  se.subscribe("Client2", ["topic2", "topic3"], [2, 2])
  assert se.subscribers("topic1") == ["Client1"]
  assert se.subscribers("topic2") == ["Client1", "Client2"]
  se.subscribe("Client2", ["#"], [2])
  assert se.subscribers("topic1") == ["Client1", "Client2"]
  assert se.subscribers("topic2") == ["Client1", "Client2"]
  assert se.subscribers("topic3") == ["Client2"]
  assert set(map(lambda s:s.getTopic(), se.getSubscriptions("Client2"))) == set(["#", "topic2", "topic3"])
  logger.info("Before clear: %s", se.getSubscriptions("Client2"))
  se.clearSubscriptions("Client2")
  assert se.getSubscriptions("Client2") == []
  assert se.getSubscriptions("Client1") != []
  logger.info("After clear, client1: %s", se.getSubscriptions("Client1"))
  logger.info("After clear, client2: %s", se.getSubscriptions("Client2"))
 