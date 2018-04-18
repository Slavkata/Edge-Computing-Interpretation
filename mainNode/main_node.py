import paho.mqtt.client as mqtt
import re
import inspect

clients_count = 0
clients_done = 0

# The callback for when the client is connected to a server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$SYS/broker/clients/active")
    client.subscribe("TaskFile")
    client.subscribe("DataFile")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #log metadata
    if msg.topic == "TaskFile":
        file = open("TaskFile", "wb")
        file.write(msg.payload)
        file.close()

    if msg.topic == "DataFile":
        file = open("DataFile", "wb")
        file.write(msg.payload)
        file.close()
        # client.publish("InputDataFile", msg.payload)

    if msg.topic == "$SYS/broker/clients/active":
        clients_count = int(msg.payload) - 2
        if clients_count > 0:
            client.publish("InputTaskFile", msg.payload)
            split_file()
            
            for i in range(1..clients_count + 1):
                client.publish("InputDataFile" + i, msg.payload)
                client.subscribe("node" + i + "_output")

    if msg.topic == re.match(r'.*_output', msg.topic):
        file = open(msg.topic, "wb")
        file.write(msg.payload)
        file.close()
        count += 1

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.104", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
