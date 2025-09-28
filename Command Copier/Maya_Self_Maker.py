import maya.cmds as cmds

def working_stuff():
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
        image1="text.png",  # <-- you can swap this with any .png icon in Maya's icons folder
        label="Logger", # < -- name that appears on the button
        sourceType="python", # <-- specify that this is a python command
        command='import Command_Copier; Command_Copier.command_logger_ui()' # <-- command section of the button make sure to import the script of not it will throw an error
    )

# Testing function to create shelf buttons dynamically
def create_self_button(edit_name: str, shelf_name: str, shelf_icon: str, command: str, parent_shelf: str, code_type: str):
    
    import Command_Copier # Ensure the script is imported

    if not cmds.shelfLayout(parent_shelf, exists=True):
        cmds.shelfLayout(parent_shelf, parent="ShelfLayout")
    
    cmds.shelfButton( # <-- creates a shelf button
        parent = parent_shelf, # <-- change to your shelf name
        annotation = shelf_name, # < -- name that appears when you hover over the button
        image1 = shelf_icon,  # <-- you can swap this with any .png icon in Maya's icons folder
        label = edit_name, # < -- name that appears on the button
        sourceType = code_type, # <-- specify that this is a python command
        command = command # <-- command section of the button make sure to import the script of not it will throw an error
    )

create_self_button("loggertest", "Command Logger", "text.png", 'import Command_Copier; Command_Copier.command_logger_ui()', "Maya_Tools", "python")