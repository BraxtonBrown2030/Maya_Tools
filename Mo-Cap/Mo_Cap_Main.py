import maya.cmds as cmds

def mo_cap_main():
    cmds.defineDataServer(server = "127.0.0.1:5052", device = "moCap")
    cmds.listInputDeviceAxes("moCap")
    # cmds.defineDataServer(undefine=True, d="handTracker") # undefine the device if needed use this to stop the data stream and end the program
    
    """
    listDeviceAttachments 
    listInputDeviceAxes take the current imported device and lists all the axes that are available to be connected to attributes in Maya.
    
    need to assign the axes to the attributes in Maya
    
    check blue tooth camera and input reevaluation
    
    """
    