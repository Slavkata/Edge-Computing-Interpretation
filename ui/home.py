from appJar import gui
import paho.mqtt.client as mqtt
import sys
# sys.path.insert(0, '/home/nikolatz/Edge-Computing-Interpretation/mainNode')
# from main_node import runMain
def press(button) :
    if button=="Send the work":
        # result = 1 runMain(app.getEntry("f1"), app.getEntry("f2"))
        client.publish("DataFile", app.getEntry("f1"))
        client.publish("ScriptFile", app.getEntry("f2"))
        client.publish("StartWork")

def on_connect(client, userdata, flags, rc):
    client.subscribe("Result")

def on_message(client, userdata, msg):
    if msg.topic == "Result":
        file = open("result.txt", "w")
        file.write(msg.payload.decode("utf-8"))
        file.close()
        app.openPage("Welcome to projecto", 1)
        app.stopPage()

app = gui()
app.setBg("DarkKhaki")

app.startPagedWindow("Welcome to projecto")

app.startPage()
app.addLabel("w1", "You have to choose two files")
app.stopPage()

app.startPage()
app.addLabel("l1", "upload a file")
app.setLabelBg("l1", "green")
app.setLabelSticky("l1", "both")
app.addFileEntry("f1")
app.setEntrySticky("f1", "both")
app.stopPage()

app.startPage()
app.addLabel("l2", "upload a script")
app.setLabelBg("l2", "green")
app.setLabelSticky("l2", "both")
app.addFileEntry("f2")
app.setEntrySticky("f2", "both")
app.stopPage()

app.startPage()
app.addButton("Send the work", press)
app.setButtonAlign("Send the work", "center")
app.setButtonSticky("Send the work", "both")
app.stopPage()

app.stopPagedWindow()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.109", 1883, 60)
client.loop_start()
# start the GUI
app.go()
