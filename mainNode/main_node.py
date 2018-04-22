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
# vvariable tto indicate that we dont wannna add new  nodes
working = False

# The callback for when the client is connected to a server.
def on_connect(client, userdata, flags, rc):
    client.subscribe("$SYS/broker/clients/connected")
    client.subscribe("DataFile")
    client.subscribe("ScriptFile")
    client.subscribe("StartWork")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdataa, msg):
    global clients_count
    global task
    global script
    global finalResult
    global working
    if msg.topic == "ScriptFile":
        script = msg.payload
    if msg.topic == "DataFile":
        task = msg.payload
        # client.publish("InputDataFile", msg.payload)
    if msg.topic == "StartWork":
        working = True
        finalResult = list(range(clients_count))
        openScript = open(script, "rb")
        client.publish("InputProgram", openScript.read())
        split_file(clients_count)
        for i in range(len(bytesPerNodeArray)):
            print("InputFile" + str(i + 1))
            client.publish("InputFile" + str(i + 1), bytesPerNodeArray[i])
            client.subscribe(str(i + 1) + "_output")

    if msg.topic == "$SYS/broker/clients/connected":
        if working == False:
            clients_count = int(msg.payload) - 2
            print(clients_count)

    if re.match(r'._output', msg.topic):
        global clients_done
        # global finalResult
        node = msg.topic.split('_')[0]
        finalResult[int(node)-1] = msg.payload
        clients_done+=1;
        if clients_done == clients_count:
            result = b''
            for i in range (len(finalResult)):
                result += finalResult[i]
                # result.apppend(finalResult[i])
            print(result)
            client.publish("Result", result)
            working = False
            clients_done = 0
            #return the result

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



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.109", 1883, 60)
client.loop_forever()
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
