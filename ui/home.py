from appJar import gui
import sys
sys.path.insert(0, '/home/nikolatz/Edge-Computing-Interpretation/mainNode')
from main_node import runMain
def press(button) :
    if button=="Send the work":
        # fileToWorkOn = open(app.getEntry("f1"), "r")
        # script = open(app.getEntry("f2"), "r")
        result = runMain(app.getEntry("f1"), app.getEntry("f2"))
        print(result)
        app.startSubWindow("result", modal=True)
        app.addMessage("mess", """You can put a lot of text in this widget.
The text will be wrapped over multiple lines.
It's not possible to apply different styles to different words.""")
    app.showSubWindow("result")
app = gui()
app.setBg("DarkKhaki")

app.startPagedWindow("Welcome to projecto")
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
# start the GUI
app.go()
