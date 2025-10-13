import maya.cmds as cmds
import winsound as ws
# Create a new window
window = cmds.window(title="Image Window")

# Add a pane layout to the window
cmds.paneLayout()

# Add an image to the layout
cmds.image(image='C:\\Users\\blast\\Desktop\\image\\image.png')

# Show the window
cmds.showWindow(window)



# Define a function to play the sound
def play_sound_on_click(*args):
    # Specify the path to the sound file
    ws.PlaySound("C:\\Users\\blast\\Desktop\\image\\sound_1.wav", ws.SND_FILENAME)
    cmds.confirmDialog(title="Sound Played", message="The sound has been played!", button=["OK"])

# Create a simple UI with a button
if cmds.window("myWindow", exists=True):
    cmds.deleteUI("myWindow")

cmds.window("myWindow", title="Play Sound Example")
cmds.columnLayout()
cmds.button(label="Play Sound", command=play_sound_on_click)
cmds.showWindow("myWindow")


# getting the path to the chat_control file and importing it
#script_dir = os.path.dirname(r"C:\auto rig project\chat_control.py")
#sys.path.append(script_dir)
#import chat_control as cc
