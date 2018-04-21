import paho.mqtt.client as mqtt
import re
import os
import inspect

finalResult = []
bytesPerNodeArray = []
task = ""
script = ""
clients_count = 0
clients_done = 0

# The callback for when the client is connected to a server.
def on_connect(client, userdata, flags, rc):
    client.subscribe("$SYS/broker/clients/connected")
    client.subscribe("DataFile")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global clients_count
    if msg.topic == "DataFile":
        print(msg.payload)
        # client.publish("InputDataFile", msg.payload)

    if msg.topic == "$SYS/broker/clients/connected":
        print(int(msg.payload) - 1)
        clients_count = int(msg.payload) - 1
        if clients_count > 1:
            global script
            global finalResult
            # the result of each node will be stored here
            finalResult = list(range(clients_count))
            openTask = open(script, "rb")
            client.publish("InputProgram", openTask.read())
            split_file(clients_count)
            for i in range(len(bytesPerNodeArray)):
                print("InputFile" + str(i + 1))
                client.publish("InputFile" + str(i + 1), bytesPerNodeArray[i])
                client.subscribe(str(i + 1) + "_output")

    if re.match(r'._output', msg.topic):
        global clients_done
        # global finalResult
        node = msg.topic.split('_')[0]
        finalResult[int(node)-1] = msg.payload
        clients_done+=1;
        if clients_done == clients_count:
            # for i in range(len(finalResult)):
            client.disconnect()

        # file = open(msg.topic, "wb")
        # file.write(msg.payload)
        # file.close()
        # count += 1

def split_file(nodes):
    global bytesPerNodeArray
    bytesPerNodeArray = list(range(nodes))
    global task
    openTask = open(task, "rb")
    statinfo = os.stat(task)
    byttesPerNode = statinfo.st_size//nodes
    # print( openTask.read(byttesPerNode))
    for i in range(len(bytesPerNodeArray)):
        bytesPerNodeArray[i] = openTask.read(byttesPerNode)

    bytesPerNodeArray[nodes-1] = bytesPerNodeArray[nodes-1] + openTask.read(statinfo.st_size%nodes)
    # fileSize = openTask.seek(0, 2)
    # openTask.tell()


def runMain(taskFile, funcFile):
    global task
    global script
    global finalResult
    task = taskFile
    script = funcFile
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.1.114", 1883, 60)
    client.loop_forever()
    return finalResult

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
