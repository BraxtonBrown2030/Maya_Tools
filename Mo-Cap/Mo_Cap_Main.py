import maya.cmds as cmds

def mo_cap_main():
    cmds.defineDataServer(server = "127.0.0.1:5052", device = "moCap")
    cmds.listInputDeviceAxes("handTracker")