import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("InputFile2")
    client.subscribe("InputProgram")
    # client.subscribe("$SYS/broker/clients/active")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic)
    if msg.topic == "InputFile2":
        handle_files(msg.payload)
    elif msg.topic == "InputProgram":
        handle_program(msg.payload)

def handle_files(byteArray):
    from program import execute
    newFile = execute(byteArray)
    client.publish("2_output", newFile)
    # f = open("InputFile", "wb")
    # f.write(byteArray)
    # print(byteArray)
    # f.close()

def handle_program(byteArray):
    print(byteArray)
    f = open("program.py", "wb")
    f.write(byteArray)
    f.close()
    #fork a process of given program with given InputFile

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.109", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
