import maya.cmds as cmds

# script has to be in the main maya script folder for the check toi happen when added to shelf
# Make sure YourScript.py is in Maya's scripts path
import Command_Copier

# Create a shelf tab (if it doesn't exist already)
if not cmds.shelfLayout("Maya_Tools", exists=True): 
    cmds.shelfLayout("Maya_Tools", parent="ShelfLayout") # checks for existing shelf and make it if not
                    # shelf name , parent is always ShelfLayout
# Add a shelf button that runs the command_logger_ui function from Command_Copier
cmds.shelfButton( # <-- creates a shelf button
    parent="Maya_Tools", # <-- change to your shelf name
    annotation="Command Logger", # < -- name that appears when you hover over the button
    image1="commandButton.png",  # <-- you can swap this with any .png icon in Maya's icons folder
    label="Logger", # < -- name that appears on the button
    sourceType="python", # <-- specify that this is a python command
    command='import Command_Copier; Command_Copier.command_logger_ui()' # <-- command section of the button make sure to import the script of not it will throw an error
)