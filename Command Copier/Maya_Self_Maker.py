import maya.cmds as cmds
import importlib

def create_self_button(parent_shelf: str, shelf_name: str, edit_name: str, shelf_icon: str, code_type: str, script_name: str, main_name: str): 
    
    importlib.import_module(script_name) # Ensure the script is imported

    if not cmds.shelfLayout(parent_shelf, exists=True):
        cmds.shelfLayout(parent_shelf, parent="ShelfLayout")
    
    cmds.shelfButton( # <-- creates a shelf button
        parent = parent_shelf, # <-- change to your shelf name
        annotation = shelf_name, # < -- name that appears when you hover over the button
        image1 = shelf_icon,  # <-- you can swap this with any .png icon in Maya's icons folder
        label = edit_name, # < -- name that appears on the button
        sourceType = code_type, # <-- specify that this is a python command
        command = f"import {script_name}; {script_name}.{main_name}()" # <-- command section of the button make sure to import the script of not it will throw an error
    )

# create_self_button("Maya_Tools","Command Logger", "logger", "text.png", "python", "Command_Copier", "command_logger_ui")
#              shelf name ^   button name ^ Editor name ^    icon ^ code type ^  script name ^   main function ^