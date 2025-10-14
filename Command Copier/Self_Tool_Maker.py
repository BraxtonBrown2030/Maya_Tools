import Maya_Self_Maker as msm
import maya.cmds as cmds

def self_testing_window():
    if cmds.window("selfTestWin", exists=True):
        cmds.deleteUI("selfTestWin")
    
    window = cmds.window("selfTestWin", title="Self Tool Maker Test", widthHeight=(300, 150))
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="This is a test window for the Self Tool Maker.")
    cmds.button(label="Create Self Button", command=lambda x: msm.create_self_button())
    cmds.setParent("..")
    
    cmds.showWindow(window)

self_testing_window()


"""

get user input for button parameters and create the button on the specified shelf
make option for updating userpefs is needed.


"""
